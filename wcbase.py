#!/usr/bin/env python3
"""Datos base del torneo y construcción del modelo — fuente única de verdad.

Antes, gen_html.py y master.py tenían cada uno su propia copia del cuadro, los
resultados reales y la maquinaria de ratings. Cualquier corrección había que
hacerla dos veces, y basta olvidar una para que las dos salidas se contradigan
(así se coló el cruce de semifinales mal emparejado). Ahora ambos importan de aquí.
"""
import os, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)) or "."

data = [
 ("A","11 jun","México",14,"Sudáfrica",60),("A","12 jun","Corea del Sur",25,"República Checa",40),
 ("A","18 jun","República Checa",40,"Sudáfrica",60),("A","19 jun","México",14,"Corea del Sur",25),
 ("A","25 jun","República Checa",40,"México",14),("A","25 jun","Sudáfrica",60,"Corea del Sur",25),
 ("B","12 jun","Canadá",30,"Bosnia y Herzegovina",64),("B","13 jun","Catar",56,"Suiza",19),
 ("B","18 jun","Suiza",19,"Bosnia y Herzegovina",64),("B","18 jun","Canadá",30,"Catar",56),
 ("B","24 jun","Suiza",19,"Canadá",30),("B","24 jun","Bosnia y Herzegovina",64,"Catar",56),
 ("C","13 jun","Estados Unidos",17,"Paraguay",41),("C","14 jun","Australia",27,"Turquía",22),
 ("C","19 jun","Estados Unidos",17,"Australia",27),("C","20 jun","Turquía",22,"Paraguay",41),
 ("C","26 jun","Turquía",22,"Estados Unidos",17),("C","26 jun","Paraguay",41,"Australia",27),
 ("D","13 jun","Brasil",6,"Marruecos",7),("D","14 jun","Haití",83,"Escocia",42),
 ("D","19 jun","Escocia",42,"Marruecos",7),("D","20 jun","Brasil",6,"Haití",83),
 ("D","24 jun","Marruecos",7,"Haití",83),("D","24 jun","Escocia",42,"Brasil",6),
 ("E","14 jun","Alemania",10,"Curazao",82),("E","14 jun","Costa de Marfil",33,"Ecuador",23),
 ("E","20 jun","Alemania",10,"Costa de Marfil",33),("E","21 jun","Ecuador",23,"Curazao",82),
 ("E","25 jun","Ecuador",23,"Alemania",10),("E","25 jun","Curazao",82,"Costa de Marfil",33),
 ("F","14 jun","Países Bajos",8,"Japón",18),("F","15 jun","Suecia",38,"Túnez",45),
 ("F","20 jun","Países Bajos",8,"Suecia",38),("F","21 jun","Túnez",45,"Japón",18),
 ("F","25 jun","Japón",18,"Suecia",38),("F","25 jun","Túnez",45,"Países Bajos",8),
 ("G","15 jun","Arabia Saudita",61,"Uruguay",16),("G","15 jun","España",2,"Cabo Verde",67),
 ("G","21 jun","España",2,"Arabia Saudita",61),("G","21 jun","Uruguay",16,"Cabo Verde",67),
 ("G","27 jun","Cabo Verde",67,"Arabia Saudita",61),("G","27 jun","Uruguay",16,"España",2),
 ("H","15 jun","Bélgica",9,"Egipto",29),("H","16 jun","Irán",20,"Nueva Zelanda",85),
 ("H","21 jun","Bélgica",9,"Irán",20),("H","22 jun","Nueva Zelanda",85,"Egipto",29),
 ("H","27 jun","Egipto",29,"Irán",20),("H","27 jun","Nueva Zelanda",85,"Bélgica",9),
 ("I","16 jun","Francia",3,"Senegal",15),("I","16 jun","Irak",57,"Noruega",31),
 ("I","22 jun","Francia",3,"Irak",57),("I","23 jun","Noruega",31,"Senegal",15),
 ("I","26 jun","Noruega",31,"Francia",3),("I","26 jun","Senegal",15,"Irak",57),
 ("J","17 jun","Inglaterra",4,"Croacia",11),("J","17 jun","Ghana",73,"Panamá",34),
 ("J","23 jun","Inglaterra",4,"Ghana",73),("J","23 jun","Panamá",34,"Croacia",11),
 ("J","27 jun","Croacia",11,"Ghana",73),("J","27 jun","Panamá",34,"Inglaterra",4),
 ("K","17 jun","Portugal",5,"RD Congo",46),("K","18 jun","Uzbekistán",50,"Colombia",13),
 ("K","23 jun","Portugal",5,"Uzbekistán",50),("K","24 jun","Colombia",13,"RD Congo",46),
 ("K","27 jun","Colombia",13,"Portugal",5),("K","27 jun","RD Congo",46,"Uzbekistán",50),
 ("L","17 jun","Argentina",1,"Argelia",28),("L","17 jun","Austria",24,"Jordania",63),
 ("L","22 jun","Argentina",1,"Austria",24),("L","23 jun","Jordania",63,"Argelia",28),
 ("L","28 jun","Argelia",28,"Austria",24),("L","28 jun","Jordania",63,"Argentina",1),
]

