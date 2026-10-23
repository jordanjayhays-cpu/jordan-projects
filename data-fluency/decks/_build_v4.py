#!/usr/bin/env python3
"""v4: two decks, two themes, scaffolded story (one dot → the menu → sort → split).
   Outputs whats-in-your-cup-v4.html (paper & ink) and healthy-makes-money-v4.html (navy & yellow)."""
import json, pathlib
HERE = pathlib.Path(__file__).parent
DATA = (HERE / 'menu-data.json').read_text()

THEMES = {
 'paper': dict(
   name="What's in Your Cup",
   fonts="family=Archivo+Black&family=Archivo:wght@400;500;600&family=Courier+Prime:wght@400;700",
   display='"Archivo Black","Arial Black",Impact,sans-serif', body='"Archivo","Helvetica Neue",Arial,sans-serif', mono='"Courier Prime","Courier New",monospace',
   bg='#F6F1E7', fg='#161311', fg2='#5E574E', muted='#8E867B', rule='#D9D2C4', accent='#D7262A', scheme='light', glow=0,
   hex=dict(sand='#2A2521',over='#D7262A',sugar='#E08A1E',salt='#2F6DB5',zero='#1F9D55',pink='#E8A0AB',gold='#E08A1E',grey='#B5AD9F',dim='#E3DCCF',paper='#161311',sugary='#E9B9BF',other='#DDD6C8',loss='#D7262A',gain='#E08A1E'),
   overKey='over', italicAccent=0),
 'navy': dict(
   name='Healthy Makes Money',
   fonts="family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,800&family=Manrope:wght@400;500;700&family=JetBrains+Mono:wght@400;600",
   display='"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif', body='"Manrope","Helvetica Neue",Arial,sans-serif', mono='"JetBrains Mono","SFMono-Regular",Menlo,monospace',
   bg='#0E1626', fg='#F2F5FA', fg2='#A9B4C8', muted='#5F6C85', rule='#1F2B42', accent='#FFC244', scheme='dark', glow=1,
   hex=dict(sand='#3B4B6B',over='#FFC244',sugar='#FFC244',salt='#4FA3FF',zero='#3DDC97',pink='#FF8FA3',gold='#FFC244',grey='#6B7A99',dim='#1C2740',paper='#F2F5FA',sugary='#4A3550',other='#222E47',loss='#FF5A4E',gain='#FFC244'),
   overKey='over', italicAccent=0),
}

