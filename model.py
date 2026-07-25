#!/usr/bin/env python3
"""Modelo de goles Dixon-Coles con ataque/defensa separados y aprendizaje secuencial.

Reemplaza el modelo anterior, que forzaba lam_local + lam_visita = T = 2.6 en TODOS
los partidos (solo repartía ese total según la diferencia de Elo). Aquí cada equipo
tiene un parámetro de ataque y otro de defensa independientes:

    lam_local  = exp(mu + atk[L] - dfn[V] + ventaja_local)
    lam_visita = exp(mu + atk[V] - dfn[L])

de modo que el total de goles esperado varía según el emparejamiento: dos equipos
ofensivos producen un partido con más goles que dos defensivos.

Dos correcciones adicionales:

1. Dixon-Coles (1997): el Poisson independiente subestima 0-0 y 1-1 y sobreestima
   1-0 y 0-1. La función tau reajusta esas cuatro celdas conservando la masa total.
2. Aprendizaje secuencial: en vez de un único ajuste masivo por xG al final, los
   parámetros se actualizan partido a partido por gradiente de la log-verosimilitud
   Poisson, usando una mezcla de xG y goles como observación (el xG predice el
   rendimiento futuro mejor que el marcador).
"""
import math
import numpy as np

MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
         "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}


def datekey(s):
    """'11 jun' -> (6, 11); permite ordenar partidos cronológicamente."""
    try:
        p = s.strip().split()
        return (MESES.get(p[1][:3].lower(), 0), int(p[0]))
    except Exception:
        return (99, 99)


