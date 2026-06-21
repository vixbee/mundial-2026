import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
import math, numpy as np, json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, Reference

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
anchors=[(1,1877),(2,1876),(3,1875),(4,1826),(5,1764),(6,1761),(7,1758),(8,1756),(9,1735),(10,1730),
(11,1717),(12,1700),(13,1693),(14,1689),(15,1681),(16,1675),(17,1670),(18,1660),(19,1649),(20,1625),
(22,1600),(23,1594),(24,1590),(25,1586),(27,1578),(28,1566),(29,1560),(30,1555),(31,1548),(33,1535),
(34,1530),(38,1514),(40,1502),(41,1498),(42,1495),(45,1484),(46,1478),(50,1465),(56,1448),(57,1445),
(60,1435),(61,1432),(63,1426),(64,1423),(67,1414),(73,1396),(82,1368),(83,1365),(85,1358)]
xs=[a for a,_ in anchors]; ys=[b for _,b in anchors]
def pts(r):
    if r<=xs[0]: return ys[0]
    if r>=xs[-1]:
        sl=(ys[-1]-ys[-2])/(xs[-1]-xs[-2]); return ys[-1]+sl*(r-xs[-1])
    for i in range(len(xs)-1):
        if xs[i]<=r<=xs[i+1]:
            t=(r-xs[i])/(xs[i+1]-xs[i]); return ys[i]+t*(ys[i+1]-ys[i])
HOSTS={"México","Estados Unidos","Canadá"}; T=2.6
DIV_F=220.0; HB_F=60.0      # escala FIFA original (para "proyección original")
HB=60.0; DIV=220.0          # se reasignan a la escala Elo tras el ajuste
ELO={}                      # rating Elo por equipo
def pmf(k,l): return math.exp(-l)*l**k/math.factorial(k)
def lam(home,hr,away,ar):
    rh=ELO[home]+(HB if home in HOSTS else 0); ra=ELO[away]+(HB if away in HOSTS else 0)
    S=(rh-ra)/DIV; return max(0.18,(T+S)/2), max(0.18,(T-S)/2)
def model(home,hr,away,ar):
    lh,la=lam(home,hr,away,ar); Mx=9
    ph=[pmf(i,lh) for i in range(Mx)]; pa=[pmf(j,la) for j in range(Mx)]
    pw=pd=pl=0.0; best=(0,0); bp=-1
    for i in range(Mx):
        for j in range(Mx):
            p=ph[i]*pa[j]
            if p>bp: bp=p; best=(i,j)
            if i>j: pw+=p
            elif i==j: pd+=p
            else: pl+=p
    s=pw+pd+pl; return pw/s,pd/s,pl/s,best
def proj_fifa(home,hr,away,ar):
    rh=pts(hr)+(HB_F if home in HOSTS else 0); ra=pts(ar)+(HB_F if away in HOSTS else 0)
    S=(rh-ra)/DIV_F; lh=max(0.18,(T+S)/2); la=max(0.18,(T-S)/2)
    ph=[pmf(i,lh) for i in range(9)]; pa=[pmf(j,la) for j in range(9)]
    best=(0,0); bp=-1
    for i in range(9):
        for j in range(9):
            p=ph[i]*pa[j]
            if p>bp: bp=p; best=(i,j)
    return best

groups={}
for g,_,h,hr,a,ar in data:
    groups.setdefault(g,{}); groups[g][h]=hr; groups[g][a]=ar
names=[]; team_grp={}; team_rank={}
for g in sorted(groups):
    for nm,rk in groups[g].items():
        if nm not in team_grp: team_grp[nm]=g; team_rank[nm]=rk; names.append(nm)