TEMPLATE = r'''<title>/*TITLE*/</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?/*FONTS*/&display=swap">
<style>
/* Layout: the data is the page. Full-viewport stage of 260 dots; text slides float over it dimmed; data slides give the dots the whole screen with one caption, one number, one how-to-read line. */
:root{ --bg:/*BG*/; --fg:/*FG*/; --fg2:/*FG2*/; --muted:/*MUTED*/; --rule:/*RULE*/; --accent:/*ACCENT*/;
  --over:/*C_OVER*/; --sugar:/*C_SUGAR*/; --zero:/*C_ZERO*/; --loss:/*C_LOSS*/;
  --display:/*DISPLAY*/; --body:/*BODY*/; --mono:/*MONO*/; color-scheme:/*SCHEME*/; }
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--body);font-size:16px;line-height:1.45;overflow:hidden;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0}
.stage{position:fixed;inset:0;transition:opacity .7s ease,filter .7s ease}
.stage.dim{opacity:.16;filter:blur(2px)} .stage.half{opacity:.45}
.stage svg{width:100%;height:100%;display:block}
.bar{position:fixed;top:0;left:0;right:0;height:4px;background:var(--rule);z-index:6}
.bar i{display:block;height:100%;background:var(--accent);width:0;transition:width .5s ease}
.chrome{position:fixed;left:max(24px,env(safe-area-inset-left,0px));right:max(24px,env(safe-area-inset-right,0px));z-index:5;font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--fg2);display:flex;justify-content:space-between;gap:16px;pointer-events:none}
.chrome.top{top:calc(16px + env(safe-area-inset-top,0px))}
.chrome.bottom{bottom:calc(14px + env(safe-area-inset-bottom,0px));align-items:flex-end}
.chrome .brand{color:var(--fg);font-weight:700}
.arc{display:flex;gap:14px}
.arc span{position:relative;padding-left:12px}
.arc span::before{content:"";position:absolute;left:0;top:50%;width:6px;height:6px;border-radius:50%;background:var(--rule);transform:translateY(-50%)}
.arc span.on{color:var(--fg)} .arc span.on::before{background:var(--accent)}
.src{max-width:46vw;line-height:1.5;color:var(--muted);text-align:right;font-size:11px}
button.notes{pointer-events:auto;font:inherit;font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;background:var(--bg);border:1px solid var(--rule);color:var(--fg2);padding:5px 10px;border-radius:3px;cursor:pointer}
button.notes:active{transform:scale(.97)}
/* text slide */
.text{position:fixed;inset:0;display:grid;place-items:center;padding:8vh 6vw;z-index:3;pointer-events:none;opacity:0;transform:translateY(16px);transition:opacity .45s cubic-bezier(.2,.8,.2,1),transform .55s cubic-bezier(.2,.9,.1,1)}
.text.on{opacity:1;transform:none;pointer-events:auto}
.text .wrap{max-width:1180px;width:100%;display:grid;gap:clamp(14px,2.4vh,28px)}
.eyebrow{font-family:var(--mono);font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
h1{font-family:var(--display);font-weight:800;font-size:clamp(42px,7.6vw,116px);line-height:.98;margin:0;letter-spacing:-.02em;text-wrap:balance}
h1 em{font-style:normal;color:var(--accent)}
h1 em.red{color:var(--over)} h1 em.green{color:var(--zero)} h1 em.amber{color:var(--sugar)}
.lede{font-family:var(--body);font-weight:400;font-size:clamp(19px,2.2vw,30px);line-height:1.35;color:var(--fg2);max-width:36ch;margin:0}
.lede b{color:var(--fg);font-weight:700}
.goto{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
/* data captions */
.cap{position:fixed;z-index:4;pointer-events:none;opacity:0;transition:opacity .5s .3s}
.cap.on{opacity:1}
.cap.tl{top:calc(48px + env(safe-area-inset-top,0px));left:max(24px,env(safe-area-inset-left,0px));max-width:min(48vw,640px)}
.cap.tl h2{font-family:var(--display);font-weight:800;font-size:clamp(22px,2.5vw,36px);line-height:1.05;margin:0;letter-spacing:-.015em;text-wrap:balance}
.cap.tl h2 em{font-style:normal;color:var(--accent)} .cap.tl h2 em.red{color:var(--over)} .cap.tl h2 em.green{color:var(--zero)} .cap.tl h2 em.amber{color:var(--sugar)}
.cap.tl .howto{margin-top:10px;font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--fg);background:var(--bg);border-left:3px solid var(--accent);padding:6px 10px;display:inline-block}
.cap.tr{top:calc(44px + env(safe-area-inset-top,0px));right:max(24px,env(safe-area-inset-right,0px));text-align:right}
.cap.tr .v{font-family:var(--display);font-weight:800;font-size:clamp(48px,7vw,112px);line-height:.9;letter-spacing:-.03em;font-variant-numeric:tabular-nums;color:var(--fg)}
.cap.tr .v.sugar{color:var(--sugar)} .cap.tr .v.red{color:var(--over)} .cap.tr .v.green{color:var(--zero)}
.cap.tr .l{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--fg2);margin-top:6px}
.cap.bl{bottom:calc(48px + env(safe-area-inset-bottom,0px));left:max(24px,env(safe-area-inset-left,0px));display:grid;gap:6px;font-family:var(--mono);font-size:12px;letter-spacing:.04em;color:var(--fg2)}
.cap.bl span{display:flex;align-items:center;gap:10px}
.cap.bl i{width:11px;height:11px;border-radius:50%;display:inline-block;flex:none}
/* svg */
svg text{font-family:var(--mono);font-size:13.5px;fill:var(--fg2);letter-spacing:.03em}
svg text.big{font-family:var(--display);font-weight:800;font-size:34px;fill:var(--fg);letter-spacing:-.01em}
svg text.lab{fill:var(--fg);font-weight:700}
svg text.axt{font-family:var(--display);font-weight:800;font-size:19px;fill:var(--fg);letter-spacing:.01em}
svg .axl{stroke:var(--fg);stroke-width:1.5}
svg .axis line,svg .axis path{stroke:var(--rule)}
svg .rule{stroke:var(--fg2);stroke-dasharray:4 5;stroke-width:1}
svg .rule.hard{stroke:var(--over);stroke-dasharray:none;stroke-width:2}
svg .call{stroke:var(--fg2);fill:none;stroke-width:1}
svg .region{fill:var(--bg);stroke:var(--rule);stroke-width:1.5;rx:18}
svg .cube{fill:var(--fg);stroke:var(--bg);stroke-width:1.5;rx:3}
/* overlays */
.overlay{position:fixed;inset:0;z-index:4;display:grid;place-items:center;padding:clamp(70px,11vh,110px) 5vw;opacity:0;pointer-events:none;transition:opacity .5s}
.overlay.on{opacity:1;pointer-events:auto}
.overlay > *{width:100%;max-width:1400px;min-width:0}
.cups{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:40px;justify-items:center}
.cup{width:min(50vmin,420px);aspect-ratio:1;border-radius:50%;background:#2A1E16;border:4px solid var(--rule);position:relative;display:grid;place-items:center;box-shadow:0 30px 80px rgba(0,0,0,.25)}
.cup .g{font-family:var(--display);font-weight:800;font-size:clamp(56px,10vmin,120px);color:var(--zero)}
.cup .cube{position:absolute;width:11%;height:11%;background:#F6F1E7;border-radius:12%;box-shadow:inset -3px -3px 0 rgba(0,0,0,.15),0 4px 10px rgba(0,0,0,.4)}
.cups .eq{font-family:var(--display);font-weight:800;font-size:90px;color:var(--accent)}
.cups .cap2{display:grid;justify-items:center;gap:6px;margin-top:18px;text-align:center}
.cups .cap2 b{font-family:var(--display);font-weight:800;font-size:34px}
.cups .cap2 span{font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--fg2)}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.cards.four{grid-template-columns:repeat(4,minmax(0,1fr))}
.card{border:1.5px solid var(--rule);border-radius:8px;padding:26px;display:grid;gap:14px;background:var(--bg);align-content:start}
.card .n{font-family:var(--mono);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
.card h3{font-family:var(--display);font-weight:800;font-size:clamp(24px,2.4vw,34px);line-height:1.05;margin:0;letter-spacing:-.015em}
.card .big{font-family:var(--display);font-weight:800;font-size:clamp(44px,5vw,72px);line-height:1;color:var(--zero);letter-spacing:-.03em}
.card p{margin:0;color:var(--fg2);font-size:16px}
.card .ui{border:1.5px solid var(--rule);border-radius:12px;padding:12px 14px;font-size:14px;display:grid;gap:8px}
.card .ui .row{display:flex;justify-content:space-between;gap:8px;padding:8px 10px;border-radius:8px;border:1.5px solid transparent}
.card .ui .row.new{border-color:var(--zero);color:var(--zero)}
.card .ui small{color:var(--fg2);font-family:var(--mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase}
.card table{width:100%;border-collapse:collapse;font-size:14px}
.card td{padding:6px 0;border-top:1px solid var(--rule)}
.card td:last-child{text-align:right;font-family:var(--mono);font-size:12.5px;white-space:nowrap}
.card td.g{color:var(--zero)} .card td.a{color:var(--sugar)}
.ask{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px}
.ask > div{background:var(--bg);border:1.5px solid var(--rule);border-radius:8px;padding:26px}
.ask h4{font-family:var(--mono);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0 0 14px;border-bottom:1px solid var(--rule);padding-bottom:10px}
.ask ul{margin:0;padding:0;list-style:none;display:grid;gap:12px;font-size:16px;color:var(--fg2)}
.ask li b{color:var(--fg);font-weight:700}
.money{width:100%;height:min(70vh,760px)}
.behind{display:grid;gap:28px;background:var(--bg);border:1.5px solid var(--rule);border-radius:8px;padding:30px}
.behind .arcline{height:130px;width:100%}
.behind .row4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px}
.behind .row4 div{border-top:1px solid var(--rule);padding-top:10px}
.behind .row4 .k{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
.behind .row4 p{margin:6px 0 0;font-family:var(--display);font-weight:800;font-size:24px;line-height:1.08;letter-spacing:-.01em}
.behind .books{font-family:var(--mono);font-size:12px;letter-spacing:.02em;color:var(--fg2);line-height:1.9}
.behind .books b{color:var(--fg);font-weight:700}
#notes[hidden]{display:none}
#notes{position:fixed;left:max(16px,env(safe-area-inset-left,0px));right:max(16px,env(safe-area-inset-right,0px));bottom:calc(56px + env(safe-area-inset-bottom,0px));margin:0 auto;max-width:900px;background:var(--bg);border:2px solid var(--accent);border-radius:6px;padding:16px 20px;z-index:8;display:grid;gap:8px;font-size:15px;box-shadow:0 20px 60px rgba(0,0,0,.3)}
#notes .k{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
#notes .course{color:var(--fg2);font-size:13.5px}
@media (max-width:900px){
  h1{font-size:38px} .lede{font-size:18px}
  .cap.tl{max-width:70vw} .cap.tr .v{font-size:44px} .cap.bl{display:none} .src{display:none} .arc{display:none}
  .cards,.cards.four,.ask,.behind .row4{grid-template-columns:1fr}
  .cups{grid-template-columns:1fr} .cups .eq{display:none} .cup{width:40vmin}
  .overlay{overflow:auto;place-items:start;padding-top:70px}
}
@media (prefers-reduced-motion:reduce){ *{transition:none!important} }
</style>

<div class="bar"><i id="bar"></i></div>
<div class="stage" id="stage"><svg id="svg" viewBox="0 0 1280 720" preserveAspectRatio="xMidYMid slice" role="img" aria-label="260 menu items as dots">
  <defs id="defs"><filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
</svg></div>
<div class="text" id="text"></div>
<div class="cap tl" id="captl"></div><div class="cap tr" id="captr"></div><div class="cap bl" id="capbl"></div>
<div class="overlay" id="overlay"></div>
<div class="chrome top"><span class="brand">/*TITLE*/</span><span id="count">01</span></div>
<div class="chrome bottom"><div class="arc" id="arc"></div><div class="src" id="src"></div><div><button class="notes" id="nbtn" type="button">Notes · N</button></div></div>
<div id="notes" hidden><div class="k">Speaker</div><div id="nt"></div><div class="course" id="nc"></div></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script>
const DATA = /*DATA*/;
const T = /*THEME*/;
const HEX=T.hex; const GLOW=!!T.glow;
const DEFAULT_SRC = "Data: Nutrition Facts for McDonald's Menu (Kaggle, US, 260 items) · 1 cube = 4 g of sugar · US menu used as a stand-in for Madrid";
const CUP = new Set(['Beverages','Coffee & Tea','Smoothies & Shakes','Desserts']);
const W=1280,H=720,M=120;
const LIT=new Set(['sugar','over','salt','zero','pink','gold']);
const rScale=d3.scaleSqrt().domain([0,1900]).range([2.8,13]);
const items=DATA.map((d,i)=>({...d,i,cup:CUP.has(d.cat),r:rScale(d.cal)}));
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const fmt=d3.format(',');
const defs=d3.select('#defs');
Object.entries(HEX).forEach(([k,c])=>{ const g=defs.append('radialGradient').attr('id','g-'+k).attr('cx','38%').attr('cy','35%').attr('r','70%');
  g.append('stop').attr('offset','0%').attr('stop-color',GLOW?d3.color(c).brighter(.9):d3.color(c).brighter(.35)); g.append('stop').attr('offset','100%').attr('stop-color',c); });

/* ---------- numbers ---------- */
const N={};
N.total=items.length; N.over50=items.filter(d=>d.sugar>50).length; N.zero=items.filter(d=>d.sugar===0).length;
N.cup=items.filter(d=>d.cup).length; N.plate=N.total-N.cup; N.plateMax=d3.max(items.filter(d=>!d.cup),d=>d.sugar);
N.maxItem=items.reduce((a,b)=>b.sugar>a.sugar?b:a);
const catAvg=c=>d3.mean(items.filter(d=>d.cat===c),d=>d.sugar);
N.coffee=items.filter(d=>d.cat==='Coffee & Tea').length; N.coffeeAvg=catAvg('Coffee & Tea'); N.sodaAvg=catAvg('Beverages');
N.coffeeMax=items.filter(d=>d.cat==='Coffee & Tea').reduce((a,b)=>b.sugar>a.sugar?b:a);
items.forEach(d=>{const m=d.item.match(/\((Small|Medium|Large)\)$/);d.size=m?m[1]:null});
N.sized=items.filter(d=>d.size).length; N.sizeAvg={}; ['Small','Medium','Large'].forEach(s=>N.sizeAvg[s]=d3.mean(items.filter(d=>d.size===s),d=>d.sugar));
const byName=new Map(items.map(d=>[d.item,d])); const pairs=[];
items.forEach(d=>{ if(/\(Large\)$/.test(d.item)){const s=byName.get(d.item.replace('(Large)','(Small)')); if(s)pairs.push({a:d,b:s,t:'smaller'})}});
items.forEach(d=>{ if(/Crispy/.test(d.item)){const g=byName.get(d.item.replace('Crispy','Grilled')); if(g)pairs.push({a:d,b:g,t:'grilled'})}});
items.forEach(d=>{ if(/^Diet /.test(d.item)){const r=byName.get(d.item.replace(/^Diet Coke/,'Coca-Cola Classic').replace(/^Diet /,'')); if(r)pairs.push({a:r,b:d,t:'diet'})}});
N.pairs=pairs.length; N.pSmaller=pairs.filter(p=>p.t==='smaller').length; N.pGrilled=pairs.filter(p=>p.t==='grilled').length; N.pDiet=pairs.filter(p=>p.t==='diet').length;
N.grilledSave=d3.extent(pairs.filter(p=>p.t==='grilled'),p=>p.a.cal-p.b.cal); N.smallSave=d3.median(pairs.filter(p=>p.t==='smaller'),p=>p.a.sugar-p.b.sugar);
N.coke=byName.get('Coca-Cola Classic (Medium)'); N.cokeCubes=Math.round(N.coke.sugar/4);
N.onePair=pairs.find(p=>p.a.item==='Coca-Cola Classic (Large)');
const cubesOf=g=>Math.round(g/4);

/* ---------- layouts ---------- */
const sx=d3.scaleLinear().domain([0,130]).range([M,W-M]);
const ysw=d3.scaleLinear().domain([0,900]).range([570,215]); const SW={a:430,b:850};
const SZ={Small:330,Medium:640,Large:950}; const sySize=d3.scaleLinear().domain([0,130]).range([570,200]);
function base(){return items.map(d=>({x:W/2,y:H/2,r:d.r,fill:'sand',op:1}))}
function swarm(nodesIn,xs,ys,sxv=1,syv=0.1){ const nodes=nodesIn.map(d=>({i:d.i,x:xs(d),y:ys(d),r:d.r}));
  const sim=d3.forceSimulation(nodes).force('x',d3.forceX(n=>xs(items[n.i])).strength(sxv)).force('y',d3.forceY(n=>ys(items[n.i])).strength(syv)).force('c',d3.forceCollide(n=>n.r+1.6).iterations(3)).stop();
  for(let k=0;k<220;k++)sim.tick(); return nodes; }
const cache={}; function L(name){ if(cache[name])return cache[name]; const p=LAYOUTS[name](); cache[name]=p; return p; }
const sugarFill=d=>d.sugar>50?T.overKey:'sand';
const swapCol={smaller:'grey',grilled:'sugar',diet:'zero'};
const LAYOUTS={
  one(){ const p=base().map(o=>({...o,op:0,r:0})); p[N.coke.i]={x:W/2-140,y:H/2+10,r:34,fill:'sand',op:1}; return p; },
  circle(){ const p=base(); const nodes=items.map((d,i)=>{const t=i*2.39996,r=21*Math.sqrt(i);return {i,x:W/2+r*Math.cos(t),y:H/2+r*Math.sin(t),r:d.r}});
    const sim=d3.forceSimulation(nodes).force('c',d3.forceCollide(n=>n.r+2)).force('x',d3.forceX(W/2).strength(.02)).force('y',d3.forceY(H/2).strength(.02)).stop(); for(let k=0;k<120;k++)sim.tick();
    nodes.forEach(n=>{p[n.i].x=n.x;p[n.i].y=n.y}); return p; },
  swarmPlain(){ const p=base(); swarm(items,d=>sx(d.sugar),()=>385).forEach(n=>{p[n.i].x=n.x;p[n.i].y=n.y}); return p; },
  swarm(){ return L('swarmPlain').map((o,i)=>({...o,fill:sugarFill(items[i])})); },
  cupplate(){ const p=base().map(o=>({...o,r:o.r*.8})); swarm(items.map(d=>({...d,r:d.r*.8})),d=>sx(d.sugar),d=>d.cup?258:482).forEach(n=>{p[n.i].x=n.x;p[n.i].y=n.y;p[n.i].fill=sugarFill(items[n.i])}); return p; },
  coffee(){ const p=L('cupplate').map(o=>({...o})); items.forEach(d=>{const q=p[d.i]; if(d.cat==='Coffee & Tea'){q.fill='sugar';q.op=1}else{q.fill='sand';q.op=d.cup?.4:.18}}); return p; },
  sizes(){ const p=L('coffee').map(o=>({...o,fill:'sand',op:0,r:0}));
    swarm(items.filter(d=>d.size),d=>SZ[d.size],d=>sySize(d.sugar),.12,1).forEach(n=>{const d=items[n.i];p[n.i]={x:n.x,y:n.y,r:d.r,fill:d.sugar>50?T.overKey:'sand',op:1}}); return p; },
  swaps(){ const p=L('sizes').map(o=>({...o,op:0,r:0})); const seen=new Set();
    pairs.forEach(pr=>{ if(!seen.has(pr.a.i)){p[pr.a.i]={x:SW.a,y:ysw(pr.a.cal),r:pr.a.r,fill:swapCol[pr.t],op:1};seen.add(pr.a.i)} if(!seen.has(pr.b.i)){p[pr.b.i]={x:SW.b,y:ysw(pr.b.cal),r:pr.b.r,fill:swapCol[pr.t],op:1};seen.add(pr.b.i)} }); return p; },
  swapsOne(){ const p=L('swaps').map(o=>({...o,op:0,r:0})); const pr=N.onePair; p[pr.a.i]={...L('swaps')[pr.a.i],r:16,fill:'sand',op:1}; p[pr.b.i]={...L('swaps')[pr.b.i],r:11,fill:'zero',op:1}; return p; },
  swapsSmaller(){ const p=L('swaps').map(o=>({...o})); const idx=new Set(pairs.filter(pr=>pr.t==='smaller').flatMap(pr=>[pr.a.i,pr.b.i]));
    items.forEach(d=>{ if(p[d.i].op>0){ if(idx.has(d.i)){p[d.i].fill='loss';p[d.i].op=1}else{p[d.i].fill='dim';p[d.i].op=.7} } }); return p; },
  swapsDiet(){ const p=L('swaps').map(o=>({...o})); const idx=new Set(pairs.filter(pr=>pr.t==='diet').flatMap(pr=>[pr.a.i,pr.b.i]));
    items.forEach(d=>{ if(p[d.i].op>0){ if(idx.has(d.i)){p[d.i].fill='zero';p[d.i].op=1}else{p[d.i].fill='dim';p[d.i].op=.7} } }); return p; },
  hidden(){ return L('swaps').map(o=>({...o,op:0,r:0})); },
};
function ordersField(){ const n=1000, pts=[]; for(let i=0;i<n;i++){const t=i*2.39996,r=8.6*Math.sqrt(i);pts.push({x:W/2+r*Math.cos(t),y:H/2+10+r*Math.sin(t),k:i<8?'zero':i<58?'gold':i<458?'sugary':'other'})}
  const rnd=d3.randomLcg(7); for(let i=pts.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[pts[i].k,pts[j].k]=[pts[j].k,pts[i].k]} return pts; }

/* ---------- annotations ---------- */
function cubesRow(g,x,y,n,size=16,gap=5,perRow=7){ for(let k=0;k<n;k++){ const cx=x+(k%perRow)*(size+gap), cy=y+Math.floor(k/perRow)*(size+gap); g.append('rect').attr('class','cube').attr('x',cx).attr('y',cy).attr('width',size).attr('height',size); } }
const AN={
  one(g){ const x=W/2-140,y=H/2+10; label(g,x+70,y-60,N.coke.item,true); label(g,x+70,y-38,N.coke.cal+' calories · the dot is sized by calories');
    label(g,x+70,y+2,N.coke.sugar+' g of sugar = '+N.cokeCubes+' sugar cubes',true); cubesRow(g,x+70,y+14,N.cokeCubes,18,6,7);
    g.append('line').attr('x1',x+36).attr('x2',x+62).attr('y1',y).attr('y2',y).attr('stroke',HEX.paper).attr('stroke-opacity',.5); },
  circle(g){},
  swarmPlain(g){ axisCubes(g,600,true); vline(g,sx(50),200,585,'A whole day of sugar: 12 cubes',true); },
  swarm(g){ axisCubes(g,600,true); vline(g,sx(50),200,585,'A whole day of sugar: 12 cubes',true); },
  cupplate(g){ gBack.append('rect').attr('class','region').attr('x',M-30).attr('y',150).attr('width',W-2*M+60).attr('height',210); gBack.append('rect').attr('class','region').attr('x',M-30).attr('y',372).attr('width',W-2*M+60).attr('height',218);
    axisCubes(g,600,false); vline(g,sx(50),150,590,'A whole day of sugar: 12 cubes',true);
    label(g,M-10,176,'IN A CUP',true); label(g,M-10,196,N.cup+' things you drink or eat with a spoon');
    g.append('text').attr('x',W-M+20).attr('y',398).attr('text-anchor','end').attr('class','lab').text('ON A PLATE'); g.append('text').attr('x',W-M+20).attr('y',418).attr('text-anchor','end').text(N.plate+' things you eat with your hands');
    const mx=L('cupplate')[N.maxItem.i]; callout(g,mx.x,mx.y,mx.x-150,mx.y-66,N.maxItem.item.replace(' Candies',''),cubesOf(N.maxItem.sugar)+' cubes · two and a half days');
    const pm=items.filter(d=>!d.cup).reduce((a,b)=>b.sugar>a.sugar?b:a); const pp=L('cupplate')[pm.i]; callout(g,pp.x,pp.y,pp.x+90,pp.y+76,'Sweetest thing on a plate',cubesOf(pm.sugar)+' cubes · '+pm.item); },
  coffee(g){ axisCubes(g,600,false); vline(g,sx(50),158,578,'A whole day of sugar: 12 cubes',true);
    label(g,M-10,183,'COFFEE AND TEA · '+N.coffee+' DRINKS',true,HEX.sugar); label(g,M-10,203,'average '+cubesOf(N.coffeeAvg)+' cubes · sodas average '+cubesOf(N.sodaAvg)+' cubes');
    const cm=L('coffee')[N.coffeeMax.i]; callout(g,cm.x,cm.y,cm.x-130,cm.y-74,N.coffeeMax.item,cubesOf(N.coffeeMax.sugar)+' cubes'); },
  sizes(g){ g.append('g').attr('class','axis').attr('transform','translate(205,0)').call(d3.axisLeft(sySize).tickValues([0,20,40,60,80,100,120]).tickFormat(d=>d/4+' cubes')).call(s=>s.select('.domain').attr('class','axl'));
    g.append('text').attr('class','axt').attr('transform',`translate(100,${(570+200)/2}) rotate(-90)`).attr('text-anchor','middle').text('SUGAR PER DRINK, IN CUBES ↑');
    g.append('line').attr('class','axl').attr('x1',205).attr('x2',W-M).attr('y1',570).attr('y2',570); g.append('text').attr('class','axt').attr('x',(205+W-M)/2).attr('y',676).attr('text-anchor','middle').text('CUP SIZE →');
    g.append('line').attr('class','rule hard').attr('x1',205).attr('x2',W-M).attr('y1',sySize(50)).attr('y2',sySize(50)); g.append('text').attr('x',W-M).attr('y',sySize(50)+22).attr('text-anchor','end').attr('fill',HEX.over).attr('font-weight',700).text('12 CUBES = A DAY');
    ['Small','Medium','Large'].forEach(s=>{ const a=N.sizeAvg[s]; g.append('line').attr('x1',SZ[s]-120).attr('x2',SZ[s]+120).attr('y1',sySize(a)).attr('y2',sySize(a)).attr('stroke',HEX.sugar).attr('stroke-width',3);
      g.append('text').attr('x',SZ[s]).attr('y',620).attr('text-anchor','middle').attr('class','big').text(s); g.append('text').attr('x',SZ[s]+128).attr('y',sySize(a)+4).attr('fill',HEX.sugar).text('average '+cubesOf(a)+' cubes'); }); },
  swapsOne(g){ const pr=N.onePair; const ya=ysw(pr.a.cal), yb=ysw(pr.b.cal);
    g.append('line').attr('x1',SW.a).attr('y1',ya).attr('x2',SW.b).attr('y2',yb).attr('stroke',HEX.zero).attr('stroke-width',3);
    swapChrome(g); callout(g,SW.a,ya,SW.a-60,ya-90,pr.a.item,pr.a.cal+' cal · '+cubesOf(pr.a.sugar)+' cubes'); callout(g,SW.b,yb,SW.b+60,yb+90,pr.b.item,pr.b.cal+' cal · '+cubesOf(pr.b.sugar)+' cubes');
    label(g,1000,330,'One line = one swap',true); label(g,1000,352,'left: what you order now'); label(g,1000,372,'right: the same thing, healthier'); label(g,1000,392,'lower = fewer calories'); },
  swaps(g){ pairs.forEach(pr=>g.append('line').attr('x1',SW.a).attr('y1',ysw(pr.a.cal)).attr('x2',SW.b).attr('y2',ysw(pr.b.cal)).attr('stroke',HEX[swapCol[pr.t]]).attr('stroke-opacity',pr.t==='smaller'?.45:.9).attr('stroke-width',pr.t==='smaller'?1:1.8));
    swapChrome(g); rlabels(g,[[N.pSmaller+' × Small instead of Large','grey',cubesOf(N.smallSave)+' cubes less · cheaper'],[N.pGrilled+' × grilled, not crispy','sugar',N.grilledSave[0]+' to '+N.grilledSave[1]+' fewer calories'],[N.pDiet+' × Zero, not regular','zero','same cup, same price, 0 cubes']]); },
  swapsSmaller(g){ pairs.forEach(pr=>g.append('line').attr('x1',SW.a).attr('y1',ysw(pr.a.cal)).attr('x2',SW.b).attr('y2',ysw(pr.b.cal)).attr('stroke',pr.t==='smaller'?HEX.loss:HEX.dim).attr('stroke-opacity',pr.t==='smaller'?.8:.7).attr('stroke-width',pr.t==='smaller'?1.4:1));
    swapChrome(g); rlabels(g,[[N.pSmaller+' × a Large and its Small','loss','smaller cup · smaller bill'],[(N.pairs-N.pSmaller)+' other swaps','grey','faded for now']]); },
  swapsDiet(g){ pairs.forEach(pr=>g.append('line').attr('x1',SW.a).attr('y1',ysw(pr.a.cal)).attr('x2',SW.b).attr('y2',ysw(pr.b.cal)).attr('stroke',pr.t==='diet'?HEX.zero:HEX.dim).attr('stroke-opacity',pr.t==='diet'?.95:.7).attr('stroke-width',pr.t==='diet'?2.4:1));
    swapChrome(g); rlabels(g,[[N.pDiet+' × Zero, not regular','zero','same cup, same price, 0 cubes'],[(N.pairs-N.pDiet)+' other swaps','grey','smaller food, or grilled']]); },
  hidden(g){},
};
function rlabels(g,rows){ rows.forEach((r,k)=>{ label(g,1000,260+k*70,r[0],true,HEX[r[1]]); label(g,1000,282+k*70,r[2]); }); }
function swapChrome(g){ g.append('text').attr('x',SW.a).attr('y',185).attr('text-anchor','middle').attr('class','big').text('What you order now'); g.append('text').attr('x',SW.b).attr('y',185).attr('text-anchor','middle').attr('class','big').text('The healthier twin');
  g.append('g').attr('class','axis').attr('transform','translate(230,0)').call(d3.axisLeft(ysw).ticks(5).tickFormat(d=>d+' cal')).call(s=>s.select('.domain').attr('class','axl'));
  g.append('text').attr('class','axt').attr('transform',`translate(150,${(570+215)/2}) rotate(-90)`).attr('text-anchor','middle').text('CALORIES PER ITEM ↑');
  g.append('line').attr('class','axl').attr('x1',230).attr('x2',1000).attr('y1',570).attr('y2',570); g.append('text').attr('class','axt').attr('x',(SW.a+SW.b)/2).attr('y',620).attr('text-anchor','middle').text('← THE SAME ITEM, TWO VERSIONS →'); }
function axisCubes(g,y,noteY){ g.append('g').attr('class','axis').attr('transform',`translate(0,${y})`).call(d3.axisBottom(sx).tickValues([0,20,40,60,80,100,120]).tickFormat(d=>d/4+' cubes')).call(s=>s.select('.domain').attr('class','axl'));
  g.append('text').attr('class','axt').attr('x',W-M).attr('y',y+66).attr('text-anchor','end').text('SUGAR PER SERVING, IN SUGAR CUBES →');
  if(noteY){ g.append('text').attr('x',M).attr('y',215).text('↕ UP AND DOWN MEANS NOTHING. DOTS JUST SPREAD OUT SO YOU CAN SEE EACH ONE'); } }
function vline(g,x,y1,y2,t,hard){ g.append('line').attr('class','rule'+(hard?' hard':'')).attr('x1',x).attr('x2',x).attr('y1',y1).attr('y2',y2); g.append('text').attr('x',x+10).attr('y',y1-10).attr('fill',hard?HEX.over:HEX.paper).attr('font-weight',700).text(t.toUpperCase()); }
function hline(g,y,x1,x2,t,hard,color){ g.append('line').attr('class','rule'+(hard?' hard':'')).attr('x1',x1).attr('x2',x2).attr('y1',y).attr('y2',y).attr('stroke',color||null); g.append('text').attr('x',x2).attr('y',y-10).attr('text-anchor','end').attr('fill',color||(hard?HEX.over:HEX.paper)).attr('font-weight',700).text(t.toUpperCase()); }
function label(g,x,y,t,strong,color){ g.append('text').attr('x',x).attr('y',y).attr('class',strong?'lab':'').attr('fill',color||null).text(t); }
function callout(g,x,y,tx,ty,t1,t2){ g.append('path').attr('class','call').attr('d',`M${x},${y} Q${(x+tx)/2},${ty} ${tx},${ty}`); g.append('text').attr('x',tx).attr('y',ty-16).attr('class','lab').attr('text-anchor',tx>x?'start':'end').text(t1); g.append('text').attr('x',tx).attr('y',ty+2).attr('text-anchor',tx>x?'start':'end').text(t2); }

/* ---------- overlays ---------- */
const cubes=()=>{ const r=d3.randomLcg(3); let s=''; for(let i=0;i<10;i++){const a=i/10*Math.PI*2+r()*.4, d=.22+r()*.16; s+=`<i class="cube" style="left:${50+Math.cos(a)*d*100-5.5}%;top:${50+Math.sin(a)*d*100-5.5}%;transform:rotate(${r()*40-20}deg)"></i>`} return s; };
function moneyChart(){ const rows=[['Big fries→Small',-2.65],['Coke→water',-1.16],['Coke→Zero',0],['+apple',1.30],['+tomatoes',1.35],['+pineapple',1.70],['+gazpacho',2.05]];
  const w=1240,h=620,x0=40,bw=100,gap=22,y0=300,sc=80; let s=`<svg class="money" viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Money lost or gained per order">`;
  s+=`<line x1="${x0}" x2="${w-20}" y1="${y0}" y2="${y0}" stroke="${HEX.paper}" stroke-width="1.5"/><text transform="translate(18,${y0}) rotate(-90)" text-anchor="middle" font-family="${T.display}" font-weight="800" font-size="18" fill="${HEX.paper}">€ PER ORDER, FOR MCDONALD'S</text><text x="${w/2}" y="${h-6}" text-anchor="middle" font-family="${T.display}" font-weight="800" font-size="18" fill="${HEX.paper}">THE CHANGE TO THE ORDER →</text><text x="${x0}" y="${y0-14}" font-family="${T.mono}" font-size="12" fill="${HEX.gain}" letter-spacing="1.5">MCDONALD'S MAKES MORE ↑</text><text x="${x0}" y="${y0+24}" font-family="${T.mono}" font-size="12" fill="${HEX.loss}" letter-spacing="1.5">MCDONALD'S MAKES LESS ↓</text>`;
  rows.forEach((r,i)=>{ const x=x0+330+i*(bw+gap); const v=r[1]; const hh=Math.abs(v)*sc; const col=v<0?HEX.loss:v>0?HEX.gain:HEX.zero;
    if(v===0){ s+=`<circle cx="${x+bw/2}" cy="${y0}" r="18" fill="none" stroke="${col}" stroke-width="4"/>`; } else { s+=`<rect x="${x}" y="${v>0?y0-hh:y0}" width="${bw}" height="${hh}" rx="8" fill="${col}"/>`; }
    s+=`<text x="${x+bw/2}" y="${v>=0?y0-hh-18:y0+hh+34}" text-anchor="middle" font-family="${T.display}" font-weight="800" font-size="38" fill="${col}">${v===0?'€0':(v>0?'+':'−')+'€'+Math.abs(v).toFixed(2)}</text>`;
    s+=`<text x="${x+bw/2}" y="${h-52}" text-anchor="middle" font-family="${T.body}" font-size="16" fill="${HEX.paper}">${r[0]}</text>`; });
  s+=`</svg>`; return s; }
const OV={
  cups:()=>`<div class="cups"><div><div class="cup">${cubes()}</div><div class="cap2"><b>Coke</b><span>€3.56 · 42 g · about 10 cubes</span></div></div><div class="eq">=</div><div><div class="cup"><div class="g">0</div></div><div class="cap2"><b>Coke Zero</b><span>€3.56 · 0 cubes · same cup</span></div></div></div>`,
  basket:()=>`<div class="cards four">
    <div class="card"><div class="n">1 · the drink</div><h3>Zero, not Coke</h3><div class="big">−${cubesOf(42)} cubes</div><p>of sugar gone. Same price. Same cup.</p></div>
    <div class="card"><div class="n">2 · the size</div><h3>Small, not Large</h3><div class="big">−${cubesOf(N.smallSave)} cubes</div><p>on a typical drink. Cheaper too.</p></div>
    <div class="card"><div class="n">3 · the chicken</div><h3>Grilled, not crispy</h3><div class="big">−${N.grilledSave[0]}–${N.grilledSave[1]}</div><p>calories, on every one of the ${N.pGrilled} chicken dishes.</p></div>
    <div class="card"><div class="n">4 · the extra</div><h3>Add an apple</h3><div class="big">+1 fruit</div><p>€1.30 on Glovo Madrid. Fruit is cheap, it just hides at the bottom of the list.</p></div></div>`,
  money:()=>moneyChart(),
  nudges:()=>`<div class="cards">
    <div class="card"><div class="n">Nudge 1 · meal page</div><h3>Zero right under Coke</h3><div class="ui"><div class="row">○ Coke<span>€3.56</span></div><div class="row new">○ Coke Zero <small>same price · 0 cubes</small></div><div class="row">○ Fanta Zero</div><small>nothing is picked for you</small></div><table><tr><td>Customer</td><td class="g">−10 cubes ✓</td></tr><tr><td>McDonald's</td><td>€0 · same sale =</td></tr><tr><td>Glovo</td><td>€0 · same fee =</td></tr></table></div>
    <div class="card"><div class="n">Nudge 2 · home</div><h3>"Reorder with Zero"</h3><div class="ui"><div class="row">Big Mac menu · with Coke<span>€9.30</span></div><div class="row" style="border-color:var(--rule)">Reorder</div><div class="row new">Reorder with Zero <small>same price</small></div></div><table><tr><td>Customer</td><td class="g">−10 cubes, every reorder ✓</td></tr><tr><td>McDonald's</td><td>€0 =</td></tr><tr><td>Glovo</td><td>€0 · faster reorders =</td></tr></table></div>
    <div class="card"><div class="n">Nudge 3 · basket</div><h3>Fruit before fries</h3><div class="ui"><div class="row">Big Mac menu + Zero<span>€9.30</span></div><div class="row new">Add fruit or veg? <small>apple €1.30 · gazpacho €2.05</small></div><div class="row" style="color:var(--muted)">more sides · fries…</div></div><table><tr><td>Customer</td><td class="g">+1 fruit, only if tapped ✓</td></tr><tr><td>McDonald's</td><td class="a">+€0.91 to €1.44 +</td></tr><tr><td>Glovo</td><td class="a">+€0.39 to €0.62 +</td></tr></table></div></div>`,
  ask:()=>`<div class="ask">
    <div><h4>We ask for one decision</h4><ul><li><b>A four-week test in Madrid.</b> Half of McDonald's orders on Glovo see the three nudges. Half do not.</li><li><b>Nothing pre-picked, same-size buttons, ads say ad.</b> EU Consumer Rights Directive art. 22, Digital Services Act arts. 25 and 26.</li><li><b>Do it before a regulator does.</b> New York already puts a salt icon on menus. California made water the default kids' drink.</li></ul></div>
    <div><h4>We count</h4><ul><li><b>Basket value.</b> Same or bigger, or we stop.</li><li><b>How many pick Zero.</b></li><li><b>How many add fruit or veg.</b></li><li><b>How many come back</b> after "nice pick!"</li></ul></div>
    <div><h4>What this data can't tell us</h4><ul><li><b>It is the US menu.</b> Spain's list is shorter. The pattern is the same.</li><li><b>No sales numbers.</b> A shake nobody orders counts as much as fries. The test fixes that.</li><li><b>The percentages on the scale slide are our guesses.</b> 40 % sugary drink, 2 % switch, 5 % add a side, 30 % commission.</li></ul></div></div>`,
  behind:(arcs)=>`<div class="behind"><svg class="arcline" viewBox="0 0 1000 130" preserveAspectRatio="none" aria-hidden="true"><path d="M20,110 C250,80 380,36 520,28 C600,24 640,46 700,68 C800,100 900,106 980,110" fill="none" stroke="${T.accent}" stroke-width="2.5"/>${[['SETTING + HOOK',60,110],['RISING ACTION',300,62],['AHA',520,28],['SOLUTION',720,74],['NEXT STEPS',930,110]].map(a=>`<circle cx="${a[1]}" cy="${a[2]}" r="5" fill="${HEX.paper}"/><text x="${a[1]}" y="${a[2]-14}" text-anchor="middle" font-family="${T.mono}" font-size="11" fill="${T.fg2}" letter-spacing="1.5">${a[0]}</text>`).join('')}</svg>
    <div class="row4">${arcs.map(a=>`<div><div class="k">${a[0]}</div><p>${a[1]}</p></div>`).join('')}</div>
    <div class="books"><b>Gestalt, Session 2</b> figure-ground · similarity (one colour = one meaning) · common region (the two boxes) · focal point (one thing lit) · proximity (columns) · continuity (one line = one swap) · <b>Glance test</b> one idea per slide, text and data on separate slides (Duarte) · <b>Story arc</b> Brent Dykes, Effective Data Storytelling · <b>One mark per item</b> Ben Jones, Learning to See Data · <b>Declutter</b> Cole Nussbaumer Knaflic, Storytelling with Data · <b>Palette</b> Kate Strachnyi, ColorWise · <b>Unit charts</b> Nathan Yau, Visualize This · <b>Delivery</b> Lea Pica, Present Beyond Measure · <b>AI strategy</b> Kavita Ganesan, The Business Case for AI<br>Built with D3.js and AI help (Claude). Ideas, analysis and the Glovo price survey: Group 3.</div></div>`,
};

/* ---------- beats → slides ---------- */
const BEATS = /*BEATS*/;
const S=[]; BEATS.forEach(b=>{ if(b.single){S.push({...b,type:b.single})} else if(b.layout==='hidden'&&!b.ov){S.push({...b,type:'text'})} else {S.push({...b,type:'text'}); S.push({...b,type:'data'})} });
const STAGES=['Setting + hook','Rising action','Aha','Solution','Next steps'];

/* ---------- render ---------- */
const svg=d3.select('#svg'); const gBack=svg.append('g'); const gOrders=svg.append('g').attr('opacity',0); const gDots=svg.append('g'); const gAn=svg.append('g');
const dots=gDots.selectAll('circle').data(items).join('circle').attr('cx',W/2).attr('cy',H/2).attr('r',0).attr('fill','url(#g-sand)');
const op=ordersField();
gOrders.selectAll('circle').data(op).join('circle').attr('cx',d=>d.x).attr('cy',d=>d.y).attr('r',d=>d.k==='zero'?8:d.k==='gold'?6:4.6).attr('fill',d=>`url(#g-${d.k})`).attr('filter',d=>GLOW&&(d.k==='zero'||d.k==='gold')?'url(#glow)':null);
gOrders.append('text').attr('x',W/2).attr('y',H-70).attr('text-anchor','middle').attr('class','lab').text('ONE MONTH OF ORDERS · 1 DOT = 1,000 ORDERS');
d3.select('#arc').selectAll('span').data(STAGES).join('span').text(d=>d);

let cur=0, showNotes=false, lastLayout='';
function applyLayout(name,dur){ const P=name==='orders'?L('hidden'):L(name);
  dots.transition().duration(dur).delay((d,i)=>reduced?0:(i%41)*8).ease(d3.easeCubicInOut).attr('cx',d=>P[d.i].x).attr('cy',d=>P[d.i].y).attr('r',d=>P[d.i].r).attr('fill',d=>`url(#g-${P[d.i].fill})`).attr('opacity',d=>P[d.i].op).attr('filter',d=>GLOW&&LIT.has(P[d.i].fill)&&P[d.i].op>.5?'url(#glow)':null);
  gOrders.transition().duration(dur).attr('opacity',name==='orders'?1:0);
  gAn.transition().duration(reduced?0:200).attr('opacity',0).on('end',()=>{ gAn.selectAll('*').remove(); gBack.selectAll('*').remove(); (AN[name]||(()=>{}))(gAn); gAn.attr('opacity',0).transition().delay(reduced?0:dur*.75).duration(reduced?0:500).attr('opacity',1); gBack.attr('opacity',0).transition().delay(reduced?0:dur*.75).duration(reduced?0:500).attr('opacity',1); });
  lastLayout=name; }
function render(i){
  cur=Math.max(0,Math.min(S.length-1,i)); const s=S[cur]; const dur=reduced?0:1000;
  const isText=s.type==='text'||s.type==='title'; const isData=s.type==='data'; const isOv=s.type==='ov';
  const stage=document.getElementById('stage'); stage.classList.toggle('dim',(isText&&s.type!=='title')||isOv); stage.classList.toggle('half',s.type==='title');
  const t=d3.select('#text'); if(isText){ t.html(`<div class="wrap"><div class="eyebrow">${s.eye}</div><h1>${s.h}</h1>${s.lede?`<p class="lede">${s.lede}</p>`:''}<div class="goto">${s.type==='title'?'→ press right to start':'→ see it in the data'}</div></div>`); t.classed('on',true);} else t.classed('on',false);
  if(s.type==='title'){applyLayout(s.layout||'circle',dur)}
  if((isData||isOv)&&s.layout&&s.layout!==lastLayout)applyLayout(s.layout,dur);
  const on=isData;
  d3.select('#captl').classed('on',on).html(on?`<h2>${s.h}</h2>${s.howto?`<div class="howto">How to read · ${s.howto}</div>`:''}`:'');
  d3.select('#captr').classed('on',on&&!!s.stat).html(on&&s.stat?`<div class="v ${s.stat[2]||''}">${typeof s.stat[1]==='number'?fmt(s.stat[1]):s.stat[1]}</div><div class="l">${s.stat[0]}</div>`:'');
  d3.select('#capbl').classed('on',on&&!!(s.key&&s.key.length)).html(on&&s.key?s.key.map(k=>`<span><i style="background:${HEX[k[0]]}"></i>${k[1]}</span>`).join(''):'');
  const ov=d3.select('#overlay'); if(isOv){ov.html(typeof s.ov==='function'?s.ov():OV[s.ov]()); ov.classed('on',true)} else {ov.classed('on',false); setTimeout(()=>{if(S[cur].type!=='ov')ov.html('')},500)}
  d3.select('#count').text(String(cur+1).padStart(2,'0')+' / '+S.length); d3.select('#bar').style('width',((cur+1)/S.length*100)+'%');
  d3.select('#arc').selectAll('span').classed('on',(d,k)=>k===s.stage);
  d3.select('#src').text((isData||isOv)?(s.src||DEFAULT_SRC):'');
  d3.select('#nt').text(s.note||''); d3.select('#nc').text(s.course?'Course link: '+s.course:'');
  try{localStorage.setItem('deck4-'+document.title,cur)}catch(e){}
}
function next(){render(cur+1)} function prev(){render(cur-1)}
addEventListener('keydown',e=>{ if(['ArrowRight','ArrowDown',' ','PageDown'].includes(e.key)){e.preventDefault();next()} else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();prev()} else if(e.key==='Home'){render(0)} else if(e.key==='End'){render(S.length-1)} else if(e.key.toLowerCase()==='n'){toggleNotes()} });
addEventListener('click',e=>{ if(e.target.closest('button,a,#notes'))return; (e.clientX>innerWidth/2)?next():prev(); });
let tx=null; addEventListener('touchstart',e=>{tx=e.touches[0].clientX},{passive:true}); addEventListener('touchend',e=>{ if(tx==null)return; const dx=e.changedTouches[0].clientX-tx; if(Math.abs(dx)>40){dx<0?next():prev()} tx=null; });
function toggleNotes(){ showNotes=!showNotes; document.getElementById('notes').hidden=!showNotes; }
document.getElementById('nbtn').addEventListener('click',e=>{e.stopPropagation();toggleNotes()});
let start=0; try{ const h=location.hash.replace('#s',''); if(h&&!isNaN(h))start=+h-1; else { const v=localStorage.getItem('deck4-'+document.title); if(v!=null)start=+v; } }catch(e){}
render(start);
</script>
'''

