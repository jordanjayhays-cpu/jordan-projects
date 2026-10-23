#!/usr/bin/env python3
"""Builds two Data Fluency decks from one engine:
   whats-in-your-cup.html  (audience: McDonald's customers)
   healthy-makes-money.html (audience: Glovo partnerships team)
Run from this folder. Reads menu-data.json."""
import json, pathlib
HERE = pathlib.Path(__file__).parent
DATA = (HERE / 'menu-data.json').read_text()

TEMPLATE = r'''<title>/*TITLE*/</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;900&family=Archivo:ital,wght@0,400;0,500;0,600;1,400&family=Azeret+Mono:wght@400;500&display=swap">
<style>
/* Layout: dark stage, 260 dots that travel between layouts; text column left, stage right; stacks on phones. One idea per slide. */
:root{
  --ink:#0B0A09; --ink-2:#15130F; --paper:#F3EADB; --paper-2:#B8AE9C; --muted:#6F675B; --rule:#2A2622;
  --sand:#4A443B; --sugar:#E9A23B; --over:#FF4A3C; --salt:#4FA3FF; --zero:#3DDC97; --pink:#F08A9B; --gold:#E9A23B;
  --accent:/*ACCENT*/;
  --display:"Big Shoulders Display","Archivo Narrow","Arial Narrow",Impact,sans-serif;
  --body:"Archivo","Helvetica Neue",Arial,sans-serif;
  --mono:"Azeret Mono","SFMono-Regular",Menlo,Consolas,monospace;
  color-scheme:dark;
}
html,body{height:100%}
body{margin:0;background:var(--ink);color:var(--paper);font-family:var(--body);font-size:16px;line-height:1.45;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0;overflow:hidden}
.deck{height:100%;display:grid;grid-template-rows:auto 1fr auto;max-width:1680px;margin:0 auto}
header{display:flex;align-items:center;gap:18px;padding-block:14px 10px;border-bottom:1px solid var(--rule);font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--paper-2)}
header .brand{color:var(--paper);font-weight:500}
header .bar{flex:1;height:2px;background:var(--rule);position:relative;border-radius:2px;overflow:hidden}
header .bar i{position:absolute;inset:0 auto 0 0;background:var(--accent);width:0;transition:width .5s ease}
header .count{font-variant-numeric:tabular-nums}
main{display:grid;grid-template-columns:minmax(300px,420px) 1fr;gap:28px;min-height:0;padding-block:18px}
aside{min-width:0;display:flex;flex-direction:column;gap:16px;justify-content:center}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent)}
h1{font-family:var(--display);font-weight:900;font-size:clamp(40px,5vw,72px);line-height:.94;margin:0;letter-spacing:.005em;text-wrap:balance;text-transform:uppercase}
h1 em{font-style:normal;color:var(--accent)}
h1 em.red{color:var(--over)} h1 em.blue{color:var(--salt)} h1 em.green{color:var(--zero)} h1 em.amber{color:var(--sugar)}
.lede{font-size:18px;color:var(--paper-2);max-width:40ch;margin:0}
.lede b{color:var(--paper);font-weight:600}
.stat{display:flex;align-items:baseline;justify-content:space-between;gap:16px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding-block:10px}
.stat .l{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--paper-2)}
.stat .v{font-family:var(--display);font-weight:900;font-size:clamp(44px,4.6vw,64px);line-height:1;color:var(--paper);font-variant-numeric:tabular-nums}
.stat .v.sugar{color:var(--sugar)} .stat .v.red{color:var(--over)} .stat .v.blue{color:var(--salt)} .stat .v.green{color:var(--zero)}
.key{display:flex;flex-direction:column;gap:6px;font-family:var(--mono);font-size:11px;letter-spacing:.06em;color:var(--paper-2)}
.key span{display:flex;align-items:center;gap:10px}
.key i{width:10px;height:10px;border-radius:50%;display:inline-block;flex:none}
.howto{font-family:var(--mono);font-size:11px;letter-spacing:.08em;color:var(--accent);border-left:2px solid var(--accent);padding-left:10px;text-transform:uppercase}
.stage{position:relative;min-width:0;min-height:0;border:1px solid var(--rule);border-radius:4px;background:var(--ink-2);overflow:hidden}
.stage svg{position:absolute;inset:0;width:100%;height:100%}
.stage .overlay{position:absolute;inset:0;padding:clamp(16px,3vw,44px);display:flex;flex-direction:column;justify-content:center;gap:20px;pointer-events:none;opacity:0;transition:opacity .5s}
.stage .overlay.on{opacity:1;pointer-events:auto}
.stage .overlay > *{min-width:0}
svg text{font-family:var(--mono);font-size:12.5px;fill:var(--paper-2);letter-spacing:.04em}
svg text.big{font-family:var(--display);font-weight:900;font-size:34px;fill:var(--paper);letter-spacing:.01em}
svg text.lab{fill:var(--paper)}
svg .axis line,svg .axis path{stroke:var(--rule)}
svg .rule{stroke:var(--paper-2);stroke-dasharray:4 5;stroke-width:1}
svg .rule.hard{stroke:var(--over);stroke-dasharray:none;stroke-width:1.5}
svg .call{stroke:var(--paper-2);fill:none;stroke-width:1}
svg .region{fill:rgba(255,255,255,.035);stroke:var(--rule);stroke-width:1;rx:14}
footer{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-block:10px 14px;border-top:1px solid var(--rule);font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);flex-wrap:wrap}
footer .arc{display:flex;gap:14px}
footer .arc span{position:relative;padding-left:12px}
footer .arc span::before{content:"";position:absolute;left:0;top:50%;width:6px;height:6px;border-radius:50%;background:var(--rule);transform:translateY(-50%)}
footer .arc span.on{color:var(--paper)} footer .arc span.on::before{background:var(--accent)}
footer .src{min-width:0;max-width:60%;line-height:1.5}
.hint{color:var(--muted)}
button.notes{font:inherit;font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;background:none;border:1px solid var(--rule);color:var(--paper-2);padding:4px 10px;border-radius:3px;cursor:pointer}
button.notes:focus-visible,.stage:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
#notes[hidden]{display:none}
#notes{position:absolute;left:max(16px,env(safe-area-inset-left,0px));right:max(16px,env(safe-area-inset-right,0px));bottom:52px;margin:0 auto;max-width:900px;background:var(--ink);border:1px solid var(--accent);border-radius:4px;padding:16px 20px;z-index:5;display:grid;gap:8px;font-size:15px;box-shadow:0 20px 60px rgba(0,0,0,.6)}
#notes .k{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
#notes .course{color:var(--paper-2);font-size:13.5px}
/* overlays */
.cups{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:24px;justify-items:center}
.cup{width:min(34vmin,300px);aspect-ratio:1;border-radius:50%;background:#2A1E16;border:3px solid #3A2C21;position:relative;display:grid;place-items:center}
.cup .g{font-family:var(--display);font-weight:900;font-size:clamp(40px,6vmin,76px);color:var(--zero)}
.cup .cube{position:absolute;width:11%;height:11%;background:var(--paper);border-radius:12%;box-shadow:inset -3px -3px 0 rgba(0,0,0,.15)}
.cups .eq{font-family:var(--display);font-weight:900;font-size:64px;color:var(--accent)}
.cups .cap{display:grid;justify-items:center;gap:4px;margin-top:10px}
.cups .cap b{font-family:var(--display);font-weight:700;font-size:28px;letter-spacing:.02em;text-transform:uppercase}
.cups .cap span{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--paper-2)}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.cards.four{grid-template-columns:repeat(4,minmax(0,1fr))}
.card{border:1px solid var(--rule);border-radius:4px;padding:16px;display:grid;gap:10px;background:rgba(0,0,0,.25);align-content:start}
.card .n{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
.card h3{font-family:var(--display);font-weight:900;font-size:30px;line-height:1;margin:0;text-transform:uppercase}
.card .big{font-family:var(--display);font-weight:900;font-size:48px;line-height:1;color:var(--zero)}
.card p{margin:0;color:var(--paper-2);font-size:14px}
.card .ui{border:1px solid var(--rule);border-radius:10px;padding:10px 12px;font-size:13px;display:grid;gap:6px;background:var(--ink)}
.card .ui .row{display:flex;justify-content:space-between;gap:8px;padding:6px 8px;border-radius:6px;border:1px solid transparent}
.card .ui .row.new{border-color:var(--zero);color:var(--zero)}
.card .ui small{color:var(--paper-2);font-family:var(--mono);font-size:9.5px;letter-spacing:.08em;text-transform:uppercase}
.card table{width:100%;border-collapse:collapse;font-size:13px}
.card td{padding:4px 0;border-top:1px solid var(--rule)}
.card td:last-child{text-align:right;font-family:var(--mono);font-size:12px;white-space:nowrap}
.card td.g{color:var(--zero)} .card td.a{color:var(--sugar)}
.ask{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.ask h4{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin:0 0 10px;border-bottom:1px solid var(--rule);padding-bottom:8px}
.ask ul{margin:0;padding:0;list-style:none;display:grid;gap:8px;font-size:14px;color:var(--paper-2)}
.ask li b{color:var(--paper);font-weight:600}
.money{width:100%;height:100%;min-height:0}
.behind{display:grid;gap:22px}
.behind .arcline{height:120px}
.behind .row4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.behind .row4 div{border-top:1px solid var(--rule);padding-top:8px}
.behind .row4 .k{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
.behind .row4 p{margin:4px 0 0;font-family:var(--display);font-weight:700;font-size:24px;line-height:1.05;text-transform:uppercase}
.behind .books{font-family:var(--mono);font-size:11px;letter-spacing:.04em;color:var(--paper-2);line-height:1.8}
.behind .books b{color:var(--paper);font-weight:500}
@media (max-width:900px){
  main{grid-template-columns:1fr;grid-template-rows:auto 1fr;gap:14px}
  aside{justify-content:flex-start;gap:10px}
  h1{font-size:34px} .lede{font-size:14px} .stat .v{font-size:38px}
  .key,.howto{display:none}
  .cards,.cards.four,.ask,.behind .row4{grid-template-columns:1fr}
  .cups{grid-template-columns:1fr} .cups .eq{display:none}
  footer .src{display:none}
}
@media (prefers-reduced-motion:reduce){ *{transition:none!important} }
</style>

<div class="deck">
  <header>
    <span class="brand">/*TITLE*/</span>
    <span>Group 3 · IE IMBA · Data Fluency</span>
    <span class="bar"><i id="bar"></i></span>
    <span class="count" id="count">01</span>
  </header>
  <main>
    <aside id="text" aria-live="polite"></aside>
    <div class="stage" id="stage" tabindex="0" aria-label="Data stage">
      <svg id="svg" viewBox="0 0 1100 720" preserveAspectRatio="xMidYMid meet" role="img" aria-label="260 menu items as dots"></svg>
      <div class="overlay" id="overlay"></div>
    </div>
  </main>
  <footer>
    <div class="arc" id="arc"></div>
    <div class="src" id="src"></div>
    <div><button class="notes" id="nbtn" type="button">Notes · N</button> <span class="hint">· arrows to move</span></div>
  </footer>
  <div id="notes" hidden><div class="k" id="nk">Speaker</div><div id="nt"></div><div class="course" id="nc"></div></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script>
const DATA = /*DATA*/;
const DEFAULT_SRC = "Data: Nutrition Facts for McDonald's Menu (Kaggle, US, 260 items) · US menu used as a stand-in for Madrid";
const CUP = new Set(['Beverages','Coffee & Tea','Smoothies & Shakes','Desserts']);
const W=1100,H=720;
const C={sand:'#4A443B',sugar:'#E9A23B',over:'#FF4A3C',salt:'#4FA3FF',zero:'#3DDC97',pink:'#F08A9B',gold:'#E9A23B',paper:'#F3EADB',muted:'#2E2A25',grey:'#8B8378',dim:'#2B2723'};
const rScale=d3.scaleSqrt().domain([0,1900]).range([2.4,11]);
const items=DATA.map((d,i)=>({...d,i,cup:CUP.has(d.cat),r:rScale(d.cal)}));
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const fmt=d3.format(',');

/* ---------- numbers, all computed from the data ---------- */
const N={};
N.total=items.length;
N.over50=items.filter(d=>d.sugar>50).length;
N.zero=items.filter(d=>d.sugar===0).length;
N.cup=items.filter(d=>d.cup).length; N.plate=N.total-N.cup;
N.plateMax=d3.max(items.filter(d=>!d.cup),d=>d.sugar);
N.maxItem=items.reduce((a,b)=>b.sugar>a.sugar?b:a);
const catAvg=c=>d3.mean(items.filter(d=>d.cat===c),d=>d.sugar);
N.coffee=items.filter(d=>d.cat==='Coffee & Tea').length; N.coffeeAvg=catAvg('Coffee & Tea'); N.sodaAvg=catAvg('Beverages'); N.shakeAvg=catAvg('Smoothies & Shakes'); N.shakes=items.filter(d=>d.cat==='Smoothies & Shakes').length;
N.coffeeMax=items.filter(d=>d.cat==='Coffee & Tea').reduce((a,b)=>b.sugar>a.sugar?b:a);
items.forEach(d=>{const m=d.item.match(/\((Small|Medium|Large)\)$/);d.size=m?m[1]:null});
N.sized=items.filter(d=>d.size).length;
N.sizeAvg={}; ['Small','Medium','Large'].forEach(s=>N.sizeAvg[s]=d3.mean(items.filter(d=>d.size===s),d=>d.sugar));
N.salt48=items.filter(d=>!d.cup&&d.sodium>=1150).length;
N.nuggets=items.find(d=>/40 piece/.test(d.item)); N.bigb=items.filter(d=>/Big Breakfast with Hotcakes/.test(d.item)).reduce((a,b)=>b.sodium>a.sodium?b:a);
const byName=new Map(items.map(d=>[d.item,d]));
const pairs=[];
items.forEach(d=>{ if(/\(Large\)$/.test(d.item)){const s=byName.get(d.item.replace('(Large)','(Small)')); if(s)pairs.push({a:d,b:s,t:'smaller'})}});
items.forEach(d=>{ if(/Crispy/.test(d.item)){const g=byName.get(d.item.replace('Crispy','Grilled')); if(g)pairs.push({a:d,b:g,t:'grilled'})}});
items.forEach(d=>{ if(/^Diet /.test(d.item)){const r=byName.get(d.item.replace(/^Diet Coke/,'Coca-Cola Classic').replace(/^Diet /,'')); if(r)pairs.push({a:r,b:d,t:'diet'})}});
N.pairs=pairs.length; N.pSmaller=pairs.filter(p=>p.t==='smaller').length; N.pGrilled=pairs.filter(p=>p.t==='grilled').length; N.pDiet=pairs.filter(p=>p.t==='diet').length;
N.grilledSave=d3.extent(pairs.filter(p=>p.t==='grilled'),p=>p.a.cal-p.b.cal);
N.smallSave=d3.median(pairs.filter(p=>p.t==='smaller'),p=>p.a.sugar-p.b.sugar);

/* ---------- layouts ---------- */
const sx=d3.scaleLinear().domain([0,130]).range([90,1050]);
function base(){return items.map(d=>({x:W/2,y:H/2,r:d.r,fill:C.sand,op:1}))}
function swarm(nodesIn,xs,ys,sxv=1,syv=0.1){
  const nodes=nodesIn.map(d=>({i:d.i,x:xs(d),y:ys(d),r:d.r}));
  const sim=d3.forceSimulation(nodes).force('x',d3.forceX(n=>xs(items[n.i])).strength(sxv)).force('y',d3.forceY(n=>ys(items[n.i])).strength(syv)).force('c',d3.forceCollide(n=>n.r+1.4).iterations(3)).stop();
  for(let k=0;k<200;k++)sim.tick(); return nodes;
}
const cache={}; function L(name){ if(cache[name])return cache[name]; const p=LAYOUTS[name](); cache[name]=p; return p; }
const sugarFill=d=>d.sugar>50?C.over:C.sand;
const swapCol={smaller:C.grey,grilled:C.sugar,diet:C.zero};
const ysw=d3.scaleLinear().domain([0,900]).range([650,90]);
const LAYOUTS={
  circle(){ const p=base(); const nodes=items.map((d,i)=>{const t=i*2.39996,r=20*Math.sqrt(i);return {i,x:W/2+r*Math.cos(t),y:H/2+r*Math.sin(t),r:d.r}});
    const sim=d3.forceSimulation(nodes).force('c',d3.forceCollide(n=>n.r+1.6)).force('x',d3.forceX(W/2).strength(.02)).force('y',d3.forceY(H/2).strength(.02)).stop(); for(let k=0;k<120;k++)sim.tick();
    nodes.forEach(n=>{p[n.i].x=n.x;p[n.i].y=n.y}); return p; },
  swarm(){ const p=base(); swarm(items,d=>sx(d.sugar),()=>370).forEach(n=>{p[n.i].x=n.x;p[n.i].y=n.y;p[n.i].fill=sugarFill(items[n.i])}); return p; },
  cupplate(){ const p=base(); swarm(items,d=>sx(d.sugar),d=>d.cup?230:530).forEach(n=>{p[n.i].x=n.x;p[n.i].y=n.y;p[n.i].fill=sugarFill(items[n.i])}); return p; },
  coffee(){ const p=L('cupplate').map(o=>({...o})); items.forEach(d=>{const q=p[d.i]; if(d.cat==='Coffee & Tea'){q.fill=C.sugar;q.op=1}else{q.fill=C.sand;q.op=d.cup?.5:.22}}); return p; },
  sizes(){ const p=L('coffee').map(o=>({...o,fill:C.sand,op:0,r:0})); const sy=d3.scaleLinear().domain([0,130]).range([650,90]); const col={Small:240,Medium:550,Large:860};
    swarm(items.filter(d=>d.size),d=>col[d.size],d=>sy(d.sugar),.12,1).forEach(n=>{const d=items[n.i];p[n.i]={x:n.x,y:n.y,r:d.r,fill:d.sugar>50?C.over:C.sand,op:1}}); return p; },
  salt(){ const p=L('sizes').map(o=>({...o})); const xs=d3.scaleLinear().domain([0,1900]).range([90,1050]), ys=d3.scaleLinear().domain([0,3700]).range([650,80]);
    items.forEach(d=>{p[d.i]={x:xs(d.cal),y:ys(d.sodium),r:d.r,fill:d.cup?C.sand:(d.sodium>=1150?C.salt:C.grey),op:d.cup?.18:1}}); return p; },
  swaps(){ const p=L('salt').map(o=>({...o,op:0,r:0})); const seen=new Set();
    pairs.forEach(pr=>{ if(!seen.has(pr.a.i)){p[pr.a.i]={x:330,y:ysw(pr.a.cal),r:pr.a.r,fill:swapCol[pr.t],op:1};seen.add(pr.a.i)} if(!seen.has(pr.b.i)){p[pr.b.i]={x:770,y:ysw(pr.b.cal),r:pr.b.r,fill:swapCol[pr.t],op:1};seen.add(pr.b.i)} }); return p; },
  swapsDiet(){ const p=L('swaps').map(o=>({...o})); const dietIdx=new Set(pairs.filter(pr=>pr.t==='diet').flatMap(pr=>[pr.a.i,pr.b.i]));
    items.forEach(d=>{ if(p[d.i].op>0){ if(dietIdx.has(d.i)){p[d.i].fill=C.zero;p[d.i].op=1}else{p[d.i].fill=C.dim;p[d.i].op=.6} } }); return p; },
  hidden(){ return L('swaps').map(o=>({...o,op:0,r:0})); },
};
function ordersField(){ const n=1000, pts=[]; for(let i=0;i<n;i++){const t=i*2.39996,r=9.6*Math.sqrt(i);pts.push({x:W/2+60+r*Math.cos(t),y:H/2-10+r*Math.sin(t),k:i<8?'zero':i<58?'fruit':i<458?'sugary':'other'})}
  const rnd=d3.randomLcg(7); for(let i=pts.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[pts[i].k,pts[j].k]=[pts[j].k,pts[i].k]} return pts; }

/* ---------- annotations ---------- */
const AN={
  circle(g){},
  swarm(g){ axisX(g,660,'More sugar this way'); vline(g,sx(50),120,640,'A whole day of sugar · 50 g · about 12 cubes',true); },
  cupplate(g){ g.append('rect').attr('class','region').attr('x',70).attr('y',120).attr('width',960).attr('height',230); g.append('rect').attr('class','region').attr('x',70).attr('y',400).attr('width',960).attr('height',260);
    axisX(g,680,'More sugar this way'); vline(g,sx(50),120,660,'A whole day of sugar · 50 g',true);
    label(g,90,145,'IN A CUP',true); label(g,90,165,N.cup+' things you drink or eat with a spoon');
    label(g,90,425,'ON A PLATE',true); label(g,90,445,N.plate+' things you eat with your hands');
    const mx=L('cupplate')[N.maxItem.i]; callout(g,mx.x,mx.y,mx.x-140,mx.y-60,N.maxItem.item.replace(' Candies',''),N.maxItem.sugar+' g · two and a half days of sugar');
    const pm=items.filter(d=>!d.cup).reduce((a,b)=>b.sugar>a.sugar?b:a); const pp=L('cupplate')[pm.i]; callout(g,pp.x,pp.y,pp.x+80,pp.y+70,'Sweetest thing on a plate',pm.sugar+' g · '+pm.item); },
  coffee(g){ axisX(g,680,'More sugar this way'); vline(g,sx(50),120,660,'A whole day of sugar · 50 g',true);
    label(g,90,145,'COFFEE AND TEA · '+N.coffee+' DRINKS',true,C.sugar); label(g,90,165,'they average '+Math.round(N.coffeeAvg)+' g · sodas average '+Math.round(N.sodaAvg)+' g');
    const cm=L('coffee')[N.coffeeMax.i]; callout(g,cm.x,cm.y,cm.x-120,cm.y-70,N.coffeeMax.item,N.coffeeMax.sugar+' g · about '+Math.round(N.coffeeMax.sugar/4)+' cubes'); },
  sizes(g){ const sy=d3.scaleLinear().domain([0,130]).range([650,90]); const col={Small:240,Medium:550,Large:860};
    hline(g,sy(50),90,1050,'A whole day of sugar · 50 g',true);
    ['Small','Medium','Large'].forEach(s=>{ const a=N.sizeAvg[s]; g.append('line').attr('x1',col[s]-110).attr('x2',col[s]+110).attr('y1',sy(a)).attr('y2',sy(a)).attr('stroke',C.sugar).attr('stroke-width',2);
      g.append('text').attr('x',col[s]).attr('y',690).attr('text-anchor','middle').attr('class','big').text(s.toUpperCase());
      g.append('text').attr('x',col[s]+118).attr('y',sy(a)+4).attr('fill',C.sugar).text('average '+Math.round(a)+' g'); }); },
  salt(g){ const xs=d3.scaleLinear().domain([0,1900]).range([90,1050]), ys=d3.scaleLinear().domain([0,3700]).range([650,80]);
    g.append('g').attr('class','axis').attr('transform','translate(0,650)').call(d3.axisBottom(xs).ticks(5).tickSize(-570).tickFormat(d=>d)).call(s=>s.select('.domain').remove()).selectAll('line').attr('stroke','#1E1B17');
    g.append('text').attr('x',1050).attr('y',690).attr('text-anchor','end').text('MORE CALORIES THIS WAY →');
    g.append('text').attr('x',90).attr('y',70).text('MORE SALT THIS WAY ↑');
    hline(g,ys(1150),90,1050,'Half a day of salt · 1,150 mg',false,C.salt);
    const food=items.filter(d=>!d.cup); const mx=d3.mean(food,d=>d.cal),my=d3.mean(food,d=>d.sodium); const b=d3.sum(food,d=>(d.cal-mx)*(d.sodium-my))/d3.sum(food,d=>(d.cal-mx)**2); const a=my-b*mx; const xmax=d3.max(food,d=>d.cal);
    g.append('line').attr('x1',xs(0)).attr('y1',ys(a)).attr('x2',xs(xmax)).attr('y2',ys(a+b*xmax)).attr('stroke',C.paper).attr('stroke-opacity',.5).attr('stroke-dasharray','2 4');
    g.append('text').attr('x',90).attr('y',215).attr('fill',C.paper).text('ALMOST A STRAIGHT LINE: MORE CALORIES, MORE SALT');
    callout(g,xs(N.nuggets.cal),ys(N.nuggets.sodium),xs(N.nuggets.cal)-330,ys(N.nuggets.sodium)+10,N.nuggets.item,fmt(N.nuggets.sodium)+' mg · a day and a half of salt');
    callout(g,xs(N.bigb.cal),ys(N.bigb.sodium),xs(N.bigb.cal)-70,ys(N.bigb.sodium)-100,'Big Breakfast with Hotcakes',fmt(N.bigb.sodium)+' mg · one day of salt'); },
  swaps(g){ pairs.forEach(pr=>g.append('line').attr('x1',330).attr('y1',ysw(pr.a.cal)).attr('x2',770).attr('y2',ysw(pr.b.cal)).attr('stroke',swapCol[pr.t]).attr('stroke-opacity',pr.t==='smaller'?.35:.8).attr('stroke-width',pr.t==='smaller'?1:1.6));
    swapChrome(g); label(g,850,120,N.pSmaller+' × Small instead of Large',true,C.grey); label(g,850,140,Math.round(N.smallSave)+' g less sugar · cheaper'); label(g,850,180,N.pGrilled+' × grilled, not crispy',true,C.sugar); label(g,850,200,N.grilledSave[0]+' to '+N.grilledSave[1]+' fewer calories'); label(g,850,240,N.pDiet+' × Zero, not regular',true,C.zero); label(g,850,260,'same cup, same price, 0 g'); },
  swapsDiet(g){ pairs.forEach(pr=>g.append('line').attr('x1',330).attr('y1',ysw(pr.a.cal)).attr('x2',770).attr('y2',ysw(pr.b.cal)).attr('stroke',pr.t==='diet'?C.zero:C.dim).attr('stroke-opacity',pr.t==='diet'?.9:.6).attr('stroke-width',pr.t==='diet'?2:1));
    swapChrome(g); label(g,850,120,N.pDiet+' × Zero, not regular',true,C.zero); label(g,850,140,'same cup, same price, 0 g'); label(g,850,180,(N.pairs-N.pDiet)+' other swaps',true,C.grey); label(g,850,200,'smaller food, or grilled'); },
  hidden(g){},
};
function swapChrome(g){ g.append('text').attr('x',330).attr('y',60).attr('text-anchor','middle').attr('class','big').text('WHAT YOU ORDER NOW'); g.append('text').attr('x',770).attr('y',60).attr('text-anchor','middle').attr('class','big').text('THE SWAP');
  g.append('g').attr('class','axis').attr('transform','translate(90,0)').call(d3.axisLeft(ysw).ticks(4).tickFormat(d=>d+' cal')).call(s=>s.select('.domain').remove()); }
function axisX(g,y,t){ g.append('g').attr('class','axis').attr('transform',`translate(0,${y})`).call(d3.axisBottom(sx).ticks(6).tickFormat(d=>d+' g')).call(s=>s.select('.domain').remove()); g.append('text').attr('x',1050).attr('y',y+40).attr('text-anchor','end').text(t.toUpperCase()+' →'); }
function vline(g,x,y1,y2,t,hard){ g.append('line').attr('class','rule'+(hard?' hard':'')).attr('x1',x).attr('x2',x).attr('y1',y1).attr('y2',y2); g.append('text').attr('x',x+8).attr('y',y1-8).attr('fill',hard?C.over:C.paper).text(t.toUpperCase()); }
function hline(g,y,x1,x2,t,hard,color){ g.append('line').attr('class','rule'+(hard?' hard':'')).attr('x1',x1).attr('x2',x2).attr('y1',y).attr('y2',y).attr('stroke',color||null); g.append('text').attr('x',x2).attr('y',y-8).attr('text-anchor','end').attr('fill',color||(hard?C.over:C.paper)).text(t.toUpperCase()); }
function label(g,x,y,t,strong,color){ g.append('text').attr('x',x).attr('y',y).attr('class',strong?'lab':'').attr('fill',color||null).attr('font-weight',strong?500:400).text(t); }
function callout(g,x,y,tx,ty,t1,t2){ g.append('path').attr('class','call').attr('d',`M${x},${y} Q${(x+tx)/2},${ty} ${tx},${ty}`); g.append('text').attr('x',tx).attr('y',ty-16).attr('class','lab').attr('text-anchor',tx>x?'start':'end').text(t1); g.append('text').attr('x',tx).attr('y',ty+2).attr('text-anchor',tx>x?'start':'end').text(t2); }

/* ---------- overlays ---------- */
const cubes=()=>{ const r=d3.randomLcg(3); let s=''; for(let i=0;i<10;i++){const a=i/10*Math.PI*2+r()*.4, d=.22+r()*.16; s+=`<i class="cube" style="left:${50+Math.cos(a)*d*100-5.5}%;top:${50+Math.sin(a)*d*100-5.5}%;transform:rotate(${r()*40-20}deg)"></i>`} return s; };
function moneyChart(){ const rows=[['Big fries→Small',-2.65],['Coke→water',-1.16],['Coke→Zero',0],['+apple',1.30],['+tomatoes',1.35],['+pineapple',1.70],['+gazpacho',2.05]];
  const w=1000,h=560,x0=40,bw=100,gap=30,y0=270,sc=70; let s=`<svg class="money" viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Money lost or gained per order">`;
  s+=`<line x1="${x0}" x2="${w-20}" y1="${y0}" y2="${y0}" stroke="#B8AE9C"/><text x="${x0}" y="${y0-14}" font-family="Azeret Mono,monospace" font-size="11" fill="#E9A23B" letter-spacing="1.5">MORE MONEY ↑</text><text x="${x0}" y="${y0+24}" font-family="Azeret Mono,monospace" font-size="11" fill="#FF4A3C" letter-spacing="1.5">LESS MONEY ↓</text>`;
  rows.forEach((r,i)=>{ const x=x0+100+i*(bw+gap); const v=r[1]; const hh=Math.abs(v)*sc; const col=v<0?'#FF4A3C':v>0?'#E9A23B':'#3DDC97';
    if(v===0){ s+=`<circle cx="${x+bw/2}" cy="${y0}" r="14" fill="none" stroke="${col}" stroke-width="3"/>`; } else { s+=`<rect x="${x}" y="${v>0?y0-hh:y0}" width="${bw}" height="${hh}" rx="6" fill="${col}"/>`; }
    s+=`<text x="${x+bw/2}" y="${v>=0?y0-hh-16:y0+hh+28}" text-anchor="middle" font-family="Big Shoulders Display,Impact,sans-serif" font-weight="900" font-size="34" fill="${col}">${v===0?'€0':(v>0?'+':'−')+'€'+Math.abs(v).toFixed(2)}</text>`;
    s+=`<text x="${x+bw/2}" y="${h-36}" text-anchor="middle" font-family="Archivo,Arial,sans-serif" font-size="14" fill="#F3EADB">${r[0]}</text>`; });
  s+=`<text x="${w-20}" y="${h-10}" text-anchor="end" font-family="Azeret Mono,monospace" font-size="10" fill="#6F675B" letter-spacing="1.5">PER ORDER · PRICES: GLOVO MADRID, 10 OCT 2026</text></svg>`; return s; }
const OV={
  cups:()=>`<div class="cups"><div><div class="cup">${cubes()}</div><div class="cap"><b>Coke</b><span>€3.56 · 42 g · about 10 cubes</span></div></div><div class="eq">=</div><div><div class="cup"><div class="g">0 g</div></div><div class="cap"><b>Coke Zero</b><span>€3.56 · 0 g · same cup</span></div></div></div>`,
  basket:()=>`<div class="cards four">
    <div class="card"><div class="n">1 · the drink</div><h3>Zero, not Coke</h3><div class="big">−42 g</div><p>sugar gone. Same price. Same cup.</p></div>
    <div class="card"><div class="n">2 · the size</div><h3>Small, not Large</h3><div class="big">−${Math.round(N.smallSave)} g</div><p>sugar gone on a typical drink. Cheaper too.</p></div>
    <div class="card"><div class="n">3 · the chicken</div><h3>Grilled, not crispy</h3><div class="big">−${N.grilledSave[0]} to ${N.grilledSave[1]}</div><p>calories gone. Every one of the ${N.pGrilled} chicken dishes.</p></div>
    <div class="card"><div class="n">4 · the extra</div><h3>Add an apple</h3><div class="big">+1 fruit</div><p>€1.30 on Glovo Madrid. Fruit is cheap, it just hides at the bottom of the list.</p></div>
  </div>`,
  money:()=>moneyChart(),
  nudges:()=>`<div class="cards">
    <div class="card"><div class="n">Nudge 1 · meal page</div><h3>Zero right under Coke</h3><div class="ui"><div class="row">○ Coke<span>€3.56</span></div><div class="row new">○ Coke Zero <small>same price · 0 g</small></div><div class="row">○ Fanta Zero</div><small>nothing is picked for you</small></div><table><tr><td>Customer</td><td class="g">−42 g sugar ✓</td></tr><tr><td>McDonald's</td><td>€0 · same sale =</td></tr><tr><td>Glovo</td><td>€0 · same fee =</td></tr></table></div>
    <div class="card"><div class="n">Nudge 2 · home</div><h3>"Reorder with Zero"</h3><div class="ui"><div class="row">Big Mac menu · with Coke<span>€9.30</span></div><div class="row" style="border-color:var(--rule)">Reorder</div><div class="row new">Reorder with Zero <small>same price</small></div></div><table><tr><td>Customer</td><td class="g">−42 g, every reorder ✓</td></tr><tr><td>McDonald's</td><td>€0 =</td></tr><tr><td>Glovo</td><td>€0 · faster reorders =</td></tr></table></div>
    <div class="card"><div class="n">Nudge 3 · basket</div><h3>Fruit before fries</h3><div class="ui"><div class="row">Big Mac menu + Zero<span>€9.30</span></div><div class="row new">Add fruit or veg? <small>apple €1.30 · gazpacho €2.05</small></div><div class="row" style="color:var(--muted)">more sides · fries…</div></div><table><tr><td>Customer</td><td class="g">+1 fruit, only if tapped ✓</td></tr><tr><td>McDonald's</td><td class="a">+€0.91 to €1.44 +</td></tr><tr><td>Glovo</td><td class="a">+€0.39 to €0.62 +</td></tr></table></div>
  </div>`,
  ask:()=>`<div class="ask">
    <div><h4>We ask for one decision</h4><ul><li><b>A four-week test in Madrid.</b> Half of McDonald's orders on Glovo see the three nudges. Half do not.</li><li><b>Nothing pre-picked, same-size buttons, ads say ad.</b> That is EU law (Consumer Rights Directive art. 22, Digital Services Act arts. 25 and 26).</li><li><b>Do it before a regulator does.</b> New York already puts a salt icon on menus. California made water the default kids' drink.</li></ul></div>
    <div><h4>We count</h4><ul><li><b>Basket value.</b> Same or bigger, or we stop.</li><li><b>How many pick Zero.</b></li><li><b>How many add fruit or veg.</b></li><li><b>How many come back</b> after "nice pick!"</li></ul></div>
    <div><h4>What this data can't tell us</h4><ul><li><b>It is the US menu.</b> Spain's list is shorter. The pattern is the same.</li><li><b>No sales numbers.</b> A shake nobody orders counts as much as fries. The test fixes that.</li><li><b>The percentages on the last slide are our guesses.</b> 40 % sugary drink, 2 % switch, 5 % add a side, 30 % commission.</li></ul></div>
  </div>`,
  behind:(arcs)=>`<div class="behind"><svg class="arcline" viewBox="0 0 1000 120" preserveAspectRatio="none" aria-hidden="true"><path d="M20,100 C250,70 380,30 520,22 C600,18 640,40 700,60 C800,92 900,98 980,100" fill="none" stroke="#E9A23B" stroke-width="2"/>${[['SETTING + HOOK',60,100],['RISING ACTION',300,56],['AHA',520,22],['SOLUTION',720,66],['NEXT STEPS',930,100]].map(a=>`<circle cx="${a[1]}" cy="${a[2]}" r="5" fill="#F3EADB"/><text x="${a[1]}" y="${a[2]-14}" text-anchor="middle" font-family="Azeret Mono,monospace" font-size="11" fill="#B8AE9C" letter-spacing="1.5">${a[0]}</text>`).join('')}</svg>
    <div class="row4">${arcs.map(a=>`<div><div class="k">${a[0]}</div><p>${a[1]}</p></div>`).join('')}</div>
    <div class="books"><b>Gestalt, Session 2</b> figure-ground (dark page, bright dots) · similarity (one colour = one meaning) · common region (the two boxes) · focal point (one thing lit) · proximity (columns) · continuity (one line = one swap) · <b>Story arc</b> Brent Dykes, Effective Data Storytelling · <b>One mark per item</b> Ben Jones, Learning to See Data · <b>Declutter</b> Cole Nussbaumer Knaflic, Storytelling with Data · <b>Palette</b> Kate Strachnyi, ColorWise · <b>Unit charts</b> Nathan Yau, Visualize This · <b>Delivery</b> Lea Pica, Present Beyond Measure · <b>AI strategy</b> Kavita Ganesan, The Business Case for AI<br>Built with D3.js and AI help (Claude). Ideas, analysis and the Glovo price survey: Group 3.</div></div>`,
};

/* ---------- slides ---------- */
const S = /*SLIDES*/;
const STAGES=['Setting + hook','Rising action','Aha','Solution','Next steps'];

/* ---------- render ---------- */
const svg=d3.select('#svg');
const gOrders=svg.append('g').attr('id','orders').attr('opacity',0);
const gDots=svg.append('g').attr('id','dots');
const gAn=svg.append('g').attr('id','an');
const dots=gDots.selectAll('circle').data(items).join('circle').attr('cx',W/2).attr('cy',H/2).attr('r',0).attr('fill',C.sand);
const op=ordersField(); const ocol={zero:C.zero,fruit:C.gold,sugary:'#5A3A40',other:'#2E2A25'};
gOrders.selectAll('circle').data(op).join('circle').attr('cx',d=>d.x).attr('cy',d=>d.y).attr('r',d=>d.k==='zero'?7:d.k==='fruit'?5.5:4.2).attr('fill',d=>ocol[d.k]).attr('stroke',d=>d.k==='zero'?C.zero:null).attr('stroke-opacity',.35).attr('stroke-width',6);
gOrders.append('text').attr('x',W/2+60).attr('y',700).attr('text-anchor','middle').attr('class','lab').text('ONE MONTH OF ORDERS · 1 DOT = 1,000 ORDERS');
d3.select('#arc').selectAll('span').data(STAGES).join('span').text(d=>d);

let cur=0, showNotes=false;
function render(i){
  cur=Math.max(0,Math.min(S.length-1,i)); const s=S[cur]; const dur=reduced?0:900;
  const t=d3.select('#text'); t.style('opacity',0).html(`<div class="eyebrow">${s.eye}</div><h1>${s.h}</h1><p class="lede">${s.lede}</p>
    <div class="stat"><span class="l">${s.stat[0]}</span><span class="v ${s.stat[2]||''}">${typeof s.stat[1]==='number'?fmt(s.stat[1]):s.stat[1]}</span></div>
    ${s.key&&s.key.length?`<div class="key">${s.key.map(k=>`<span><i style="background:${k[0]}"></i>${k[1]}</span>`).join('')}</div>`:''}
    ${s.howto?`<div class="howto">How to read · ${s.howto}</div>`:''}`);
  t.transition().duration(reduced?0:400).style('opacity',1);
  const P=s.layout==='orders'?L('hidden'):L(s.layout);
  dots.transition().duration(dur).delay((d,i)=>reduced?0:(i%37)*9).ease(d3.easeCubicInOut).attr('cx',d=>P[d.i].x).attr('cy',d=>P[d.i].y).attr('r',d=>P[d.i].r).attr('fill',d=>P[d.i].fill).attr('opacity',d=>P[d.i].op);
  gOrders.transition().duration(dur).attr('opacity',s.layout==='orders'?1:0);
  gAn.transition().duration(reduced?0:200).attr('opacity',0).on('end',()=>{ gAn.selectAll('*').remove(); (AN[s.layout]||(()=>{}))(gAn); gAn.attr('opacity',0).transition().delay(reduced?0:dur*.7).duration(reduced?0:500).attr('opacity',1); });
  const ov=d3.select('#overlay'); if(s.ov){ov.html(typeof s.ov==='function'?s.ov():OV[s.ov]()); ov.classed('on',true)} else {ov.classed('on',false); setTimeout(()=>{if(!S[cur].ov)ov.html('')},500)}
  d3.select('#count').text(String(cur+1).padStart(2,'0')+' / '+S.length);
  d3.select('#bar').style('width',((cur+1)/S.length*100)+'%');
  d3.select('#arc').selectAll('span').classed('on',(d,k)=>k===s.stage);
  d3.select('#src').text(s.src||DEFAULT_SRC);
  d3.select('#nt').text(s.note); d3.select('#nc').text('Course link: '+s.course);
  try{localStorage.setItem('deck-slide-'+document.title,cur)}catch(e){}
}
function next(){render(cur+1)} function prev(){render(cur-1)}
addEventListener('keydown',e=>{ if(['ArrowRight','ArrowDown',' ','PageDown'].includes(e.key)){e.preventDefault();next()} else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();prev()} else if(e.key==='Home'){render(0)} else if(e.key==='End'){render(S.length-1)} else if(e.key.toLowerCase()==='n'){toggleNotes()} });
document.getElementById('stage').addEventListener('click',e=>{ const r=e.currentTarget.getBoundingClientRect(); if(e.target.closest('a,button'))return; (e.clientX-r.left)>r.width/2?next():prev(); });
let tx=null; addEventListener('touchstart',e=>{tx=e.touches[0].clientX},{passive:true}); addEventListener('touchend',e=>{ if(tx==null)return; const dx=e.changedTouches[0].clientX-tx; if(Math.abs(dx)>40){dx<0?next():prev()} tx=null; });
function toggleNotes(){ showNotes=!showNotes; document.getElementById('notes').hidden=!showNotes; }
document.getElementById('nbtn').addEventListener('click',toggleNotes);
let start=0; try{ const h=location.hash.replace('#s',''); if(h&&!isNaN(h))start=+h-1; else { const v=localStorage.getItem('deck-slide-'+document.title); if(v!=null)start=+v; } }catch(e){}
render(start);
</script>
'''