idx={nm:i for i,nm in enumerate(names)}; NT=len(names)
# Rating Elo (eloratings) en vez del ranking FIFA, con recalibración del divisor por desviación estándar
ELO_KNOWN=json.load(open("elo.json",encoding="utf-8"))
_kp=np.array([pts(team_rank[nm]) for nm in ELO_KNOWN]); _ke=np.array([float(ELO_KNOWN[nm]) for nm in ELO_KNOWN])
_b,_a=np.polyfit(_kp,_ke,1)
for nm in names: ELO[nm]=float(ELO_KNOWN[nm]) if nm in ELO_KNOWN else float(_a+_b*pts(team_rank[nm]))
_pa=np.array([pts(team_rank[nm]) for nm in names]); _ea=np.array([ELO[nm] for nm in names])
ratio=float(np.std(_ea)/np.std(_pa))
DIV=DIV_F*ratio; HB=HB_F*ratio
rankpts=np.array([ELO[nm]+(HB if nm in HOSTS else 0) for nm in names])
# Ajuste por xG de partidos jugados (nutre la fuerza para los partidos por jugar)
XG=json.load(open("xg.json",encoding="utf-8"))
rankpts0=rankpts.copy()
xgf=np.zeros(NT);xga=np.zeros(NT);exf=np.zeros(NT);exa=np.zeros(NT);ng=np.zeros(NT)
for k,(xh,xa) in XG.items():
    h,a=k.split("|");ih=idx[h];ia=idx[a];S0=(rankpts0[ih]-rankpts0[ia])/DIV
    eh=max(0.18,(T+S0)/2);ea=max(0.18,(T-S0)/2)
    xgf[ih]+=xh;xga[ih]+=xa;exf[ih]+=eh;exa[ih]+=ea;ng[ih]+=1
    xgf[ia]+=xa;xga[ia]+=xh;exf[ia]+=ea;exa[ia]+=eh;ng[ia]+=1
AL=0.75;KX=55.0*ratio;MX=70.0*ratio;adj=np.zeros(NT)
for t in range(NT):
    if ng[t]==0:continue
    perf=math.log((xgf[t]+AL)/(exf[t]+AL))+math.log((exa[t]+AL)/(xga[t]+AL))
    adj[t]=max(-MX,min(MX,KX*perf*(ng[t]/(ng[t]+1.0))))
rankpts=rankpts0+adj

def wdl(rh,ra):
    S=(rh-ra)/DIV; lh=max(0.18,(T+S)/2); la=max(0.18,(T-S)/2); Mx=9
    ph=[pmf(i,lh) for i in range(Mx)]; pa=[pmf(j,la) for j in range(Mx)]
    pw=pd=pl=0.0
    for i in range(Mx):
        for j in range(Mx):
            p=ph[i]*pa[j]
            if i>j: pw+=p
            elif i==j: pd+=p
            else: pl+=p
    s=pw+pd+pl; return pw/s,pd/s,pl/s
Padv=np.zeros((NT,NT))
for i in range(NT):
    for j in range(NT):
        if i==j: continue
        pw,pd,pl=wdl(rankpts[i],rankpts[j]); Padv[i,j]=pw+(pd*pw/(pw+pl) if pw+pl>0 else .5)

Sarr=np.array([(rankpts[idx[d[2]]]-rankpts[idx[d[4]]])/DIV for d in data])
lam_h=np.maximum(0.18,(T+Sarr)/2)
lam_a=np.maximum(0.18,(T-Sarr)/2); Mt=len(data)
grp_matches={}
for mi,(g,_,h,hr,a,ar) in enumerate(data): grp_matches.setdefault(g,[]).append((mi,idx[h],idx[a]))
glist=sorted(grp_matches); gpos={g:i for i,g in enumerate(glist)}
grp_teams={g:sorted(groups[g].keys()) for g in groups}
grp_local={g:{nm:i for i,nm in enumerate(grp_teams[g])} for g in groups}

N=20000; rng=np.random.default_rng(20260611)
hg=rng.poisson(lam_h,size=(N,Mt)); ag=rng.poisson(lam_a,size=(N,Mt))
RES=json.load(open("results.json",encoding="utf-8"))
midx={(d[2],d[4]):i for i,d in enumerate(data)}
for k,(gh,ga) in RES.items():
    h,a=k.split("|"); mi=midx[(h,a)]; hg[:,mi]=gh; ag[:,mi]=ga
