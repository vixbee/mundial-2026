import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
import math, json, numpy as np

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
EN={"México":"Mexico","Sudáfrica":"South Africa","Corea del Sur":"South Korea","República Checa":"Czechia",
"Canadá":"Canada","Bosnia y Herzegovina":"Bosnia & Herz.","Catar":"Qatar","Suiza":"Switzerland",
"Estados Unidos":"USA","Paraguay":"Paraguay","Australia":"Australia","Turquía":"Türkiye","Brasil":"Brazil",
"Marruecos":"Morocco","Escocia":"Scotland","Haití":"Haiti","Alemania":"Germany","Curazao":"Curaçao",
"Costa de Marfil":"Ivory Coast","Ecuador":"Ecuador","Países Bajos":"Netherlands","Japón":"Japan","Suecia":"Sweden",
"Túnez":"Tunisia","Arabia Saudita":"Saudi Arabia","Uruguay":"Uruguay","España":"Spain","Cabo Verde":"Cape Verde",
"Bélgica":"Belgium","Egipto":"Egypt","Irán":"Iran","Nueva Zelanda":"New Zealand","Francia":"France","Senegal":"Senegal",
"Noruega":"Norway","Irak":"Iraq","Inglaterra":"England","Croacia":"Croatia","Panamá":"Panama","Ghana":"Ghana",
"Portugal":"Portugal","Colombia":"Colombia","RD Congo":"DR Congo","Uzbekistán":"Uzbekistan","Argentina":"Argentina",
"Austria":"Austria","Argelia":"Algeria","Jordania":"Jordan"}
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
ELO={}                      # rating Elo por equipo; se llena tras definir names
def pmf(k,l): return math.exp(-l)*l**k/math.factorial(k)
def lam(home,hr,away,ar):
    rh=ELO[home]+(HB if home in HOSTS else 0); ra=ELO[away]+(HB if away in HOSTS else 0)
    S=(rh-ra)/DIV; return max(0.18,(T+S)/2),max(0.18,(T-S)/2)
def model(home,hr,away,ar):
    lh,la=lam(home,hr,away,ar);Mx=9
    ph=[pmf(i,lh) for i in range(Mx)];pa=[pmf(j,la) for j in range(Mx)]
    pw=pd=pl=0.0;best=(0,0);bp=-1
    for i in range(Mx):
        for j in range(Mx):
            p=ph[i]*pa[j]
            if p>bp:bp=p;best=(i,j)
            if i>j:pw+=p
            elif i==j:pd+=p
            else:pl+=p
    s=pw+pd+pl;return pw/s,pd/s,pl/s,best
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
    groups.setdefault(g,{});groups[g][h]=hr;groups[g][a]=ar
names=[];team_grp={};team_rank={}
for g in sorted(groups):
    for nm,rk in groups[g].items():
        if nm not in team_grp:team_grp[nm]=g;team_rank[nm]=rk;names.append(nm)
idx={nm:i for i,nm in enumerate(names)};NT=len(names)
# --- Rating Elo (eloratings) en vez del ranking FIFA, con recalibración del divisor ---
ELO_KNOWN=json.load(open("elo.json",encoding="utf-8"))
_kp=np.array([pts(team_rank[nm]) for nm in ELO_KNOWN]);_ke=np.array([float(ELO_KNOWN[nm]) for nm in ELO_KNOWN])
_b,_a=np.polyfit(_kp,_ke,1)
for nm in names: ELO[nm]=float(ELO_KNOWN[nm]) if nm in ELO_KNOWN else float(_a+_b*pts(team_rank[nm]))
_pa=np.array([pts(team_rank[nm]) for nm in names]);_ea=np.array([ELO[nm] for nm in names])
ratio=float(np.std(_ea)/np.std(_pa))
DIV=DIV_F*ratio; HB=HB_F*ratio
rankpts=np.array([ELO[nm]+(HB if nm in HOSTS else 0) for nm in names])
# Ajuste por xG de partidos jugados: nutre la fuerza usada para los partidos POR JUGAR.
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
    S=(rh-ra)/DIV;lh=max(0.18,(T+S)/2);la=max(0.18,(T-S)/2);Mx=9
    ph=[pmf(i,lh) for i in range(Mx)];pa=[pmf(j,la) for j in range(Mx)]
    pw=pd=pl=0.0
    for i in range(Mx):
        for j in range(Mx):
            p=ph[i]*pa[j]
            if i>j:pw+=p
            elif i==j:pd+=p
            else:pl+=p
    s=pw+pd+pl;return pw/s,pd/s,pl/s