# ---------------- Deck 1: for McDonald's customers ----------------
SLIDES_CUP = r'''[
 {stage:0,eye:'For anyone who eats at McDonald\'s',h:'What\'s in <em>your cup?</em>',lede:`Every dot is one thing on the McDonald's menu. <b>260</b> of them. A bigger dot has more calories. Let's sort them and see where the sugar hides.`,stat:['Things on the menu',N.total],key:[[C.sand,'one dot = one thing on the menu']],howto:'bigger dot = more calories',layout:'circle',
  note:'Every dot is one thing on the menu. Two hundred and sixty. Watch them move. They will show you where the sugar is.',course:'Gestalt: figure-ground. Dark page, bright dots, nothing else. Ben Jones: one mark per item.'},
 {stage:1,eye:'Sugar',h:'<em class="red">62</em> things have a whole day\'s sugar in one go.',lede:`Doctors say about <b>50 g</b> of sugar a day. That is about 12 sugar cubes. Every <b>red</b> dot has more than that in a single serving.`,stat:['Red dots',N.over50,'red'],key:[[C.over,'more than a day of sugar (50 g)'],[C.sand,'less than that']],howto:'dots move right = more sugar',layout:'swarm',
  note:'Line them up by sugar. The red line is one day of sugar, about twelve cubes. Sixty-two things cross it in one serving.',course:'Gestalt: similarity, red always means "too much sugar" in this deck. Session 3: red only for the alert.'},
 {stage:2,eye:'The big one',h:'Every red dot is a <em class="red">drink or a dessert.</em>',lede:`Top box: things you drink or eat with a spoon. Bottom box: things you eat with your hands. All <b>62</b> red dots are in the top box. The sweetest food has <b>${N.plateMax} g</b>.`,stat:['Red dots in the food box',0,'red'],key:[[C.over,'more than a day of sugar'],[C.sand,'less than that']],howto:'two boxes. red only in the top one',layout:'cupplate',
  note:'(Pause.) Two boxes. Drinks and desserts on top, food below. Every red dot is on top. The sweetest thing on a plate has thirty-two grams. The sugar is in the cup, not the burger.',course:'Gestalt: common region, the two boxes do the work. Session 7: this is the aha moment.'},
 {stage:1,eye:'Surprise',h:'Coffee drinks are <em class="amber">sweeter than soda.</em>',lede:`<b>${N.coffee}</b> of the 260 things are coffees and teas. On average they have <b>${Math.round(N.coffeeAvg)} g</b> of sugar. Sodas average ${Math.round(N.sodaAvg)}. The sweetest coffee has ${N.coffeeMax.sugar} g.`,stat:['Coffee and tea, average sugar',Math.round(N.coffeeAvg)+' g','sugar'],key:[[C.sugar,'coffee and tea'],[C.sand,'everything else, faded']],howto:'only coffee is lit up',layout:'coffee',
  note:'Guess the sweetest group. Not shakes. Coffee. Ninety-five coffee drinks, forty grams on average. More than a soda. The sweetest one has ninety-nine.',course:'Gestalt: focal point, one thing lit, the rest faded. Session 7: lead with the surprising number.'},
 {stage:1,eye:'Size',h:'Bigger cup, <em class="amber">more sugar.</em>',lede:`Small: <b>${Math.round(N.sizeAvg.Small)} g</b>. Medium: <b>${Math.round(N.sizeAvg.Medium)} g</b>. Large: <b>${Math.round(N.sizeAvg.Large)} g</b>. A Large drink is over a whole day of sugar by itself.`,stat:['Large vs Small','+'+Math.round(N.sizeAvg.Large-N.sizeAvg.Small)+' g','sugar'],key:[[C.over,'more than a day of sugar'],[C.sand,'less than that'],[C.sugar,'the average for that size']],howto:'each drink goes to its cup size. up = more sugar',layout:'sizes',
  note:'Same drinks, three cup sizes. Each size up is about ten grams more. The average Large is over a day of sugar on its own.',course:'Gestalt: proximity, three columns read as three groups. Knaflic: one axis, one message.'},
 {stage:1,eye:'Food',h:'Food\'s problem is <em class="blue">salt</em>, not sugar.',lede:`Doctors say about 2,300 mg of salt a day. <b>${N.salt48}</b> dishes have half of that or more. 40 nuggets have a day and a half.`,stat:['Dishes with half a day of salt',N.salt48,'blue'],key:[[C.salt,'food with half a day of salt'],[C.grey,'other food'],[C.sand,'drinks and desserts, faded']],howto:'up = more salt. right = more calories',layout:'salt',
  note:'Now the food. Its problem is salt. Forty-eight dishes have half a day of salt. The more calories, the more salt, almost a straight line.',course:'Gestalt: continuity, the dotted line leads the eye. Session 7 Challenger lesson: plain words, no statistics.'},
 {stage:3,eye:'Easy swaps',h:'Same food. <em class="green">Three easy swaps.</em>',lede:`Large to Small: about <b>${Math.round(N.smallSave)} g</b> less sugar. Crispy to grilled: <b>${N.grilledSave[0]} to ${N.grilledSave[1]}</b> fewer calories. Coke to Coke Zero: <b>42 g</b> less sugar, same price.`,stat:['Swaps already on the menu',N.pairs],key:[[C.grey,'Small instead of Large'],[C.sugar,'grilled instead of crispy'],[C.zero,'Zero instead of regular']],howto:'left = what you order now. right = the swap. one line = one swap',layout:'swaps',
  note:'Every swap is already on the menu. Left is what you order now, right is the swap. Grey: order the Small. Amber: grilled. Green: Zero. Green costs the same.',course:'Gestalt: continuity, each line is one swap. Knaflic: slope chart for before and after.'},
 {stage:4,eye:'Your turn',h:'Your <em class="green">better basket.</em>',lede:`Four small choices. None of them costs more. Most of them cost less.`,stat:['Extra cost','€0','green'],key:[],howto:'',layout:'hidden',ov:'basket',src:'Sugar and calories: Kaggle US menu · Coke Zero price: Glovo Madrid, 10 Oct 2026 · Coke sugar: Coca-Cola Spain label',
  note:'Four choices. Zero not Coke. Small not Large. Grilled not crispy. Add an apple. Same food, less sugar, no extra money.',course:'Session 7: resolution = what the audience should do. Gestalt: similarity, four cards, same shape, same job.'},
 {stage:4,eye:'Behind the story',h:'Data + visuals + <em>a story.</em>',lede:`One dataset, 260 dots, nine moves. The nutrition facts are the whole story.`,stat:['Slides',9],key:[],layout:'hidden',ov:()=>OV.behind([['Characters','Anyone who orders at McDonald\'s'],['Setting','260 things on the menu, one dot each'],['Conflict','The sugar hides in the cup'],['Resolution','Four swaps, no extra cost']]),src:'Story arc: Brent Dykes · Gestalt principles: IMBA Data Fluency, Session 2 · hero framework: Session 7',
  note:'Hero: the customer. Guide: us. Every chart follows one Gestalt rule. Twenty seconds, then questions.',course:'Session 2 Gestalt principles, Session 7 hero framework, the seven Book of the Day picks.'},
]'''