FIRST=np.zeros((N,12),dtype=int);SEC=np.zeros((N,12),dtype=int);THIRD=np.zeros((N,12),dtype=int)
tkeys=np.zeros((N,12)); first=np.zeros(NT);second=np.zeros(NT);third_adv=np.zeros(NT);adv=np.zeros(NT)
for gp,g in enumerate(glist):
    lc=grp_local[g]; nt=len(grp_teams[g]); gl=np.array([idx[nm] for nm in grp_teams[g]])
    P=np.zeros((N,nt));GF=np.zeros((N,nt));GA=np.zeros((N,nt))
    for mi,hi,ai in grp_matches[g]:
        hl=lc[names[hi]];al=lc[names[ai]];h=hg[:,mi];a=ag[:,mi]
        GF[:,hl]+=h;GA[:,hl]+=a;GF[:,al]+=a;GA[:,al]+=h
        dr=h==a;P[:,hl]+=np.where(h>a,3,np.where(dr,1,0));P[:,al]+=np.where(a>h,3,np.where(dr,1,0))
    key=P*1e6+(GF-GA)*1e3+GF*1e1+rng.random((N,nt));order=np.argsort(-key,axis=1)
    FIRST[:,gp]=gl[order[:,0]];SEC[:,gp]=gl[order[:,1]];THIRD[:,gp]=gl[order[:,2]];tkeys[:,gp]=key[np.arange(N),order[:,2]]
    first+=np.bincount(gl[order[:,0]],minlength=NT);second+=np.bincount(gl[order[:,1]],minlength=NT)
ot=np.argsort(-tkeys,axis=1);top8=ot[:,:8];qmask=np.zeros((N,12),bool);qmask[np.arange(N)[:,None],top8]=True
for gp in range(12):
    adv+=np.bincount(FIRST[:,gp],minlength=NT)+np.bincount(SEC[:,gp],minlength=NT)
    m=qmask[:,gp];c=np.bincount(THIRD[m,gp],minlength=NT);third_adv+=c;adv+=c

slots=[("M74",set("ABCDF")),("M77",set("CDFGH")),("M79",set("CEFHI")),("M80",set("EHIJK")),
       ("M81",set("BEFIJ")),("M82",set("AEHIJ")),("M85",set("EFGIJ")),("M87",set("DEIJL"))]
def match_thirds(advg):
    assign={};used=set();ss=sorted(slots,key=lambda s:sum(1 for g in advg if g in s[1]))
    def bt(i):
        if i==len(ss):return True
        sid,elig=ss[i]
        for g in advg:
            if g in elig and g not in used:
                used.add(g);assign[sid]=g
                if bt(i+1):return True
                used.discard(g);assign.pop(sid,None)
        return False
    bt(0);return assign
GL=list("ABCDEFGHIJKL")
r16=[("M89","M74","M77"),("M90","M73","M75"),("M91","M76","M78"),("M92","M79","M80"),
     ("M93","M83","M84"),("M94","M81","M82"),("M95","M86","M88"),("M96","M85","M87")]
qf=[("M97","M89","M90"),("M98","M93","M94"),("M99","M91","M92"),("M100","M95","M96")]
sf=[("M101","M97","M98"),("M102","M99","M100")]
oct=np.zeros(NT);cua=np.zeros(NT);sem=np.zeros(NT);fin=np.zeros(NT);champ=np.zeros(NT)
U=rng.random((N,31))
r32order=["M73","M74","M75","M76","M77","M78","M79","M80","M81","M82","M83","M84","M85","M86","M87","M88"]
for t in range(N):
    F=FIRST[t];Sd=SEC[t];Th=THIRD[t]
    advg=[GL[gp] for gp in range(12) if qmask[t,gp]];am=match_thirds(advg)
    third={sid:Th[gpos[am[sid]]] for sid in am}
    W={GL[gp]:F[gp] for gp in range(12)};R={GL[gp]:Sd[gp] for gp in range(12)}
    m={"M73":(R["A"],R["B"]),"M74":(W["E"],third["M74"]),"M75":(W["F"],R["C"]),"M76":(W["C"],R["F"]),
       "M77":(W["I"],third["M77"]),"M78":(R["E"],R["I"]),"M79":(W["A"],third["M79"]),"M80":(W["L"],third["M80"]),
       "M81":(W["D"],third["M81"]),"M82":(W["G"],third["M82"]),"M83":(R["K"],R["L"]),"M84":(W["H"],R["J"]),
       "M85":(W["B"],third["M85"]),"M86":(W["J"],R["H"]),"M87":(W["K"],third["M87"]),"M88":(R["D"],R["G"])}
    win={};ui=0
    for sid in r32order:
        a,b=m[sid];w=a if U[t,ui]<Padv[a,b] else b;ui+=1;win[sid]=w;oct[w]+=1
    for sid,x,y in r16:
        a,b=win[x],win[y];w=a if U[t,ui]<Padv[a,b] else b;ui+=1;win[sid]=w;cua[w]+=1
    for sid,x,y in qf:
        a,b=win[x],win[y];w=a if U[t,ui]<Padv[a,b] else b;ui+=1;win[sid]=w;sem[w]+=1
    for sid,x,y in sf:
        a,b=win[x],win[y];w=a if U[t,ui]<Padv[a,b] else b;ui+=1;win[sid]=w;fin[w]+=1
    a,b=win["M101"],win["M102"];w=a if U[t,ui]<Padv[a,b] else b;champ[w]+=1