EN = {"México":"Mexico","Sudáfrica":"South Africa","Corea del Sur":"South Korea","República Checa":"Czechia",
"Canadá":"Canada","Bosnia y Herzegovina":"Bosnia & Herz.","Catar":"Qatar","Suiza":"Switzerland",
"Estados Unidos":"USA","Paraguay":"Paraguay","Australia":"Australia","Turquía":"Türkiye","Brasil":"Brazil",
"Marruecos":"Morocco","Escocia":"Scotland","Haití":"Haiti","Alemania":"Germany","Curazao":"Curaçao",
"Costa de Marfil":"Ivory Coast","Ecuador":"Ecuador","Países Bajos":"Netherlands","Japón":"Japan","Suecia":"Sweden",
"Túnez":"Tunisia","Arabia Saudita":"Saudi Arabia","Uruguay":"Uruguay","España":"Spain","Cabo Verde":"Cape Verde",
"Bélgica":"Belgium","Egipto":"Egypt","Irán":"Iran","Nueva Zelanda":"New Zealand","Francia":"France","Senegal":"Senegal",
"Noruega":"Norway","Irak":"Iraq","Inglaterra":"England","Croacia":"Croatia","Panamá":"Panama","Ghana":"Ghana",
"Portugal":"Portugal","Colombia":"Colombia","RD Congo":"DR Congo","Uzbekistán":"Uzbekistan","Argentina":"Argentina",
"Austria":"Austria","Argelia":"Algeria","Jordania":"Jordan"}

HOSTS = {"México", "Estados Unidos", "Canadá"}
T_GOALS = 2.6
DIV_F = 220.0
HB_F = 60.0

anchors = [(1,1877),(2,1876),(3,1875),(4,1826),(5,1764),(6,1761),(7,1758),(8,1756),(9,1735),(10,1730),
(11,1717),(12,1700),(13,1693),(14,1689),(15,1681),(16,1675),(17,1670),(18,1660),(19,1649),(20,1625),
(22,1600),(23,1594),(24,1590),(25,1586),(27,1578),(28,1566),(29,1560),(30,1555),(31,1548),(33,1535),
(34,1530),(38,1514),(40,1502),(41,1498),(42,1495),(45,1484),(46,1478),(50,1465),(56,1448),(57,1445),
(60,1435),(61,1432),(63,1426),(64,1423),(67,1414),(73,1396),(82,1368),(83,1365),(85,1358)]
_xs = [a for a, _ in anchors]
_ys = [b for _, b in anchors]


def pts(r):
    if r <= _xs[0]:
        return _ys[0]
    if r >= _xs[-1]:
        sl = (_ys[-1] - _ys[-2]) / (_xs[-1] - _xs[-2])
        return _ys[-1] + sl * (r - _xs[-1])
    for i in range(len(_xs) - 1):
        if _xs[i] <= r <= _xs[i + 1]:
            t = (r - _xs[i]) / (_xs[i + 1] - _xs[i])
            return _ys[i] + t * (_ys[i + 1] - _ys[i])


# ---- Cuadro real. Los grupos terminaron, así que los cruces son hechos, no proyección.
REAL32 = [("M73","Sudáfrica","Canadá"),("M74","Países Bajos","Marruecos"),("M75","Alemania","Paraguay"),
("M76","Francia","Suecia"),("M77","Costa de Marfil","Noruega"),("M78","Brasil","Japón"),
("M79","Inglaterra","RD Congo"),("M80","México","Ecuador"),("M81","Estados Unidos","Bosnia y Herzegovina"),
("M82","Bélgica","Senegal"),("M83","España","Austria"),("M84","Portugal","Croacia"),
("M85","Suiza","Argelia"),("M86","Colombia","Ghana"),("M87","Australia","Egipto"),("M88","Argentina","Cabo Verde")]

