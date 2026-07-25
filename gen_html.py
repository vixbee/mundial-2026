#!/usr/bin/env python3
"""Corre el modelo y escribe wcdata.json.

El modelo de goles vive en model.py y los datos del torneo en wcbase.py; aquí solo
se simula el torneo y se arma la salida.
"""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
import math, json
import numpy as np
import wcbase
from wcbase import (data, EN, HOSTS, T_GOALS, DIV_F, HB_F, pts, REAL32, REAL_KO,
                    ro, r16, qf, sf, brk_meta, KOVEN, KOTIME,
                    WINNERS_G, RUNNERS_G, oriented_score)
from history import is_host

# ---------------------------------------------------------------- modelo
mdl, ctx = wcbase.build_model()
names = ctx["names"]; idx = ctx["idx"]; team_rank = ctx["team_rank"]
groups = ctx["groups"]; RES = ctx["RES"]; XG = ctx["XG"]; SCHED = ctx["SCHED"]
hp = ctx["hp"]
NT = len(names)

# Proyección "original" (ranking FIFA puro), se conserva como columna de contraste.
def pmf(k, l): return math.exp(-l) * l ** k / math.factorial(k)

def proj_fifa(home, hr, away, ar):
    rh = pts(hr) + (HB_F if home in HOSTS else 0)
    ra = pts(ar) + (HB_F if away in HOSTS else 0)
    S = (rh - ra) / DIV_F
    lh = max(0.18, (T_GOALS + S) / 2); la = max(0.18, (T_GOALS - S) / 2)
    ph = [pmf(i, lh) for i in range(9)]; pa = [pmf(j, la) for j in range(9)]
    best = (0, 0); bp = -1
    for i in range(9):
        for j in range(9):
            p = ph[i] * pa[j]
            if p > bp: bp = p; best = (i, j)
    return best

def venue_of_group(home, away):
    return SCHED.get("|".join(sorted([home, away])), {}).get("venue", "")

# Matriz de avance en eliminatorias (sede neutral: nadie es local).
Padv = np.zeros((NT, NT))
for i in range(NT):
    for j in range(NT):
        if i != j:
            Padv[i, j] = mdl.p_advance(i, j)

# Tasas de gol por partido de grupo, ya con ataque/defensa separados.
lam_h = np.zeros(len(data)); lam_a = np.zeros(len(data))
for mi, (g, _d, h, hr, a, ar) in enumerate(data):
    ve = venue_of_group(h, a)
    lh, la = mdl.rates(idx[h], idx[a], is_host(h, ve), is_host(a, ve))
    lam_h[mi] = lh; lam_a[mi] = la

# ---------------------------------------------------------------- simulación
glist = sorted(groups)
gpos = {g: i for i, g in enumerate(glist)}
grp_teams = {g: sorted(groups[g].keys()) for g in groups}
grp_local = {g: {nm: i for i, nm in enumerate(grp_teams[g])} for g in groups}
grp_matches = {}
for mi, (g, _d, h, hr, a, ar) in enumerate(data):
    grp_matches.setdefault(g, []).append((mi, idx[h], idx[a]))

Mt = len(data)
N = 20000
rng = np.random.default_rng(20260611)
hg = rng.poisson(lam_h, size=(N, Mt))
ag = rng.poisson(lam_a, size=(N, Mt))
midx = {(d[2], d[4]): i for i, d in enumerate(data)}
for k, (gh_, ga_) in RES.items():
    h, a = k.split("|")
    mi = midx[(h, a)]
    hg[:, mi] = gh_; ag[:, mi] = ga_