# seeds for bracket sheet (most-likely)
Wm={};Rm={};Thm={};Thp={}
for g in glist:
    by=sorted(grp_teams[g],key=lambda nm:adv[idx[nm]],reverse=True);q1,q2,q3=by[0],by[1],by[2]
    if first[idx[q1]]>=first[idx[q2]]: Wm[g],Rm[g]=q1,q2
    else: Wm[g],Rm[g]=q2,q1
    Thm[g]=q3;Thp[g]=third_adv[idx[q3]]/N
advg8=[g for g,_ in sorted(Thp.items(),key=lambda kv:kv[1],reverse=True)[:8]]
amap=match_thirds(advg8)
def sl(t_,c): return f"{t_} ({c})"
def thr(sid): return sl(Thm[amap[sid]],f"3º {amap[sid]}")
R32=[("M73","28 jun","SoFi, Los Ángeles",sl(Rm['A'],'2A'),sl(Rm['B'],'2B')),
 ("M74","29 jun","Gillette, Boston",sl(Wm['E'],'1E'),thr("M74")),("M75","29 jun","Estadio BBVA, Monterrey",sl(Wm['F'],'1F'),sl(Rm['C'],'2C')),
 ("M76","29 jun","NRG, Houston",sl(Wm['C'],'1C'),sl(Rm['F'],'2F')),("M77","30 jun","MetLife, Nueva York/NJ",sl(Wm['I'],'1I'),thr("M77")),
 ("M78","30 jun","AT&T, Dallas",sl(Rm['E'],'2E'),sl(Rm['I'],'2I')),("M79","30 jun","Estadio Azteca, CDMX",sl(Wm['A'],'1A'),thr("M79")),
 ("M80","1 jul","",sl(Wm['L'],'1L'),thr("M80")),("M81","1 jul","",sl(Wm['D'],'1D'),thr("M81")),
 ("M82","1 jul","",sl(Wm['G'],'1G'),thr("M82")),("M83","2 jul","BMO Field, Toronto",sl(Rm['K'],'2K'),sl(Rm['L'],'2L')),
 ("M84","2 jul","SoFi, Los Ángeles",sl(Wm['H'],'1H'),sl(Rm['J'],'2J')),("M85","2 jul","BC Place, Vancouver",sl(Wm['B'],'1B'),thr("M85")),
 ("M86","3 jul","Hard Rock, Miami",sl(Wm['J'],'1J'),sl(Rm['H'],'2H')),("M87","3 jul","Arrowhead, Kansas City",sl(Wm['K'],'1K'),thr("M87")),
 ("M88","3 jul","AT&T, Dallas",sl(Rm['D'],'2D'),sl(Rm['G'],'2G'))]

# ================= WORKBOOK =================
wb=Workbook(); FONT="Arial"
green=PatternFill("solid",fgColor="C6EFCE");yellow=PatternFill("solid",fgColor="FFEB9C");red=PatternFill("solid",fgColor="FFC7CE");blue=PatternFill("solid",fgColor="DDEBF7")
hdrf=PatternFill("solid",fgColor="1F3864");hf=Font(name=FONT,color="FFFFFF",bold=True,size=11)
thin=Side(style="thin",color="D9D9D9");bd=Border(left=thin,right=thin,top=thin,bottom=thin)
ctr=Alignment(horizontal="center",vertical="center");lft=Alignment(horizontal="left",vertical="center")
def hdr(ws,headers,row,maxcol):
    for c,h in enumerate(headers,1):
        cell=ws.cell(row=row,column=c,value=h);cell.fill=hdrf;cell.font=hf;cell.alignment=ctr;cell.border=bd

