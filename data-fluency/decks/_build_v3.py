#!/usr/bin/env python3
"""Builds v3 of both Data Fluency decks: every beat = one text slide + one full-screen data slide.
   Outputs whats-in-your-cup-v3.html and healthy-makes-money-v3.html. Run from this folder."""
import pathlib
HERE = pathlib.Path(__file__).parent
DATA = (HERE / 'menu-data.json').read_text()

TEMPLATE = r'''<title>/*TITLE*/</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,900;1,9..144,300;1,9..144,900&family=Archivo:wght@400;500;600&family=Azeret+Mono:wght@400;500&display=swap">
<style>
/* Layout: the data IS the page. A full-viewport stage of 260 dots; text slides float over it dimmed, data slides give the dots the whole screen with one caption. */
:root{
  --ink:#0A0908; --paper:#F4ECDD; --paper-2:#B9AF9D; --muted:#6E665A; --rule:#2B2722;
  --sand:#4A443B; --sugar:#F0A63A; --over:#FF4A3C; --salt:#4FA3FF; --zero:#3DDC97; --pink:#F08A9B; --gold:#F0A63A;
  --accent:/*ACCENT*/;
  --display:"Fraunces","Iowan Old Style",Georgia,serif;
  --body:"Archivo","Helvetica Neue",Arial,sans-serif;
  --mono:"Azeret Mono","SFMono-Regular",Menlo,Consolas,monospace;
  color-scheme:dark;
}
html,body{height:100%}
body{margin:0;background:var(--ink);color:var(--paper);font-family:var(--body);font-size:16px;line-height:1.45;overflow:hidden;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0}
.stage{position:fixed;inset:0;transition:opacity .7s ease,filter .7s ease}
.stage.dim{opacity:.22;filter:blur(1.5px)}
.stage.half{opacity:.5}
.stage svg{width:100%;height:100%;display:block}
.vignette{position:fixed;inset:0;pointer-events:none;background:radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,.55) 100%)}
.bar{position:fixed;top:0;left:0;right:0;height:3px;background:var(--rule);z-index:6}
.bar i{display:block;height:100%;background:var(--accent);width:0;transition:width .5s ease}
.chrome{position:fixed;left:max(24px,env(safe-area-inset-left,0px));right:max(24px,env(safe-area-inset-right,0px));z-index:5;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--paper-2);display:flex;justify-content:space-between;gap:16px;pointer-events:none}
.chrome.top{top:calc(14px + env(safe-area-inset-top,0px))}
.chrome.bottom{bottom:calc(14px + env(safe-area-inset-bottom,0px));align-items:flex-end}
.chrome .brand{color:var(--paper);font-weight:500}
.chrome .count{font-variant-numeric:tabular-nums}
.arc{display:flex;gap:14px}
.arc span{position:relative;padding-left:12px}
.arc span::before{content:"";position:absolute;left:0;top:50%;width:6px;height:6px;border-radius:50%;background:var(--rule);transform:translateY(-50%)}
.arc span.on{color:var(--paper)} .arc span.on::before{background:var(--accent)}
.src{max-width:46vw;line-height:1.5;color:var(--muted);text-align:right}
button.notes{pointer-events:auto;font:inherit;font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;background:rgba(10,9,8,.6);border:1px solid var(--rule);color:var(--paper-2);padding:5px 10px;border-radius:3px;cursor:pointer}
button.notes:active{transform:scale(.97)}
/* text slide */
.text{position:fixed;inset:0;display:grid;place-items:center;padding:8vh 6vw;z-index:3;pointer-events:none;opacity:0;transform:translateY(16px);transition:opacity .45s cubic-bezier(.2,.8,.2,1),transform .55s cubic-bezier(.2,.9,.1,1)}
.text.on{opacity:1;transform:none;pointer-events:auto}
.text .wrap{max-width:1180px;width:100%;display:grid;gap:clamp(14px,2.4vh,28px)}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent)}
h1{font-family:var(--display);font-weight:900;font-variation-settings:"opsz" 144;font-size:clamp(44px,8.2vw,124px);line-height:.95;margin:0;letter-spacing:-.015em;text-wrap:balance}
h1 em{font-style:italic;font-weight:900;color:var(--accent)}
h1 em.red{color:var(--over)} h1 em.blue{color:var(--salt)} h1 em.green{color:var(--zero)} h1 em.amber{color:var(--sugar)}
.lede{font-family:var(--display);font-weight:300;font-variation-settings:"opsz" 30;font-size:clamp(20px,2.4vw,32px);line-height:1.3;color:var(--paper-2);max-width:34ch;margin:0}
.lede b{color:var(--paper);font-weight:300;font-style:italic}
.goto{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
/* data slide captions */
.cap{position:fixed;z-index:4;pointer-events:none;opacity:0;transition:opacity .5s .3s}
.cap.on{opacity:1}
.cap.tl{top:calc(44px + env(safe-area-inset-top,0px));left:max(24px,env(safe-area-inset-left,0px));max-width:min(46vw,620px)}
.cap.tl h2{font-family:var(--display);font-weight:900;font-variation-settings:"opsz" 72;font-size:clamp(22px,2.6vw,38px);line-height:1.02;margin:0;letter-spacing:-.01em;text-wrap:balance}
.cap.tl h2 em{font-style:italic;color:var(--accent)} .cap.tl h2 em.red{color:var(--over)} .cap.tl h2 em.blue{color:var(--salt)} .cap.tl h2 em.green{color:var(--zero)} .cap.tl h2 em.amber{color:var(--sugar)}
.cap.tl .howto{margin-top:10px;font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);border-left:2px solid var(--accent);padding-left:10px}
.cap.tr{top:calc(40px + env(safe-area-inset-top,0px));right:max(24px,env(safe-area-inset-right,0px));text-align:right}
.cap.tr .v{font-family:var(--display);font-weight:900;font-variation-settings:"opsz" 144;font-size:clamp(48px,7vw,112px);line-height:.9;letter-spacing:-.02em;font-variant-numeric:tabular-nums;color:var(--paper)}
.cap.tr .v.sugar{color:var(--sugar)} .cap.tr .v.red{color:var(--over)} .cap.tr .v.blue{color:var(--salt)} .cap.tr .v.green{color:var(--zero)}
.cap.tr .l{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--paper-2);margin-top:6px}
.cap.bl{bottom:calc(48px + env(safe-area-inset-bottom,0px));left:max(24px,env(safe-area-inset-left,0px));display:grid;gap:6px;font-family:var(--mono);font-size:11px;letter-spacing:.06em;color:var(--paper-2)}
.cap.bl span{display:flex;align-items:center;gap:10px}
.cap.bl i{width:10px;height:10px;border-radius:50%;display:inline-block;flex:none;box-shadow:0 0 8px currentColor}
/* svg */
svg text{font-family:var(--mono);font-size:13px;fill:var(--paper-2);letter-spacing:.04em}
svg text.big{font-family:var(--display);font-weight:900;font-size:36px;fill:var(--paper);letter-spacing:-.01em}
svg text.lab{fill:var(--paper)}
svg .axis line,svg .axis path{stroke:var(--rule)}
svg .rule{stroke:var(--paper-2);stroke-dasharray:4 5;stroke-width:1}
svg .rule.hard{stroke:var(--over);stroke-dasharray:none;stroke-width:1.5;filter:url(#glowline)}
svg .call{stroke:var(--paper-2);fill:none;stroke-width:1}
svg .region{fill:rgba(255,255,255,.035);stroke:var(--rule);stroke-width:1;rx:18}
/* overlays (full screen) */
.overlay{position:fixed;inset:0;z-index:4;display:grid;place-items:center;padding:clamp(70px,11vh,110px) 5vw;opacity:0;pointer-events:none;transition:opacity .5s}
.overlay.on{opacity:1;pointer-events:auto}
.overlay > *{width:100%;max-width:1400px;min-width:0}
.cups{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:40px;justify-items:center}
.cup{width:min(52vmin,440px);aspect-ratio:1;border-radius:50%;background:radial-gradient(circle at 40% 35%,#3A2A1E,#1E1510 70%);border:3px solid #3A2C21;position:relative;display:grid;place-items:center;box-shadow:0 30px 80px rgba(0,0,0,.6)}
.cup .g{font-family:var(--display);font-weight:900;font-size:clamp(56px,10vmin,120px);color:var(--zero);text-shadow:0 0 30px rgba(61,220,151,.5)}
.cup .cube{position:absolute;width:11%;height:11%;background:var(--paper);border-radius:12%;box-shadow:inset -3px -3px 0 rgba(0,0,0,.15),0 4px 10px rgba(0,0,0,.4)}
.cups .eq{font-family:var(--display);font-weight:900;font-size:90px;color:var(--accent)}
.cups .cap2{display:grid;justify-items:center;gap:6px;margin-top:18px;text-align:center}
.cups .cap2 b{font-family:var(--display);font-weight:900;font-size:36px}
.cups .cap2 span{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--paper-2)}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.cards.four{grid-template-columns:repeat(4,minmax(0,1fr))}
.card{border:1px solid var(--rule);border-radius:6px;padding:26px;display:grid;gap:14px;background:rgba(10,9,8,.72);backdrop-filter:blur(6px);align-content:start}
.card .n{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent)}
.card h3{font-family:var(--display);font-weight:900;font-size:clamp(26px,2.6vw,38px);line-height:1;margin:0;letter-spacing:-.01em}
.card .big{font-family:var(--display);font-weight:900;font-size:clamp(48px,5.4vw,78px);line-height:1;color:var(--zero);text-shadow:0 0 24px rgba(61,220,151,.35)}
.card p{margin:0;color:var(--paper-2);font-size:16px}
.card .ui{border:1px solid var(--rule);border-radius:12px;padding:12px 14px;font-size:14px;display:grid;gap:8px;background:var(--ink)}
.card .ui .row{display:flex;justify-content:space-between;gap:8px;padding:8px 10px;border-radius:8px;border:1px solid transparent}
.card .ui .row.new{border-color:var(--zero);color:var(--zero);box-shadow:0 0 14px rgba(61,220,151,.25)}
.card .ui small{color:var(--paper-2);font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase}
.card table{width:100%;border-collapse:collapse;font-size:14px}
.card td{padding:6px 0;border-top:1px solid var(--rule)}
.card td:last-child{text-align:right;font-family:var(--mono);font-size:12.5px;white-space:nowrap}
.card td.g{color:var(--zero)} .card td.a{color:var(--sugar)}
.ask{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px}
.ask > div{background:rgba(10,9,8,.72);border:1px solid var(--rule);border-radius:6px;padding:26px}
.ask h4{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin:0 0 14px;border-bottom:1px solid var(--rule);padding-bottom:10px}
.ask ul{margin:0;padding:0;list-style:none;display:grid;gap:12px;font-size:16px;color:var(--paper-2)}
.ask li b{color:var(--paper);font-weight:600}
.money{width:100%;height:min(70vh,760px)}
.behind{display:grid;gap:28px;background:rgba(10,9,8,.72);border:1px solid var(--rule);border-radius:6px;padding:30px}
.behind .arcline{height:130px;width:100%}
.behind .row4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px}
.behind .row4 div{border-top:1px solid var(--rule);padding-top:10px}
.behind .row4 .k{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
.behind .row4 p{margin:6px 0 0;font-family:var(--display);font-weight:900;font-size:26px;line-height:1.05}
.behind .books{font-family:var(--mono);font-size:11.5px;letter-spacing:.04em;color:var(--paper-2);line-height:1.9}
.behind .books b{color:var(--paper);font-weight:500}
#notes[hidden]{display:none}
#notes{position:fixed;left:max(16px,env(safe-area-inset-left,0px));right:max(16px,env(safe-area-inset-right,0px));bottom:calc(56px + env(safe-area-inset-bottom,0px));margin:0 auto;max-width:900px;background:var(--ink);border:1px solid var(--accent);border-radius:4px;padding:16px 20px;z-index:8;display:grid;gap:8px;font-size:15px;box-shadow:0 20px 60px rgba(0,0,0,.6)}
#notes .k{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
#notes .course{color:var(--paper-2);font-size:13.5px}
.focus:focus-visible{outline:2px solid var(--accent)}
@media (max-width:900px){
  h1{font-size:40px} .lede{font-size:18px}
  .cap.tl{max-width:70vw} .cap.tr .v{font-size:44px} .cap.bl{display:none} .src{display:none} .arc{display:none}
  .cards,.cards.four,.ask,.behind .row4{grid-template-columns:1fr}
  .cups{grid-template-columns:1fr} .cups .eq{display:none} .cup{width:40vmin}
  .overlay{overflow:auto;place-items:start;padding-top:70px}
}
@media (prefers-reduced-motion:reduce){ *{transition:none!important} }
</style>

<div class="bar"><i id="bar"></i></div>
<div class="stage" id="stage"><svg id="svg" viewBox="0 0 1280 720" preserveAspectRatio="xMidYMid slice" role="img" aria-label="260 menu items as dots">
  <defs id="defs"><filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="glowline" x="-5%" y="-200%" width="110%" height="500%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
</svg></div>
<div class="vignette"></div>
<div class="text" id="text"></div>
<div class="cap tl" id="captl"></div><div class="cap tr" id="captr"></div><div class="cap bl" id="capbl"></div>
<div class="overlay" id="overlay"></div>
<div class="chrome top"><span class="brand">/*TITLE*/</span><span class="count" id="count">01</span></div>
<div class="chrome bottom"><div class="arc" id="arc"></div><div class="src" id="src"></div><div><button class="notes" id="nbtn" type="button">Notes · N</button></div></div>
<div id="notes" hidden><div class="k">Speaker</div><div id="nt"></div><div class="course" id="nc"></div></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script>
const DATA = /*DATA*/;
const DEFAULT_SRC = "Data: Nutrition Facts for McDonald's Menu (Kaggle, US, 260 items) · US menu used as a stand-in for Madrid";
const CUP = new Set(['Beverages','Coffee & Tea','Smoothies & Shakes','Desserts']);
const W=1280,H=720,M=120;
const HEX={sand:'#4A443B',sugar:'#F0A63A',over:'#FF4A3C',salt:'#4FA3FF',zero:'#3DDC97',pink:'#F08A9B',gold:'#F0A63A',grey:'#8B8378',dim:'#2B2723',paper:'#F4ECDD',sugary:'#5A3A40',other:'#2E2A25'};
const LIT=new Set(['sugar','over','salt','zero','pink','gold']);
const rScale=d3.scaleSqrt().domain([0,1900]).range([2.8,13]);
const items=DATA.map((d,i)=>({...d,i,cup:CUP.has(d.cat),r:rScale(d.cal)}));
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const fmt=d3.format(',');

/* gradients: lighter centre so dots read as objects, not flat discs */
const defs=d3.select('#defs');
Object.entries(HEX).forEach(([k,c])=>{ const g=defs.append('radialGradient').attr('id','g-'+k).attr('cx','38%').attr('cy','35%').attr('r','70%');
  g.append('stop').attr('offset','0%').attr('stop-color',d3.color(c).brighter(.9)); g.append('stop').attr('offset','100%').attr('stop-color',c); });

/* ---------- numbers ---------- */
const N={};
N.total=items.length; N.over50=items.filter(d=>d.sugar>50).length; N.zero=items.filter(d=>d.sugar===0).length;
N.cup=items.filter(d=>d.cup).length; N.plate=N.total-N.cup; N.plateMax=d3.max(items.filter(d=>!d.cup),d=>d.sugar);
N.maxItem=items.reduce((a,b)=>b.sugar>a.sugar?b:a);
const catAvg=c=>d3.mean(items.filter(d=>d.cat===c),d=>d.sugar);
N.coffee=items.filter(d=>d.cat==='Coffee & Tea').length; N.coffeeAvg=catAvg('Coffee & Tea'); N.sodaAvg=catAvg('Beverages'); N.shakeAvg=catAvg('Smoothies & Shakes'); N.shakes=items.filter(d=>d.cat==='Smoothies & Shakes').length;
N.coffeeMax=items.filter(d=>d.cat==='Coffee & Tea').reduce((a,b)=>b.sugar>a.sugar?b:a);
items.forEach(d=>{const m=d.item.match(/\((Small|Medium|Large)\)$/);d.size=m?m[1]:null});
N.sized=items.filter(d=>d.size).length; N.sizeAvg={}; ['Small','Medium','Large'].forEach(s=>N.sizeAvg[s]=d3.mean(items.filter(d=>d.size===s),d=>d.sugar));
N.salt48=items.filter(d=>!d.cup&&d.sodium>=1150).length;
N.nuggets=items.find(d=>/40 piece/.test(d.item)); N.bigb=items.filter(d=>/Big Breakfast with Hotcakes/.test(d.item)).reduce((a,b)=>b.sodium>a.sodium?b:a);
const byName=new Map(items.map(d=>[d.item,d])); const pairs=[];
items.forEach(d=>{ if(/\(Large\)$/.test(d.item)){const s=byName.get(d.item.replace('(Large)','(Small)')); if(s)pairs.push({a:d,b:s,t:'smaller'})}});
items.forEach(d=>{ if(/Crispy/.test(d.item)){const g=byName.get(d.item.replace('Crispy','Grilled')); if(g)pairs.push({a:d,b:g,t:'grilled'})}});
items.forEach(d=>{ if(/^Diet /.test(d.item)){const r=byName.get(d.item.replace(/^Diet Coke/,'Coca-Cola Classic').replace(/^Diet /,'')); if(r)pairs.push({a:r,b:d,t:'diet'})}});
N.pairs=pairs.length; N.pSmaller=pairs.filter(p=>p.t==='smaller').length; N.pGrilled=pairs.filter(p=>p.t==='grilled').length; N.pDiet=pairs.filter(p=>p.t==='diet').length;
N.grilledSave=d3.extent(pairs.filter(p=>p.t==='grilled'),p=>p.a.cal-p.b.cal); N.smallSave=d3.median(pairs.filter(p=>p.t==='smaller'),p=>p.a.sugar-p.b.sugar);

/* ---------- layouts (fill = key into HEX) ---------- */
const sx=d3.scaleLinear().domain([0,130]).range([M,W-M]);
const ysw=d3.scaleLinear().domain([0,900]).range([600,215]);
const SW={a:430,b:850};
const SZ={Small:330,Medium:640,Large:950}; const sySize=d3.scaleLinear().domain([0,130]).range([600,200]);
const xsC=d3.scaleLinear().domain([0,1900]).range([M,W-M]), ysN=d3.scaleLinear().domain([0,3700]).range([600,200]);
function base(){return items.map(d=>({x:W/2,y:H/2,r:d.r,fill:'sand',op:1}))}
function swarm(nodesIn,xs,ys,sxv=1,syv=0.1){ const nodes=nodesIn.map(d=>({i:d.i,x:xs(d),y:ys(d),r:d.r}));
  const sim=d3.forceSimulation(nodes).force('x',d3.forceX(n=>xs(items[n.i])).strength(sxv)).force('y',d3.forceY(n=>ys(items[n.i])).strength(syv)).force('c',d3.forceCollide(n=>n.r+1.6).iterations(3)).stop();
  for(let k=0;k<220;k++)sim.tick(); return nodes; }
const cache={}; function L(name){ if(cache[name])return cache[name]; const p=LAYOUTS[name](); cache[name]=p; return p; }
const sugarFill=d=>d.sugar>50?'over':'sand';
const swapCol={smaller:'grey',grilled:'sugar',diet:'zero'};
const LAYOUTS={
  circle(){ const p=base(); const nodes=items.map((d,i)=>{const t=i*2.39996,r=21*Math.sqrt(i);return {i,x:W/2+r*Math.cos(t),y:H/2+r*Math.sin(t),r:d.r}});
    const sim=d3.forceSimulation(nodes).force('c',d3.forceCollide(n=>n.r+2)).force('x',d3.forceX(W/2).strength(.02)).force('y',d3.forceY(H/2).strength(.02)).stop(); for(let k=0;k<120;k++)sim.tick();
    nodes.forEach(n=>{p[n.i].x=n.x;p[n.i].y=n.y}); return p; },
  swarm(){ const p=base(); swarm(items,d=>sx(d.sugar),()=>400).forEach(n=>{p[n.i].x=n.x;p[n.i].y=n.y;p[n.i].fill=sugarFill(items[n.i])}); return p; },
  cupplate(){ const p=base(); swarm(items,d=>sx(d.sugar),d=>d.cup?270:500).forEach(n=>{p[n.i].x=n.x;p[n.i].y=n.y;p[n.i].fill=sugarFill(items[n.i])}); return p; },
  coffee(){ const p=L('cupplate').map(o=>({...o})); items.forEach(d=>{const q=p[d.i]; if(d.cat==='Coffee & Tea'){q.fill='sugar';q.op=1}else{q.fill='sand';q.op=d.cup?.45:.2}}); return p; },
  sizes(){ const p=L('coffee').map(o=>({...o,fill:'sand',op:0,r:0}));
    swarm(items.filter(d=>d.size),d=>SZ[d.size],d=>sySize(d.sugar),.12,1).forEach(n=>{const d=items[n.i];p[n.i]={x:n.x,y:n.y,r:d.r,fill:d.sugar>50?'over':'sand',op:1}}); return p; },
  salt(){ const p=L('sizes').map(o=>({...o})); items.forEach(d=>{p[d.i]={x:xsC(d.cal),y:ysN(d.sodium),r:d.r,fill:d.cup?'sand':(d.sodium>=1150?'salt':'grey'),op:d.cup?.15:1}}); return p; },
  swaps(){ const p=L('salt').map(o=>({...o,op:0,r:0})); const seen=new Set();
    pairs.forEach(pr=>{ if(!seen.has(pr.a.i)){p[pr.a.i]={x:SW.a,y:ysw(pr.a.cal),r:pr.a.r,fill:swapCol[pr.t],op:1};seen.add(pr.a.i)} if(!seen.has(pr.b.i)){p[pr.b.i]={x:SW.b,y:ysw(pr.b.cal),r:pr.b.r,fill:swapCol[pr.t],op:1};seen.add(pr.b.i)} }); return p; },
  swapsDiet(){ const p=L('swaps').map(o=>({...o})); const dietIdx=new Set(pairs.filter(pr=>pr.t==='diet').flatMap(pr=>[pr.a.i,pr.b.i]));
    items.forEach(d=>{ if(p[d.i].op>0){ if(dietIdx.has(d.i)){p[d.i].fill='zero';p[d.i].op=1}else{p[d.i].fill='dim';p[d.i].op=.7} } }); return p; },
  hidden(){ return L('swaps').map(o=>({...o,op:0,r:0})); },
};
function ordersField(){ const n=1000, pts=[]; for(let i=0;i<n;i++){const t=i*2.39996,r=8.6*Math.sqrt(i);pts.push({x:W/2+r*Math.cos(t),y:H/2+10+r*Math.sin(t),k:i<8?'zero':i<58?'gold':i<458?'sugary':'other'})}
  const rnd=d3.randomLcg(7); for(let i=pts.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[pts[i].k,pts[j].k]=[pts[j].k,pts[i].k]} return pts; }

/* ---------- annotations ---------- */
const AN={
  circle(g){},
  swarm(g){ axisX(g,630,'More sugar this way'); vline(g,sx(50),200,615,'A whole day of sugar · 50 g · about 12 cubes',true); },
  cupplate(g){ g.append('rect').attr('class','region').attr('x',M-30).attr('y',165).attr('width',W-2*M+60).attr('height',210); g.append('rect').attr('class','region').attr('x',M-30).attr('y',395).attr('width',W-2*M+60).attr('height',210);
    axisX(g,630,'More sugar this way'); vline(g,sx(50),165,605,'A whole day of sugar · 50 g',true);
    label(g,M-10,190,'IN A CUP',true); label(g,M-10,210,N.cup+' things you drink or eat with a spoon');
    label(g,M-10,420,'ON A PLATE',true); label(g,M-10,440,N.plate+' things you eat with your hands');
    const mx=L('cupplate')[N.maxItem.i]; callout(g,mx.x,mx.y,mx.x-150,mx.y-66,N.maxItem.item.replace(' Candies',''),N.maxItem.sugar+' g · two and a half days of sugar');
    const pm=items.filter(d=>!d.cup).reduce((a,b)=>b.sugar>a.sugar?b:a); const pp=L('cupplate')[pm.i]; callout(g,pp.x,pp.y,pp.x+90,pp.y+76,'Sweetest thing on a plate',pm.sugar+' g · '+pm.item); },
  coffee(g){ axisX(g,630,'More sugar this way'); vline(g,sx(50),165,605,'A whole day of sugar · 50 g',true);
    label(g,M-10,190,'COFFEE AND TEA · '+N.coffee+' DRINKS',true,HEX.sugar); label(g,M-10,210,'they average '+Math.round(N.coffeeAvg)+' g · sodas average '+Math.round(N.sodaAvg)+' g');
    const cm=L('coffee')[N.coffeeMax.i]; callout(g,cm.x,cm.y,cm.x-130,cm.y-74,N.coffeeMax.item,N.coffeeMax.sugar+' g · about '+Math.round(N.coffeeMax.sugar/4)+' cubes'); },
  sizes(g){ hline(g,sySize(50),M,W-M,'A whole day of sugar · 50 g',true);
    ['Small','Medium','Large'].forEach(s=>{ const a=N.sizeAvg[s]; g.append('line').attr('x1',SZ[s]-120).attr('x2',SZ[s]+120).attr('y1',sySize(a)).attr('y2',sySize(a)).attr('stroke',HEX.sugar).attr('stroke-width',2.5).attr('filter','url(#glowline)');
      g.append('text').attr('x',SZ[s]).attr('y',645).attr('text-anchor','middle').attr('class','big').text(s); g.append('text').attr('x',SZ[s]+128).attr('y',sySize(a)+4).attr('fill',HEX.sugar).text('average '+Math.round(a)+' g'); }); },
  salt(g){ g.append('g').attr('class','axis').attr('transform','translate(0,600)').call(d3.axisBottom(xsC).ticks(5).tickSize(-400).tickFormat(d=>d)).call(s=>s.select('.domain').remove()).selectAll('line').attr('stroke','#1C1916');
    g.append('text').attr('x',W-M).attr('y',588).attr('text-anchor','end').text('MORE CALORIES THIS WAY →'); g.append('text').attr('x',M).attr('y',190).text('MORE SALT THIS WAY ↑');
    hline(g,ysN(1150),M,W-M,'Half a day of salt · 1,150 mg',false,HEX.salt);
    const food=items.filter(d=>!d.cup); const mx=d3.mean(food,d=>d.cal),my=d3.mean(food,d=>d.sodium); const b=d3.sum(food,d=>(d.cal-mx)*(d.sodium-my))/d3.sum(food,d=>(d.cal-mx)**2); const a=my-b*mx; const xmax=d3.max(food,d=>d.cal);
    g.append('line').attr('x1',xsC(0)).attr('y1',ysN(a)).attr('x2',xsC(xmax)).attr('y2',ysN(a+b*xmax)).attr('stroke',HEX.paper).attr('stroke-opacity',.5).attr('stroke-dasharray','2 4');
    g.append('text').attr('x',M).attr('y',290).attr('fill',HEX.paper).text('ALMOST A STRAIGHT LINE: MORE CALORIES, MORE SALT');
    callout(g,xsC(N.nuggets.cal),ysN(N.nuggets.sodium),xsC(N.nuggets.cal)-130,ysN(N.nuggets.sodium)+150,N.nuggets.item,fmt(N.nuggets.sodium)+' mg · a day and a half of salt');
    callout(g,xsC(N.bigb.cal),ysN(N.bigb.sodium),xsC(N.bigb.cal)-80,ysN(N.bigb.sodium)-104,'Big Breakfast with Hotcakes',fmt(N.bigb.sodium)+' mg · one day of salt'); },
  swaps(g){ pairs.forEach(pr=>g.append('line').attr('x1',SW.a).attr('y1',ysw(pr.a.cal)).attr('x2',SW.b).attr('y2',ysw(pr.b.cal)).attr('stroke',HEX[swapCol[pr.t]]).attr('stroke-opacity',pr.t==='smaller'?.35:.85).attr('stroke-width',pr.t==='smaller'?1:1.8));
    swapChrome(g); rlabels(g,[[N.pSmaller+' × Small instead of Large','grey',Math.round(N.smallSave)+' g less sugar · cheaper'],[N.pGrilled+' × grilled, not crispy','sugar',N.grilledSave[0]+' to '+N.grilledSave[1]+' fewer calories'],[N.pDiet+' × Zero, not regular','zero','same cup, same price, 0 g']]); },
  swapsDiet(g){ pairs.forEach(pr=>g.append('line').attr('x1',SW.a).attr('y1',ysw(pr.a.cal)).attr('x2',SW.b).attr('y2',ysw(pr.b.cal)).attr('stroke',pr.t==='diet'?HEX.zero:HEX.dim).attr('stroke-opacity',pr.t==='diet'?.95:.7).attr('stroke-width',pr.t==='diet'?2.2:1).attr('filter',pr.t==='diet'?'url(#glowline)':null));
    swapChrome(g); rlabels(g,[[N.pDiet+' × Zero, not regular','zero','same cup, same price, 0 g'],[(N.pairs-N.pDiet)+' other swaps','grey','smaller food, or grilled']]); },
  hidden(g){},
};
function rlabels(g,rows){ rows.forEach((r,k)=>{ label(g,1000,260+k*70,r[0],true,HEX[r[1]]); label(g,1000,282+k*70,r[2]); }); }
function swapChrome(g){ g.append('text').attr('x',SW.a).attr('y',185).attr('text-anchor','middle').attr('class','big').text('What you order now'); g.append('text').attr('x',SW.b).attr('y',185).attr('text-anchor','middle').attr('class','big').text('The swap');
  g.append('g').attr('class','axis').attr('transform','translate(200,0)').call(d3.axisLeft(ysw).ticks(4).tickFormat(d=>d+' cal')).call(s=>s.select('.domain').remove()); }
function axisX(g,y,t){ g.append('g').attr('class','axis').attr('transform',`translate(0,${y})`).call(d3.axisBottom(sx).ticks(6).tickFormat(d=>d+' g')).call(s=>s.select('.domain').remove()); g.append('text').attr('x',W-M).attr('y',y-12).attr('text-anchor','end').text(t.toUpperCase()+' →'); }
function vline(g,x,y1,y2,t,hard){ g.append('line').attr('class','rule'+(hard?' hard':'')).attr('x1',x).attr('x2',x).attr('y1',y1).attr('y2',y2); g.append('text').attr('x',x+10).attr('y',y1-10).attr('fill',hard?HEX.over:HEX.paper).text(t.toUpperCase()); }
function hline(g,y,x1,x2,t,hard,color){ g.append('line').attr('class','rule'+(hard?' hard':'')).attr('x1',x1).attr('x2',x2).attr('y1',y).attr('y2',y).attr('stroke',color||null); g.append('text').attr('x',x2).attr('y',y-10).attr('text-anchor','end').attr('fill',color||(hard?HEX.over:HEX.paper)).text(t.toUpperCase()); }
function label(g,x,y,t,strong,color){ g.append('text').attr('x',x).attr('y',y).attr('class',strong?'lab':'').attr('fill',color||null).attr('font-weight',strong?500:400).text(t); }
function callout(g,x,y,tx,ty,t1,t2){ g.append('path').attr('class','call').attr('d',`M${x},${y} Q${(x+tx)/2},${ty} ${tx},${ty}`); g.append('text').attr('x',tx).attr('y',ty-16).attr('class','lab').attr('text-anchor',tx>x?'start':'end').text(t1); g.append('text').attr('x',tx).attr('y',ty+2).attr('text-anchor',tx>x?'start':'end').text(t2); }

/* ---------- overlays ---------- */
const cubes=()=>{ const r=d3.randomLcg(3); let s=''; for(let i=0;i<10;i++){const a=i/10*Math.PI*2+r()*.4, d=.22+r()*.16; s+=`<i class="cube" style="left:${50+Math.cos(a)*d*100-5.5}%;top:${50+Math.sin(a)*d*100-5.5}%;transform:rotate(${r()*40-20}deg)"></i>`} return s; };
function moneyChart(){ const rows=[['Big fries→Small',-2.65],['Coke→water',-1.16],['Coke→Zero',0],['+apple',1.30],['+tomatoes',1.35],['+pineapple',1.70],['+gazpacho',2.05]];
  const w=1200,h=620,x0=40,bw=120,gap=36,y0=300,sc=80; let s=`<svg class="money" viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Money lost or gained per order">`;
  s+=`<line x1="${x0}" x2="${w-20}" y1="${y0}" y2="${y0}" stroke="#B9AF9D"/><text x="${x0}" y="${y0-14}" font-family="Azeret Mono,monospace" font-size="12" fill="#F0A63A" letter-spacing="1.5">MORE MONEY ↑</text><text x="${x0}" y="${y0+24}" font-family="Azeret Mono,monospace" font-size="12" fill="#FF4A3C" letter-spacing="1.5">LESS MONEY ↓</text>`;
  rows.forEach((r,i)=>{ const x=x0+90+i*(bw+gap); const v=r[1]; const hh=Math.abs(v)*sc; const col=v<0?'#FF4A3C':v>0?'#F0A63A':'#3DDC97';
    if(v===0){ s+=`<circle cx="${x+bw/2}" cy="${y0}" r="18" fill="none" stroke="${col}" stroke-width="4"/>`; } else { s+=`<rect x="${x}" y="${v>0?y0-hh:y0}" width="${bw}" height="${hh}" rx="8" fill="${col}"/>`; }
    s+=`<text x="${x+bw/2}" y="${v>=0?y0-hh-18:y0+hh+34}" text-anchor="middle" font-family="Fraunces,Georgia,serif" font-weight="900" font-size="40" fill="${col}">${v===0?'€0':(v>0?'+':'−')+'€'+Math.abs(v).toFixed(2)}</text>`;
    s+=`<text x="${x+bw/2}" y="${h-40}" text-anchor="middle" font-family="Archivo,Arial,sans-serif" font-size="16" fill="#F4ECDD">${r[0]}</text>`; });
  s+=`</svg>`; return s; }
const OV={
  cups:()=>`<div class="cups"><div><div class="cup">${cubes()}</div><div class="cap2"><b>Coke</b><span>€3.56 · 42 g · about 10 cubes</span></div></div><div class="eq">=</div><div><div class="cup"><div class="g">0 g</div></div><div class="cap2"><b>Coke Zero</b><span>€3.56 · 0 g · same cup</span></div></div></div>`,
  basket:()=>`<div class="cards four">
    <div class="card"><div class="n">1 · the drink</div><h3>Zero, not Coke</h3><div class="big">−42 g</div><p>sugar gone. Same price. Same cup.</p></div>
    <div class="card"><div class="n">2 · the size</div><h3>Small, not Large</h3><div class="big">−${Math.round(N.smallSave)} g</div><p>sugar gone on a typical drink. Cheaper too.</p></div>
    <div class="card"><div class="n">3 · the chicken</div><h3>Grilled, not crispy</h3><div class="big">−${N.grilledSave[0]}–${N.grilledSave[1]}</div><p>calories gone. Every one of the ${N.pGrilled} chicken dishes.</p></div>
    <div class="card"><div class="n">4 · the extra</div><h3>Add an apple</h3><div class="big">+1 fruit</div><p>€1.30 on Glovo Madrid. Fruit is cheap, it just hides at the bottom of the list.</p></div></div>`,
  money:()=>moneyChart(),
  nudges:()=>`<div class="cards">
    <div class="card"><div class="n">Nudge 1 · meal page</div><h3>Zero right under Coke</h3><div class="ui"><div class="row">○ Coke<span>€3.56</span></div><div class="row new">○ Coke Zero <small>same price · 0 g</small></div><div class="row">○ Fanta Zero</div><small>nothing is picked for you</small></div><table><tr><td>Customer</td><td class="g">−42 g sugar ✓</td></tr><tr><td>McDonald's</td><td>€0 · same sale =</td></tr><tr><td>Glovo</td><td>€0 · same fee =</td></tr></table></div>
    <div class="card"><div class="n">Nudge 2 · home</div><h3>"Reorder with Zero"</h3><div class="ui"><div class="row">Big Mac menu · with Coke<span>€9.30</span></div><div class="row" style="border-color:var(--rule)">Reorder</div><div class="row new">Reorder with Zero <small>same price</small></div></div><table><tr><td>Customer</td><td class="g">−42 g, every reorder ✓</td></tr><tr><td>McDonald's</td><td>€0 =</td></tr><tr><td>Glovo</td><td>€0 · faster reorders =</td></tr></table></div>
    <div class="card"><div class="n">Nudge 3 · basket</div><h3>Fruit before fries</h3><div class="ui"><div class="row">Big Mac menu + Zero<span>€9.30</span></div><div class="row new">Add fruit or veg? <small>apple €1.30 · gazpacho €2.05</small></div><div class="row" style="color:var(--muted)">more sides · fries…</div></div><table><tr><td>Customer</td><td class="g">+1 fruit, only if tapped ✓</td></tr><tr><td>McDonald's</td><td class="a">+€0.91 to €1.44 +</td></tr><tr><td>Glovo</td><td class="a">+€0.39 to €0.62 +</td></tr></table></div></div>`,
  ask:()=>`<div class="ask">
    <div><h4>We ask for one decision</h4><ul><li><b>A four-week test in Madrid.</b> Half of McDonald's orders on Glovo see the three nudges. Half do not.</li><li><b>Nothing pre-picked, same-size buttons, ads say ad.</b> EU Consumer Rights Directive art. 22, Digital Services Act arts. 25 and 26.</li><li><b>Do it before a regulator does.</b> New York already puts a salt icon on menus. California made water the default kids' drink.</li></ul></div>
    <div><h4>We count</h4><ul><li><b>Basket value.</b> Same or bigger, or we stop.</li><li><b>How many pick Zero.</b></li><li><b>How many add fruit or veg.</b></li><li><b>How many come back</b> after "nice pick!"</li></ul></div>
    <div><h4>What this data can't tell us</h4><ul><li><b>It is the US menu.</b> Spain's list is shorter. The pattern is the same.</li><li><b>No sales numbers.</b> A shake nobody orders counts as much as fries. The test fixes that.</li><li><b>The percentages on the scale slide are our guesses.</b> 40 % sugary drink, 2 % switch, 5 % add a side, 30 % commission.</li></ul></div></div>`,
  behind:(arcs)=>`<div class="behind"><svg class="arcline" viewBox="0 0 1000 130" preserveAspectRatio="none" aria-hidden="true"><path d="M20,110 C250,80 380,36 520,28 C600,24 640,46 700,68 C800,100 900,106 980,110" fill="none" stroke="#F0A63A" stroke-width="2"/>${[['SETTING + HOOK',60,110],['RISING ACTION',300,62],['AHA',520,28],['SOLUTION',720,74],['NEXT STEPS',930,110]].map(a=>`<circle cx="${a[1]}" cy="${a[2]}" r="5" fill="#F4ECDD"/><text x="${a[1]}" y="${a[2]-14}" text-anchor="middle" font-family="Azeret Mono,monospace" font-size="11" fill="#B9AF9D" letter-spacing="1.5">${a[0]}</text>`).join('')}</svg>
    <div class="row4">${arcs.map(a=>`<div><div class="k">${a[0]}</div><p>${a[1]}</p></div>`).join('')}</div>
    <div class="books"><b>Gestalt, Session 2</b> figure-ground (dark page, bright dots) · similarity (one colour = one meaning) · common region (the two boxes) · focal point (one thing lit) · proximity (columns) · continuity (one line = one swap) · <b>3-second glance test</b> one idea per slide, text and data on separate slides · <b>Story arc</b> Brent Dykes, Effective Data Storytelling · <b>One mark per item</b> Ben Jones, Learning to See Data · <b>Declutter</b> Cole Nussbaumer Knaflic, Storytelling with Data · <b>Palette</b> Kate Strachnyi, ColorWise · <b>Unit charts</b> Nathan Yau, Visualize This · <b>Delivery</b> Lea Pica, Present Beyond Measure · <b>AI strategy</b> Kavita Ganesan, The Business Case for AI<br>Built with D3.js and AI help (Claude). Ideas, analysis and the Glovo price survey: Group 3.</div></div>`,
};

/* ---------- beats → slides ---------- */
const BEATS = /*BEATS*/;
const S=[]; BEATS.forEach(b=>{ if(b.single){S.push({...b,type:b.single})} else {S.push({...b,type:'text'}); S.push({...b,type:'data'})} });
const STAGES=['Setting + hook','Rising action','Aha','Solution','Next steps'];

/* ---------- render ---------- */
const svg=d3.select('#svg'); const gOrders=svg.append('g').attr('opacity',0); const gDots=svg.append('g'); const gAn=svg.append('g');
const dots=gDots.selectAll('circle').data(items).join('circle').attr('cx',W/2).attr('cy',H/2).attr('r',0).attr('fill','url(#g-sand)');
const op=ordersField();
gOrders.selectAll('circle').data(op).join('circle').attr('cx',d=>d.x).attr('cy',d=>d.y).attr('r',d=>d.k==='zero'?8:d.k==='gold'?6:4.6).attr('fill',d=>`url(#g-${d.k})`).attr('filter',d=>d.k==='zero'||d.k==='gold'?'url(#glow)':null);
gOrders.append('text').attr('x',W/2).attr('y',H-70).attr('text-anchor','middle').attr('class','lab').text('ONE MONTH OF ORDERS · 1 DOT = 1,000 ORDERS');
d3.select('#arc').selectAll('span').data(STAGES).join('span').text(d=>d);

let cur=0, showNotes=false, lastLayout='circle';
function applyLayout(name,dur){ const P=name==='orders'?L('hidden'):L(name);
  dots.transition().duration(dur).delay((d,i)=>reduced?0:(i%41)*8).ease(d3.easeCubicInOut).attr('cx',d=>P[d.i].x).attr('cy',d=>P[d.i].y).attr('r',d=>P[d.i].r).attr('fill',d=>`url(#g-${P[d.i].fill})`).attr('opacity',d=>P[d.i].op).attr('filter',d=>LIT.has(P[d.i].fill)&&P[d.i].op>.5?'url(#glow)':null);
  gOrders.transition().duration(dur).attr('opacity',name==='orders'?1:0);
  gAn.transition().duration(reduced?0:200).attr('opacity',0).on('end',()=>{ gAn.selectAll('*').remove(); (AN[name]||(()=>{}))(gAn); gAn.attr('opacity',0).transition().delay(reduced?0:dur*.75).duration(reduced?0:500).attr('opacity',1); });
  lastLayout=name; }
function render(i){
  cur=Math.max(0,Math.min(S.length-1,i)); const s=S[cur]; const dur=reduced?0:1000;
  const isText=s.type==='text'||s.type==='title'; const isData=s.type==='data'; const isOv=s.type==='ov';
  const stage=document.getElementById('stage'); stage.classList.toggle('dim',isText&&s.type!=='title'||isOv); stage.classList.toggle('half',s.type==='title');
  /* text */
  const t=d3.select('#text'); if(isText){ t.html(`<div class="wrap"><div class="eyebrow">${s.eye}</div><h1>${s.h}</h1>${s.lede?`<p class="lede">${s.lede}</p>`:''}<div class="goto">${s.type==='title'?'→ press right to start':'→ see the data'}</div></div>`); t.classed('on',true);} else t.classed('on',false);
  /* layout */
  if(s.type==='title'){applyLayout(s.layout||'circle',dur)}
  if(isData){ if(s.layout!==lastLayout)applyLayout(s.layout,dur); }
  if(isOv){ if(s.layout&&s.layout!==lastLayout)applyLayout(s.layout,dur); }
  /* captions */
  const on=isData;
  d3.select('#captl').classed('on',on).html(on?`<h2>${s.h}</h2>${s.howto?`<div class="howto">How to read · ${s.howto}</div>`:''}`:'');
  d3.select('#captr').classed('on',on&&s.stat).html(on&&s.stat?`<div class="v ${s.stat[2]||''}">${typeof s.stat[1]==='number'?fmt(s.stat[1]):s.stat[1]}</div><div class="l">${s.stat[0]}</div>`:'');
  d3.select('#capbl').classed('on',on&&s.key&&s.key.length).html(on&&s.key?s.key.map(k=>`<span><i style="background:${HEX[k[0]]};color:${HEX[k[0]]}"></i>${k[1]}</span>`).join(''):'');
  /* overlay */
  const ov=d3.select('#overlay'); if(isOv){ov.html(typeof s.ov==='function'?s.ov():OV[s.ov]()); ov.classed('on',true)} else {ov.classed('on',false); setTimeout(()=>{if(S[cur].type!=='ov')ov.html('')},500)}
  /* chrome */
  d3.select('#count').text(String(cur+1).padStart(2,'0')+' / '+S.length); d3.select('#bar').style('width',((cur+1)/S.length*100)+'%');
  d3.select('#arc').selectAll('span').classed('on',(d,k)=>k===s.stage);
  d3.select('#src').text((isData||isOv)?(s.src||DEFAULT_SRC):'');
  d3.select('#nt').text(s.note||''); d3.select('#nc').text(s.course?'Course link: '+s.course:'');
  try{localStorage.setItem('deck3-'+document.title,cur)}catch(e){}
}
function next(){render(cur+1)} function prev(){render(cur-1)}
addEventListener('keydown',e=>{ if(['ArrowRight','ArrowDown',' ','PageDown'].includes(e.key)){e.preventDefault();next()} else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();prev()} else if(e.key==='Home'){render(0)} else if(e.key==='End'){render(S.length-1)} else if(e.key.toLowerCase()==='n'){toggleNotes()} });
addEventListener('click',e=>{ if(e.target.closest('button,a,#notes'))return; (e.clientX>innerWidth/2)?next():prev(); });
let tx=null; addEventListener('touchstart',e=>{tx=e.touches[0].clientX},{passive:true}); addEventListener('touchend',e=>{ if(tx==null)return; const dx=e.changedTouches[0].clientX-tx; if(Math.abs(dx)>40){dx<0?next():prev()} tx=null; });
function toggleNotes(){ showNotes=!showNotes; document.getElementById('notes').hidden=!showNotes; }
document.getElementById('nbtn').addEventListener('click',e=>{e.stopPropagation();toggleNotes()});
let start=0; try{ const h=location.hash.replace('#s',''); if(h&&!isNaN(h))start=+h-1; else { const v=localStorage.getItem('deck3-'+document.title); if(v!=null)start=+v; } }catch(e){}
render(start);
</script>
'''