FIRST = np.zeros((N, 12), int); SEC = np.zeros((N, 12), int); THIRD = np.zeros((N, 12), int)
tk = np.zeros((N, 12))
first = np.zeros(NT); second = np.zeros(NT); third_adv = np.zeros(NT); adv = np.zeros(NT)
for gp, g in enumerate(glist):
    lc = grp_local[g]; nt = len(grp_teams[g])
    gl = np.array([idx[nm] for nm in grp_teams[g]])
    P = np.zeros((N, nt)); GF = np.zeros((N, nt)); GA = np.zeros((N, nt))
    for mi, hi, ai in grp_matches[g]:
        hl = lc[names[hi]]; al = lc[names[ai]]
        h_ = hg[:, mi]; a_ = ag[:, mi]
        GF[:, hl] += h_; GA[:, hl] += a_; GF[:, al] += a_; GA[:, al] += h_
        dr = h_ == a_
        P[:, hl] += np.where(h_ > a_, 3, np.where(dr, 1, 0))
        P[:, al] += np.where(a_ > h_, 3, np.where(dr, 1, 0))
    key = P * 1e6 + (GF - GA) * 1e3 + GF * 1e1 + rng.random((N, nt))
    o = np.argsort(-key, axis=1)
    FIRST[:, gp] = gl[o[:, 0]]; SEC[:, gp] = gl[o[:, 1]]; THIRD[:, gp] = gl[o[:, 2]]
    tk[:, gp] = key[np.arange(N), o[:, 2]]
    first += np.bincount(gl[o[:, 0]], minlength=NT)
    second += np.bincount(gl[o[:, 1]], minlength=NT)
ot = np.argsort(-tk, axis=1); top8 = ot[:, :8]
qmask = np.zeros((N, 12), bool); qmask[np.arange(N)[:, None], top8] = True
for gp in range(12):
    adv += np.bincount(FIRST[:, gp], minlength=NT) + np.bincount(SEC[:, gp], minlength=NT)
    m_ = qmask[:, gp]
    c = np.bincount(THIRD[m_, gp], minlength=NT); third_adv += c; adv += c

slots = [("M74", set("ABCDF")), ("M77", set("CDFGH")), ("M79", set("CEFHI")), ("M80", set("EHIJK")),
         ("M81", set("BEFIJ")), ("M82", set("AEHIJ")), ("M85", set("EFGIJ")), ("M87", set("DEIJL"))]

def mt(advg):
    assign = {}; used = set()
    ss = sorted(slots, key=lambda s: sum(1 for g in advg if g in s[1]))
    def bt(i):
        if i == len(ss): return True
        sid, el = ss[i]
        for g in advg:
            if g in el and g not in used:
                used.add(g); assign[sid] = g
                if bt(i + 1): return True
                used.discard(g); assign.pop(sid, None)
        return False
    bt(0); return assign

GL = list("ABCDEFGHIJKL")
M32IDX = {mid: (idx[a], idx[b]) for mid, a, b in REAL32}
REAL_KO_IDX = {mid: idx[nm] for mid, (nm, _) in REAL_KO.items()}

oct_ = np.zeros(NT); cua = np.zeros(NT); sem = np.zeros(NT); fin = np.zeros(NT); champ = np.zeros(NT)
U = rng.random((N, 31))
for t in range(N):
    win = {}; ui = 0
    for sid in ro:
        a, b = M32IDX[sid]
        w = REAL_KO_IDX[sid] if sid in REAL_KO_IDX else (a if U[t, ui] < Padv[a, b] else b)
        ui += 1; win[sid] = w; oct_[w] += 1
    for sid, x, y in r16:
        a, b = win[x], win[y]
        w = REAL_KO_IDX[sid] if sid in REAL_KO_IDX else (a if U[t, ui] < Padv[a, b] else b)
        ui += 1; win[sid] = w; cua[w] += 1
    for sid, x, y in qf:
        a, b = win[x], win[y]
        w = REAL_KO_IDX[sid] if sid in REAL_KO_IDX else (a if U[t, ui] < Padv[a, b] else b)
        ui += 1; win[sid] = w; sem[w] += 1
    for sid, x, y in sf:
        a, b = win[x], win[y]
        w = REAL_KO_IDX[sid] if sid in REAL_KO_IDX else (a if U[t, ui] < Padv[a, b] else b)
        ui += 1; win[sid] = w; fin[w] += 1
    a, b = win["M101"], win["M102"]
    champ[a if U[t, ui] < Padv[a, b] else b] += 1

