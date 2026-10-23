#!/usr/bin/env python3
"""v6: 'Ship the Healthy Default'. The Glovo story told by Glovo's own product team, as a feature pitch.
   Delivery-app look: warm white, Glovo yellow, app-style cards. Reuses the v4 engine + v5 cube stacks.
   Output: ship-the-healthy-default-v6.html"""
import json, pathlib
from _build_v5_cubes import TEMPLATE5
from _build_v4 import DATA
HERE = pathlib.Path(__file__).parent

THEME = dict(
  name='Ship the Healthy Default',
  fonts="family=Plus+Jakarta+Sans:wght@500;700;800&family=DM+Sans:wght@400;500;700&family=DM+Mono:wght@400;500",
  display='"Plus Jakarta Sans","Helvetica Neue",Arial,sans-serif', body='"DM Sans","Helvetica Neue",Arial,sans-serif', mono='"DM Mono","SFMono-Regular",Menlo,monospace',
  bg='#FFFBEF', fg='#1C1A14', fg2='#5C574A', muted='#948E7E', rule='#EAE2C8', accent='#F2B705', scheme='light', glow=0,
  hex=dict(sand='#2A2720',over='#E5484D',sugar='#F2B705',salt='#2F6BFF',zero='#17A864',pink='#F6A5AA',gold='#F2B705',grey='#B9B2A1',dim='#EFE9D6',paper='#1C1A14',sugary='#F9D0D2',other='#EFE9D6',loss='#E5484D',gain='#17A864',cube='#FFFFFF',cubeEdge='#1C1A14'),
  overKey='over')

EXTRA_OV = r'''
  fair:()=>`<div class="cards">
    <div class="card"><div class="n">Rule 1 · EU Consumer Rights Directive art. 22</div><h3>Never pre-tick</h3><div class="ui"><div class="row">○ Coke<span>€3.56</span></div><div class="row new">○ Coke Zero <small>same price · 0 cubes</small></div><small>nothing is selected for the user</small></div><p>The healthy option is shown first, never chosen for them.</p></div>
    <div class="card"><div class="n">Rule 2 · Digital Services Act art. 25</div><h3>Same-size buttons</h3><div class="ui"><div class="row" style="border-color:var(--rule);justify-content:center">Reorder</div><div class="row new" style="justify-content:center">Reorder with Zero</div></div><p>No dark patterns. Both choices get the same tap target.</p></div>
    <div class="card"><div class="n">Rule 3 · Digital Services Act art. 26</div><h3>Ads say "ad"</h3><div class="ui"><div class="row new">Better menu · €10.60 <small>Ad</small></div><div class="row">McPollo −40%</div></div><p>When McDonald's pays for the Better Menu tile, the user sees the label.</p></div></div>`,
  ship:()=>`<div class="cards">
    <div class="card"><div class="n">Screen 1 · meal page · sprint 1</div><h3>Zero first</h3><div class="ui"><div class="row">○ Coke<span>€3.56</span></div><div class="row new">○ Coke Zero <small>same price · 0 cubes</small></div><div class="row">○ Fanta Zero</div><small>nothing is picked for you</small></div><table><tr><td>User</td><td class="g">−10 cubes ✓</td></tr><tr><td>Partner</td><td>€0 · same sale =</td></tr><tr><td>Glovo</td><td>€0 · same fee =</td></tr><tr><td>Effort</td><td>reorder a list</td></tr></table></div>
    <div class="card"><div class="n">Screen 2 · home · sprint 1</div><h3>Reorder with Zero</h3><div class="ui"><div class="row">Big Mac menu · with Coke<span>€9.30</span></div><div class="row" style="border-color:var(--rule)">Reorder</div><div class="row new">Reorder with Zero <small>same price</small></div></div><table><tr><td>User</td><td class="g">−10 cubes, every reorder ✓</td></tr><tr><td>Partner</td><td>€0 =</td></tr><tr><td>Glovo</td><td>€0 · faster reorders =</td></tr><tr><td>Effort</td><td>one button</td></tr></table></div>
    <div class="card"><div class="n">Screen 3 · basket · sprint 2</div><h3>Fruit in the add-on rail</h3><div class="ui"><div class="row">Big Mac menu + Zero<span>€9.30</span></div><div class="row new">Add fruit or veg? <small>apple €1.30 · gazpacho €2.05</small></div><div class="row" style="color:var(--muted)">more sides · fries…</div></div><table><tr><td>User</td><td class="g">+1 fruit, only if tapped ✓</td></tr><tr><td>Partner</td><td class="a">+€0.91 to €1.44 +</td></tr><tr><td>Glovo</td><td class="a">+€0.39 to €0.62 +</td></tr><tr><td>Effort</td><td>re-sort the rail</td></tr></table></div></div>`,
  experiment:()=>`<div class="ask">
    <div><h4>Hypothesis</h4><ul><li><b>If</b> Zero is shown first, a Reorder-with-Zero button exists, and fruit sits at the top of the add-on rail,</li><li><b>then</b> basket value stays the same or grows and the share of sugary drinks falls,</li><li><b>because</b> the healthy choice costs nothing extra and is finally visible.</li></ul></div>
    <div><h4>Metrics · 4 weeks · Madrid · 50/50 split</h4><ul><li><b>Primary:</b> average basket value (guardrail: must not drop).</li><li><b>Secondary:</b> share of orders with Zero; share with a fruit or veg add-on.</li><li><b>Retention:</b> 30-day reorder rate after "nice pick!".</li><li><b>Guardrail:</b> checkout time, support tickets.</li></ul></div>
    <div><h4>What we don't know yet</h4><ul><li><b>Sales mix.</b> The menu data has no volumes. The test fixes that.</li><li><b>Our inputs are guesses.</b> 40 % of orders include a sugary drink, 2 % switch, 5 % add a side, 30 % commission.</li><li><b>US menu as proxy.</b> Spain's list is shorter; the pattern is the same. Swap in the Spanish nutrition file before launch.</li></ul></div></div>`,
'''