BEATS_CUP = r'''[
 {single:'title',stage:0,eye:'For anyone who eats at McDonald\'s · Group 3 · IE IMBA Data Fluency',h:'What\'s in <em>your cup?</em>',lede:'A story told by the McDonald\'s menu itself. One dot per thing on it.',layout:'circle',
  note:'Behind me: the whole McDonald\'s menu, one dot per thing. We will start with just one of them.',course:'Session 7: setting + hook. Hero = the customer.'},
 {stage:0,eye:'Start with one thing',h:'Meet a medium Coke.',lede:'One dot. The dot\'s size is its calories. The cubes next to it are its sugar. <b>One cube is 4 g.</b>',stat:['sugar cubes in a medium Coke',N.cokeCubes,'red'],key:[],howto:'1 dot = 1 thing on the menu · 1 cube = 4 g of sugar',layout:'one',
  note:'This is a medium Coke. One dot. The cubes are its sugar: fourteen of them. Keep that picture; every other dot works the same way.',course:'Ben Jones: show the unit first. Gestalt: figure-ground.'},
 {stage:0,eye:'Now the whole menu',h:'Now all <em>260</em> things.',lede:'Burgers, fries, coffees, shakes, salads. Every one is a dot. Bigger dot, more calories.',stat:['things on the menu',N.total],key:[['sand','one thing on the menu']],howto:'bigger dot = more calories',layout:'circle',
  note:'Now the full menu. Two hundred and sixty dots. The Coke is in there somewhere. Let\'s sort them.',course:'Ben Jones: one mark per item.'},
 {stage:1,eye:'Sort them',h:'Line them up by <em>sugar.</em>',lede:'Left: no sugar. Right: lots of sugar. The red line is <b>12 cubes</b>, what doctors call a whole day.',stat:['cubes = a whole day of sugar',12,'red'],key:[['sand','one thing on the menu']],howto:'right = more sugar. the red line = 12 cubes, a whole day',layout:'swarmPlain',
  note:'Same dots, now lined up by sugar. Left is none, right is lots. The red line is twelve cubes, a whole day of sugar for an adult.',course:'Session 3: never truncate; the axis starts at zero. Axis in cubes so a 12-year-old can read it.'},
 {stage:1,eye:'Count the red',h:'<em class="red">62</em> things cross the line on their own.',lede:'One serving, more than a day of sugar. Those are the red dots.',stat:['things over a whole day of sugar',N.over50,'red'],key:[['over','more than 12 cubes in one serving'],['sand','less than that']],howto:'red = more than a day of sugar in one go',layout:'swarm',
  note:'Sixty-two things cross the line in one serving. We colour them red. Red means the same thing on every slide from now on.',course:'Gestalt: similarity, red always means "too much sugar". Session 3: red only for the alert.'},
 {stage:2,eye:'The big one',h:'Every red dot is a <em class="red">drink or a dessert.</em>',lede:'Top box: things you drink or eat with a spoon. Bottom box: things you eat with your hands.',stat:['red dots in the food box',0,'red'],key:[['over','more than 12 cubes'],['sand','less than that']],howto:'two boxes. red only in the top one',layout:'cupplate',
  note:'(Pause.) Split the menu in two. Drinks and desserts on top, food below. Every red dot is on top. The sweetest thing on a plate is eight cubes. The sugar is in the cup, not the burger.',course:'Gestalt: common region, the two boxes do the work. Session 7: the aha moment.'},
 {stage:1,eye:'Which cups?',h:'Coffee drinks are <em class="amber">sweeter than soda.</em>',lede:`<b>${N.coffee}</b> coffees and teas, the biggest group on the menu. On average <b>${cubesOf(N.coffeeAvg)} cubes</b>. Sodas average ${cubesOf(N.sodaAvg)}.`,stat:['cubes in an average coffee drink',cubesOf(N.coffeeAvg),'sugar'],key:[['sugar','coffee and tea'],['sand','everything else, faded']],howto:'only coffee is lit up',layout:'coffee',
  note:'Which cups? Not the shakes, there are only twenty-eight of them. Coffee. Ninety-five coffee drinks, ten cubes on average, more than a soda.',course:'Gestalt: focal point. Session 7: lead with the surprising number.'},
 {stage:1,eye:'And the size',h:'Bigger cup, <em class="amber">more sugar.</em>',lede:`Small <b>${cubesOf(N.sizeAvg.Small)} cubes</b>. Medium <b>${cubesOf(N.sizeAvg.Medium)}</b>. Large <b>${cubesOf(N.sizeAvg.Large)}</b>. A Large is over a whole day by itself.`,stat:['extra cubes, Large vs Small','+'+cubesOf(N.sizeAvg.Large-N.sizeAvg.Small),'sugar'],key:[['over','more than 12 cubes'],['sand','less than that'],['sugar','the average for that size']],howto:'each drink goes to its cup size. higher = more sugar',layout:'sizes',
  note:'Same drinks, three cup sizes. Each size up adds about two or three cubes. The average Large is over a day of sugar on its own.',course:'Gestalt: proximity, three columns read as three groups.'},
 {stage:3,eye:'The good news',h:'Most things have a <em class="green">healthier twin.</em>',lede:'Same menu, same counter. A Large has a Small. Crispy has grilled. Coke has Coke Zero.',stat:['one example','1'],key:[['sand','what you order now'],['zero','its healthier twin']],howto:'one line = one swap. left: now. right: the twin. lower = fewer calories',layout:'swapsOne',
  note:'Here is one example. A Large Coke on the left, nineteen cubes. Its twin on the right: the Small, ten cubes. One line, one swap.',course:'Knaflic: slope chart for before and after. Scaffold one line before showing all.'},
 {stage:3,eye:'All the twins',h:'<em class="green">64</em> twins already on the menu.',lede:`<b>${N.pSmaller}</b> are "order the Small". <b>${N.pGrilled}</b> are grilled, not crispy. <b>${N.pDiet}</b> are Zero, same cup, same price.`,stat:['twins on the menu',N.pairs,'green'],key:[['grey','Small instead of Large'],['sugar','grilled instead of crispy'],['zero','Zero instead of regular']],howto:'one line = one swap. colour = what kind of swap',layout:'swaps',
  note:'Now all sixty-four. Grey: order the Small. Amber: grilled instead of crispy. Green: Zero instead of regular. Green costs exactly the same.',course:'Gestalt: continuity, each line is one swap.'},
 {stage:4,eye:'Your turn',h:'Your <em class="green">better basket.</em>',lede:'Four small choices. None of them costs more.',layout:'hidden',
  note:'Four choices. Zero not Coke. Small not Large. Grilled not crispy. Add an apple.',course:'Session 7: resolution = what the audience should do.'},
 {single:'ov',stage:4,ov:'basket',layout:'hidden',src:'Sugar and calories: Kaggle US menu · 1 cube = 4 g · Coke Zero price: Glovo Madrid, 10 Oct 2026 · Coke sugar: Coca-Cola Spain label',
  note:'Same food, less sugar, no extra money. That is the whole message.',course:'Gestalt: similarity, four cards, same shape, same job.'},
 {single:'ov',stage:4,ov:()=>OV.behind([['Characters','Anyone who orders at McDonald\'s'],['Setting','260 things on the menu, one dot each'],['Conflict','The sugar hides in the cup'],['Resolution','Four swaps, no extra cost']]),layout:'hidden',src:'Story arc: Brent Dykes · Gestalt: Session 2 · hero framework: Session 7',
  note:'Hero: the customer. Guide: us. Every chart follows one Gestalt rule. Twenty seconds, then questions.',course:'Session 2 Gestalt, Session 7 hero framework, the seven Book of the Day picks.'},
]'''