Padv=np.zeros((NT,NT))
for i in range(NT):
    for j in range(NT):
        if i==j:continue
        pw,pd,pl=wdl(rankpts[i],rankpts[j]);Padv[i,j]=pw+(pd*pw/(pw+pl) if pw+pl>0 else .5)
Sarr=np.array([(rankpts[idx[d[2]]]-rankpts[idx[d[4]]])/DIV for d in data])
lam_h=np.maximum(0.18,(T+Sarr)/2)
lam_a=np.maximum(0.18,(T-Sarr)/2);Mt=len(data)
grp_matches={}
for mi,(g,_,h,hr,a,ar) in enumerate(data):grp_matches.setdefault(g,[]).append((mi,idx[h],idx[a]))
glist=sorted(grp_matches);gpos={g:i for i,g in enumerate(glist)}
grp_teams={g:sorted(groups[g].keys()) for g in groups}
grp_local={g:{nm:i for i,nm in enumerate(grp_teams[g])} for g in groups}
N=20000;rng=np.random.default_rng(20260611)
hg=rng.poisson(lam_h,size=(N,Mt));ag=rng.poisson(lam_a,size=(N,Mt))
RES=json.load(open("results.json",encoding="utf-8"))
midx={(d[2],d[4]):i for i,d in enumerate(data)}
for k,(gh,ga) in RES.items():
    h,a=k.split("|"); mi=midx[(h,a)]; hg[:,mi]=gh; ag[:,mi]=ga
FIRST=np.zeros((N,12),int);SEC=np.zeros((N,12),int);THIRD=np.zeros((N,12),int)
tk=np.zeros((N,12));first=np.zeros(NT);second=np.zeros(NT);third_adv=np.zeros(NT);adv=np.zeros(NT)
for gp,g in enumerate(glist):
    lc=grp_local[g];nt=len(grp_teams[g]);gl=np.array([idx[nm] for nm in grp_teams[g]])
    P=np.zeros((N,nt));GF=np.zeros((N,nt));GA=np.zeros((N,nt))
    for mi,hi,ai in grp_matches[g]:
        hl=lc[names[hi]];al=lc[names[ai]];h=hg[:,mi];a=ag[:,mi]
        GF[:,hl]+=h;GA[:,hl]+=a;GF[:,al]+=a;GA[:,al]+=h
        dr=h==a;P[:,hl]+=np.where(h>a,3,np.where(dr,1,0));P[:,al]+=np.where(a>h,3,np.where(dr,1,0))
    key=P*1e6+(GF-GA)*1e3+GF*1e1+rng.random((N,nt));o=np.argsort(-key,axis=1)
    FIRST[:,gp]=gl[o[:,0]];SEC[:,gp]=gl[o[:,1]];THIRD[:,gp]=gl[o[:,2]];tk[:,gp]=key[np.arange(N),o[:,2]]
    first+=np.bincount(gl[o[:,0]],minlength=NT);second+=np.bincount(gl[o[:,1]],minlength=NT)
ot=np.argsort(-tk,axis=1);top8=ot[:,:8];qmask=np.zeros((N,12),bool);qmask[np.arange(N)[:,None],top8]=True
for gp in range(12):
    adv+=np.bincount(FIRST[:,gp],minlength=NT)+np.bincount(SEC[:,gp],minlength=NT)
    m=qmask[:,gp];c=np.bincount(THIRD[m,gp],minlength=NT);third_adv+=c;adv+=c