TEMPLATE6 = (TEMPLATE5
  .replace("const OV={", "const OV={"+EXTRA_OV, 1)
  .replace("MCDONALD'S MAKES MORE ↑","THE PARTNER MAKES MORE ↑").replace("MCDONALD'S MAKES LESS ↓","THE PARTNER MAKES LESS ↓").replace("€ PER ORDER, FOR MCDONALD'S","€ PER ORDER, FOR THE PARTNER")
  # app-style cards: yellow top bar on the mock screens
  .replace(".card .ui{border:1.5px solid var(--rule);border-radius:12px;padding:12px 14px;font-size:14px;display:grid;gap:8px}",
           ".card .ui{border:1.5px solid var(--rule);border-radius:16px;padding:12px 14px;font-size:14px;display:grid;gap:8px;position:relative;overflow:hidden;padding-top:22px}\n.card .ui::before{content:\"\";position:absolute;left:0;right:0;top:0;height:10px;background:var(--accent)}")
)

BEATS = r'''[
 {single:'title',stage:0,eye:'Glovo product team · feature pitch · Group 3 · IE IMBA Data Fluency',h:'Ship the <em>healthy default.</em> Keep the basket.',lede:'Three screens. Zero lost revenue. 336 kg less sugar a month in Madrid.',layout:'circle',
  note:'We own the order flow. Every screen is a decision we make for a million orders a month. Here is one worth making.',course:'Session 7: hero = the product team; guide = the data. Dykes: open on what is at stake.'},
 {single:'title',stage:0,eye:'The one sentence · Knaflic\'s "Big Idea"',h:'The order flow decides what Madrid eats. <em>Three screens</em> cut the sugar and keep every euro.',lede:'That is the pitch. The next slides are the evidence, then the build.',layout:'hidden',
  note:'One sentence. The app decides what people eat more than the menu does. We can use that for good and for revenue at the same time.',course:'Knaflic: one complete sentence, a point of view, what is at stake.'},
 {stage:0,eye:'One order on our app',h:'A Big Mac menu with Coke. <em>€9.30.</em>',lede:'The Coke in that order is <b>14 sugar cubes</b>. One cube is 4 g.',stat:['cubes in the Coke',N.cokeCubes,'red'],key:[],howto:'1 cube = 4 g of sugar · taller stack = more sugar',stacks:()=>({cols:[{label:'A whole day',n:12,sub:'what doctors call enough'},{label:'The Coke in the order',n:N.cokeCubes,sub:'Coca-Cola Classic (Medium) · '+N.coke.sugar+' g',color:'over'}]}),layout:'stacks',
  note:'Our best-selling bundle. The drink in it is fourteen cubes of sugar, more than a whole day, before the burger.',course:'Ben Jones: explain the unit first. Yau: one shape per unit.'},
 {stage:1,eye:'The menu we sell',h:'The sweetest groups we sell are <em class="red">drinks.</em>',lede:'Average cubes per item, every group of the McDonald\'s menu, biggest first.',stat:['menu groups',9],key:[],howto:'one stack per group · average cubes · red = drinks and desserts',stacks:()=>({cols:[...new Set(items.map(d=>d.cat))].map(c=>({label:({'Smoothies & Shakes':'Shakes','Coffee & Tea':'Coffee','Beverages':'Sodas','Beef & Pork':'Beef','Chicken & Fish':'Chicken','Snacks & Sides':'Sides'})[c]||c,n:cubesOf(catAvg(c)),color:CUP.has(c)?'over':null})).sort((a,b)=>b.n-a.n),dayLine:true,note:'RED STACKS = DRINKS AND DESSERTS · WHITE STACKS = FOOD'}),layout:'stacks',
  note:'Every group we list, averaged. The tall red ones are shakes, coffees, desserts and sodas. The food is short. The sugar problem is a drinks problem.',course:'Session 3: sort largest to smallest. Strachnyi: red means one thing in this deck.'},
 {stage:2,eye:'The finding',h:'Every item over a day of sugar is <em class="red">in a cup.</em>',lede:'All 260 items, one dot each. Top box: drinks and desserts. Bottom box: food.',stat:['over-the-limit items that are food',0,'red'],key:[['over','more than 12 cubes'],['sand','less than that']],howto:'two boxes · red only in the top one · right = more sugar',layout:'cupplate',
  note:'(Pause.) Every red dot is in the top box. The drink is the lever, and the drink is a screen we own.',course:'Dykes: the aha. Gestalt: common region.'},
 {stage:1,eye:'The catch',h:'Healthier usually means a <em class="red">smaller basket.</em>',lede:`The menu already has <b>${N.pairs}</b> healthier twins. <b>${N.pSmaller}</b> are "order the Small". Smaller basket, smaller commission.`,stat:['twins that shrink the basket',N.pSmaller,'red'],key:[['loss','a Large and its Small'],['dim','other twins, faded']],howto:'one line = one swap · left: now · right: the twin · red = shrinks the basket',layout:'swapsSmaller',
  note:'Here is why no one has shipped this. Forty-three of the healthier options are just the Small. Smaller basket, smaller fee for us. We would never push that.',course:'Session 7: the conflict. Gestalt: continuity.'},
 {stage:2,eye:'The exception',h:'<em class="green">8</em> twins cost nothing. All are drinks.',lede:'Coke to Coke Zero. Same cup, same price, same basket, zero cubes.',stat:['free swaps',N.pDiet,'green'],key:[['zero','Zero instead of regular'],['dim','other twins, faded']],howto:'only the free swaps are lit',layout:'swapsDiet',
  note:'Eight swaps cost nothing. All drinks. Same basket value, same commission, no sugar. That is the feature.',course:'Gestalt: focal point. PICA, Insight: the chart answers at a glance.'},
 {stage:3,eye:'Same price',h:'Same price. <em class="green">Zero cubes.</em>',lede:'On our Madrid listing a Coke and a Coke Zero both cost <b>€3.56</b>.',layout:'hidden',
  note:'Ten cubes or none. Same price. Same basket. Nobody loses a cent.',course:'Dykes: the plan the guide hands the hero.'},
 {single:'ov',stage:3,ov:'cups',layout:'hidden',src:'Prices: Glovo Madrid, 10 Oct 2026 · Sugar: Coca-Cola Spain label, medium 40 cl · 1 cube ≈ 4 g',
  note:'Same cup, same price. One has ten cubes. One has none.',course:'Gestalt: similarity, two identical cups, one difference.'},
 {stage:3,eye:'Add-ons grow the basket',h:'Adding beats <em>shrinking.</em>',lede:'Make the order smaller and the partner loses €1 to €3. Zero is €0. An apple or a gazpacho adds <b>€1.30 to €2.05</b>, and we take our share of every add-on.',layout:'hidden',
  note:'Red goes down: shrinking loses money. Green: Zero, flat. Yellow goes up: add-ons. Our commission rides on the add-ons.',course:'Gestalt: similarity, down = lost, up = gained. Session 2: axis at zero.'},
 {single:'ov',stage:3,ov:'money',layout:'hidden',src:'Prices: Glovo Madrid McDonald\'s listing, 10 Oct 2026 · per order, before Glovo\'s fee',
  note:'The healthy choices that pay are the add-ons, not the shrinks.',course:'Yau: read the bar height.'},
 {stage:3,eye:'What we ship',h:'Three screens. <em>Two sprints.</em>',lede:'Zero shown first on the meal page. A "Reorder with Zero" button on home. Fruit at the top of the add-on rail in the basket.',layout:'hidden',
  note:'Three changes to screens we already own. Two sprints. No new partner contracts.',course:'Session 3: Z-pattern, most important screen first.'},
 {single:'ov',stage:3,ov:'ship',layout:'hidden',src:'Concept screens · prices Glovo Madrid · Glovo fee assumed 30 % · effort estimates are ours',
  note:'Screen one and two in sprint one, screen three in sprint two. Every row is same money or more, for the partner and for us.',course:'Gestalt: similarity, three cards, same shape, same job.'},
 {stage:3,eye:'Fair by design',h:'Healthy, not <em>sneaky.</em>',lede:'Nothing pre-ticked. Same-size buttons. Ads say ad. The law already says so, and so does our brand.',layout:'hidden',
  note:'We are not tricking anyone. The user always chooses. We only make the good choice visible.',course:'EU CRD art. 22, DSA arts. 25 and 26.'},
 {single:'ov',stage:3,ov:'fair',layout:'hidden',src:'EU Consumer Rights Directive art. 22 · Digital Services Act arts. 25 and 26',
  note:'Three rules, three screens. Compliance is built in, not bolted on.',course:'Session 1 AI policy mindset: be transparent about what the system does.'},
 {stage:3,eye:'Scale',h:'Only a few need to <em>say yes.</em>',lede:'One million orders a month. If <b>2 in 100</b> switch to Zero and 5 in 100 add a side: <b>336 kg</b> less sugar, <b>€45,500</b> more for the partner, <b>€19,500</b> more for Glovo.',stat:['more for Glovo, per month','€19,500','green'],key:[['sugary','has a sugary drink'],['zero','picked Zero instead'],['gold','added fruit or veg'],['other','1 dot = 1,000 orders']],howto:'one dot = 1,000 orders',layout:'orders',src:'OUR GUESSES, NOT DATA: 1,000,000 orders · 40 % include a sugary drink · 2 % of those pick Zero · 5 % add a €1.30 side · 30 % commission · the test replaces these',
  note:'These percentages are our guesses. Even so: two in a hundred switch, and that is 336 kilos of sugar a month, forty-five thousand euros for the partner, nineteen for us.',course:'Yau: unit charts make scale felt. Session 7: say what is assumed.'},
 {stage:4,eye:'The experiment',h:'A/B it for <em>four weeks.</em>',lede:'Half of Madrid orders get the three screens. Half don\'t. Basket value is the guardrail.',layout:'hidden',
  note:'Standard A/B. Four weeks, Madrid, fifty-fifty. If basket value drops we stop.',course:'Session 7: resolution = one decision to ask for.'},
 {single:'ov',stage:4,ov:'experiment',layout:'hidden',
  note:'Hypothesis, metrics, guardrails, and what we do not know. Then the guesses become numbers. Questions.',course:'Session 7: say what the data cannot tell you. PICA, Context.'},
 {single:'ov',stage:4,ov:()=>OV.behind([['Characters','Glovo product team, McDonald\'s, a million Madrid orders'],['Setting','260 menu items, measured in sugar cubes'],['Conflict','Healthy usually shrinks the basket'],['Resolution','Three screens, same basket, four-week A/B']]),layout:'hidden',src:'Big Idea: Knaflic · PICA: Lea Pica · arc: Dykes · unit: Yau · how to read: Jones · colour: Strachnyi · moving marks: Rosling · Gestalt: Session 2',
  note:'Hero: our own team. Guide: the data. Twenty seconds, then questions.',course:'The seven Book of the Day picks, each used once on purpose.'},
]'''

def build():
    t = THEME
    html = (TEMPLATE6.replace('/*TITLE*/', t['name']).replace('/*FONTS*/', t['fonts'])
      .replace('/*BG*/', t['bg']).replace('/*FG2*/', t['fg2']).replace('/*FG*/', t['fg']).replace('/*MUTED*/', t['muted']).replace('/*RULE*/', t['rule']).replace('/*ACCENT*/', t['accent'])
      .replace('/*C_OVER*/', t['hex']['over']).replace('/*C_SUGAR*/', t['hex']['sugar']).replace('/*C_ZERO*/', t['hex']['zero']).replace('/*C_LOSS*/', t['hex']['loss'])
      .replace('/*DISPLAY*/', t['display']).replace('/*BODY*/', t['body']).replace('/*MONO*/', t['mono']).replace('/*SCHEME*/', t['scheme'])
      .replace('/*THEME*/', json.dumps({k:v for k,v in t.items() if k!='fonts'})).replace('/*BEATS*/', BEATS).replace('/*DATA*/', DATA))
    (HERE / 'ship-the-healthy-default-v6.html').write_text(html); print('ship-the-healthy-default-v6.html', len(html), 'bytes')

if __name__=='__main__':
    build()