# Sheet 0: Inicio
ws0=wb.active; ws0.title="Inicio"
ws0["A1"]="Proyección Mundial 2026 — Archivo maestro"; ws0["A1"].font=Font(name=FONT,bold=True,size=18)
ws0["A2"]="Modelo basado en el ranking FIFA del 11 de junio de 2026"; ws0["A2"].font=Font(name=FONT,italic=True,size=11,color="595959")
intro=[("",""),
 ("Contenido del archivo",""),
 ("1. Partidos A-L","Proyección de los 72 partidos de grupos: probabilidad de victoria/empate/derrota, marcador más probable y ganador."),
 ("2. Avance Montecarlo","Probabilidad de cada selección de ganar su grupo y de avanzar (20.000 torneos simulados)."),
 ("3. Gráficos avance","Barras de probabilidad de avanzar por grupo."),
 ("4. Cuadro R32","Dieciseisavos emparejados con los clasificados más probables (estructura oficial FIFA)."),
 ("5. Camino a la final","Probabilidad de llegar a octavos, cuartos, semis, final y de ser campeón."),
 ("6. Favoritos","Gráfico de los 12 candidatos al título."),
 ("",""),
 ("Metodología",""),
 ("Puntos","Cada posición FIFA se convierte en puntos aproximados; la diferencia alimenta una fórmula tipo Elo (divisor 600)."),
 ("Goles","Del desbalance se derivan goles esperados y se modelan con Poisson (media 2.6 goles/partido)."),
 ("Anfitriones","Ventaja de +60 puntos solo a México, EE.UU. y Canadá en sus partidos."),
 ("Simulación","20.000 torneos completos con puntos 3/1/0, desempates oficiales y penales por fuerza relativa."),
 ("",""),
 ("Advertencias","Es una estimación probabilística reproducible, NO un pronóstico fiable. Solo usa el ranking: ignora lesiones, forma y bajas. Los cruces de octavos en adelante usan el orden estándar del cuadro."),
]
r=4
for a,b in intro:
    ca=ws0.cell(row=r,column=1,value=a); cb=ws0.cell(row=r,column=2,value=b)
    if a in ("Contenido del archivo","Metodología","Advertencias"): ca.font=Font(name=FONT,bold=True,size=12)
    else: ca.font=Font(name=FONT,bold=True,size=10)
    cb.font=Font(name=FONT,size=10); cb.alignment=Alignment(wrap_text=True,vertical="top")
    r+=1
ws0.column_dimensions["A"].width=20; ws0.column_dimensions["B"].width=95

# Sheet 1: Partidos A-L
ws=wb.create_sheet("Partidos A-L")
ws["A1"]="Resultados reales y proyección — 72 partidos de grupos (hora de Ciudad de México)"; ws["A1"].font=Font(name=FONT,bold=True,size=14); ws.merge_cells("A1:R1")
SCHED=json.load(open("sched.json",encoding="utf-8"))
H=["Grupo","Fecha","Hora (CDMX)","Estadio","Local","Rank L","Visitante","Rank V","Dif. ranking","Prob. Local","Prob. Empate","Prob. Visitante","Marcador","Pronóstico / Resultado","Ganador / Empate","Estado","Proy. original","xG (L–V)"]
hdr(ws,H,3,18); r=4
for g,date,home,hrk,away,ark in data:
    pw,pd,pl,best=model(home,hrk,away,ark)
    sc=SCHED["|".join(sorted([home,away]))]
    real=RES.get(f"{home}|{away}")
    projo="%d – %d"%proj_fifa(home,hrk,away,ark)
    xgp=XG.get(f"{home}|{away}"); xgstr=f"{xgp[0]:.2f} – {xgp[1]:.2f}" if xgp else "—"
    if real:
        gh,ga=real; marc=f"{gh} – {ga}"; estado="FINAL"
        if gh>ga: pron=f"Ganó {home}";gan=home;fav=5
        elif ga>gh: pron=f"Ganó {away}";gan=away;fav=7
        else: pron="Empate";gan="Empate";fav=None
    else:
        marc="—"; estado="Proyección"
        gap=pw-pl
        if abs(gap)<0.08: pron="Parejo";gan="Empate";fav=None
        elif gap>0: pron=f"Favorito: {home}";gan=home;fav=5
        else: pron=f"Favorito: {away}";gan=away;fav=7
    vals=[g,sc["date"],sc["time"],sc["venue"],home,hrk,away,ark,f"=ABS(F{r}-H{r})",round(pw,3),round(pd,3),round(pl,3),marc,pron,gan,estado,projo,xgstr]
    for c,v in enumerate(vals,1):
        cell=ws.cell(row=r,column=c,value=v); cell.border=bd; cell.font=Font(name=FONT,size=11)
        cell.alignment=lft if c in (4,5,7,14) else ctr
    for c in (10,11,12): ws.cell(row=r,column=c).number_format="0%"
    ws.cell(row=r,column=17).font=Font(name=FONT,size=11,italic=True,color="7F7F7F")
    if estado=="FINAL": ws.cell(row=r,column=16).font=Font(name=FONT,size=11,bold=True,color="1F3864")
    if fav is None:
        for c in (13,14,15): ws.cell(row=r,column=c).fill=yellow; ws.cell(row=r,column=c).font=Font(name=FONT,size=11,bold=True,color="9C6500")
    else:
        ws.cell(row=r,column=fav).fill=green; ws.cell(row=r,column=fav).font=Font(name=FONT,size=11,bold=True,color="006100")
        for c in (14,15): ws.cell(row=r,column=c).fill=green; ws.cell(row=r,column=c).font=Font(name=FONT,size=11,bold=True,color="006100")
    r+=1
