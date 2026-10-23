#!/usr/bin/env python3
"""v5 STRETCH deck: 'Sugar Cubes'. Same dot engine as v4, plus a sugar-cube stack layer.
   Frameworks applied explicitly: Knaflic Big Idea, Pica PICA, Dykes arc, Jones how-to-read, Yau unit charts, Strachnyi one colour per meaning, Rosling moving marks, Session 2 Gestalt.
   Output: sugar-cubes-v5.html"""
import json, pathlib
from _build_v4 import TEMPLATE, DATA
HERE = pathlib.Path(__file__).parent

THEME = dict(
  name='Sugar Cubes',
  fonts="family=Nunito:wght@500;700;900&family=DM+Mono:wght@400;500",
  display='"Nunito","Helvetica Neue",Arial,sans-serif', body='"Nunito","Helvetica Neue",Arial,sans-serif', mono='"DM Mono","SFMono-Regular",Menlo,monospace',
  bg='#F4F7FB', fg='#172033', fg2='#4E5A70', muted='#8A95A8', rule='#D5DCE8', accent='#2F6BFF', scheme='light', glow=0,
  hex=dict(sand='#2B3447',over='#E63946',sugar='#F4A62A',salt='#2F6BFF',zero='#1FA46B',pink='#F4A6B0',gold='#F4A62A',grey='#AEB7C7',dim='#E1E6EF',paper='#172033',sugary='#F9C9CF',other='#E1E6EF',loss='#E63946',gain='#F4A62A',cube='#FFFFFF',cubeEdge='#172033'),
  overKey='over')

# ---- extra engine code: cube stacks ----
EXTRA_LAYOUTS = r'''
  stacks(){ return L('hidden'); },
'''
EXTRA_AN = r'''
  stacks(g){ /* drawn by drawStacks via the slide's `stacks` spec */ if(window.__stackSpec) drawStacks(g, window.__stackSpec); },
'''
EXTRA_HELPERS = r'''
/* ---------- sugar-cube stacks (Yau: one shape per unit; Jones: the mark is explained before the chart) ---------- */
const CUBE=15, CGAP=3, CSTEP=CUBE+CGAP, BASE=560, DAY=12;
function drawStacks(g, spec){
  const cols=spec.cols; const n=cols.length; const colW=Math.min(170, (W-2*M)/n); const x0=(W-colW*n)/2;
  if(spec.dayLine!==false){ const y=BASE-DAY*CSTEP; g.append('line').attr('class','rule hard').attr('x1',M-20).attr('x2',W-M+20).attr('y1',y).attr('y2',y); g.append('text').attr('x',W-M+20).attr('y',y-10).attr('text-anchor','end').attr('fill',HEX.over).attr('font-weight',700).text('A WHOLE DAY OF SUGAR: 12 CUBES'); }
  g.append('line').attr('class','axl').attr('x1',M-20).attr('x2',W-M+20).attr('y1',BASE+2).attr('y2',BASE+2);
  cols.forEach((c,ci)=>{ const cx=x0+colW*ci+colW/2; const perRow=c.n>26?2:1; const w=perRow*CSTEP-CGAP;
    for(let k=0;k<c.n;k++){ const row=Math.floor(k/perRow), col=k%perRow; const x=cx-w/2+col*CSTEP, y=BASE-(row+1)*CSTEP+CGAP;
      g.append('rect').attr('class','cube').attr('x',x).attr('y',y).attr('width',CUBE).attr('height',CUBE).attr('fill',c.color?HEX[c.color]:HEX.cube).attr('stroke',HEX.cubeEdge).attr('opacity',0)
        .transition().delay(reduced?0:ci*120+k*28).duration(reduced?0:220).attr('opacity',1); }
    const top=BASE-Math.ceil(c.n/perRow)*CSTEP; const big=n<=5; g.append('text').attr('class',big?'big':'lab').attr('font-size',big?null:'20px').attr('x',cx).attr('y',(c.n?top:BASE)-14).attr('text-anchor','middle').attr('fill',c.n>DAY?HEX.over:HEX.paper).text(big?(c.n+(c.n===1?' cube':' cubes')):c.n);
    g.append('text').attr('class','lab').attr('x',cx).attr('y',BASE+34).attr('text-anchor','middle').text(c.label); if(c.sub)g.append('text').attr('x',cx).attr('y',BASE+56).attr('text-anchor','middle').text(c.sub); });
  if(spec.note){ g.append('text').attr('x',M-20).attr('y',BASE+100).text(spec.note); }
}
'''