# ---------------------------------------------------------------- salida
Wm = {}; Rm = {}; Thm = {}; Thp = {}
for g in glist:
    by = sorted(grp_teams[g], key=lambda nm: adv[idx[nm]], reverse=True)
    q1, q2, q3 = by[0], by[1], by[2]
    if first[idx[q1]] >= first[idx[q2]]: Wm[g], Rm[g] = q1, q2
    else: Wm[g], Rm[g] = q2, q1
    Thm[g] = q3; Thp[g] = third_adv[idx[q3]] / N
advg8 = [g for g, _ in sorted(Thp.items(), key=lambda kv: kv[1], reverse=True)[:8]]
amap = mt(advg8)

def side(team, code): return {"es": team, "en": EN[team], "code": code}
def qc(nm): return "1.º grupo" if nm in WINNERS_G else ("2.º grupo" if nm in RUNNERS_G else "3.º")
bsides = {mid: (side(a, qc(a)), side(b, qc(b))) for mid, a, b in REAL32}

D = {"groups": {}}
for g in glist:
    teams = sorted(grp_teams[g], key=lambda nm: adv[idx[nm]], reverse=True)
    D["groups"][g] = {"teams": [{"es": nm, "en": EN[nm], "rank": team_rank[nm],
                                 "pwin": round(first[idx[nm]] / N, 3),
                                 "padv": round(adv[idx[nm]] / N, 3)} for nm in teams],
                      "matches": []}
for g, date, home, hr, away, ar in data:
    ve = venue_of_group(home, away)
    pw, pd, pl, best = mdl.wdl(idx[home], idx[away], is_host(home, ve), is_host(away, ve))
    gap = pw - pl
    res = "draw" if abs(gap) < 0.08 else ("home" if gap > 0 else "away")
    sc = SCHED["|".join(sorted([home, away]))]
    real = RES.get(f"{home}|{away}")
    bf = proj_fifa(home, hr, away, ar)
    md = {"date": sc["date"], "time": sc["time"], "venue": sc["venue"],
          "h": home, "he": EN[home], "a": away, "ae": EN[away], "hr": hr, "ar": ar,
          "pw": round(pw, 2), "pd": round(pd, 2), "pl": round(pl, 2),
          "sc": f"{best[0]}–{best[1]}", "proj": f"{bf[0]}–{bf[1]}",
          "xg": XG.get(f"{home}|{away}"), "res": res, "done": 0}
    if real:
        gh_, ga_ = real
        md["done"] = 1; md["sc"] = f"{gh_}–{ga_}"
        md["res"] = "draw" if gh_ == ga_ else ("home" if gh_ > ga_ else "away")
    D["groups"][g]["matches"].append(md)

D["bracket"] = [{"mid": mid, "date": dt, "venue": ve,
                 "e1": bsides[mid][0], "e2": bsides[mid][1],
                 "done": 1 if mid in REAL_KO else 0,
                 "score": oriented_score(mid, bsides[mid][0]["es"], bsides[mid][1]["es"]),
                 "winner": REAL_KO.get(mid, ("", ""))[0]} for mid, dt, ve in brk_meta]

m32 = {mid: (idx[bsides[mid][0]["es"]], idx[bsides[mid][1]["es"]]) for mid in ro}
def cw(a, b): return a if Padv[a, b] >= Padv[b, a] else b
def cl(a, b): return b if Padv[a, b] >= Padv[b, a] else a
def nmo(i): return {"es": names[i], "en": EN[names[i]]}

win = {mid: (REAL_KO_IDX[mid] if mid in REAL_KO_IDX else cw(*m32[mid])) for mid in ro}