for col,wd in {"A":7,"B":9,"C":10,"D":30,"E":20,"F":8,"G":20,"H":8,"I":12,"J":11,"K":12,"L":13,"M":12,"N":22,"O":20,"P":12,"Q":13,"R":13}.items(): ws.column_dimensions[col].width=wd
ws.freeze_panes="A4"; ws.auto_filter.ref=f"A3:R{r-1}"

# Sheet 2: Avance Montecarlo
wsA=wb.create_sheet("Avance Montecarlo")
wsA["A1"]="Probabilidad de avanzar — Montecarlo (20.000 torneos)"; wsA["A1"].font=Font(name=FONT,bold=True,size=14); wsA.merge_cells("A1:G1")
hdr(wsA,["Grupo","Selección","Rank","Prob. ganar grupo","Prob. 1º o 2º","Prob. avanzar","Prob. avanzar"],3,7); r=4; grp_rows={}
for g in glist:
    rowsg=sorted([(nm,team_rank[nm],first[idx[nm]]/N,(first[idx[nm]]+second[idx[nm]])/N,adv[idx[nm]]/N) for nm in grp_teams[g]],key=lambda x:x[4],reverse=True)
    grp_rows[g]=(r,r+len(rowsg)-1)
    for nm,rk,pw,pt,pa in rowsg:
        for c,v in enumerate([g,nm,rk,round(pw,3),round(pt,3),round(pa,3),round(pa,3)],1):
            cell=wsA.cell(row=r,column=c,value=v); cell.border=bd; cell.font=Font(name=FONT,size=11); cell.alignment=lft if c==2 else ctr
        for c in (4,5,6,7): wsA.cell(row=r,column=c).number_format="0%"
        if pa>=0.55: f,fc=green,"006100"
        elif pa>=0.25: f,fc=yellow,"9C6500"
        else: f,fc=red,"9C0006"
        for c in (2,7): wsA.cell(row=r,column=c).fill=f; wsA.cell(row=r,column=c).font=Font(name=FONT,size=11,bold=True,color=fc)
        r+=1
for col,wd in {"A":7,"B":20,"C":7,"D":17,"E":13,"F":13,"G":13}.items(): wsA.column_dimensions[col].width=wd
wsA.freeze_panes="A4"; wsA.auto_filter.ref=f"A3:G{r-1}"

# Sheet 3: Gráficos avance
wsG=wb.create_sheet("Gráficos avance")
wsG["A1"]="Probabilidad de avanzar por grupo"; wsG["A1"].font=Font(name=FONT,bold=True,size=14)
for i,g in enumerate(glist):
    r0,r1=grp_rows[g]; ch=BarChart(); ch.type="col"; ch.title=f"Grupo {g}"; ch.legend=None
    ch.y_axis.numFmt='0%'; ch.y_axis.scaling.min=0; ch.y_axis.scaling.max=1; ch.height=6.2; ch.width=10
    ch.add_data(Reference(wsA,min_col=7,min_row=r0,max_row=r1),titles_from_data=False)
    ch.set_categories(Reference(wsA,min_col=2,min_row=r0,max_row=r1))
    wsG.add_chart(ch,f"{'B' if i%2==0 else 'L'}{3+(i//2)*13}")

