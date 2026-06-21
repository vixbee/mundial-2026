import os
os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
import json
D=json.load(open("wcdata.json"))
html=r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Proyección Mundial 2026</title>
<style>
:root{
 --blue-900:#0a2a66;--blue-700:#143c8c;--blue-500:#1f5fd0;--gold:#ffc72c;
 --bg:#eaeef7;--card:#ffffff;--ink:#13233f;--muted:#5a6b86;--line:#dbe3f0;
 --green-bg:#d9f0dd;--green-fg:#1c6b2b;--amber-bg:#fdecc6;--amber-fg:#8a5a00;--red-bg:#fbdada;--red-fg:#9c2a2a;
 --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
 --sans:"Segoe UI",system-ui,-apple-system,Roboto,Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.45}
a{color:inherit}
.topbar{background:linear-gradient(120deg,var(--blue-900),var(--blue-700));color:#fff;padding:18px 20px;border-bottom:4px solid var(--gold)}
.topbar .wrap{max-width:1080px;margin:0 auto;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:12px}
.crest{width:42px;height:42px;border-radius:8px;background:var(--gold);color:var(--blue-900);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;font-family:var(--mono);letter-spacing:-1px}
.brand h1{font-size:20px;margin:0;font-weight:800;letter-spacing:.3px}
.brand p{margin:2px 0 0;font-size:12px;color:#c6d4f0}
.spacer{flex:1}
.lang{display:flex;border:1px solid rgba(255,255,255,.35);border-radius:999px;overflow:hidden;font-size:12px;font-weight:700}
.lang button{background:transparent;color:#c6d4f0;border:0;padding:7px 12px;cursor:pointer;font-weight:700}
.lang button.on{background:var(--gold);color:var(--blue-900)}
nav.tabs{position:sticky;top:0;z-index:5;background:#fff;border-bottom:1px solid var(--line);box-shadow:0 1px 6px rgba(10,42,102,.05)}
nav.tabs .wrap{max-width:1080px;margin:0 auto;display:flex;gap:4px;padding:8px 14px;overflow-x:auto}
nav.tabs button{white-space:nowrap;border:0;background:transparent;color:var(--muted);font-weight:700;font-size:14px;padding:9px 14px;border-radius:8px;cursor:pointer}
nav.tabs button.on{background:var(--blue-500);color:#fff}
nav.tabs button:focus-visible,.lang button:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
main{max-width:1080px;margin:0 auto;padding:18px 14px 40px}
.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:12.5px;color:var(--muted);margin:2px 4px 16px;align-items:center}
.sw{width:13px;height:13px;border-radius:4px;display:inline-block;vertical-align:-2px;margin-right:5px}
.gh{font-size:13px;font-weight:800;color:var(--blue-700);text-transform:uppercase;letter-spacing:1px;margin:22px 4px 4px;border-left:3px solid var(--gold);padding-left:8px}
.gsub{font-size:12px;color:var(--muted);margin:0 4px 10px 11px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin-bottom:8px}
.match{display:grid;grid-template-columns:58px 1fr 150px 120px;gap:12px;align-items:center}
.date{font-size:11px;color:var(--muted);font-family:var(--mono);line-height:1.35}
.date b{display:block;color:var(--ink);font-weight:700;font-family:var(--sans);font-size:12px}
.venue{font-size:11px;color:var(--muted);margin-top:7px;padding-top:6px;border-top:1px dashed var(--line)}
.fin{display:inline-block;margin-top:4px;font-size:9px;font-weight:800;letter-spacing:.5px;color:#fff;background:var(--green-fg);border-radius:4px;padding:1px 5px}
.finbox{font-size:12px;color:var(--muted);font-style:italic;align-self:center}
.card.done{border-left:3px solid var(--green-fg)}
.score.real{color:var(--green-fg)}
.teams{display:flex;align-items:center;gap:8px;min-width:0}
.tn{flex:1;min-width:0;font-size:14px}
.tn.r{text-align:right}
.tn .rk{color:var(--muted);font-size:11px;font-family:var(--mono)}
.fav{background:var(--green-bg);color:var(--green-fg);font-weight:700;border-radius:6px;padding:2px 7px}
.score{font-family:var(--mono);font-weight:800;font-size:16px;white-space:nowrap;color:var(--blue-900)}
.pbar{height:9px;border-radius:5px;overflow:hidden;display:flex;border:1px solid var(--line)}
.pbar i{display:block;height:100%}
.plab{font-size:10px;color:var(--muted);font-family:var(--mono);margin-top:3px;display:flex;justify-content:space-between}
.chip{font-size:11.5px;font-weight:700;padding:5px 8px;border-radius:6px;text-align:center}
.chip.w{background:var(--green-bg);color:var(--green-fg)}
.chip.d{background:var(--amber-bg);color:var(--amber-fg)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.adv-row{display:grid;grid-template-columns:1fr 64px 1fr;gap:10px;align-items:center;padding:6px 0;border-top:1px solid var(--line)}
.adv-row:first-of-type{border-top:0}
.adv-name{font-size:13.5px;font-weight:600}
.adv-rk{font-size:11px;color:var(--muted);font-family:var(--mono)}
.adv-win{font-family:var(--mono);font-size:12px;color:var(--blue-700);text-align:center}
.advbar{height:16px;border-radius:5px;background:#eef2f9;overflow:hidden;position:relative;border:1px solid var(--line)}
.advbar i{display:block;height:100%}
.advbar span{position:absolute;right:6px;top:0;line-height:16px;font-size:10.5px;font-weight:700;font-family:var(--mono)}
.bk{display:flex;justify-content:space-between;align-items:center;gap:8px}
.bk .mno{font-family:var(--mono);font-size:11px;color:#fff;background:var(--blue-500);border-radius:5px;padding:2px 6px;font-weight:700}
.bk .ven{font-size:11px;color:var(--muted)}
.bteam{display:flex;align-items:center;gap:8px;padding:5px 0;font-size:14px}
.code{font-family:var(--mono);font-size:10.5px;color:var(--blue-700);background:#e8eefb;border-radius:5px;padding:1px 6px;font-weight:700;min-width:34px;text-align:center}
.fav-row{display:grid;grid-template-columns:130px 1fr 48px;gap:10px;align-items:center;margin-bottom:7px}
.fav-row .fn{font-size:13.5px;font-weight:600}
.fav-bar{height:20px;border-radius:5px;background:#eef2f9;overflow:hidden;border:1px solid var(--line)}
.fav-bar i{display:block;height:100%;background:linear-gradient(90deg,var(--blue-500),var(--gold))}
.fav-row .fp{font-family:var(--mono);font-weight:800;font-size:13px;color:var(--blue-900);text-align:right}
.fav-sub{font-size:10.5px;color:var(--muted);font-family:var(--mono);margin:-2px 0 9px 2px}
.ko-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.ko-round{display:flex;flex-direction:column;gap:8px}
.ko-h{font-size:12px;font-weight:800;color:var(--blue-700);text-transform:uppercase;letter-spacing:.5px;text-align:center;padding-bottom:2px}
.ko-tie{background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.ko-team{font-size:13px;padding:7px 9px}
.ko-team+.ko-team{border-top:1px solid var(--line)}
.ko-team.kw{background:var(--green-bg);color:var(--green-fg);font-weight:700}
.ko-ven{font-size:10px;color:var(--muted);padding:5px 9px;border-top:1px dashed var(--line);background:#fafbfe}
.champ-banner{margin-top:14px;background:linear-gradient(120deg,var(--blue-900),var(--blue-700));color:#fff;border-radius:10px;padding:14px 16px;font-size:15px;text-align:center;border:2px solid var(--gold)}
.champ-banner b{color:var(--gold)}
footer{max-width:1080px;margin:0 auto;padding:0 14px 50px}
.note{background:#fff;border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:8px;padding:12px 14px;font-size:12.5px;color:var(--muted)}
.dl{display:inline-block;margin:14px 0 0;background:var(--blue-700);color:#fff;text-decoration:none;font-weight:700;font-size:13px;padding:10px 16px;border-radius:8px}
.dl:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
.hidden{display:none}
@media(max-width:640px){
 .match{grid-template-columns:1fr;gap:8px}
 .match .date{order:-1}
 .grid2{grid-template-columns:1fr}
 .ko-grid{grid-template-columns:1fr}
 .fav-row{grid-template-columns:96px 1fr 44px}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
</head>
<body>
<header class="topbar"><div class="wrap">
 <div class="brand"><div class="crest">26</div><div><h1 data-t="title"></h1><p data-t="sub"></p><p id="asof" style="margin:2px 0 0;font-size:11px;color:#9fb4e0"></p></div></div>
 <div class="spacer"></div>
 <div class="lang"><button id="bes" class="on" onclick="setLang('es')">ES</button><button id="ben" onclick="setLang('en')">EN</button></div>
</div></header>
<nav class="tabs"><div class="wrap">
 <button class="on" data-tab="matches" data-t="tab_m"></button>
 <button data-tab="advance" data-t="tab_a"></button>
 <button data-tab="bracket" data-t="tab_b"></button>
 <button data-tab="fav" data-t="tab_f"></button>
 <button data-tab="ko" data-t="tab_k"></button>
</div></nav>
<main>
 <div class="legend" data-sec="matches advance">
   <span><span class="sw" style="background:var(--green-bg);border:1px solid var(--line)"></span><span data-t="lg_fav"></span></span>
   <span><span class="sw" style="background:var(--amber-bg);border:1px solid var(--line)"></span><span data-t="lg_draw"></span></span>
 </div>
 <section id="matches"></section>
 <section id="advance" class="hidden"></section>
 <section id="bracket" class="hidden"></section>
 <section id="fav" class="hidden"></section>
 <section id="ko" class="hidden"></section>
</main>
<footer>
 <div class="note" data-t="note"></div>
 <a class="dl" href="Proyeccion-Mundial-2026-MAESTRO.xlsx" download data-t="dl"></a>
</footer>
<script>
let DATA=__DATA__;
const T={
 es:{title:"Proyección Mundial 2026",sub:"Resultados reales + xG al 16 jun · modelo + cuotas de mercado · horarios CDMX",
   tab_m:"Partidos",tab_a:"Avance",tab_b:"Eliminatorias",tab_f:"Favoritos",
   lg_fav:"Favorito por modelo",lg_draw:"Partido parejo / empate",
   group:"Grupo",home:"L",draw:"E",away:"V",wins:n=>"Gana "+n,drawtxt:"Empate",
   winG:"Gana grupo",adv:"Avanza",r32:"Dieciseisavos (Round of 32)",
   favttl:"Probabilidad de ser campeón",favNote:"Mezcla 70% mercado + 30% modelo (con xG)",fModel:"modelo",fMkt:"mercado",   tab_k:"Cuadro",roctavos:"Octavos de final",rcuartos:"Cuartos de final",rsemis:"Semifinales",rfinal:"Final",rthird:"Tercer lugar",champLabel:"Campeón proyectado",koNote:"Ruta más probable partido a partido: en cada llave avanza el favorito del modelo. Es un escenario único.",
   note:"Estimación probabilística generada con un modelo Elo + Poisson sobre el ranking FIFA del 11 de junio de 2026 y 20.000 torneos simulados; con ventaja de local solo para los anfitriones. No es un pronóstico fiable: ignora lesiones, forma y bajas. Los cruces desde octavos usan el orden estándar del cuadro. Para que el botón de descarga funcione, sube el archivo Excel junto a esta página.",
   dl:"Descargar Excel completo",venueLabel:"Estadio",won:n=>"Ganó "+n,fin:"FINAL",finalLabel:"Resultado final",projShort:"proy.",third:g=>"3.º "+g},
 en:{title:"2026 World Cup Projection",sub:"Real results + xG to Jun 16 · model + market odds · times in Mexico City",
   tab_m:"Matches",tab_a:"Advancement",tab_b:"Knockouts",tab_f:"Favourites",
   lg_fav:"Model favourite",lg_draw:"Tight match / draw",
   group:"Group",home:"H",draw:"D",away:"A",wins:n=>n+" win",drawtxt:"Draw",
   winG:"Win group",adv:"Advance",r32:"Round of 32",
   favttl:"Probability of winning the title",favNote:"70% market + 30% model (with xG) blend",fModel:"model",fMkt:"market",
   tab_k:"Bracket",roctavos:"Round of 16",rcuartos:"Quarter-finals",rsemis:"Semi-finals",rfinal:"Final",rthird:"Third place",champLabel:"Projected champion",koNote:"Most likely path tie by tie: the model favourite advances each round. A single scenario.",
   note:"Probabilistic estimate from an Elo + Poisson model on the June 11, 2026 FIFA ranking and 20,000 simulated tournaments, with home advantage only for the host nations. Not a reliable forecast: it ignores injuries, form and absences. Knockout pairings from the Round of 16 use the standard bracket order. For the download button to work, upload the Excel file next to this page.",
   dl:"Download full Excel",venueLabel:"Venue",won:n=>n+" won",fin:"FINAL",finalLabel:"Final score",projShort:"proj.",third:g=>"3rd "+g}
};
let lang="es",tab="matches";
const $=s=>document.querySelector(s),$$=s=>document.querySelectorAll(s);
function nm(o){return lang==="es"?o.es:o.en}
function pct(x){return Math.round(x*100)+"%"}
function advColor(p){return p>=.55?["var(--green-bg)","var(--green-fg)"]:p>=.25?["var(--amber-bg)","var(--amber-fg)"]:["var(--red-bg)","var(--red-fg)"]}

function renderMatches(){
 let h="";
 for(const g of Object.keys(DATA.groups)){
  const G=DATA.groups[g];
  h+=`<div class="gh">${T[lang].group} ${g}</div>`;
  h+=`<div class="gsub">${G.teams.map(t=>nm(t)).join(" · ")}</div>`;
  for(const m of G.matches){
   const hn=lang==="es"?m.h:m.he, an=lang==="es"?m.a:m.ae;
   const done=m.done===1;
   const hf=m.res==="home"?'fav':'', af=m.res==="away"?'fav':'';
   const chip=m.res==="draw"?`<div class="chip d">${T[lang].drawtxt}</div>`:`<div class="chip w">${(done?T[lang].won:T[lang].wins)(m.res==="home"?hn:an)}</div>`;
   const mid=done?`<div class="finbox">${T[lang].finalLabel}</div>`:`<div>
       <div class="pbar"><i style="width:${m.pw*100}%;background:var(--blue-500)"></i><i style="width:${m.pd*100}%;background:var(--gold)"></i><i style="width:${m.pl*100}%;background:#9db4dd"></i></div>
       <div class="plab"><span>${T[lang].home} ${pct(m.pw)}</span><span>${T[lang].draw} ${pct(m.pd)}</span><span>${T[lang].away} ${pct(m.pl)}</span></div>
     </div>`;
   const extra=(done?` · ${T[lang].projShort} ${m.proj}`:"")+(m.xg?` · xG ${m.xg[0].toFixed(2)}–${m.xg[1].toFixed(2)}`:"");
   h+=`<div class="card${done?' done':''}"><div class="match">
     <div class="date"><b>${m.date}</b>${m.time}${done?`<span class="fin">${T[lang].fin}</span>`:''}</div>
     <div class="teams">
       <div class="tn r"><span class="${hf}">${hn}</span> <span class="rk">${m.hr}</span></div>
       <div class="score${done?' real':''}">${m.sc}</div>
       <div class="tn"><span class="rk">${m.ar}</span> <span class="${af}">${an}</span></div>
     </div>
     ${mid}
     ${chip}
   </div><div class="venue">${T[lang].venueLabel}: ${m.venue}${extra}</div></div>`;
  }
 }
 $("#matches").innerHTML=h;
}
function renderAdvance(){
 let h='<div class="grid2">';
 for(const g of Object.keys(DATA.groups)){
  const G=DATA.groups[g];
  h+=`<div class="card"><div class="gh" style="margin-top:0">${T[lang].group} ${g}</div>`;
  for(const t of G.teams){
   const [bg,fg]=advColor(t.padv);
   h+=`<div class="adv-row">
     <div><div class="adv-name">${nm(t)}</div><div class="adv-rk">FIFA ${t.rank} · ${T[lang].winG} ${pct(t.pwin)}</div></div>
     <div class="adv-win">${T[lang].adv}</div>
     <div class="advbar"><i style="width:${t.padv*100}%;background:${bg}"></i><span style="color:${fg}">${pct(t.padv)}</span></div>
   </div>`;
  }
  h+="</div>";
 }
 h+="</div>";
 $("#advance").innerHTML=h;
}
function fmtCode(c){return c.startsWith("3:")?T[lang].third(c.slice(2)):c}
function renderBracket(){
 let h=`<div class="gh">${T[lang].r32}</div><div class="grid2">`;
 for(const b of DATA.bracket){
  h+=`<div class="card">
    <div class="bk"><span class="mno">${b.mid}</span><span class="ven">${b.date} · ${b.venue}</span></div>
    <div class="bteam"><span class="code">${fmtCode(b.e1.code)}</span><span>${nm(b.e1)}</span></div>
    <div class="bteam"><span class="code">${fmtCode(b.e2.code)}</span><span>${nm(b.e2)}</span></div>
  </div>`;
 }
 h+="</div>";
 $("#bracket").innerHTML=h;
}
function renderFav(){
 const mx=DATA.champions[0].p;
 let h=`<div class="gh">${T[lang].favttl}</div><div class="gsub">${T[lang].favNote}</div><div class="card">`;
 for(const c of DATA.champions){
  h+=`<div class="fav-row"><div class="fn">${nm(c)}</div><div class="fav-bar"><i style="width:${(c.p/mx*100)}%"></i></div><div class="fp">${pct(c.p)}</div></div><div class="fav-sub">${T[lang].fModel} ${pct(c.pmodel)} · ${T[lang].fMkt} ${pct(c.pmkt)}</div>`;
 }
 h+="</div>";
 $("#fav").innerHTML=h;
}
function renderKO(){
 const K=DATA.knockout; if(!K){return;}
 function tie(m){
  const aw=m.w==="a", bw=m.w==="b";
  const v=m.venue?`<div class="ko-ven">${m.date} · ${m.venue}</div>`:"";
  return `<div class="ko-tie"><div class="ko-team${aw?' kw':''}">${nm(m.a)}</div><div class="ko-team${bw?' kw':''}">${nm(m.b)}</div>${v}</div>`;
 }
 function round(title,arr){return `<div class="ko-round"><div class="ko-h">${title}</div>${arr.map(tie).join("")}</div>`;}
 let h=`<div class="gh">${T[lang].roctavos} → ${T[lang].rfinal}</div><div class="gsub">${T[lang].koNote}</div>`;
 h+=`<div class="ko-grid">`;
 h+=round(T[lang].roctavos,K.octavos);
 h+=round(T[lang].rcuartos,K.cuartos);
 h+=round(T[lang].rsemis,K.semis);
 h+=round(T[lang].rfinal,[K.final]);
 h+=`</div>`;
 h+=`<div class="champ-banner">🏆 ${T[lang].champLabel}: <b>${nm(K.champion)}</b> · ${pct(K.champion_p)}</div>`;
 h+=`<div class="ko-round" style="margin-top:10px"><div class="ko-h">${T[lang].rthird}</div>${tie(K.third)}</div>`;
 $("#ko").innerHTML=h;
}
function renderAll(){renderMatches();renderAdvance();renderBracket();renderFav();renderKO();applyT();}
function applyT(){
 document.documentElement.lang=lang;
 $$("[data-t]").forEach(e=>{const k=e.getAttribute("data-t");const v=T[lang][k];if(typeof v==="string")e.textContent=v;});
 $("#bes").classList.toggle("on",lang==="es");$("#ben").classList.toggle("on",lang==="en");
 $$(".legend").forEach(l=>l.classList.toggle("hidden",!l.getAttribute("data-sec").includes(tab)));
 if(typeof updateStamp==="function")updateStamp();
}
function setLang(l){lang=l;renderAll();}
function setTab(t){tab=t;["matches","advance","bracket","fav","ko"].forEach(s=>$("#"+s).classList.toggle("hidden",s!==t));$$("nav.tabs button").forEach(b=>b.classList.toggle("on",b.dataset.tab===t));applyT();}
$$("nav.tabs button").forEach(b=>b.addEventListener("click",()=>setTab(b.dataset.tab)));
function updateStamp(){const el=$("#asof");if(el)el.textContent=DATA.generated?((lang==="es"?"Datos al ":"Data as of ")+DATA.generated+" · "+(lang==="es"?"se actualiza solo":"auto-updating")):"";}
async function loadData(){
 try{
  const r=await fetch("wcdata.json?t="+Date.now(),{cache:"no-store"});
  if(r.ok){const j=await r.json(); if(j&&j.groups){DATA=j; renderAll();}}
 }catch(e){/* archivo local o sin red: se conservan los datos incrustados */}
}
renderAll();setTab("matches");updateStamp();
loadData();
setInterval(loadData, 600000);
document.addEventListener("visibilitychange",()=>{if(!document.hidden)loadData();});
</script>
</body>
</html>
"""
html=html.replace("__DATA__", json.dumps(D,ensure_ascii=False))
open("index.html","w",encoding="utf-8").write(html)
print("written", len(html),"bytes")