def rnd(pairs):
    out = []
    for mid, x, y in pairs:
        a, b = win[x], win[y]
        w = REAL_KO_IDX[mid] if mid in REAL_KO_IDX else cw(a, b)
        win[mid] = w
        dt, ve = KOVEN.get(mid, ("", ""))
        out.append({"mid": mid, "a": nmo(a), "b": nmo(b), "w": "a" if w == a else "b",
                    "date": dt, "venue": ve, "time": KOTIME.get(mid, ""),
                    "done": 1 if mid in REAL_KO else 0,
                    "score": oriented_score(mid, names[a], names[b])})
    return out

octavos = rnd(r16); cuartos = rnd(qf); semis = rnd(sf)
fa, fb = win["M101"], win["M102"]; champ_idx = cw(fa, fb)
sl1 = cl(win["M97"], win["M99"]); sl2 = cl(win["M98"], win["M100"]); third3 = cw(sl1, sl2)
fd, fv = KOVEN["M104"]; td, tv = KOVEN["M103"]
D["knockout"] = {"octavos": octavos, "cuartos": cuartos, "semis": semis,
 "final": {"mid": "M104", "a": nmo(fa), "b": nmo(fb), "w": "a" if champ_idx == fa else "b",
           "date": fd, "venue": fv, "time": KOTIME["M104"]},
 "champion": nmo(champ_idx), "champion_p": round(champ[champ_idx] / N, 3),
 "third": {"a": nmo(sl1), "b": nmo(sl2), "w": "a" if third3 == sl1 else "b",
           "date": td, "venue": tv, "time": KOTIME["M103"]}}

ODDS = json.load(open("odds.json", encoding="utf-8"))
imp = {nm: 100.0 / (o + 100.0) for nm, o in ODDS.items()}
ssum = sum(imp.values())
pmkt = {nm: imp[nm] / ssum for nm in imp}
WB = 0.8
pmodel = {names[i]: champ[i] / N for i in range(NT)}
blend = {nm: WB * pmkt.get(nm, 0.0) + (1 - WB) * pmodel[nm] for nm in names}
bs = sum(blend.values())
blend = {nm: blend[nm] / bs for nm in blend}
chb = sorted(names, key=lambda nm: blend[nm], reverse=True)[:12]
D["champions"] = [{"es": nm, "en": EN[nm], "p": round(blend[nm], 3),
                   "pmodel": round(pmodel[nm], 3), "pmkt": round(pmkt.get(nm, 0.0), 3)}
                  for nm in chb]
D["blend_w"] = WB
# Resultados crudos de la simulación, para que master.py arme el Excel sin
# volver a simular (y por tanto sin poder contradecir a la web).
D["sim"] = {nm: {"pwin": first[idx[nm]] / N, "padv": adv[idx[nm]] / N,
                 "poct": oct_[idx[nm]] / N, "pcua": cua[idx[nm]] / N,
                 "psem": sem[idx[nm]] / N, "pfin": fin[idx[nm]] / N,
                 "pchamp": champ[idx[nm]] / N,
                 "pmkt": pmkt.get(nm, 0.0), "blend": blend[nm],
                 "grp": ctx["team_grp"][nm], "rank": team_rank[nm]}
            for nm in names}
D["fit"] = {"logloss": round(hp["logloss"], 4), "brier": round(hp["brier"], 4),
            "logloss_base": round(hp["logloss_base"], 4),
            "brier_base": round(hp["brier_base"], 4),
            "n": hp["n_matches"], "K": hp["K"], "rho": hp["rho"], "xg_w": hp["xg_w"]}

import datetime as _dt
_M = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]
_n = _dt.datetime.utcnow() - _dt.timedelta(hours=6)
D["generated"] = f"{_n.day} {_M[_n.month-1]} {_n.year}, {_n.strftime('%H:%M')} CDMX"
json.dump(D, open("wcdata.json", "w"), ensure_ascii=False)
print("data ready; blended top:", chb[0], round(blend[chb[0]], 3),
      "| modelo", round(pmodel[chb[0]], 3), "| mercado", round(pmkt.get(chb[0], 0), 3))
print(f"ajuste fuera de muestra: logloss {hp['logloss']:.4f} vs {hp['logloss_base']:.4f} (modelo anterior)")