# Sheet 4: Cuadro R32
wsR=wb.create_sheet("Cuadro R32")
wsR["A1"]="Dieciseisavos (Round of 32) — clasificados más probables"; wsR["A1"].font=Font(name=FONT,bold=True,size=14); wsR.merge_cells("A1:E1")
hdr(wsR,["Partido","Fecha","Equipo 1 (proyectado)","Equipo 2 (proyectado)","Sede"],3,5); r=4
for mid,fe,se,e1,e2 in R32:
    for c,v in enumerate([mid,fe,e1,e2,se],1):
        cell=wsR.cell(row=r,column=c,value=v); cell.border=bd; cell.font=Font(name=FONT,size=11); cell.alignment=ctr if c in(1,2) else lft
        if c in (3,4): cell.fill=blue
    r+=1
for col,wd in {"A":9,"B":9,"C":30,"D":30,"E":26}.items(): wsR.column_dimensions[col].width=wd
wsR.freeze_panes="A4"

# Sheet 5: Camino a la final
wsK=wb.create_sheet("Camino a la final")
wsK["A1"]="Probabilidades en eliminatorias — Montecarlo"; wsK["A1"].font=Font(name=FONT,bold=True,size=14); wsK.merge_cells("A1:I1")
hdr(wsK,["Selección","Grupo","Rank","Clasifica","Octavos","Cuartos","Semifinal","Final","Campeón"],3,9)
allrows=sorted([(names[i],team_grp[names[i]],team_rank[names[i]],adv[i]/N,oct[i]/N,cua[i]/N,sem[i]/N,fin[i]/N,champ[i]/N) for i in range(NT)],key=lambda x:x[8],reverse=True)
r=4
for nm,g,rk,pcl,po,pc,ps,pf,pch in allrows:
    for c,v in enumerate([nm,g,rk,round(pcl,3),round(po,3),round(pc,3),round(ps,3),round(pf,3),round(pch,3)],1):
        cell=wsK.cell(row=r,column=c,value=v); cell.border=bd; cell.font=Font(name=FONT,size=11); cell.alignment=lft if c==1 else ctr
    for c in range(4,10): wsK.cell(row=r,column=c).number_format="0%"
    if pch>=0.15: f,fc=green,"006100"
    elif pch>=0.05: f,fc=yellow,"9C6500"
    else: f,fc=None,"000000"
    if f: wsK.cell(row=r,column=1).fill=f; wsK.cell(row=r,column=9).fill=f
    wsK.cell(row=r,column=9).font=Font(name=FONT,size=11,bold=True,color=fc)
    r+=1
for col,wd in {"A":20,"B":7,"C":7,"D":11,"E":10,"F":10,"G":11,"H":9,"I":10}.items(): wsK.column_dimensions[col].width=wd
wsK.freeze_panes="A4"; wsK.auto_filter.ref=f"A3:I{r-1}"

# Sheet 6: Favoritos (modelo con xG + mercado + mezcla)
ODDS=json.load(open("odds.json",encoding="utf-8"))
imp={nm:100.0/(o+100.0) for nm,o in ODDS.items()}; ssum=sum(imp.values())
pmkt={nm:imp[nm]/ssum for nm in imp}; WB=0.7
pmodel={names[i]:champ[i]/N for i in range(NT)}
blend={nm:WB*pmkt.get(nm,0.0)+(1-WB)*pmodel[nm] for nm in names}
bs=sum(blend.values()); blend={nm:blend[nm]/bs for nm in blend}
favs=sorted(names,key=lambda nm:blend[nm],reverse=True)[:12]
wsF=wb.create_sheet("Favoritos")
wsF["A1"]="Probabilidad de ser campeón — modelo (con xG) + mercado (cuotas)"; wsF["A1"].font=Font(name=FONT,bold=True,size=14); wsF.merge_cells("A1:D1")
wsF["A2"]="Mezcla 70% mercado / 30% modelo. Modelo = simulación condicionada a resultados reales y xG. Mercado = cuotas de campeón al 16 jun, sin margen de la casa."
wsF["A2"].font=Font(name=FONT,italic=True,size=9,color="595959"); wsF.merge_cells("A2:D2")
hdr(wsF,["Selección","Modelo","Mercado","Mezcla"],3,4)
for k,nm in enumerate(favs):
    wsF.cell(row=4+k,column=1,value=nm).alignment=lft; wsF.cell(row=4+k,column=1).border=bd
    for c,v in [(2,pmodel[nm]),(3,pmkt.get(nm,0.0)),(4,blend[nm])]:
        cell=wsF.cell(row=4+k,column=c,value=round(v,3)); cell.number_format="0%"; cell.alignment=ctr; cell.border=bd
    bl=blend[nm]
    if bl>=0.12: f,fc=green,"006100"
    elif bl>=0.05: f,fc=yellow,"9C6500"
    else: f,fc=None,None
    if f: wsF.cell(row=4+k,column=4).fill=f; wsF.cell(row=4+k,column=4).font=Font(name=FONT,size=11,bold=True,color=fc)