BEATS_CUP = r'''[
 {single:'title',stage:0,eye:'For anyone who eats at McDonald\'s · Group 3 · IE IMBA Data Fluency',h:'What\'s in <em>your cup?</em>',lede:'Every dot is one thing on the McDonald\'s menu. 260 of them.',layout:'circle',
  note:'Every dot behind me is one thing on the menu. Two hundred and sixty. Watch them move.',course:'Gestalt: figure-ground. Dark page, bright dots, nothing else. Ben Jones: one mark per item.'},
 {stage:1,eye:'Sugar',h:'<em class="red">62</em> things have a whole day\'s sugar in one go.',lede:'Doctors say about <b>50 g</b> a day. That is 12 sugar cubes.',stat:['things over a day of sugar',N.over50,'red'],key:[['over','more than a day of sugar (50 g)'],['sand','less than that']],howto:'dots move right = more sugar',layout:'swarm',
  note:'Line them up by sugar. The red line is one day of sugar, about twelve cubes. Sixty-two things cross it in one serving.',course:'Gestalt: similarity, red always means "too much sugar". Session 3: red only for the alert.'},
 {stage:2,eye:'The big one',h:'Every red dot is a <em class="red">drink or a dessert.</em>',lede:'The sweetest thing on a plate has <b>32 g</b>.',stat:['red dots in the food box',0,'red'],key:[['over','more than a day of sugar'],['sand','less than that']],howto:'two boxes. red only in the top one',layout:'cupplate',
  note:'(Pause.) Two boxes. Drinks and desserts on top, food below. Every red dot is on top. The sugar is in the cup, not the burger.',course:'Gestalt: common region, the two boxes do the work. Session 7: the aha moment.'},
 {stage:1,eye:'Surprise',h:'Coffee drinks are <em class="amber">sweeter than soda.</em>',lede:`<b>${N.coffee}</b> coffees and teas. They average <b>${Math.round(N.coffeeAvg)} g</b>. Sodas average ${Math.round(N.sodaAvg)}.`,stat:['coffee & tea, average sugar',Math.round(N.coffeeAvg)+' g','sugar'],key:[['sugar','coffee and tea'],['sand','everything else, faded']],howto:'only coffee is lit up',layout:'coffee',
  note:'Guess the sweetest group. Not shakes. Coffee. Ninety-five drinks, forty grams on average. The sweetest one has ninety-nine.',course:'Gestalt: focal point, one thing lit. Session 7: lead with the surprising number.'},
 {stage:1,eye:'Size',h:'Bigger cup, <em class="amber">more sugar.</em>',lede:`Small <b>${Math.round(N.sizeAvg.Small)} g</b>. Medium <b>${Math.round(N.sizeAvg.Medium)} g</b>. Large <b>${Math.round(N.sizeAvg.Large)} g</b>.`,stat:['Large vs Small','+'+Math.round(N.sizeAvg.Large-N.sizeAvg.Small)+' g','sugar'],key:[['over','more than a day of sugar'],['sand','less than that'],['sugar','the average for that size']],howto:'each drink goes to its cup size. up = more sugar',layout:'sizes',
  note:'Same drinks, three cup sizes. Each size up is about ten grams more. The average Large is over a day of sugar on its own.',course:'Gestalt: proximity, three columns read as three groups. Knaflic: one axis, one message.'},
 {stage:1,eye:'Food',h:'Food\'s problem is <em class="blue">salt</em>, not sugar.',lede:`<b>${N.salt48}</b> dishes have half a day of salt or more.`,stat:['dishes with half a day of salt',N.salt48,'blue'],key:[['salt','food with half a day of salt'],['grey','other food'],['sand','drinks and desserts, faded']],howto:'up = more salt. right = more calories',layout:'salt',
  note:'Now the food. Its problem is salt. Forty-eight dishes have half a day of salt. The more calories, the more salt, almost a straight line.',course:'Gestalt: continuity, the dotted line leads the eye. Session 7 Challenger lesson: plain words.'},
 {stage:3,eye:'Easy swaps',h:'Same food. <em class="green">Three easy swaps.</em>',lede:`Small not Large. Grilled not crispy. Zero not Coke. All <b>${N.pairs}</b> are already on the menu.`,stat:['swaps already on the menu',N.pairs],key:[['grey','Small instead of Large'],['sugar','grilled instead of crispy'],['zero','Zero instead of regular']],howto:'left = what you order now. right = the swap. one line = one swap',layout:'swaps',
  note:'Every swap is already on the menu. Left is now, right is the swap. Grey: order the Small. Amber: grilled. Green: Zero, which costs the same.',course:'Gestalt: continuity, each line is one swap. Knaflic: slope chart for before and after.'},
 {stage:4,eye:'Your turn',h:'Your <em class="green">better basket.</em>',lede:'Four small choices. None of them costs more.',layout:'hidden',
  note:'Four choices. Zero not Coke. Small not Large. Grilled not crispy. Add an apple.',course:'Session 7: resolution = what the audience should do.'},
 {single:'ov',stage:4,ov:'basket',layout:'hidden',src:'Sugar and calories: Kaggle US menu · Coke Zero price: Glovo Madrid, 10 Oct 2026 · Coke sugar: Coca-Cola Spain label',
  note:'Same food, less sugar, no extra money. That is the whole message.',course:'Gestalt: similarity, four cards, same shape, same job.'},
 {single:'ov',stage:4,ov:()=>OV.behind([['Characters','Anyone who orders at McDonald\'s'],['Setting','260 things on the menu, one dot each'],['Conflict','The sugar hides in the cup'],['Resolution','Four swaps, no extra cost']]),layout:'hidden',src:'Story arc: Brent Dykes · Gestalt: Session 2 · hero framework: Session 7',
  note:'Hero: the customer. Guide: us. Every chart follows one Gestalt rule. Twenty seconds, then questions.',course:'Session 2 Gestalt, Session 7 hero framework, the seven Book of the Day picks.'},
]'''

