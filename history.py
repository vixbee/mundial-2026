#!/usr/bin/env python3
"""Historial cronológico de partidos jugados, con goles y xG, para alimentar el modelo.

Detalles que importan:
- Las claves de xg.json no siempre respetan el orden del emparejamiento oficial
  (p. ej. el cuadro dice Noruega-Brasil pero el xG está como "Brasil|Noruega"),
  así que se busca en ambos sentidos y se intercambian los valores si hace falta.
- Los marcadores de prórroga corresponden a 120 minutos; se escalan a 90 (x0.75)
  para que sean comparables con el resto. El xG registrado ya es, en general, de
  tiempo regular, así que no se reescala.
- La ventaja de local en eliminatorias solo aplica si el equipo anfitrión juega en
  su propio país (Canadá jugando en Los Ángeles no es local).
"""
import re
from model import datekey

HOST_COUNTRY = {"México": "MEX", "Estados Unidos": "USA", "Canadá": "CAN"}
_MEX_KEYS = ("azteca", "cdmx", "mexico city", "méxico", "monterrey", "guadalajara",
             "zapopan", "akron", "bbva")
_CAN_KEYS = ("toronto", "vancouver", "bmo", "bc place")


def venue_country(venue):
    v = (venue or "").lower()
    if any(k in v for k in _MEX_KEYS):
        return "MEX"
    if any(k in v for k in _CAN_KEYS):
        return "CAN"
    return "USA"


def is_host(team, venue):
    c = HOST_COUNTRY.get(team)
    return bool(c) and c == venue_country(venue)


def lookup_xg(XG, a, b):
    """Devuelve (xg_a, xg_b) probando ambos órdenes de la clave."""
    v = XG.get(f"{a}|{b}")
    if v:
        return float(v[0]), float(v[1])
    v = XG.get(f"{b}|{a}")
    if v:
        return float(v[1]), float(v[0])
    return None, None


_SCORE = re.compile(r"(\d+)\s*[–\-]\s*(\d+)")


def parse_score(s):
    """'3–2 (aet)' -> (3, 2, 0.75).  El tercer valor escala 120' a 90'."""
    m = _SCORE.search(s or "")
    if not m:
        return None
    gh, ga = int(m.group(1)), int(m.group(2))
    extra = ("aet" in s.lower()) or ("pens" in s.lower())
    return gh, ga, (0.75 if extra else 1.0)


def build(data, RES, XG, SCHED, REAL32, REAL_KO, r16, qf, sf, idx, KOVEN, brk_meta):
    """Devuelve la lista de partidos jugados, ordenada cronológicamente."""
    out = []

    # --- fase de grupos ---
    for g, date, home, hr, away, ar in data:
        real = RES.get(f"{home}|{away}")
        if not real:
            continue
        sc = SCHED.get("|".join(sorted([home, away])), {})
        venue = sc.get("venue", "")
        xh, xa = lookup_xg(XG, home, away)
        out.append(dict(
            mid=f"G:{home}|{away}", ih=idx[home], ia=idx[away],
            gh=int(real[0]), ga=int(real[1]),
            gh_obs=float(real[0]), ga_obs=float(real[1]),
            xgh=xh, xga=xa,
            host_h=is_host(home, venue), host_a=is_host(away, venue),
            date=sc.get("date", date), stage="grupos", w=1.0,
        ))

    # --- eliminatorias: resolver los emparejamientos reales ronda por ronda ---
    venue_of = {mid: ve for mid, dt, ve in brk_meta}
    date_of = {mid: dt for mid, dt, ve in brk_meta}
    for mid, (dt, ve) in KOVEN.items():
        venue_of.setdefault(mid, ve)
        date_of.setdefault(mid, dt)

    pairs = {mid: (a, b) for mid, a, b in REAL32}
    winner = {}
    for mid, (nm, _sc) in REAL_KO.items():
        winner[mid] = nm

    for mid, x, y in list(r16) + list(qf) + list(sf):
        if x in winner and y in winner:
            pairs[mid] = (winner[x], winner[y])

    for mid in sorted(pairs, key=lambda k: int(k[1:])):
        if mid not in REAL_KO:
            continue
        home, away = pairs[mid]
        win_name, raw = REAL_KO[mid]
        parsed = parse_score(raw)
        if not parsed:
            continue
        gh, ga, scale = parsed
        # El marcador está escrito desde la perspectiva del ganador; hay que
        # orientarlo al orden del emparejamiento o se invierte quién ganó.
        if gh != ga and win_name == away:
            gh, ga = ga, gh
        venue = venue_of.get(mid, "")
        xh, xa = lookup_xg(XG, home, away)
        out.append(dict(
            mid=mid, ih=idx[home], ia=idx[away],
            gh=gh, ga=ga, gh_obs=gh * scale, ga_obs=ga * scale,
            xgh=xh, xga=xa,
            host_h=is_host(home, venue), host_a=is_host(away, venue),
            date=date_of.get(mid, ""), stage="eliminatorias", w=1.0,
        ))

    out.sort(key=lambda m: datekey(m["date"]))
    return out