BEATS_MONEY = r'''[
 {single:'title',stage:0,eye:'A pitch for the Glovo partnerships team · Group 3 · IE IMBA Data Fluency',h:'Healthy can <em>make money.</em>',lede:'Three changes to the McDonald\'s order flow. Same basket or bigger. Less sugar.',layout:'circle',
  note:'Behind me: the whole McDonald\'s menu, one dot per item. We will show where the sugar is, why healthy usually loses money, and the one swap that does not.',course:'Session 7: setting + hook. Hero = Glovo, guide = us.'},
 {stage:0,eye:'Start with one order',h:'A Big Mac menu with Coke. <em>€9.30.</em>',lede:'The Coke is the dot. Its size is its calories. The cubes are its sugar. <b>One cube is 4 g.</b>',stat:['sugar cubes in the Coke',N.cokeCubes,'red'],key:[],howto:'1 dot = 1 menu item · 1 cube = 4 g of sugar',layout:'one',src:'Order and price: Glovo Madrid, 10 Oct 2026 · Sugar: Kaggle US medium Coke',
  note:'One order. Big Mac menu with a Coke, nine thirty on Glovo. The Coke is this dot. Fourteen cubes of sugar.',course:'Ben Jones: show the unit first.'},
 {stage:0,eye:'The whole menu',h:'Now all <em>260</em> items.',lede:'Every item on the menu is a dot. Bigger dot, more calories.',stat:['menu items',N.total],key:[['sand','one menu item']],howto:'bigger dot = more calories',layout:'circle',
  note:'The full menu. Two hundred and sixty dots.',course:'Ben Jones: one mark per item.'},
 {stage:1,eye:'Sort by sugar',h:'<em class="amber">62</em> items carry a whole day of sugar.',lede:'Right = more sugar. The line is <b>12 cubes</b>, a whole day. Yellow dots cross it in one serving.',stat:['items over a day of sugar',N.over50,'sugar'],key:[['over','more than 12 cubes in one serving'],['sand','less than that']],howto:'right = more sugar. yellow = more than a day in one go',layout:'swarm',
  note:'Sorted by sugar. The line is twelve cubes, a whole day. Sixty-two items cross it on their own.',course:'Gestalt: similarity. Session 3: one highlight colour.'},
 {stage:2,eye:'The finding',h:'All of them are <em class="amber">in the cup.</em>',lede:'Top box: drinks and desserts. Bottom box: food. Every yellow dot is on top.',stat:['over-the-limit items that are food',0,'sugar'],key:[['over','more than 12 cubes'],['sand','less than that']],howto:'two boxes. yellow only in the top one',layout:'cupplate',
  note:'(Pause.) Every item with a day of sugar is a drink or a dessert. So the fix is in the cup. And the cup is where the free swap lives.',course:'Gestalt: common region. Session 7: the aha moment.'},
 {stage:1,eye:'The catch',h:'Healthier usually means <em class="red">smaller.</em>',lede:`The menu has <b>${N.pairs}</b> "healthier twins". <b>${N.pSmaller}</b> of them are a Large and its Small. Smaller cup, smaller bill.`,stat:['twins that shrink the bill',N.pSmaller,'red'],key:[['loss','a Large and its Small'],['dim','other twins, faded']],howto:'one line = one swap. left: now. right: the twin. red = loses money',layout:'swapsSmaller',
  note:'Here is why nobody pushes healthy. Sixty-four healthier twins exist. Forty-three are "order the Small". Healthier means a smaller bill.',course:'Session 7: the conflict. Gestalt: continuity, one line per swap.'},
 {stage:2,eye:'The exception',h:'<em class="green">8</em> twins cost nothing. All are drinks.',lede:'Coke to Coke Zero. Same cup, same price, zero cubes.',stat:['free swaps',N.pDiet,'green'],key:[['zero','Zero instead of regular'],['dim','other twins, faded']],howto:'only the free swaps are lit up',layout:'swapsDiet',
  note:'Light up the swaps that cost nothing. Eight. All drinks. This is the lever.',course:'Gestalt: focal point. Session 3: highlight palette.'},
 {stage:3,eye:'Same price',h:'Same price. <em class="green">No sugar.</em>',lede:'On Glovo Madrid, Coke and Coke Zero both cost <b>€3.56</b>.',layout:'hidden',
  note:'Ten cubes or none. Same price. Nobody loses a cent.',course:'Brent Dykes: the plan the guide hands the hero.'},
 {single:'ov',stage:3,ov:'cups',layout:'hidden',src:'Prices: Glovo Madrid, 10 Oct 2026 · Sugar: Coca-Cola Spain label, medium 40 cl · 1 cube ≈ 4 g',
  note:'One has about ten sugar cubes. The other has none. Same cup.',course:'Gestalt: similarity, two identical cups, one difference.'},
 {stage:3,eye:'Add, don\'t shrink',h:'Adding beats <em>shrinking.</em>',lede:'Make the order smaller: McDonald\'s loses €1 to €3. Zero: €0. Add an apple or a gazpacho: <b>+€1.30 to +€2.05</b>.',layout:'hidden',
  note:'Red goes down: make it smaller, lose money. Green: Zero, same money. Yellow goes up: add fruit, make money.',course:'Gestalt: similarity, red down, yellow up. Session 2: axis starts at zero.'},
 {single:'ov',stage:3,ov:'money',layout:'hidden',src:'Prices: Glovo Madrid McDonald\'s listing, 10 Oct 2026 · per order, before Glovo\'s fee',
  note:'The healthy choices that pay are the add-ons, not the shrinks.',course:'Nathan Yau: read the bar height.'},
 {stage:3,eye:'The plan',h:'Three nudges. <em>Nothing pre-picked.</em>',lede:'Zero under Coke. A "Reorder with Zero" button. Fruit before fries.',layout:'hidden',
  note:'Three changes to the order flow. None pre-picks. The customer always chooses.',course:'Session 3: Z-pattern, most important nudge top-left.'},
 {single:'ov',stage:3,ov:'nudges',layout:'hidden',src:'Concept for the McDonald\'s order flow on Glovo · prices Glovo Madrid · Glovo fee assumed 30 %',
  note:'Same sale, same fee, or more, on every one.',course:'EU CRD art. 22, DSA arts. 25–26: never pre-tick, same-size buttons, ads say ad.'},
 {stage:3,eye:'Scale',h:'Only a few need to <em>say yes.</em>',lede:'One million orders a month. If <b>2 in 100</b> switch to Zero and 5 in 100 add a side: <b>336 kg</b> less sugar, <b>€45,500</b> more for McDonald\'s, <b>€19,500</b> for Glovo.',stat:['more for McDonald\'s, per month','€45,500','sugar'],key:[['sugary','has a sugary drink'],['zero','picked Zero instead'],['gold','added fruit or veg'],['other','1 dot = 1,000 orders']],howto:'one dot = 1,000 orders',layout:'orders',src:'OUR GUESSES, NOT DATA: 1,000,000 orders · 40 % include a sugary drink · 2 % of those pick Zero · 5 % add a €1.30 side · 30 % commission · the test replaces these with real numbers',
  note:'These percentages are our guesses. Even so: two in a hundred switch, that is 336 kilos of sugar a month, forty-five thousand euros for McDonald\'s, nineteen for Glovo.',course:'Nathan Yau: unit charts make scale felt. Session 7: say what is assumed.'},
 {stage:4,eye:'Next steps',h:'Try it for <em>four weeks.</em>',lede:'Half of Madrid orders see the nudges. Half don\'t. Then the guesses become numbers.',layout:'hidden',
  note:'One decision: a four-week test in Madrid.',course:'Session 7: resolution = one decision to ask for.'},
 {single:'ov',stage:4,ov:'ask',layout:'hidden',
  note:'Baskets no smaller, more Zero, more fruit. Then the guesses become numbers. Questions.',course:'Session 7: say what the data cannot tell you.'},
 {single:'ov',stage:4,ov:()=>OV.behind([['Characters','Glovo, McDonald\'s, hungry Madrid'],['Setting','260 menu items, one dot each'],['Conflict','Healthy swaps shrink the bill'],['Resolution','Free swap + add-ons, four-week test']]),layout:'hidden',src:'Story arc: Brent Dykes · Gestalt: Session 2 · hero framework: Session 7',
  note:'Hero: Glovo. Guide: us. Twenty seconds, then questions.',course:'Session 2 Gestalt, Session 7 hero framework, the seven Book of the Day picks.'},
]'''