BEATS_MONEY = r'''[
 {single:'title',stage:0,eye:'A pitch for the Glovo partnerships team · Group 3 · IE IMBA Data Fluency',h:'Healthy can <em>make money.</em>',lede:'Every dot is one McDonald\'s menu item. 260 of them.',layout:'circle',
  note:'Two hundred and sixty items, one dot each. Three slides from now you will see why healthy and profitable are the same move.',course:'Session 7: setting + hook. Hero = Glovo, guide = us. Gestalt: figure-ground.'},
 {stage:1,eye:'The problem',h:'Most healthy swaps make the order <em class="red">smaller.</em>',lede:`<b>${N.pSmaller}</b> of the ${N.pairs} healthier versions are just "order the Small".`,stat:['swaps that shrink the bill',N.pSmaller,'red'],key:[['grey','Small instead of Large'],['sugar','grilled instead of crispy'],['zero','Zero instead of regular']],howto:'left = ordered now. right = the healthier version',layout:'swaps',
  note:'Sixty-four healthier versions exist today. Forty-three are "order the Small". Healthier means a smaller bill. That is the problem we fix.',course:'Session 7: the conflict. Gestalt: continuity, one line per swap.'},
 {stage:2,eye:'The finding',h:'All the sugar is <em class="red">in the cup.</em>',lede:`All <b>${N.over50}</b> items with a day of sugar are drinks or desserts.`,stat:['over-the-limit items in a cup',N.over50,'red'],key:[['over','more than a day of sugar'],['sand','less than that']],howto:'two boxes. red only in the top one',layout:'cupplate',
  note:'(Pause.) Two boxes. Every item with a day of sugar is in the top one. The fix is in the drink, and the drink is where the free swap lives.',course:'Gestalt: common region. Session 7: the aha moment.'},
 {stage:2,eye:'The free swap',h:'<em class="green">8</em> swaps cost nothing. All of them are drinks.',lede:'Coke to Coke Zero. Same cup, same price, zero sugar.',stat:['free swaps',N.pDiet,'green'],key:[['zero','Zero instead of regular'],['dim','the other swaps, faded']],howto:'only the free swaps are lit up',layout:'swapsDiet',
  note:'Light up the swaps that cost nothing. Eight. All drinks. This is the lever.',course:'Gestalt: focal point, only the green lines lit. Session 3: highlight palette.'},
 {stage:3,eye:'Same price',h:'Same price. <em class="green">No sugar.</em>',lede:'On Glovo Madrid, Coke and Coke Zero both cost <b>€3.56</b>.',layout:'hidden',
  note:'Ten cubes or none. Same price. Nobody loses a cent.',course:'Brent Dykes: the plan the guide hands the hero.'},
 {single:'ov',stage:3,ov:'cups',layout:'hidden',src:'Prices: Glovo Madrid, 10 Oct 2026 · Sugar: Coca-Cola Spain label, medium 40 cl · 1 cube ≈ 4 g',
  note:'One has about ten sugar cubes. The other has none. Same cup.',course:'Gestalt: similarity, two identical cups, one difference.'},
 {stage:3,eye:'Add, don\'t shrink',h:'Add fruit, <em class="amber">make money.</em>',lede:'Smaller loses €1 to €3. Zero is €0. An apple or a gazpacho adds <b>€1.30 to €2.05</b>.',layout:'hidden',
  note:'Red goes down: make it smaller, lose money. Green: Zero, same money. Amber goes up: add fruit, make money.',course:'Gestalt: similarity, red down, amber up. Nathan Yau: read the bar height.'},
 {single:'ov',stage:3,ov:'money',layout:'hidden',src:'Prices: Glovo Madrid McDonald\'s listing, 10 Oct 2026 · per order, before Glovo\'s fee',
  note:'The healthy choices that pay are the add-ons, not the shrinks.',course:'Session 2: never truncate; the axis starts at zero.'},
 {stage:3,eye:'The plan',h:'Three nudges. <em>Nothing pre-picked.</em>',lede:'Zero under Coke. A "Reorder with Zero" button. Fruit before fries.',layout:'hidden',
  note:'Three changes to the order flow. None pre-picks. The customer always chooses.',course:'Session 3: Z-pattern, most important nudge top-left.'},
 {single:'ov',stage:3,ov:'nudges',layout:'hidden',src:'Concept for the McDonald\'s order flow on Glovo · prices Glovo Madrid · Glovo fee assumed 30 %',
  note:'Same sale, same fee, or more, on every one.',course:'EU CRD art. 22, DSA arts. 25–26: never pre-tick, same-size buttons, ads say ad.'},
 {stage:3,eye:'Scale',h:'Only a few need to <em>say yes.</em>',lede:'If <b>2 in 100</b> switch to Zero and 5 in 100 add a side: <b>336 kg</b> less sugar, <b>€45,500</b> more for McDonald\'s, <b>€19,500</b> for Glovo.',stat:['more money for McDonald\'s, per month','€45,500','sugar'],key:[['pink','has a sugary drink'],['zero','picked Zero instead'],['gold','added fruit or veg'],['sand','1 dot = 1,000 orders']],howto:'one dot = 1,000 orders',layout:'orders',src:'OUR GUESSES, NOT DATA: 1,000,000 orders · 40 % include a sugary drink · 2 % of those pick Zero · 5 % add a €1.30 side · 30 % commission · the test replaces these with real numbers',
  note:'These percentages are our guesses. Even so: two in a hundred switch, that is 336 kilos of sugar a month, forty-five thousand euros for McDonald\'s, nineteen for Glovo.',course:'Nathan Yau: unit charts make scale felt. Session 7: say what is assumed, let the pilot replace it.'},
 {stage:4,eye:'Next steps',h:'Try it for <em>four weeks.</em>',lede:'Half of Madrid orders see the nudges. Half don\'t. Then the guesses become numbers.',layout:'hidden',
  note:'One decision: a four-week test in Madrid.',course:'Session 7: resolution = one decision to ask for.'},
 {single:'ov',stage:4,ov:'ask',layout:'hidden',
  note:'Baskets no smaller, more Zero, more fruit. Then the guesses become numbers. Questions.',course:'Session 7: say what the data cannot tell you.'},
 {single:'ov',stage:4,ov:()=>OV.behind([['Characters','Glovo, McDonald\'s, hungry Madrid'],['Setting','260 menu items, one dot each'],['Conflict','Healthy swaps shrink the bill'],['Resolution','Free swap + add-ons, four-week test']]),layout:'hidden',src:'Story arc: Brent Dykes · Gestalt: Session 2 · hero framework: Session 7',
  note:'Hero: Glovo. Guide: us. Every chart follows one Gestalt rule. Twenty seconds, then questions.',course:'Session 2 Gestalt, Session 7 hero framework, the seven Book of the Day picks.'},
]'''

def build(fname, title, accent, beats):
    html = TEMPLATE.replace('/*TITLE*/', title).replace('/*ACCENT*/', accent).replace('/*BEATS*/', beats).replace('/*DATA*/', DATA)
    (HERE / fname).write_text(html); print(fname, len(html), 'bytes')

build('whats-in-your-cup-v3.html', "What's in Your Cup", '#F0A63A', BEATS_CUP)
build('healthy-makes-money-v3.html', 'Healthy Makes Money', '#3DDC97', BEATS_MONEY)