slots=[("M74",set("ABCDF")),("M77",set("CDFGH")),("M79",set("CEFHI")),("M80",set("EHIJK")),
       ("M81",set("BEFIJ")),("M82",set("AEHIJ")),("M85",set("EFGIJ")),("M87",set("DEIJL"))]
def mt(advg):
    assign={};used=set();ss=sorted(slots,key=lambda s:sum(1 for g in advg if g in s[1]))
    def bt(i):
        if i==len(ss):return True
        sid,el=ss[i]
        for g in advg:
            if g in el and g not in used:
                used.add(g);assign[sid]=g
                if bt(i+1):return True
                used.discard(g);assign.pop(sid,None)
        return False
    bt(0);return assign
GL=list("ABCDEFGHIJKL")
r16=[("M89","M74","M77"),("M90","M73","M75"),("M91","M76","M78"),("M92","M79","M80"),("M93","M83","M84"),("M94","M81","M82"),("M95","M86","M88"),("M96","M85","M87")]
qf=[("M97","M89","M90"),("M98","M93","M94"),("M99","M91","M92"),("M100","M95","M96")];sf=[("M101","M97","M98"),("M102","M99","M100")]
oct=np.zeros(NT);cua=np.zeros(NT);sem=np.zeros(NT);fin=np.zeros(NT);champ=np.zeros(NT);U=rng.random((N,31))
ro=["M73","M74","M75","M76","M77","M78","M79","M80","M81","M82","M83","M84","M85","M86","M87","M88"]
for t in range(N):
    F=FIRST[t];Sd=SEC[t];Th=THIRD[t];advg=[GL[gp] for gp in range(12) if qmask[t,gp]];am=mt(advg)
    third={sid:Th[gpos[am[sid]]] for sid in am};W={GL[gp]:F[gp] for gp in range(12)};R={GL[gp]:Sd[gp] for gp in range(12)}
    m={"M73":(R["A"],R["B"]),"M74":(W["E"],third["M74"]),"M75":(W["F"],R["C"]),"M76":(W["C"],R["F"]),"M77":(W["I"],third["M77"]),"M78":(R["E"],R["I"]),"M79":(W["A"],third["M79"]),"M80":(W["L"],third["M80"]),"M81":(W["D"],third["M81"]),"M82":(W["G"],third["M82"]),"M83":(R["K"],R["L"]),"M84":(W["H"],R["J"]),"M85":(W["B"],third["M85"]),"M86":(W["J"],R["H"]),"M87":(W["K"],third["M87"]),"M88":(R["D"],R["G"])}
    win={};ui=0
    for sid in ro:
        a,b=m[sid];w=a if U[t,ui]<Padv[a,b] else b;ui+=1;win[sid]=w;oct[w]+=1
    for sid,x,y in r16:
        a,b=win[x],win[y];w=a if U[t,ui]<Padv[a,b] else b;ui+=1;win[sid]=w;cua[w]+=1
    for sid,x,y in qf:
        a,b=win[x],win[y];w=a if U[t,ui]<Padv[a,b] else b;ui+=1;win[sid]=w;sem[w]+=1
    for sid,x,y in sf:
        a,b=win[x],win[y];w=a if U[t,ui]<Padv[a,b] else b;ui+=1;win[sid]=w;fin[w]+=1
    a,b=win["M101"],win["M102"];w=a if U[t,ui]<Padv[a,b] else b;champ[w]+=1
Wm={};Rm={};Thm={};Thp={}
for g in glist:
    by=sorted(grp_teams[g],key=lambda nm:adv[idx[nm]],reverse=True);q1,q2,q3=by[0],by[1],by[2]
    if first[idx[q1]]>=first[idx[q2]]:Wm[g],Rm[g]=q1,q2
    else:Wm[g],Rm[g]=q2,q1
    Thm[g]=q3;Thp[g]=third_adv[idx[q3]]/N