# Resultados reales: R32 (28 jun-3 jul), R16 (4-7 jul), cuartos (9-11 jul).
REAL_KO = {"M73":("Canadá","1–0"),"M74":("Marruecos","1–1 (pens)"),"M75":("Paraguay","1–1 (pens)"),
 "M76":("Francia","3–0"),"M77":("Noruega","2–1"),"M78":("Brasil","2–1"),"M79":("Inglaterra","2–1"),
 "M80":("México","2–0"),"M81":("Estados Unidos","2–0"),"M82":("Bélgica","3–2 (aet)"),"M83":("España","3–0"),
 "M84":("Portugal","2–1"),"M85":("Suiza","2–0"),"M86":("Colombia","1–0"),"M87":("Egipto","1–1 (pens)"),
 "M88":("Argentina","3–2 (aet)"),"M89":("Marruecos","3–0"),"M90":("Francia","1–0"),"M91":("Noruega","2–1"),
 "M92":("Inglaterra","3–2"),"M93":("Bélgica","4–1"),"M94":("España","1–0"),"M95":("Suiza","0–0 (pens)"),
 "M96":("Argentina","3–2"),
 "M97":("Francia","2–0"),"M98":("Inglaterra","2–1"),"M99":("España","2–1"),"M100":("Argentina","3–1 (aet)")}

ro = ["M73","M74","M75","M76","M77","M78","M79","M80","M81","M82","M83","M84","M85","M86","M87","M88"]
r16 = [("M89","M73","M74"),("M90","M75","M76"),("M91","M77","M78"),("M92","M79","M80"),
       ("M93","M81","M82"),("M94","M83","M84"),("M95","M85","M86"),("M96","M87","M88")]
qf = [("M97","M89","M90"),("M98","M91","M92"),("M99","M93","M94"),("M100","M95","M96")]
sf = [("M101","M97","M99"),("M102","M98","M100")]

brk_meta = [("M73","28 jun","SoFi, Los Ángeles"),("M74","29 jun","Estadio BBVA, Monterrey"),
 ("M75","29 jun","Gillette, Boston"),("M76","30 jun","MetLife, NY/NJ"),("M77","30 jun","AT&T, Dallas"),
 ("M78","29 jun","NRG, Houston"),("M79","1 jul","Mercedes-Benz, Atlanta"),("M80","1 jul","Estadio Azteca, CDMX"),
 ("M81","1 jul","Bay Area, San Francisco"),("M82","1 jul","Lumen Field, Seattle"),("M83","2 jul","SoFi, Los Ángeles"),
 ("M84","2 jul","BMO Field, Toronto"),("M85","2 jul","BC Place, Vancouver"),("M86","3 jul","Arrowhead, Kansas City"),
 ("M87","3 jul","AT&T, Dallas"),("M88","3 jul","Hard Rock, Miami")]

KOVEN = {"M89":("4 jul","NRG Stadium, Houston"),"M90":("4 jul","Lincoln Financial Field, Filadelfia"),
 "M91":("5 jul","MetLife, Nueva York/NJ"),"M92":("5 jul","Estadio Azteca, Ciudad de México"),
 "M93":("6 jul","AT&T Stadium, Dallas"),"M94":("6 jul","Lumen Field, Seattle"),
 "M95":("7 jul","Mercedes-Benz, Atlanta"),"M96":("7 jul","BC Place, Vancouver"),
 "M97":("9 jul","Gillette Stadium, Boston"),"M98":("10 jul","SoFi Stadium, Los Ángeles"),
 "M99":("11 jul","Hard Rock Stadium, Miami"),"M100":("11 jul","Arrowhead Stadium, Kansas City"),
 "M101":("14 jul","AT&T Stadium, Dallas"),"M102":("15 jul","Mercedes-Benz, Atlanta"),
 "M103":("18 jul","Hard Rock Stadium, Miami"),"M104":("19 jul","MetLife, Nueva York/NJ")}

KOTIME = {"M97":"14:00","M98":"13:00","M99":"15:00","M100":"19:00",
 "M101":"13:00","M102":"13:00","M103":"15:00","M104":"13:00"}

WINNERS_G = {"México","Suiza","Brasil","Estados Unidos","Alemania","Países Bajos","Bélgica","España",
             "Francia","Argentina","Colombia","Inglaterra"}
RUNNERS_G = {"Sudáfrica","Canadá","Marruecos","Australia","Costa de Marfil","Japón","Egipto","Cabo Verde",
             "Noruega","Austria","Portugal","Croacia"}


import re as _re
_SCORE_RE = _re.compile(r"(\d+)\s*[–\-]\s*(\d+)")


def oriented_score(mid, home, away):
    """Marcador reescrito en el orden (local, visitante) del emparejamiento.

    En REAL_KO el marcador está guardado desde la perspectiva del ganador
    ('Francia', '2–0'), así que mostrarlo tal cual junto a un cruce cuyo primer
    equipo es Marruecos daría a entender que ganó Marruecos.
    """
    entry = REAL_KO.get(mid)
    if not entry:
        return ""
    win, sc = entry
    m = _SCORE_RE.search(sc)
    if not m:
        return sc
    a, b = int(m.group(1)), int(m.group(2))
    suffix = sc[m.end():].strip()
    if a != b and win == away:
        a, b = b, a
    return f"{a}–{b}" + (f" {suffix}" if suffix else "")


