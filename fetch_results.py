#!/usr/bin/env python3
"""Adaptador: descarga resultados reales del Mundial 2026 desde openfootball
(JSON público, sin API key) y los escribe en results.json con el formato del modelo."""
import json, urllib.request, sys, os
HERE=os.path.dirname(os.path.abspath(__file__))
URL="https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
OF2ES={"Mexico":"México","South Africa":"Sudáfrica","South Korea":"Corea del Sur","Czech Republic":"República Checa",
"Canada":"Canadá","Bosnia & Herzegovina":"Bosnia y Herzegovina","Qatar":"Catar","Switzerland":"Suiza",
"USA":"Estados Unidos","Paraguay":"Paraguay","Australia":"Australia","Turkey":"Turquía","Brazil":"Brasil",
"Morocco":"Marruecos","Scotland":"Escocia","Haiti":"Haití","Germany":"Alemania","Curaçao":"Curazao",
"Ivory Coast":"Costa de Marfil","Ecuador":"Ecuador","Netherlands":"Países Bajos","Japan":"Japón","Sweden":"Suecia",
"Tunisia":"Túnez","Saudi Arabia":"Arabia Saudita","Uruguay":"Uruguay","Spain":"España","Cape Verde":"Cabo Verde",
"Belgium":"Bélgica","Egypt":"Egipto","Iran":"Irán","New Zealand":"Nueva Zelanda","France":"Francia","Senegal":"Senegal",
"Norway":"Noruega","Iraq":"Irak","England":"Inglaterra","Croatia":"Croacia","Panama":"Panamá","Ghana":"Ghana",
"Portugal":"Portugal","Colombia":"Colombia","DR Congo":"RD Congo","Uzbekistan":"Uzbekistán","Argentina":"Argentina",
"Austria":"Austria","Algeria":"Argelia","Jordan":"Jordania"}
def main():
    fixtures=json.load(open(os.path.join(HERE,"fixtures.json"),encoding="utf-8"))
    fixset={(h,a) for h,a in fixtures}
    req=urllib.request.Request(URL,headers={"User-Agent":"wc2026-projection"})
    data=json.load(urllib.request.urlopen(req,timeout=30))
    res={}
    for m in data.get("matches",[]):
        sc=m.get("score",{}).get("ft")
        t1,t2=m.get("team1"),m.get("team2")
        if not sc or t1 not in OF2ES or t2 not in OF2ES: continue
        h,a=OF2ES[t1],OF2ES[t2]; g1,g2=int(sc[0]),int(sc[1])
        if (h,a) in fixset: res[f"{h}|{a}"]=[g1,g2]
        elif (a,h) in fixset: res[f"{a}|{h}"]=[g2,g1]
    json.dump(res,open(os.path.join(HERE,"results.json"),"w"),ensure_ascii=False,indent=1)
    print(f"results.json actualizado: {len(res)} partidos con marcador real (fuente: openfootball)")
if __name__=="__main__": main()