class DCModel:
    """Estado de ataque/defensa por equipo + probabilidades Dixon-Coles."""

    def __init__(self, names, strength, T=2.6, K=0.06, rho=-0.10,
                 xg_w=0.60, hadv=0.20, shrink=0.0, maxg=11):
        self.names = list(names)
        self.n = len(self.names)
        self.idx = {nm: i for i, nm in enumerate(self.names)}
        self.T = float(T)
        self.mu = math.log(self.T / 2.0)
        # Calibración inicial: reproduce el poder discriminante del modelo viejo.
        # Viejo: log(lam_L/lam_V) ~= 2*S/T con S = dif_rating/DIV.
        # Nuevo: log(lam_L/lam_V) = 2*c*(s_L - s_V)  ->  c = 1/T.
        c = 1.0 / self.T
        s = np.asarray(strength, dtype=float)
        self.prior_atk = c * s
        self.prior_dfn = c * s
        self.atk = self.prior_atk.copy()
        self.dfn = self.prior_dfn.copy()
        self.K = float(K)
        self.rho = float(rho)
        self.xg_w = float(xg_w)
        self.hadv = float(hadv)
        self.shrink = float(shrink)
        self.maxg = int(maxg)
        self._fact = np.array([math.factorial(k) for k in range(self.maxg)], dtype=float)

    def reset(self):
        self.atk = self.prior_atk.copy()
        self.dfn = self.prior_dfn.copy()

    # ---------- tasas y probabilidades ----------

    def rates(self, ih, ia, host_h=False, host_a=False):
        lh = math.exp(self.mu + self.atk[ih] - self.dfn[ia] + (self.hadv if host_h else 0.0))
        la = math.exp(self.mu + self.atk[ia] - self.dfn[ih] + (self.hadv if host_a else 0.0))
        return min(max(lh, 0.05), 6.0), min(max(la, 0.05), 6.0)

    def _pois(self, lam):
        k = np.arange(self.maxg)
        return np.exp(-lam) * lam ** k / self._fact

    def matrix(self, lh, la):
        """Matriz conjunta de marcadores (filas=goles local, columnas=goles visita)."""
        M = np.outer(self._pois(lh), self._pois(la))
        r = self.rho
        # Corrección Dixon-Coles: sum((tau-1)*P) = 0, así que la masa se conserva.
        M[0, 0] *= (1.0 - lh * la * r)
        M[0, 1] *= (1.0 + lh * r)
        M[1, 0] *= (1.0 + la * r)
        M[1, 1] *= (1.0 - r)
        M = np.maximum(M, 1e-12)
        return M / M.sum()

    def wdl(self, ih, ia, host_h=False, host_a=False):
        """(p_gana_local, p_empate, p_gana_visita, marcador_mas_probable)."""
        lh, la = self.rates(ih, ia, host_h, host_a)
        M = self.matrix(lh, la)
        pw = float(np.tril(M, -1).sum())
        pd = float(np.trace(M))
        pl = float(np.triu(M, 1).sum())
        i, j = np.unravel_index(int(M.argmax()), M.shape)
        return pw, pd, pl, (int(i), int(j))

    def p_advance(self, ih, ia, host_h=False, host_a=False, et_scale=0.30):
        """Probabilidad de que el LOCAL avance en eliminación directa.

        90' -> si empate, prórroga con tasas escaladas (30 min, algo más
        conservadoras) -> si sigue empate, penales ~ 50/50.
        """
        pw, pd, pl, _ = self.wdl(ih, ia, host_h, host_a)
        lh, la = self.rates(ih, ia, host_h, host_a)
        Me = self.matrix(lh * et_scale, la * et_scale)
        ew = float(np.tril(Me, -1).sum())
        ed = float(np.trace(Me))
        el = float(np.triu(Me, 1).sum())
        p_et = ew + ed * 0.5
        return pw + pd * p_et

    # ---------- aprendizaje secuencial ----------

    def observation(self, goals, xg):
        """Mezcla xG y goles. El xG es más estable como señal de calidad."""
        if xg is None:
            return float(goals)
        return self.xg_w * float(xg) + (1.0 - self.xg_w) * float(goals)

    def update(self, ih, ia, yh, ya, host_h=False, host_a=False, w=1.0):
        """Paso de gradiente sobre la log-verosimilitud Poisson.

        d(logL)/d(atk_L) = y_L - lam_L ;  d(logL)/d(dfn_V) = -(y_L - lam_L)
        """
        lh, la = self.rates(ih, ia, host_h, host_a)
        eh = (yh - lh) * self.K * w
        ea = (ya - la) * self.K * w
        self.atk[ih] += eh
        self.dfn[ia] -= eh
        self.atk[ia] += ea
        self.dfn[ih] -= ea
        if self.shrink > 0:
            for t in (ih, ia):
                self.atk[t] = self.prior_atk[t] + (1 - self.shrink) * (self.atk[t] - self.prior_atk[t])
                self.dfn[t] = self.prior_dfn[t] + (1 - self.shrink) * (self.dfn[t] - self.prior_dfn[t])

    # ---------- evaluación ----------

    def prequential(self, matches, learn=True):
        """Validación one-step-ahead: cada partido se predice ANTES de aprenderlo.

        matches: lista de dicts con ih, ia, gh, ga, xgh, xga, host_h, host_a.
        Devuelve (log_loss_medio, brier_medio, n).
        """
        self.reset()
        ll = 0.0
        br = 0.0
        n = 0
        for m in matches:
            pw, pd, pl, _ = self.wdl(m["ih"], m["ia"], m["host_h"], m["host_a"])
            gh, ga = m["gh"], m["ga"]
            out = 0 if gh > ga else (1 if gh == ga else 2)
            p = (pw, pd, pl)
            ll -= math.log(max(p[out], 1e-12))
            br += sum((p[k] - (1.0 if k == out else 0.0)) ** 2 for k in range(3))
            n += 1
            if learn:
                self.update(m["ih"], m["ia"],
                            self.observation(m.get("gh_obs", gh), m.get("xgh")),
                            self.observation(m.get("ga_obs", ga), m.get("xga")),
                            m["host_h"], m["host_a"], m.get("w", 1.0))
        return (ll / max(n, 1), br / max(n, 1), n)

    def fit(self, matches):
        """Reproduce el estado final recorriendo el historial en orden."""
        self.reset()
        for m in matches:
            self.update(m["ih"], m["ia"],
                        self.observation(m.get("gh_obs", m["gh"]), m.get("xgh")),
                        self.observation(m.get("ga_obs", m["ga"]), m.get("xga")),
                        m["host_h"], m["host_a"], m.get("w", 1.0))
        return self


def grid_search(names, strength, matches, T=2.6,
                Ks=(0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.14),
                rhos=(-0.20, -0.15, -0.10, -0.05, 0.0),
                xgws=(0.0, 0.25, 0.5, 0.75, 1.0),
                hadvs=(0.0, 0.10, 0.20, 0.30),
                verbose=False):
    """Elige hiperparámetros minimizando la log-loss prequencial (fuera de muestra)."""
    best = None
    for K in Ks:
        for xw in xgws:
            for ha in hadvs:
                for rho in rhos:
                    m = DCModel(names, strength, T=T, K=K, rho=rho, xg_w=xw, hadv=ha)
                    ll, br, n = m.prequential(matches)
                    if best is None or ll < best[0]:
                        best = (ll, br, dict(K=K, rho=rho, xg_w=xw, hadv=ha), n)
                        if verbose:
                            print(f"  nuevo mejor logloss={ll:.4f} brier={br:.4f} {best[2]}")
    return best