def _load(name):
    return json.load(open(os.path.join(HERE, name), encoding="utf-8"))


def build_teams():
    """names, idx, team_grp, team_rank, groups a partir de la lista de partidos."""
    groups = {}
    for g, _, h, hr, a, ar in data:
        groups.setdefault(g, {})
        groups[g][h] = hr
        groups[g][a] = ar
    names, team_grp, team_rank = [], {}, {}
    for g in sorted(groups):
        for nm, rk in groups[g].items():
            if nm not in team_grp:
                team_grp[nm] = g
                team_rank[nm] = rk
                names.append(nm)
    return names, {nm: i for i, nm in enumerate(names)}, team_grp, team_rank, groups


def elo_strength(names, team_rank):
    """Fuerza previa por equipo, en las mismas unidades que el 'S' del modelo viejo."""
    ELO_KNOWN = _load("elo.json")
    _kp = np.array([pts(team_rank[nm]) for nm in ELO_KNOWN])
    _ke = np.array([float(ELO_KNOWN[nm]) for nm in ELO_KNOWN])
    b, a = np.polyfit(_kp, _ke, 1)
    ELO = {nm: (float(ELO_KNOWN[nm]) if nm in ELO_KNOWN else float(a + b * pts(team_rank[nm])))
           for nm in names}
    _pa = np.array([pts(team_rank[nm]) for nm in names])
    _ea = np.array([ELO[nm] for nm in names])
    ratio = float(np.std(_ea) / np.std(_pa))
    DIV = DIV_F * ratio
    ev = np.array([ELO[nm] for nm in names])
    return (ev - ev.mean()) / DIV, ELO, DIV, ratio


def build_model(verbose=False, refit=False):
    """Devuelve (mdl, ctx). Ajusta hiperparámetros por validación prequencial."""
    from model import DCModel, grid_search
    from history import build as build_history

    names, idx, team_grp, team_rank, groups = build_teams()
    strength, ELO, DIV, ratio = elo_strength(names, team_rank)

    RES = _load("results.json")
    XG = _load("xg.json")
    SCHED = _load("sched.json")
    matches = build_history(data, RES, XG, SCHED, REAL32, REAL_KO,
                            r16, qf, sf, idx, KOVEN, brk_meta)

    # rho y la ventaja de local se fijan a valores defendibles en vez de ajustarse:
    # con ~100 partidos, una rejilla libre los empuja a extremos implausibles
    # (hadv=0.55 implicaría que los anfitriones marcan 73% más). rho=-0.13 es el
    # valor de Dixon-Coles (1997) y el Brier confirma que ahí está el óptimo;
    # hadv=0.21 reproduce la calibración de ventaja local del modelo anterior.
    RHO_FIXED = -0.13
    HADV_FIXED = round(2.0 * (HB_F / DIV_F) / T_GOALS, 3)

    cache = os.path.join(HERE, "model_fit.json")
    hp = None
    if not refit and os.path.exists(cache):
        try:
            hp = json.load(open(cache, encoding="utf-8"))
        except Exception:
            hp = None
    if hp is None or hp.get("n_matches") != len(matches):
        ll, br, params, n = grid_search(
            names, strength, matches, T=T_GOALS,
            Ks=(0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12),
            rhos=(RHO_FIXED,), xgws=(0.0, 0.25, 0.5, 0.75, 1.0),
            hadvs=(HADV_FIXED,), verbose=verbose)
        base = DCModel(names, strength, T=T_GOALS, K=0.0, rho=0.0, xg_w=0.0,
                       hadv=HADV_FIXED)
        bll, bbr, _ = base.prequential(matches, learn=False)
        hp = dict(params, n_matches=n, logloss=ll, brier=br,
                  logloss_base=bll, brier_base=bbr)
        json.dump(hp, open(cache, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    mdl = DCModel(names, strength, T=T_GOALS, K=hp["K"], rho=hp["rho"],
                  xg_w=hp["xg_w"], hadv=hp["hadv"]).fit(matches)

    ctx = dict(names=names, idx=idx, team_grp=team_grp, team_rank=team_rank,
               groups=groups, ELO=ELO, DIV=DIV, ratio=ratio, strength=strength,
               matches=matches, RES=RES, XG=XG, SCHED=SCHED, hp=hp)
    return mdl, ctx