def build(fname, theme, beats):
    t = THEMES[theme]
    html = (TEMPLATE.replace('/*TITLE*/', t['name']).replace('/*FONTS*/', t['fonts'])
      .replace('/*BG*/', t['bg']).replace('/*FG2*/', t['fg2']).replace('/*FG*/', t['fg']).replace('/*MUTED*/', t['muted']).replace('/*RULE*/', t['rule']).replace('/*ACCENT*/', t['accent'])
      .replace('/*C_OVER*/', t['hex']['over']).replace('/*C_SUGAR*/', t['hex']['sugar']).replace('/*C_ZERO*/', t['hex']['zero']).replace('/*C_LOSS*/', t['hex']['loss'])
      .replace('/*DISPLAY*/', t['display']).replace('/*BODY*/', t['body']).replace('/*MONO*/', t['mono']).replace('/*SCHEME*/', t['scheme'])
      .replace('/*THEME*/', json.dumps({k:v for k,v in t.items() if k!='fonts'})).replace('/*BEATS*/', beats).replace('/*DATA*/', DATA))
    (HERE / fname).write_text(html); print(fname, len(html), 'bytes')

build('whats-in-your-cup-v4.html', 'paper', BEATS_CUP)
build('healthy-makes-money-v4.html', 'navy', BEATS_MONEY)