for col,wd in {"A":18,"B":10,"C":10,"D":10}.items(): wsF.column_dimensions[col].width=wd
ch=BarChart(); ch.type="bar"; ch.title="Probabilidad de campeón (mezcla)"; ch.legend=None; ch.x_axis.numFmt='0%'; ch.height=9; ch.width=16
ch.add_data(Reference(wsF,min_col=4,min_row=4,max_row=15),titles_from_data=False); ch.set_categories(Reference(wsF,min_col=1,min_row=4,max_row=15))
wsF.add_chart(ch,"F3")

# Sheet 7: Cuadro completo (octavos -> final)
KO=json.load(open("wcdata.json",encoding="utf-8"))["knockout"]
wsK2=wb.create_sheet("Cuadro octavos-final")
wsK2["A1"]="Proyección del cuadro — de octavos a la final (avanza el favorito del modelo)"; wsK2["A1"].font=Font(name=FONT,bold=True,size=14); wsK2.merge_cells("A1:D1")
wsK2["A2"]=("Ruta más probable partido a partido a partir del cuadro de dieciseisavos: en cada llave avanza el equipo con mayor probabilidad "
 "según el modelo (condicionado a los resultados reales al 16 jun). El equipo que avanza va en verde. Es un escenario único; su probabilidad conjunta es baja.")
wsK2["A2"].font=Font(name=FONT,italic=True,size=9,color="595959"); wsK2.merge_cells("A2:D2"); wsK2["A2"].alignment=Alignment(wrap_text=True,vertical="top"); wsK2.row_dimensions[2].height=42
def ko_block(ws,title,rows_,r0):
    c=ws.cell(row=r0,column=1,value=title); c.font=Font(name=FONT,bold=True,size=12,color="1F3864"); r0+=1
    for ci,h in enumerate(["Partido","Equipo 1","Equipo 2","Sede"],1):
        cell=ws.cell(row=r0,column=ci,value=h); cell.fill=hdrf; cell.font=hf; cell.alignment=ctr; cell.border=bd
    r0+=1
    for m in rows_:
        ws.cell(row=r0,column=1,value=m.get("mid","—")).alignment=ctr
        ws.cell(row=r0,column=2,value=m["a"]["es"]).alignment=lft
        ws.cell(row=r0,column=3,value=m["b"]["es"]).alignment=lft
        sede=(m.get("date","")+" · "+m.get("venue","")).strip(" ·")
        ws.cell(row=r0,column=4,value=sede).alignment=lft
        winc=2 if m["w"]=="a" else 3
        for ci in range(1,5):
            cell=ws.cell(row=r0,column=ci); cell.border=bd; cell.font=Font(name=FONT,size=11)
        ws.cell(row=r0,column=winc).fill=green; ws.cell(row=r0,column=winc).font=Font(name=FONT,size=11,bold=True,color="006100")
        r0+=1
    return r0+1
rr=4
rr=ko_block(wsK2,"Octavos de final",KO["octavos"],rr)
rr=ko_block(wsK2,"Cuartos de final",KO["cuartos"],rr)
rr=ko_block(wsK2,"Semifinales",KO["semis"],rr)
rr=ko_block(wsK2,"Final",[KO["final"]],rr)
rr=ko_block(wsK2,"Tercer lugar",[KO["third"]],rr)
champ_cell=wsK2.cell(row=rr,column=1,value=f"CAMPEÓN PROYECTADO: {KO['champion']['es']}  ({round(KO['champion_p']*100)}% en la simulación)")
champ_cell.font=Font(name=FONT,bold=True,size=13,color="006100"); wsK2.merge_cells(start_row=rr,start_column=1,end_row=rr,end_column=4)
for col,wd in {"A":12,"B":22,"C":22,"D":34}.items(): wsK2.column_dimensions[col].width=wd

wb.save("Proyeccion-Mundial-2026-MAESTRO.xlsx")
print("Hojas:", wb.sheetnames)