TEMPLATE5 = (TEMPLATE
  .replace("const LAYOUTS={", "const LAYOUTS={"+EXTRA_LAYOUTS, 1)
  .replace("const AN={", "const AN={"+EXTRA_AN, 1)
  .replace("/* ---------- overlays ---------- */", EXTRA_HELPERS+"\n/* ---------- overlays ---------- */", 1)
  # set the stack spec before a layout is applied; stacks always re-draw
  .replace("if((isData||isOv)&&s.layout&&s.layout!==lastLayout)applyLayout(s.layout,dur);",
           "if(s.stacks){window.__stackSpec=s.stacks(); if(isData){applyLayout('stacks',dur); lastLayout='stacks:'+cur;} } else if((isData||isOv)&&s.layout&&s.layout!==lastLayout)applyLayout(s.layout,dur);")
  # cube css: outlined white cubes with a soft shadow
  .replace("svg .cube{fill:var(--fg);stroke:var(--bg);stroke-width:1.5;rx:3}", "svg .cube{stroke-width:1.5;rx:3;filter:drop-shadow(0 2px 2px rgba(23,32,51,.18))}")
)

BEATS = r'''[
 {single:'title',stage:0,eye:'For anyone who eats at McDonald\'s · Group 3 · IE IMBA Data Fluency',h:'How many <em>sugar cubes</em> are in your order?',lede:'A story told in sugar cubes. One cube is 4 grams.',layout:'circle',
  note:'We measured the whole McDonald\'s menu in sugar cubes. One cube is four grams. Everything you see today is cubes.',course:'Nathan Yau, Visualize This: pick a unit people can picture. Session 7: setting + hook.'},
 {single:'title',stage:0,eye:'The one sentence to remember · Knaflic\'s "Big Idea"',h:'Most of the sugar hides <em>in the cup</em>, and the cheapest fix is to pick the <em>Zero</em>.',lede:'That is the whole talk. The next slides show you why, one cube at a time.',layout:'hidden',
  note:'Here is the whole talk in one sentence. If you remember nothing else, remember this.',course:'Cole Nussbaumer Knaflic, Storytelling with Data: the Big Idea is one complete sentence with a point of view and what is at stake.'},
 {stage:0,eye:'The unit',h:'One cube is 4 g. A day is <em class="red">12 cubes.</em>',lede:'Doctors say about 50 g of sugar a day. That is 12 cubes. We will draw that line on every chart.',stat:['cubes in a day',12,'red'],key:[],howto:'1 cube = 4 g of sugar · the red line = 12 cubes = a whole day',stacks:()=>({cols:[{label:'A whole day',n:12,sub:'what doctors say is enough'}],dayLine:true}),layout:'stacks',
  note:'One cube is four grams. Twelve cubes is a whole day. That red line stays on every chart from now on.',course:'Ben Jones, Learning to See Data: explain the mark before the chart. PICA, Context: a benchmark on every chart.'},
 {stage:0,eye:'One drink',h:'A medium Coke is <em class="red">14 cubes.</em>',lede:'More than a whole day, in one cup, before you eat anything.',stat:['cubes in a medium Coke',N.cokeCubes,'red'],key:[],howto:'taller stack = more sugar · red number = over a day',stacks:()=>({cols:[{label:'A whole day',n:12},{label:'Medium Coke',n:N.cokeCubes,sub:N.coke.sugar+' g'}]}),layout:'stacks',
  note:'A medium Coke. Fourteen cubes. That is more than a day, in one cup, before you have eaten anything.',course:'PICA, Purpose: this chart exists to make one number feel real.'},
 {stage:1,eye:'The food',h:'A Big Mac is <em>2.</em> Fries are <em>0.</em>',lede:'The sugar is not in the burger. Keep that in mind.',stat:['cubes in a Big Mac',cubesOf(byName.get('Big Mac').sugar)],key:[],howto:'same cubes, same scale, same red line',stacks:()=>({cols:[{label:'Big Mac',n:cubesOf(byName.get('Big Mac').sugar),sub:byName.get('Big Mac').sugar+' g'},{label:'Medium fries',n:cubesOf(byName.get('Medium French Fries').sugar),sub:byName.get('Medium French Fries').sugar+' g'},{label:'Medium Coke',n:N.cokeCubes,sub:N.coke.sugar+' g'}]}),layout:'stacks',
  note:'Now the food. A Big Mac: two cubes. Fries: none. The Coke next to them: fourteen. The sugar is not in the burger.',course:'Gestalt: proximity, three stacks side by side invite comparison. Session 3: same scale, no truncation.'},
 {stage:1,eye:'Every group on the menu',h:'The sweetest groups are all <em class="red">drinks.</em>',lede:'Average cubes per item, for each group of the menu, biggest first.',stat:['menu groups',9],key:[],howto:'one stack per group · average cubes per item · sorted big to small',stacks:()=>({cols:[...new Set(items.map(d=>d.cat))].map(c=>({label:({'Smoothies & Shakes':'Shakes','Coffee & Tea':'Coffee','Beverages':'Sodas','Beef & Pork':'Beef','Chicken & Fish':'Chicken','Snacks & Sides':'Sides'})[c]||c,n:cubesOf(catAvg(c)),color:CUP.has(c)?'over':null})).sort((a,b)=>b.n-a.n),dayLine:true,note:'RED STACKS = DRINKS AND DESSERTS · WHITE STACKS = FOOD · NUMBERS = AVERAGE CUBES PER ITEM'}),layout:'stacks',
  note:'Every group of the menu, averaged, biggest first. Shakes, coffees, sodas and desserts are the tall ones, in red. All the food is short.',course:'Session 3: sort bars largest to smallest. Strachnyi, ColorWise: one colour per meaning, red = drinks here and everywhere.'},
 {stage:1,eye:'Now every single thing',h:'All <em>260</em> things, lined up by sugar.',lede:'Each dot is one thing on the menu. Right means more sugar. The red line is still 12 cubes.',stat:['things on the menu',N.total],key:[['sand','one thing on the menu']],howto:'right = more sugar · red line = 12 cubes · up and down means nothing',layout:'swarmPlain',
  note:'Now every single thing, one dot each, lined up by sugar. Same red line.',course:'Hans Rosling, 200 countries: let the marks move. Ben Jones: one mark per item.'},
 {stage:1,eye:'Count the red',h:'<em class="red">62</em> things cross the line on their own.',lede:'One serving, more than a day of sugar.',stat:['things over a day of sugar',N.over50,'red'],key:[['over','more than 12 cubes'],['sand','less than that']],howto:'red = more than a day of sugar in one go',layout:'swarm',
  note:'Sixty-two things cross the line in one serving.',course:'PICA, Insight: the chart answers the question at a glance.'},
 {stage:2,eye:'The big one',h:'Every red dot is a <em class="red">drink or a dessert.</em>',lede:'Top box: things you drink or eat with a spoon. Bottom box: things you eat with your hands.',stat:['red dots in the food box',0,'red'],key:[['over','more than 12 cubes'],['sand','less than that']],howto:'two boxes · red only in the top one',layout:'cupplate',
  note:'(Pause.) Drinks and desserts on top, food below. Every red dot is on top. The sugar is in the cup.',course:'Dykes: the aha moment. Gestalt: common region, the boxes do the work.'},
 {stage:1,eye:'Which cup?',h:'The coffee can beat the <em class="amber">Coke.</em>',lede:'An average soda, an average coffee drink, and the sweetest coffee on the menu.',stat:['cubes in the sweetest coffee',cubesOf(N.coffeeMax.sugar),'sugar'],key:[],howto:'three stacks · same scale · red line = a day',stacks:()=>({cols:[{label:'Average soda',n:cubesOf(N.sodaAvg)},{label:'Average coffee drink',n:cubesOf(N.coffeeAvg),color:'sugar'},{label:'Sweetest coffee',n:cubesOf(N.coffeeMax.sugar),sub:N.coffeeMax.item,color:'sugar'}]}),layout:'stacks',
  note:'Which cup? The coffee drinks. On average ten cubes, more than a soda. The sweetest one, a large chocolate chip frappé, is twenty-five.',course:'PICA, Context: the surprise only works next to the expected number.'},
 {stage:1,eye:'And the size',h:'Bigger cup, <em class="amber">more cubes.</em>',lede:'The average drink in each cup size.',stat:['extra cubes, Large vs Small','+'+cubesOf(N.sizeAvg.Large-N.sizeAvg.Small),'sugar'],key:[],howto:'one stack per cup size · average cubes',stacks:()=>({cols:[{label:'Small',n:cubesOf(N.sizeAvg.Small)},{label:'Medium',n:cubesOf(N.sizeAvg.Medium)},{label:'Large',n:cubesOf(N.sizeAvg.Large),color:'over'}]}),layout:'stacks',
  note:'Small, nine. Medium, twelve. Large, fourteen. The average Large is over a day by itself.',course:'Gestalt: proximity. Knaflic: declutter, three numbers, nothing else.'},
 {stage:3,eye:'The fix',h:'Same drink, <em class="green">three choices.</em>',lede:'Large Coke, Small Coke, Coke Zero. The Zero costs the same as the Coke.',stat:['cubes in a Coke Zero',0,'green'],key:[],howto:'three stacks · the green one is free of sugar and costs the same',stacks:()=>({cols:[{label:'Large Coke',n:cubesOf(byName.get('Coca-Cola Classic (Large)').sugar),color:'over'},{label:'Small Coke',n:cubesOf(byName.get('Coca-Cola Classic (Small)').sugar)},{label:'Coke Zero',n:0,sub:'same price on Glovo · €3.56',color:'zero'}]}),layout:'stacks',
  note:'Same drink, three choices. Large: nineteen cubes. Small: ten. Zero: none, and it costs the same. That is the cheapest fix on the menu.',course:'Dykes: the solution the guide hands the hero. Strachnyi: green only ever means "free of sugar".'},
 {stage:4,eye:'Your turn',h:'Your <em class="green">better basket.</em>',lede:'Four small choices. None of them costs more.',layout:'hidden',
  note:'Four choices. Zero not Coke. Small not Large. Grilled not crispy. Add an apple.',course:'Session 7: resolution = what the audience should do.'},
 {single:'ov',stage:4,ov:'basket',layout:'hidden',src:'Sugar: Kaggle US menu · 1 cube = 4 g · Coke Zero price: Glovo Madrid, 10 Oct 2026',
  note:'Same food, fewer cubes, no extra money.',course:'Gestalt: similarity, four cards, same shape.'},
 {single:'ov',stage:4,ov:()=>OV.behind([['Characters','Anyone who orders at McDonald\'s'],['Setting','260 things, measured in sugar cubes'],['Conflict','The sugar hides in the cup'],['Resolution','Pick the Zero, pick the Small, add fruit']]),layout:'hidden',src:'Big Idea: Knaflic · PICA: Lea Pica · arc: Dykes · unit: Yau · how to read: Jones · colour: Strachnyi · moving marks: Rosling · Gestalt: Session 2',
  note:'Every chart passed Lea Pica\'s four questions: why does it exist, does it answer at a glance, is the benchmark there, is the noise gone.',course:'The seven Book of the Day picks, each used once on purpose.'},
]'''

def build():
    t = THEME
    html = (TEMPLATE5.replace('/*TITLE*/', t['name']).replace('/*FONTS*/', t['fonts'])
      .replace('/*BG*/', t['bg']).replace('/*FG2*/', t['fg2']).replace('/*FG*/', t['fg']).replace('/*MUTED*/', t['muted']).replace('/*RULE*/', t['rule']).replace('/*ACCENT*/', t['accent'])
      .replace('/*C_OVER*/', t['hex']['over']).replace('/*C_SUGAR*/', t['hex']['sugar']).replace('/*C_ZERO*/', t['hex']['zero']).replace('/*C_LOSS*/', t['hex']['loss'])
      .replace('/*DISPLAY*/', t['display']).replace('/*BODY*/', t['body']).replace('/*MONO*/', t['mono']).replace('/*SCHEME*/', t['scheme'])
      .replace('/*THEME*/', json.dumps({k:v for k,v in t.items() if k!='fonts'})).replace('/*BEATS*/', BEATS).replace('/*DATA*/', DATA))
    (HERE / 'sugar-cubes-v5.html').write_text(html); print('sugar-cubes-v5.html', len(html), 'bytes')

if __name__=='__main__':
    build()