advg8=[g for g,_ in sorted(Thp.items(),key=lambda kv:kv[1],reverse=True)[:8]];amap=mt(advg8)
def side(team,code): return {"es":team,"en":EN[team],"code":code}
def thrd(sid): g=amap[sid];return side(Thm[g],"3:"+g)
brk_meta=[("M73","28 jun","SoFi, Los Ángeles"),("M74","29 jun","Gillette, Boston"),("M75","29 jun","Estadio BBVA, Monterrey"),("M76","29 jun","NRG, Houston"),("M77","30 jun","MetLife, NY/NJ"),("M78","30 jun","AT&T, Dallas"),("M79","30 jun","Estadio Azteca, CDMX"),("M80","1 jul","—"),("M81","1 jul","—"),("M82","1 jul","—"),("M83","2 jul","BMO Field, Toronto"),("M84","2 jul","SoFi, Los Ángeles"),("M85","2 jul","BC Place, Vancouver"),("M86","3 jul","Hard Rock, Miami"),("M87","3 jul","Arrowhead, Kansas City"),("M88","3 jul","AT&T, Dallas")]
bsides={"M73":(side(Rm['A'],"2A"),side(Rm['B'],"2B")),"M74":(side(Wm['E'],"1E"),thrd("M74")),"M75":(side(Wm['F'],"1F"),side(Rm['C'],"2C")),"M76":(side(Wm['C'],"1C"),side(Rm['F'],"2F")),"M77":(side(Wm['I'],"1I"),thrd("M77")),"M78":(side(Rm['E'],"2E"),side(Rm['I'],"2I")),"M79":(side(Wm['A'],"1A"),thrd("M79")),"M80":(side(Wm['L'],"1L"),thrd("M80")),"M81":(side(Wm['D'],"1D"),thrd("M81")),"M82":(side(Wm['G'],"1G"),thrd("M82")),"M83":(side(Rm['K'],"2K"),side(Rm['L'],"2L")),"M84":(side(Wm['H'],"1H"),side(Rm['J'],"2J")),"M85":(side(Wm['B'],"1B"),thrd("M85")),"M86":(side(Wm['J'],"1J"),side(Rm['H'],"2H")),"M87":(side(Wm['K'],"1K"),thrd("M87")),"M88":(side(Rm['D'],"2D"),side(Rm['G'],"2G"))}

D={"groups":{}}
for g in glist:
    teams=sorted(grp_teams[g],key=lambda nm:adv[idx[nm]],reverse=True)
    D["groups"][g]={"teams":[{"es":nm,"en":EN[nm],"rank":team_rank[nm],"pwin":round(first[idx[nm]]/N,3),"padv":round(adv[idx[nm]]/N,3)} for nm in teams],"matches":[]}
SCHED=json.load(open("sched.json",encoding="utf-8"))
for g,date,home,hr,away,ar in data:
    pw,pd,pl,best=model(home,hr,away,ar);gap=pw-pl
    res="draw" if abs(gap)<0.08 else ("home" if gap>0 else "away")
    sc=SCHED["|".join(sorted([home,away]))]
    real=RES.get(f"{home}|{away}")
    bf=proj_fifa(home,hr,away,ar)
    md={"date":sc["date"],"time":sc["time"],"venue":sc["venue"],"h":home,"he":EN[home],"a":away,"ae":EN[away],"hr":hr,"ar":ar,"pw":round(pw,2),"pd":round(pd,2),"pl":round(pl,2),"sc":f"{best[0]}–{best[1]}","proj":f"{bf[0]}–{bf[1]}","xg":XG.get(f"{home}|{away}"),"res":res,"done":0}
    if real:
        gh,ga=real; md["done"]=1; md["sc"]=f"{gh}–{ga}"
        md["res"]="draw" if gh==ga else ("home" if gh>ga else "away")
    D["groups"][g]["matches"].append(md)