# ---------------- Deck 2: pitch to Glovo ----------------
SLIDES_MONEY = r'''[
 {stage:0,eye:'A pitch for the Glovo partnerships team',h:'Healthy can <em>make money.</em>',lede:`Every dot is one McDonald's menu item. <b>260</b> of them. We will show you where the sugar is, and three ways to sell healthier without selling less.`,stat:['Menu items',N.total],key:[[C.sand,'one dot = one menu item']],howto:'bigger dot = more calories',layout:'circle',
  note:'Two hundred and sixty items, one dot each. Three slides from now you will see why healthy and profitable are the same move.',course:'Session 7: setting + hook. Hero = Glovo, guide = us. Gestalt: figure-ground.'},
 {stage:1,eye:'The problem',h:'Most healthy swaps make the order <em class="red">smaller.</em>',lede:`The menu already has <b>${N.pairs}</b> healthier versions of things. <b>${N.pSmaller}</b> of them are just "order the Small". Smaller food, smaller bill. That is why nobody pushes them.`,stat:['Swaps that shrink the bill',N.pSmaller,'red'],key:[[C.grey,'Small instead of Large'],[C.sugar,'grilled instead of crispy'],[C.zero,'Zero instead of regular']],howto:'left = ordered now. right = the healthier version. one line = one swap',layout:'swaps',
  note:'Sixty-four healthier versions exist today. Forty-three are "order the Small". Healthier means a smaller bill. That is the problem we fix.',course:'Session 7: the conflict. Gestalt: continuity, one line per swap.'},
 {stage:2,eye:'The finding',h:'All the sugar is <em class="red">in the cup.</em>',lede:`Top box: drinks and desserts. Bottom box: food. All <b>${N.over50}</b> items with a whole day of sugar (50 g) are in the top box. So fix the cup, not the burger.`,stat:['Over-the-limit items in a cup',N.over50,'red'],key:[[C.over,'more than a day of sugar'],[C.sand,'less than that']],howto:'two boxes. red only in the top one',layout:'cupplate',
  note:'(Pause.) Two boxes. Every item with a day of sugar is in the top one. The fix is in the drink, and the drink is where the free swap lives.',course:'Gestalt: common region. Session 7: the aha moment.'},
 {stage:2,eye:'The free swap',h:'<em class="green">8</em> swaps cost nothing. All of them are drinks.',lede:`Coke to Coke Zero. Same cup, same price, zero sugar. <b>${N.pDiet}</b> of the ${N.pairs} swaps work like this. McDonald's loses nothing. Glovo loses nothing.`,stat:['Free swaps',N.pDiet,'green'],key:[[C.zero,'Zero instead of regular'],[C.dim,'the other swaps, faded']],howto:'only the free swaps are lit up',layout:'swapsDiet',
  note:'Light up the swaps that cost nothing. Eight. All drinks. Same cup, same price, no sugar. This is the lever.',course:'Gestalt: focal point, only the green lines lit. Session 3: highlight palette.'},
 {stage:3,eye:'Same price',h:'Same price. <em class="green">No sugar.</em>',lede:`On Glovo Madrid a Coke and a Coke Zero both cost <b>€3.56</b>. One has about ten sugar cubes. The other has none.`,stat:['Price difference','€0','green'],key:[],howto:'',layout:'hidden',ov:'cups',src:'Prices: Glovo Madrid, 10 Oct 2026 · Sugar: Coca-Cola Spain label, medium 40 cl · 1 cube ≈ 4 g',
  note:'Ten cubes or none. Same price. Nobody loses a cent.',course:'Brent Dykes: the plan the guide hands the hero. Gestalt: similarity, two identical cups, one difference.'},
 {stage:3,eye:'Add, don\'t shrink',h:'Add fruit, <em class="amber">make money.</em>',lede:`Make the order smaller and McDonald's loses <b>€1 to €3</b>. Swap Coke for Zero: <b>€0</b>. Add an apple or a gazpacho: <b>+€1.30 to +€2.05</b>. Healthy can go up, not down.`,stat:['Add a gazpacho, per order','+€2.05','sugar'],key:[[C.over,'money lost'],[C.zero,'same money'],[C.sugar,'money added']],howto:'bars go down = lost. bars go up = gained',layout:'hidden',ov:'money',src:'Prices: Glovo Madrid McDonald\'s listing, 10 Oct 2026 · per order, before Glovo\'s fee',
  note:'Red goes down: make it smaller, lose money. Green: Zero, same money. Amber goes up: add fruit, make money. The healthy choices that pay are the add-ons.',course:'Gestalt: similarity, red down, amber up. Nathan Yau: unit values, read the bar height.'},
 {stage:3,eye:'The plan',h:'Three nudges. <em>Nothing pre-picked.</em>',lede:`Put Zero right under Coke with "same price, 0 g". Add a "Reorder with Zero" button. Show fruit before fries in the basket. Same money or more, every time.`,stat:['Nudges that shrink the order',0],key:[],howto:'',layout:'hidden',ov:'nudges',src:'Concept for the McDonald\'s order flow on Glovo · prices Glovo Madrid · Glovo fee assumed 30 %',
  note:'Three changes to the order flow. None pre-picks. The customer always chooses. Same sale, same fee, or more.',course:'Session 3: Z-pattern, most important nudge top-left. EU CRD art. 22, DSA arts. 25–26: never pre-tick.'},
 {stage:3,eye:'Scale',h:'Only a few need to <em>say yes.</em>',lede:`One month, one million orders. If <b>2 in 100</b> sugary-drink orders switch to Zero and 5 in 100 add a €1.30 side: <b>336 kg</b> less sugar, <b>€45,500</b> more for McDonald's, <b>€19,500</b> more for Glovo.`,stat:['More money for McDonald\'s, per month','€45,500','sugar'],key:[[C.pink,'has a sugary drink'],[C.zero,'picked Zero instead'],[C.gold,'added fruit or veg'],[C.sand,'1 dot = 1,000 orders']],howto:'one dot = 1,000 orders',layout:'orders',src:'OUR GUESSES, NOT DATA: 1,000,000 orders · 40 % include a sugary drink · 2 % of those pick Zero · 5 % add a €1.30 side · 30 % commission · the test replaces these with real numbers',
  note:'These percentages are our guesses. Even so: two in a hundred switch, that is 336 kilos of sugar a month, forty-five thousand euros for McDonald\'s, nineteen for Glovo.',course:'Nathan Yau: unit charts make scale felt. Session 7: say what is assumed, let the pilot replace it.'},
 {stage:4,eye:'Next steps',h:'Try it for <em>four weeks.</em>',lede:`Half of Madrid orders see the nudges. Half don't. Count basket value, Zero share, fruit share. Then the guesses become numbers.`,stat:['Decision we ask for',1],key:[],howto:'',layout:'hidden',ov:'ask',
  note:'One decision: a four-week test in Madrid. Baskets no smaller, more Zero, more fruit. Then the guesses become numbers. Questions.',course:'Session 7: resolution = one decision to ask for, plus what the data cannot tell you.'},
 {stage:4,eye:'Behind the story',h:'Data + visuals + <em>a story.</em>',lede:`One dataset, 260 dots, ten moves. The nutrition facts found the problem. The Glovo price list found the money.`,stat:['Slides',10],key:[],layout:'hidden',ov:()=>OV.behind([['Characters','Glovo, McDonald\'s, hungry Madrid'],['Setting','260 menu items, one dot each'],['Conflict','Healthy swaps shrink the bill'],['Resolution','Free swap + add-ons, four-week test']]),src:'Story arc: Brent Dykes · Gestalt principles: IMBA Data Fluency, Session 2 · hero framework: Session 7',
  note:'Hero: Glovo. Guide: us. Every chart follows one Gestalt rule. Twenty seconds, then questions.',course:'Session 2 Gestalt principles, Session 7 hero framework, the seven Book of the Day picks.'},
]'''

def build(fname, title, accent, slides):
    html = TEMPLATE.replace('/*TITLE*/', title).replace('/*ACCENT*/', accent).replace('/*SLIDES*/', slides).replace('/*DATA*/', DATA)
    (HERE / fname).write_text(html)
    print(fname, len(html), 'bytes')

build('whats-in-your-cup.html', "What's in Your Cup", '#E9A23B', SLIDES_CUP)
build('healthy-makes-money.html', 'Healthy Makes Money', '#3DDC97', SLIDES_MONEY)