D["bracket"]=[{"mid":mid,"date":dt,"venue":ve,"e1":bsides[mid][0],"e2":bsides[mid][1]} for mid,dt,ve in brk_meta]
# Proyección de llaves: avanza el favorito por el modelo (condicionado a resultados reales)
def ti(nm): return idx[nm]
m32={mid:(ti(bsides[mid][0]["es"]),ti(bsides[mid][1]["es"])) for mid in ro}
def cw(a,b): return a if Padv[a,b]>=Padv[b,a] else b
def cl(a,b): return b if Padv[a,b]>=Padv[b,a] else a
def nmo(i): return {"es":names[i],"en":EN[names[i]]}
KOVEN={"M89":("4 jul","Lincoln Financial Field, Filadelfia"),"M90":("4 jul","NRG Stadium, Houston"),
 "M91":("5 jul","MetLife, Nueva York/NJ"),"M92":("5 jul","Estadio Azteca, Ciudad de México"),
 "M93":("6 jul","AT&T Stadium, Dallas"),"M94":("6 jul","Lumen Field, Seattle"),
 "M95":("7 jul","Mercedes-Benz, Atlanta"),"M96":("7 jul","BC Place, Vancouver"),
 "M97":("9 jul","Gillette Stadium, Boston"),"M98":("10 jul","SoFi Stadium, Los Ángeles"),
 "M99":("11 jul","Hard Rock Stadium, Miami"),"M100":("11 jul","Arrowhead Stadium, Kansas City"),
 "M101":("14 jul","AT&T Stadium, Dallas"),"M102":("15 jul","Mercedes-Benz, Atlanta"),
 "M103":("18 jul","Hard Rock Stadium, Miami"),"M104":("19 jul","MetLife, Nueva York/NJ")}
win={mid:cw(*m32[mid]) for mid in ro}
def rnd(pairs):
    out=[]
    for mid,x,y in pairs:
        a,b=win[x],win[y]; w=cw(a,b); win[mid]=w
        dt,ve=KOVEN.get(mid,("",""))
        out.append({"mid":mid,"a":nmo(a),"b":nmo(b),"w":"a" if w==a else "b","date":dt,"venue":ve})
    return out
octavos=rnd(r16); cuartos=rnd(qf); semis=rnd(sf)
fa,fb=win["M101"],win["M102"]; champ_idx=cw(fa,fb)
sl1=cl(win["M97"],win["M98"]); sl2=cl(win["M99"],win["M100"]); third3=cw(sl1,sl2)
fd,fv=KOVEN["M104"]; td,tv=KOVEN["M103"]
D["knockout"]={"octavos":octavos,"cuartos":cuartos,"semis":semis,
 "final":{"mid":"M104","a":nmo(fa),"b":nmo(fb),"w":"a" if champ_idx==fa else "b","date":fd,"venue":fv},
 "champion":nmo(champ_idx),"champion_p":round(champ[champ_idx]/N,3),
 "third":{"a":nmo(sl1),"b":nmo(sl2),"w":"a" if third3==sl1 else "b","date":td,"venue":tv}}
ODDS=json.load(open("odds.json",encoding="utf-8"))
imp={nm:100.0/(o+100.0) for nm,o in ODDS.items()};ssum=sum(imp.values())
pmkt={nm:imp[nm]/ssum for nm in imp}
WB=0.8
pmodel={names[i]:champ[i]/N for i in range(NT)}
blend={nm:WB*pmkt.get(nm,0.0)+(1-WB)*pmodel[nm] for nm in names}
bs=sum(blend.values());blend={nm:blend[nm]/bs for nm in blend}
chb=sorted(names,key=lambda nm:blend[nm],reverse=True)[:12]
D["champions"]=[{"es":nm,"en":EN[nm],"p":round(blend[nm],3),"pmodel":round(pmodel[nm],3),"pmkt":round(pmkt.get(nm,0.0),3)} for nm in chb]
D["blend_w"]=WB
import datetime as _dt
_M=["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]
_n=_dt.datetime.utcnow()-_dt.timedelta(hours=6)
D["generated"]=f"{_n.day} {_M[_n.month-1]} {_n.year}, {_n.strftime('%H:%M')} CDMX"
json.dump(D,open("wcdata.json","w"),ensure_ascii=False)
print("data ready; blended top:",chb[0],round(blend[chb[0]],3),"| modelo",round(pmodel[chb[0]],3),"| mercado",round(pmkt.get(chb[0],0),3))
