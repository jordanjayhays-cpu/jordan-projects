"""Build the 3-presenter SAFE deck (14 slides) from sugar-with-that-SAFE-final.html.
Adds: three clean transition slides with an animated visual each, two new content slides,
renumbered eyebrows, 14 speaker notes. Everything else is untouched."""
import re, pathlib
SRC = pathlib.Path('sugar-with-that-SAFE-final.html'); OUT = pathlib.Path('sugar-with-that-SAFE-3parts.html')
html = SRC.read_text()

def rep(old, new, count=1):
    global html
    n = html.count(old); assert n == count, (n, old[:80])
    html = html.replace(old, new)

# ---------- CSS ----------
rep("@media (prefers-reduced-motion:no-preference){.slide.active .chart{animation:fade .35s ease-out}}", """/* transition slides: clean background, one word, one visual */
.tslide .tnum{position:absolute;left:110px;top:110px;font-family:var(--font-mono);font-size:19px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.tslide .trule{position:absolute;left:110px;top:150px;width:560px;height:14px;background:var(--ink)}
.tslide .thuge{position:absolute;left:110px;top:190px;width:600px;font-family:var(--font-display);font-weight:900;font-size:170px;line-height:.92;letter-spacing:-.045em;margin:0}
.tslide .tlede{position:absolute;left:110px;top:620px;width:540px;font-size:30px;line-height:1.35;margin:0}
.tslide .tlede strong{font-weight:800}
.tslide .twho{position:absolute;left:110px;top:900px;font-family:var(--font-mono);font-size:17px;font-weight:700;letter-spacing:.12em;color:var(--muted);text-transform:uppercase}
.tslide .tviz{position:absolute;left:760px;top:60px;width:1100px;height:940px}
.tslide .tviz svg{width:100%;height:100%;display:block;overflow:visible}
.tslide.pink .trule,.tslide.pink .thuge{color:var(--pink);background-color:transparent}.tslide.pink .trule{background:var(--pink)}
.tslide.blue .thuge{color:var(--blue)}.tslide.blue .trule{background:var(--blue)}
.tcap{font-size:21px;fill:var(--muted)}
.progress .seg{width:22px}
@media (prefers-reduced-motion:no-preference){.slide.active .chart{animation:fade .35s ease-out}}""")

# ---------- slides ----------
T1 = """
<!-- T1 -->
<section class="slide tslide" data-i="1">
  <div class="tnum">Part 1 of 3 · The menu</div>
  <div class="trule"></div>
  <h1 class="thuge">The menu.</h1>
  <p class="tlede"><strong>260 items, one dot each.</strong> Before anyone bans a menu, we should know what is on it.</p>
  <div class="twho">Presenter 1 · 4 slides</div>
  <div class="tviz" id="t1"></div>
</section>
"""
S4 = """
<!-- 4 (new) -->
<section class="slide" data-i="3">
  <div class="panel">
    <div class="eyebrow">Part 1 · The menu · <b>Calories</b></div>
    <div class="bar" style="margin-top:18px"></div>
    <h1 class="sm">21 drinks and desserts out-calorie a Big Mac</h1>
    <p class="lede">A Big Mac is 530 calories. A large chocolate shake is 850. The heaviest drink on the menu, a medium McFlurry, is 930.</p>
    <div class="stat"><span class="lbl">Drinks heavier than a Big Mac</span><span class="num">21</span></div>
    <div class="key">
      <div class="kh">KEY</div>
      <div class="row"><span class="sw" style="background:var(--pink)"></span><span>Drinks and desserts</span></div>
      <div class="row"><span class="sw" style="background:var(--grey)"></span><span>Food</span></div>
      <div class="row"><span class="sw line" style="background:var(--ink)"></span><span>Big Mac, 530 calories</span></div>
      <div class="howto">Each square is one menu item, placed by its calories. Bigger square, more sugar.</div>
    </div>
  </div>
  <div class="chart" id="c4b"></div>
</section>
"""
T2 = """
<!-- T2 -->
<section class="slide tslide pink" data-i="4">
  <div class="tnum">Part 2 of 3 · Sugar</div>
  <div class="trule"></div>
  <h1 class="thuge">Sugar.</h1>
  <p class="tlede"><strong>One medium Coke is 14 sugar cubes.</strong> A whole day's limit is 12. The problem is in the cup.</p>
  <div class="twho">Presenter 2 · 5 slides</div>
  <div class="tviz" id="t2"></div>
</section>
"""
S8 = """
<!-- 8 (new) -->
<section class="slide" data-i="7">
  <div class="panel">
    <div class="eyebrow">Part 2 · Sugar · <b>By category</b></div>
    <div class="bar" style="margin-top:18px"></div>
    <h1 class="sm">Shakes and coffees carry the most sugar</h1>
    <p class="lede">The average shake holds 78g, a day and a half of sugar. The average coffee drink holds 40g, more than the average soft drink at 28g. Food averages under 10g.</p>
    <div class="stat"><span class="lbl">Average shake</span><span class="num">78g</span></div>
    <div class="key">
      <div class="kh">KEY</div>
      <div class="row"><span class="sw sq" style="background:var(--pink)"></span><span>One sugar cube, 4g</span></div>
      <div class="row"><span class="sw sq" style="background:var(--grey)"></span><span>One sugar cube in a food category</span></div>
      <div class="row"><span class="sw line" style="background:var(--ink)"></span><span>Daily limit, 50g, about 12 cubes</span></div>
      <div class="howto">Each row is the average item in that category, drawn as sugar cubes.</div>
    </div>
  </div>
  <div class="chart" id="c8b"></div>
</section>
"""
T3 = """
<!-- T3 -->
<section class="slide tslide blue" data-i="9">
  <div class="tnum">Part 3 of 3 · Salt</div>
  <div class="trule"></div>
  <h1 class="thuge">Salt.</h1>
  <p class="tlede"><strong>48 dishes carry half a day of salt in one serving.</strong> On the plate, sugar is not the problem. Salt is.</p>
  <div class="twho">Presenter 3 · 5 slides</div>
  <div class="tviz" id="t3"></div>
</section>
"""
# insert transitions + new slides at the right spots
rep("\n<!-- 2 -->\n", "\n" + T1 + "\n<!-- 3 -->\n")
rep("\n<!-- 3 -->\n<section class=\"slide\" data-i=\"2\">", "\n<!-- 3 -->\n<section class=\"slide\" data-i=\"2\">")  # sanity: old slide 2 anchor exists
# old slide 3 (sugar strip) starts with eyebrow Serving 2 of 6 — put S4 + T2 before it
rep("\n<!-- 3 -->\n<section class=\"slide\" data-i=\"2\">\n  <div class=\"panel\">\n    <div class=\"eyebrow\">Serving 2 of 6", "\n" + S4 + T2 + "\n<!-- 6 -->\n<section class=\"slide\" data-i=\"5\">\n  <div class=\"panel\">\n    <div class=\"eyebrow\">Serving 2 of 6")
# old slide 5 (swaps, Serving 5 of 6) : put S8 before it
rep("<section class=\"slide\" data-i=\"5\">\n  <div class=\"panel\">\n    <div class=\"eyebrow\">Serving 5 of 6", S8 + "\n<!-- 9 -->\n<section class=\"slide\" data-i=\"8\">\n  <div class=\"panel\">\n    <div class=\"eyebrow\">Serving 5 of 6")
# old slide 4 (salt, Serving 4 of 6) : move after swaps, with T3 before it
m = re.search(r"\n<!-- 5 -->\n<section class=\"slide\" data-i=\"4\">.*?</section>\n", html, re.S); assert m
salt_slide = m.group(0); html = html.replace(salt_slide, "\n")
rep("\n<!-- 7 -->\n", "\n" + T3 + salt_slide + "\n<!-- 12 -->\n")

MEALS = [
 ("Keep the Big Mac. Change the cup.", "A Big Mac meal is 16 cubes of sugar. 14 of them are in the medium Coke. Small fries and a Diet Coke keep the burger and drop 310 calories.", "m1"),
 ("Grilled, not crispy. Same bun.", "The crispy chicken meal is 16 cubes and 1,050 calories. Grilled chicken, small fries and a Diet Coke: 2 cubes and 580 calories.", "m2"),
 ("Keep the latte. Lose the syrup.", "A medium caramel latte is 12 cubes on its own. A plain latte is 4. Egg McMuffin instead of sausage with egg saves another 150 calories.", "m3"),
]
S14 = ""
for n,(h,l,cid) in enumerate(MEALS,1):
    S14 += f"""
<!-- meal {n} -->
<section class="slide" data-i="0">
  <div class="panel">
    <div class="eyebrow">Part 3 · What to order · <b>Example {n} of 3</b></div>
    <div class="bar" style="margin-top:18px"></div>
    <h1 class="sm">{h}</h1>
    <p class="lede">{l}</p>
    <div class="stat"><span class="lbl">Sugar cubes saved</span><span class="num" id="{cid}-saved">–</span></div>
    <div class="key">
      <div class="kh">KEY</div>
      <div class="row"><span class="sw" style="background:var(--grey-deep)"></span><span>What people order</span></div>
      <div class="row"><span class="sw" style="background:var(--gold)"></span><span>Order this instead</span></div>
      <div class="row"><span class="sw sq" style="background:var(--pink)"></span><span>One sugar cube, 4g. Pink fill = sugar inside.</span></div>
      <div class="howto">Meals follow McDonald's own combos: main item, side, drink. Nutrition from the same 260-item dataset.</div>
    </div>
  </div>
  <div class="chart" id="{cid}"></div>
</section>
"""
rep("\n<!-- 9 (new) -->\n", "\n" + S14 + "\n<!-- closer -->\n")
rep('<div class="twho">Presenter 3 · 5 slides</div>', '<div class="twho">Presenter 3 · 8 slides</div>')

# ---------- eyebrows ----------
rep("Serving 1 of 6 · <b>The menu</b>", "Part 1 · The menu · <b>Categories</b>")
rep("Serving 2 of 6 · <b>Sugar · The finding</b>", "Part 2 · Sugar · <b>The finding</b>")
rep("Serving 3 of 6 · <b>Size</b>", "Part 2 · Sugar · <b>Size</b>")
rep("Serving 5 of 6 · <b>Swaps</b>", "Part 2 · Sugar · <b>Swaps</b>")
rep("Serving 4 of 6 · <b>Salt</b>", "Part 3 · Salt · <b>The plate</b>")
rep("Serving 6 of 6 · <b>Policy</b>", "Part 3 · Policy · <b>Four measures</b>")
rep("After the meal · <b>Recommendation</b>", "Part 3 · Policy · <b>Limits and sources</b>")
assert "Serving " not in html.replace("Serving size","")

# ---------- notes ----------
m = re.search(r"const NOTES = \[\n.*?\n\];", html, re.S); assert m
NOTES = r'''const NOTES = [
 ["Councillors, before you ban a menu, meet it. Two hundred and sixty items, one dot each. By the end of part two you will see that most of them are not your problem.", "<b>Session 7:</b> setting + hook, name the hero and the stakes. If the ban is hypothetical, say so out loud here."],
 ["(Transition, ten seconds.) Part one: the menu. Two hundred and sixty dots. Watch them settle. Everything we show today is one of these dots.", "<b>Brent Dykes:</b> setting. <b>Session 2, Gestalt:</b> similarity, one mark per item."],
 ["Hundred and fifty-seven of 260 are coffees, sodas, shakes or desserts. Twenty-one of those out-calorie a Big Mac. Every dot here is in our dashboard, filter by category. (Show the dashboard for 30 seconds, then return.)", "<b>Ben Jones, Learning to See Data:</b> one mark per item · dashboard cue (50% of the grade)"],
 ["Here is the Big Mac line: 530 calories. Twenty-one pink squares sit to the right of it. Those are drinks and desserts. A large chocolate shake is 850. A medium McFlurry, 930. Hand over to presenter two.", "<b>Session 3:</b> one reference line, one highlight colour · <b>Knaflic:</b> annotate the line, not the chart"],
 ["(Transition, ten seconds.) Part two: sugar. One medium Coke. Fourteen cubes. The dashed line is a whole day. Watch the cubes pass it.", "<b>Nathan Yau, unit charts:</b> make the count felt · <b>Hans Rosling:</b> a physical prop the audience can picture"],
 ["(Slow down, pause before the line.) Sixty-two items break the daily limit in one serving. Every single one is a drink or a dessert. The sweetest thing on a plate is thirty-two grams. This is where a ban on food stops making sense.", "<b>Session 7:</b> the aha, pause before the headline · <b>Session 3:</b> highlight palette"],
 ["Small, thirty-six grams. Medium, forty-eight. Large, fifty-seven. The average Large breaks the daily limit by itself. Read the line, the cup shape is decoration.", "<b>Session 3:</b> pictograms only when the fill line carries the number"],
 ["Now by category. The average shake is seventy-eight grams, nineteen cubes. The average coffee drink is forty grams, more than the average soft drink. Every food category stays under ten. Sugar is a drinks problem.", "<b>Nathan Yau, Visualize This:</b> unit chart, one cube is four grams · <b>Session 2:</b> proximity groups the rows"],
 ["No new menu needed. Grilled instead of crispy saves eighty to one-sixty calories on all thirteen dishes. Small instead of Large: median one-thirty calories and twenty-one grams of sugar. Hand over to presenter three.", "<b>Cole Nussbaumer Knaflic:</b> slope charts for before/after"],
 ["(Transition, ten seconds.) Part three: salt. Forty-eight dishes. Each blue dot is one dish with half a day of salt in a single serving. All of them are food.", "<b>Kate Strachnyi, ColorWise:</b> blue for salt, pink for sugar, never swapped"],
 ["Food barely carries sugar. But forty-eight dishes hold half a day's sodium. The more calories on the plate, the saltier. Forty nuggets: a day and a half of salt.", "<b>Session 7, Challenger lesson:</b> no jargon, say it in words · <b>Kate Strachnyi, ColorWise:</b> blue/pink is colourblind-safe"],
 ["Four measures instead of a ban. Small as the default drink. Sugar warning at fifty grams. Sodium warning at eleven-fifty. Grilled listed first. Together they touch 110 items and leave 150 alone. (Read only the Measure column.)", "<b>Nathan Yau, Visualize This:</b> unit charts make counts felt"],
 ["What this data cannot tell us: one chain, US menu, no sales volumes, thresholds are ours. Sources on screen. We built the charts with D3 and the dashboard in Looker Studio, with AI assistance.", "<b>Rubric:</b> limitations and sources stated · <b>Session 9 & 10:</b> honesty about the data"],
 ["Example one, the Big Mac meal. Sixteen cubes of sugar. Look where they sit: two in the burger, none in the fries, fourteen in the cup. Keep the Big Mac. Small fries, Diet Coke. Two cubes, three hundred fewer calories.", "<b>Knaflic:</b> before/after side by side · <b>Yau:</b> unit cubes under each item · <b>Session 2:</b> proximity, the cubes sit under the item they belong to"],
 ["Example two, the crispy chicken meal. Same sixteen cubes, same cup. Grilled instead of crispy is on the menu already: one hundred and sixty calories off the sandwich alone. With small fries and a Diet Coke, the meal nearly halves.", "<b>Session 7:</b> make the solution concrete · the 'grilled listed first' measure in one picture"],
 ["Example three, breakfast. The caramel latte is twelve cubes before you add any food. A plain latte is four. Swap sausage with egg for an Egg McMuffin and you save another hundred and fifty calories. The coffee counter is where the sugar hides.", "<b>Session 3:</b> pink fill means sugar inside, nothing else is coloured · <b>Rosling:</b> an object the audience can picture"],
 ["We are asking for one decision: a six-month pilot, two or three chains, Small as the default drink. Measure what people actually order. Then decide on a ban. Thank you. Questions.", "<b>Session 7:</b> resolution = one decision to ask for · <b>Brent Dykes:</b> next steps"]
];'''
html = html.replace(m.group(0), NOTES)

# ---------- charts ----------
rep("/* ---------- navigation ---------- */", r"""/* ---------- new: 4b calories strip ---------- */
(function(){
  const s = svg('c4b');
  const x = d3.scaleLinear().domain([0,1900]).range([60,1110]);
  const sz = d3.scaleSqrt().domain([0,130]).range([6,22]);
  const nodes = DATA.map(d=>({d,x:x(d.cal),y:470,s:sz(d.sugar)}));
  d3.forceSimulation(nodes).force('x',d3.forceX(n=>x(n.d.cal)).strength(1)).force('y',d3.forceY(470).strength(.08))
    .force('c',d3.forceCollide(n=>n.s/2+1.5).iterations(3)).stop().tick(260);
  const bm = DATA.find(d=>d.item==='Big Mac');
  s.append('line').attr('x1',x(bm.cal)).attr('x2',x(bm.cal)).attr('y1',120).attr('y2',880).attr('stroke',INK).attr('stroke-width',2);
  s.append('text').attr('x',x(bm.cal)+12).attr('y',120).attr('class','ann-t').text('Big Mac');
  s.append('text').attr('x',x(bm.cal)+12).attr('y',146).attr('class','ann-s').text(bm.cal+' calories');
  s.selectAll('rect').data(nodes).join('rect')
    .attr('x',n=>n.x-n.s/2).attr('y',n=>n.y-n.s/2).attr('width',n=>n.s).attr('height',n=>n.s).attr('rx',2)
    .attr('fill',n=>isDrink(n.d)?PINK:GREY);
  const ax = s.append('g').attr('class','axis').attr('transform','translate(0,890)').call(d3.axisBottom(x).tickValues([0,500,1000,1500]).tickFormat(d3.format(',')).tickSize(0));
  ax.select('.domain').remove();
  s.append('text').attr('x',1110).attr('y',930).attr('text-anchor','end').attr('class','ann-s').text('Calories per item');
  const over = nodes.filter(n=>isDrink(n.d)&&n.d.cal>bm.cal);
  const top = over.reduce((a,b)=>b.d.cal>a.d.cal?b:a);
  s.append('path').attr('d',`M ${top.x} ${top.y-top.s/2-4} C ${top.x} ${top.y-120}, ${top.x+40} ${top.y-200}, ${top.x+40} ${top.y-250}`).attr('fill','none').attr('stroke',INK).attr('stroke-width',1.8);
  s.append('text').attr('x',top.x+20).attr('y',top.y-290).attr('text-anchor','start').attr('class','ann-t').text(top.d.item.replace(/’/g,"'"));
  s.append('text').attr('x',top.x+20).attr('y',top.y-265).attr('text-anchor','start').attr('class','ann-s').text(`${top.d.cal} calories, ${(top.d.cal/bm.cal).toFixed(1)} Big Macs`);
  const big = nodes.reduce((a,b)=>b.d.cal>a.d.cal?b:a);
  s.append('text').attr('x',big.x).attr('y',big.y+big.s/2+150).attr('text-anchor','end').attr('class','ann-t').text('40 Chicken McNuggets');
  s.append('text').attr('x',big.x).attr('y',big.y+big.s/2+175).attr('text-anchor','end').attr('class','ann-s').text(`${d3.format(',')(big.d.cal)} calories, the heaviest item`);
  s.append('path').attr('d',`M ${big.x} ${big.y+big.s/2+4} L ${big.x} ${big.y+big.s/2+120}`).attr('fill','none').attr('stroke',INK).attr('stroke-width',1.8);
  s.append('text').attr('x',x(bm.cal)+12).attr('y',880).attr('class','ann-t').attr('fill',PINK).text(`${over.length} drinks and desserts past the line`);
})();

/* ---------- new: 8b sugar cubes by category ---------- */
(function(){
  const s = svg('c8b');
  const cats = d3.groups(DATA,d=>d.cat).map(([cat,items])=>({cat,n:items.length,avg:d3.mean(items,d=>d.sugar)})).sort((a,b)=>b.avg-a.avg);
  const CUBE=4, cw=30, gap=4, x0=330, y0=130, rowH=84;
  const BG=col('--bg');
  const x = c => x0 + c*(cw+gap);
  const limit = 50/CUBE;
  const yEnd = y0+cats.length*rowH-rowH+cw+20;
  s.append('line').attr('x1',x(limit)-gap/2).attr('x2',x(limit)-gap/2).attr('y1',y0-50).attr('y2',yEnd).attr('stroke',INK).attr('stroke-width',2).attr('stroke-dasharray','8 7');
  cats.forEach((c,i)=>{
    const y = y0+i*rowH, cubes = c.avg/CUBE, full = Math.floor(cubes), frac = cubes-full;
    const drink = DR.has(c.cat), col = drink?PINK:GREYD;
    s.append('text').attr('x',x0-22).attr('y',y+cw/2+7).attr('text-anchor','end').attr('class','lbl-cat').text(c.cat);
    s.append('text').attr('x',x0-22).attr('y',y+cw/2+30).attr('text-anchor','end').attr('class','lbl-n').attr('font-size',16).text(c.n+' items');
    for(let k=0;k<full;k++) s.append('rect').attr('x',x(k)).attr('y',y).attr('width',cw).attr('height',cw).attr('rx',4).attr('fill',col);
    if(frac>0.12) s.append('rect').attr('x',x(full)).attr('y',y).attr('width',cw*frac).attr('height',cw).attr('rx',4).attr('fill',col);
    s.append('text').attr('x',x(Math.ceil(cubes))+14).attr('y',y+cw/2+7).attr('class','ann-t').attr('fill',drink?PINK:INK).attr('stroke',BG).attr('stroke-width',10).attr('paint-order','stroke').text(`${Math.round(c.avg)}g`);
    s.append('text').attr('x',x(Math.ceil(cubes))+14+(c.avg>=10?62:50)).attr('y',y+cw/2+7).attr('class','ann-s').attr('stroke',BG).attr('stroke-width',10).attr('paint-order','stroke').text(`${cubes.toFixed(0)} cube${Math.round(cubes)===1?'':'s'}`);
  });
  s.append('text').attr('x',x(limit)+6).attr('y',y0-58).attr('class','ann-t').text('Daily limit · 50g');
  s.append('text').attr('x',x(limit)+6).attr('y',y0-34).attr('class','ann-s').text('about 12 cubes');
  const ax = s.append('g').attr('class','axis').attr('transform',`translate(0,${yEnd+14})`);
  [0,5,10,15,20].forEach(v=>{ ax.append('text').attr('x',x(v)).attr('y',18).attr('text-anchor','middle').text(v); });
  s.append('text').attr('x',x(20)+40).attr('y',yEnd+32).attr('class','ann-s').attr('text-anchor','start').text('sugar cubes');
  s.append('text').attr('x',x0).attr('y',yEnd+62).attr('class','ann-s').text('Average sugar per item · 1 cube = 4g');
})();

/* ---------- meal slides: icons + cubes per item ---------- */
(function(){
  const by = new Map(DATA.map(d=>[d.item,d]));
  const get = n => { const d=by.get(n); if(!d) throw new Error('missing '+n); return d; };
  const WHITE='#FFFFFF';
  const ICON = {
    burger(g,x,y,big){ // x,y = centre bottom
      const w=200;
      const bun=(yy,h,top)=>{ if(top){ g.append('path').attr('d',`M ${x-w/2} ${yy} A ${w/2} ${h} 0 0 1 ${x+w/2} ${yy} Z`).attr('fill',GREYS).attr('stroke',INK).attr('stroke-width',3);
          [-50,-15,20,55].forEach(dx=>g.append('ellipse').attr('cx',x+dx).attr('cy',yy-h*0.55).attr('rx',6).attr('ry',3.5).attr('fill',INK)); }
        else g.append('rect').attr('x',x-w/2).attr('y',yy-h).attr('width',w).attr('height',h).attr('rx',12).attr('fill',GREYS).attr('stroke',INK).attr('stroke-width',3); };
      const patty=yy=>g.append('rect').attr('x',x-w/2+6).attr('y',yy-26).attr('width',w-12).attr('height',26).attr('rx',8).attr('fill',GREYD).attr('stroke',INK).attr('stroke-width',3);
      const lettuce=yy=>g.append('path').attr('d',`M ${x-w/2-6} ${yy} ${d3.range(0,10).map(i=>`q 10 -12 21 0`).join(' ')}`).attr('fill','none').attr('stroke',INK).attr('stroke-width',3);
      let yy=y; bun(yy,34,false); yy-=34; patty(yy); yy-=26; lettuce(yy); yy-=6;
      if(big){ bun(yy,24,false); yy-=24; patty(yy); yy-=26; lettuce(yy); yy-=6; }
      bun(yy,60,true);
    },
    chicken(g,x,y,crispy){
      const w=200;
      g.append('rect').attr('x',x-w/2).attr('y',y-34).attr('width',w).attr('height',34).attr('rx',12).attr('fill',GREYS).attr('stroke',INK).attr('stroke-width',3);
      const py=y-34;
      if(crispy){ const pts=[]; for(let i=0;i<=20;i++){ const px=x-w/2+4+i*(w-8)/20; pts.push([px, py-30+(i%2?8:0)]); } pts.push([x+w/2-4,py],[x-w/2+4,py]);
        g.append('polygon').attr('points',pts.map(p=>p.join(',')).join(' ')).attr('fill',GREYD).attr('stroke',INK).attr('stroke-width',3).attr('stroke-linejoin','round'); }
      else { g.append('rect').attr('x',x-w/2+6).attr('y',py-26).attr('width',w-12).attr('height',26).attr('rx',8).attr('fill',GREYD).attr('stroke',INK).attr('stroke-width',3);
        [-50,-10,30].forEach(dx=>g.append('line').attr('x1',x+dx).attr('x2',x+dx+22).attr('y1',py-20).attr('y2',py-6).attr('stroke',INK).attr('stroke-width',3)); }
      const ly=py-32; g.append('path').attr('d',`M ${x-w/2-6} ${ly} ${d3.range(0,10).map(()=>`q 10 -12 21 0`).join(' ')}`).attr('fill','none').attr('stroke',INK).attr('stroke-width',3);
      g.append('path').attr('d',`M ${x-w/2} ${ly-6} A ${w/2} 56 0 0 1 ${x+w/2} ${ly-6} Z`).attr('fill',GREYS).attr('stroke',INK).attr('stroke-width',3);
    },
    muffin(g,x,y,sausage){
      const w=190;
      g.append('rect').attr('x',x-w/2).attr('y',y-30).attr('width',w).attr('height',30).attr('rx',10).attr('fill',GREYS).attr('stroke',INK).attr('stroke-width',3);
      let yy=y-30;
      if(sausage){ g.append('rect').attr('x',x-w/2+8).attr('y',yy-24).attr('width',w-16).attr('height',24).attr('rx',8).attr('fill',GREYD).attr('stroke',INK).attr('stroke-width',3); yy-=24; }
      g.append('ellipse').attr('cx',x).attr('cy',yy-14).attr('rx',w/2-4).attr('ry',16).attr('fill',WHITE).attr('stroke',INK).attr('stroke-width',3);
      g.append('circle').attr('cx',x+10).attr('cy',yy-16).attr('r',16).attr('fill',GREY).attr('stroke',INK).attr('stroke-width',3); yy-=28;
      g.append('rect').attr('x',x-w/2+6).attr('y',yy-18).attr('width',w-12).attr('height',18).attr('rx',4).attr('fill',GREYS).attr('stroke',INK).attr('stroke-width',3); yy-=18; // cheese
      g.append('path').attr('d',`M ${x-w/2} ${yy} L ${x-w/2} ${yy-22} A ${w/2} 26 0 0 1 ${x+w/2} ${yy-22} L ${x+w/2} ${yy} Z`).attr('fill',GREYS).attr('stroke',INK).attr('stroke-width',3);
    },
    fries(g,x,y,small){
      const k=small?0.72:1, bw=150*k, bh=110*k;
      const sticks=small?5:7;
      for(let i=0;i<sticks;i++){ const sx=x-bw/2+14*k+i*(bw-28*k)/(sticks-1); const h=(120+(i%3)*18)*k; g.append('rect').attr('x',sx-9*k).attr('y',y-bh-h+20*k).attr('width',18*k).attr('height',h).attr('rx',4).attr('fill',GREYS).attr('stroke',INK).attr('stroke-width',3); }
      g.append('path').attr('d',`M ${x-bw/2} ${y-bh} L ${x-bw/2+10*k} ${y} L ${x+bw/2-10*k} ${y} L ${x+bw/2} ${y-bh} Z`).attr('fill',GREYD).attr('stroke',INK).attr('stroke-width',3);
      g.append('text').attr('x',x).attr('y',y-bh/2+8).attr('text-anchor','middle').attr('font-size',20*k).attr('font-weight',800).attr('fill',WHITE).text(small?'S':'M');
    },
    cup(g,x,y,sugar){
      const h=200, tw=150, bw=110;
      const poly=[[x-tw/2,y-h],[x+tw/2,y-h],[x+bw/2,y],[x-bw/2,y]];
      g.append('polygon').attr('points',poly.map(p=>p.join(',')).join(' ')).attr('fill',sugar?PINKF:WHITE).attr('stroke',INK).attr('stroke-width',3);
      if(sugar){ g.append('polygon').attr('points',[[x-tw/2+2,y-h+20],[x+tw/2-2,y-h+20],[x+bw/2-2,y-2],[x-bw/2+2,y-2]].map(p=>p.join(',')).join(' ')).attr('fill',PINK).attr('opacity',.85); }
      g.append('line').attr('x1',x-tw/2-10).attr('x2',x+tw/2+10).attr('y1',y-h).attr('y2',y-h).attr('stroke',INK).attr('stroke-width',7);
      g.append('line').attr('x1',x+20).attr('x2',x+55).attr('y1',y-h+30).attr('y2',y-h-60).attr('stroke',INK).attr('stroke-width',6).attr('stroke-linecap','round');
      g.append('text').attr('x',x).attr('y',y-h/2+8).attr('text-anchor','middle').attr('font-size',22).attr('font-weight',800).attr('fill',sugar?WHITE:INK).text(sugar?'COKE':'DIET');
    },
    latte(g,x,y,syrup){
      const w=140, h=150;
      g.append('rect').attr('x',x-w/2).attr('y',y-h).attr('width',w).attr('height',h).attr('rx',14).attr('fill',syrup?PINKF:WHITE).attr('stroke',INK).attr('stroke-width',3);
      g.append('path').attr('d',`M ${x+w/2} ${y-h+30} a 34 34 0 0 1 0 68`).attr('fill','none').attr('stroke',INK).attr('stroke-width',6);
      g.append('ellipse').attr('cx',x).attr('cy',y-h).attr('rx',w/2).attr('ry',14).attr('fill',WHITE).attr('stroke',INK).attr('stroke-width',3);
      if(syrup){ g.append('path').attr('d',`M ${x-50} ${y-h-4} q 12 -14 25 0 t 25 0 t 25 0 t 25 0`).attr('fill','none').attr('stroke',PINK).attr('stroke-width',5); g.append('text').attr('x',x).attr('y',y-h/2+10).attr('text-anchor','middle').attr('font-size',18).attr('font-weight',800).attr('fill',PINK).text('CARAMEL'); }
      else g.append('text').attr('x',x).attr('y',y-h/2+10).attr('text-anchor','middle').attr('font-size',18).attr('font-weight',800).attr('fill',INK).text('LATTE');
      [-30,0,30].forEach(dx=>g.append('path').attr('d',`M ${x+dx} ${y-h-30} q 8 -10 0 -20`).attr('fill','none').attr('stroke',GREYD).attr('stroke-width',3));
    },
    hash(g,x,y){
      g.append('ellipse').attr('cx',x).attr('cy',y-45).attr('rx',95).attr('ry',45).attr('fill',GREYS).attr('stroke',INK).attr('stroke-width',3);
      d3.range(14).forEach(i=>g.append('circle').attr('cx',x-70+((i*37)%140)).attr('cy',y-45-20+((i*23)%40)).attr('r',3).attr('fill',GREYD));
    }
  };
  const meals = {
    m1:{ before:[['Big Mac',g=>ICON.burger(g,0,0,true)],['Medium French Fries',g=>ICON.fries(g,0,0,false)],['Coca-Cola Classic (Medium)',g=>ICON.cup(g,0,0,true)]],
         after:[['Big Mac',g=>ICON.burger(g,0,0,true)],['Small French Fries',g=>ICON.fries(g,0,0,true)],['Diet Coke (Medium)',g=>ICON.cup(g,0,0,false)]] },
    m2:{ before:[['Premium Crispy Chicken Classic Sandwich',g=>ICON.chicken(g,0,0,true)],['Medium French Fries',g=>ICON.fries(g,0,0,false)],['Coca-Cola Classic (Medium)',g=>ICON.cup(g,0,0,true)]],
         after:[['Premium Grilled Chicken Classic Sandwich',g=>ICON.chicken(g,0,0,false)],['Small French Fries',g=>ICON.fries(g,0,0,true)],['Diet Coke (Medium)',g=>ICON.cup(g,0,0,false)]] },
    m3:{ before:[['Sausage McMuffin with Egg',g=>ICON.muffin(g,0,0,true)],['Hash Brown',g=>ICON.hash(g,0,0)],['Caramel Latte (Medium)',g=>ICON.latte(g,0,0,true)]],
         after:[['Egg McMuffin',g=>ICON.muffin(g,0,0,false)],['Hash Brown',g=>ICON.hash(g,0,0)],['Latte (Medium)',g=>ICON.latte(g,0,0,false)]] }
  };
  const short = n => n.replace('Coca-Cola Classic (Medium)','Medium Coke').replace('Diet Coke (Medium)','Medium Diet Coke').replace('Medium French Fries','Medium fries').replace('Small French Fries','Small fries').replace('Premium Crispy Chicken Classic Sandwich','Crispy chicken sandwich').replace('Premium Grilled Chicken Classic Sandwich','Grilled chicken sandwich').replace('Caramel Latte (Medium)','Medium caramel latte').replace('Latte (Medium)','Medium latte');
  const CU=18, G=3, PER=7;
  const cubesAt=(s,x,y,n,col)=>{ const full=Math.floor(n), frac=n-full; let k=0;
    for(;k<full;k++) s.append('rect').attr('x',x+(k%PER)*(CU+G)).attr('y',y+Math.floor(k/PER)*(CU+G)).attr('width',CU).attr('height',CU).attr('rx',3).attr('fill',col);
    if(frac>.12) s.append('rect').attr('x',x+(k%PER)*(CU+G)).attr('y',y+Math.floor(k/PER)*(CU+G)).attr('width',CU*frac).attr('height',CU).attr('rx',3).attr('fill',col); };
  Object.entries(meals).forEach(([id,m])=>{
    const s = svg(id);
    const tot = items => ({cal:d3.sum(items,([n])=>get(n).cal), sug:d3.sum(items,([n])=>get(n).sugar), sod:d3.sum(items,([n])=>get(n).sodium)});
    const B=tot(m.before), A=tot(m.after);
    [['before',GREYD,'WHAT PEOPLE ORDER',m.before,B,0],['after',GOLD,'ORDER THIS INSTEAD',m.after,A,480]].forEach(([k,c,lbl,items,T,top])=>{
      s.append('circle').attr('cx',10).attr('cy',top+16).attr('r',9).attr('fill',c);
      s.append('text').attr('x',30).attr('y',top+23).attr('class','ann-s').attr('font-size',16).attr('font-weight',700).attr('letter-spacing','.14em').attr('fill',INK).text(lbl);
      items.forEach(([n,draw],i)=>{
        const d=get(n), x=150+i*300, iy=top+270;
        const g=s.append('g').attr('transform',`translate(${x},${iy})`); draw(g);
        if(i<2) s.append('text').attr('x',x+150).attr('y',iy-100).attr('text-anchor','middle').attr('font-size',40).attr('font-weight',300).attr('fill',GREYD).text('+');
        s.append('text').attr('x',x).attr('y',top+310).attr('text-anchor','middle').attr('class','ann-t').attr('font-size',21).text(short(n));
        s.append('text').attr('x',x).attr('y',top+336).attr('text-anchor','middle').attr('class','ann-s').attr('font-size',17).text(`${d3.format(',')(d.cal)} cal · ${d.sugar}g sugar`);
        const cubes=d.sugar/4, rows=Math.max(1,Math.ceil(cubes/PER)), w=Math.min(PER,Math.ceil(cubes))*(CU+G)-G;
        cubesAt(s,x-w/2,top+352,cubes,PINK);
        s.append('text').attr('x',x).attr('y',top+352+rows*(CU+G)+16).attr('text-anchor','middle').attr('class','ann-s').attr('font-size',16).attr('fill',cubes>=1?PINK:MUTED).attr('font-weight',700).text(cubes===0?'no sugar':cubes<1?'under 1 cube':`${Math.round(cubes)} cube${Math.round(cubes)===1?'':'s'}`);
      });
      s.append('text').attr('x',1000).attr('y',top+170).attr('text-anchor','middle').attr('font-size',44).attr('font-weight',300).attr('fill',GREYD).text('=');
      s.append('text').attr('x',1000).attr('y',top+270).attr('text-anchor','middle').attr('font-size',96).attr('font-weight',900).attr('letter-spacing','-.04em').attr('fill',k==='after'?GOLD:INK).text(Math.round(T.sug/4));
      s.append('text').attr('x',1000).attr('y',top+305).attr('text-anchor','middle').attr('class','ann-t').attr('font-size',21).text('cubes of sugar');
      s.append('text').attr('x',1000).attr('y',top+336).attr('text-anchor','middle').attr('class','ann-s').attr('font-size',17).text(`${d3.format(',')(T.cal)} calories`);
      s.append('text').attr('x',1000).attr('y',top+360).attr('text-anchor','middle').attr('class','ann-s').attr('font-size',17).text(`${d3.format(',')(T.sod)}mg sodium`);
      if(k==='after'){ s.append('text').attr('x',1000).attr('y',top+400).attr('text-anchor','middle').attr('class','ann-t').attr('font-size',20).attr('fill',GOLD).text(`saves ${d3.format(',')(B.cal-A.cal)} cal`);
        s.append('text').attr('x',1000).attr('y',top+426).attr('text-anchor','middle').attr('class','ann-t').attr('font-size',20).attr('fill',GOLD).text(`and ${B.sug-A.sug}g of sugar`); }
    });
    s.append('line').attr('x1',0).attr('x2',1170).attr('y1',455).attr('y2',455).attr('stroke',INK).attr('stroke-width',1.5);
    document.getElementById(id+'-saved').textContent = Math.round(B.sug/4)-Math.round(A.sug/4);
  });
})();

/* ---------- transitions: replayable visuals ---------- */
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const dur = ms => RM?0:ms;
const REPLAY = {};
REPLAY.t1 = function(){
  d3.select('#t1').selectAll('*').remove();
  const s = d3.select('#t1').append('svg').attr('viewBox','0 0 1100 940');
  const root = d3.hierarchy({children:DATA}).sum(d=>Math.max(60,d.cal||0));
  d3.pack().size([760,760]).padding(3)(root);
  const g = s.append('g').attr('transform','translate(170,40)');
  g.selectAll('circle').data(root.leaves()).join('circle')
    .attr('cx',d=>d.x).attr('cy',d=>d.y).attr('r',0).attr('fill',GREY)
    .transition().delay((d,i)=>dur(i*4)).duration(dur(420)).ease(d3.easeBackOut.overshoot(1.4)).attr('r',d=>d.r);
  s.append('text').attr('x',550).attr('y',870).attr('text-anchor','middle').attr('class','ann-t').attr('font-size',26).text('260 menu items');
  s.append('text').attr('x',550).attr('y',902).attr('text-anchor','middle').attr('class','tcap').text('One dot each. Bigger dot, more calories.');
};
REPLAY.t2 = function(){
  d3.select('#t2').selectAll('*').remove();
  const s = d3.select('#t2').append('svg').attr('viewBox','0 0 1100 940');
  const coke = DATA.find(d=>d.item==='Coca-Cola Classic (Medium)');
  const cubes = Math.round(coke.sugar/4), DAY=Math.round(50/4);
  // cup
  const cx=300, top=200, bot=760, topW=300, botW=220;
  const poly=[[cx-topW/2,top],[cx+topW/2,top],[cx+botW/2,bot],[cx-botW/2,bot]];
  s.append('clipPath').attr('id','tcup').append('polygon').attr('points',poly.map(p=>p.join(',')).join(' '));
  s.append('rect').attr('clip-path','url(#tcup)').attr('x',cx-topW/2).attr('y',bot).attr('width',topW).attr('height',0).attr('fill',PINKF)
    .transition().duration(dur(900)).ease(d3.easeCubicOut).attr('y',top+40).attr('height',bot-top-40);
  s.append('polygon').attr('points',poly.map(p=>p.join(',')).join(' ')).attr('fill','none').attr('stroke',INK).attr('stroke-width',3);
  s.append('line').attr('x1',cx-topW/2-14).attr('x2',cx+topW/2+14).attr('y1',top).attr('y2',top).attr('stroke',INK).attr('stroke-width',8);
  s.append('line').attr('x1',cx+40).attr('x2',cx+100).attr('y1',top-110).attr('y2',top+120).attr('stroke',INK).attr('stroke-width',8).attr('stroke-linecap','round');
  s.append('text').attr('x',cx).attr('y',820).attr('text-anchor','middle').attr('class','ann-t').attr('font-size',28).text('One medium Coke');
  s.append('text').attr('x',cx).attr('y',852).attr('text-anchor','middle').attr('class','tcap').text(`${coke.sugar}g of sugar · ${coke.cal} calories`);
  // cubes column
  const C=38, G=6, x0=640, base=760;
  const cy = k => base-(k+1)*(C+G);
  for(let k=0;k<cubes;k++){
    s.append('rect').attr('x',x0).attr('y',cy(k)-500).attr('width',C).attr('height',C).attr('rx',5).attr('fill',PINK).attr('opacity',0)
      .transition().delay(dur(150+k*70)).duration(dur(320)).ease(d3.easeBounceOut).attr('y',cy(k)).attr('opacity',1);
  }
  const yl = cy(DAY-1)-G/2;
  s.append('line').attr('x1',x0-40).attr('x2',x0+C+300).attr('y1',yl).attr('y2',yl).attr('stroke',INK).attr('stroke-width',2.5).attr('stroke-dasharray','9 7');
  s.append('text').attr('x',x0+C+30).attr('y',yl+30).attr('class','ann-t').attr('font-size',24).text('A whole day · 12 cubes');
  s.append('text').attr('x',x0+C+30).attr('y',yl+60).attr('class','tcap').text('WHO limit, about 50g');
  s.append('text').attr('x',x0+C+30).attr('y',cy(cubes-1)+C/2+12).attr('class','ann-t').attr('font-size',44).attr('fill',PINK).attr('opacity',0).text(`= ${cubes} cubes, over the line`)
    .transition().delay(dur(150+cubes*70)).duration(dur(400)).attr('opacity',1);
  s.append('text').attr('x',x0+C/2).attr('y',820).attr('text-anchor','middle').attr('class','tcap').text('1 cube = 4g');
};
REPLAY.t3 = function(){
  d3.select('#t3').selectAll('*').remove();
  const s = d3.select('#t3').append('svg').attr('viewBox','0 0 1100 940');
  const salt = DATA.filter(d=>!isDrink(d)&&d.sodium>=1150).sort((a,b)=>b.sodium-a.sodium);
  const cx=550, cy=430;
  s.append('circle').attr('cx',cx).attr('cy',cy).attr('r',340).attr('fill','#FFF').attr('stroke',INK).attr('stroke-width',3);
  s.append('circle').attr('cx',cx).attr('cy',cy).attr('r',250).attr('fill','none').attr('stroke',GREYS).attr('stroke-width',2);
  const root = d3.hierarchy({children:salt}).sum(d=>Math.max(400,d.sodium||0));
  d3.pack().size([470,470]).padding(6)(root);
  const g = s.append('g').attr('transform',`translate(${cx-235},${cy-235})`);
  g.selectAll('circle').data(root.leaves()).join('circle')
    .attr('cx',d=>d.x).attr('cy',d=>d.y).attr('r',0).attr('fill',BLUE)
    .transition().delay((d,i)=>dur(i*22)).duration(dur(420)).ease(d3.easeBackOut.overshoot(1.4)).attr('r',d=>d.r);
  s.append('text').attr('x',cx).attr('y',840).attr('text-anchor','middle').attr('class','ann-t').attr('font-size',28).text(`${salt.length} dishes on the plate`);
  s.append('text').attr('x',cx).attr('y',872).attr('text-anchor','middle').attr('class','tcap').text('Each dot is one dish with half a day of salt (1,150mg or more) in a single serving. Bigger dot, more salt.');
};

/* ---------- navigation ---------- */""")

# replay hook + footer hidden on transition slides; new storage key
rep("  document.getElementById('footer').hidden = (i===N-1);\n  try{ localStorage.setItem('sugar-v2-slide',String(i)); }catch(e){}",
    "  const cur = slides[i];\n  document.getElementById('footer').hidden = (i===N-1) || cur.classList.contains('tslide');\n  const tv = cur.querySelector('.tviz'); if(tv && REPLAY[tv.id]) REPLAY[tv.id]();\n  try{ localStorage.setItem('sugar-v3-slide',String(i)); }catch(e){}")
rep("localStorage.getItem('sugar-v2-slide')", "localStorage.getItem('sugar-v3-slide')")

# renumber data-i in DOM order
k = [-1]
def renum(m):
    k[0]+=1; return f'<section class="slide{m.group(1)}" data-i="{k[0]}">'
html = re.sub(r'<section class="slide([^"]*)" data-i="\d+">', renum, html)
assert k[0]+1 == 17, k
assert html.count('["') >= 14
OUT.write_text(html)
print('wrote', OUT, 'slides', k[0]+1, 'notes', len(re.findall(r'^ \["', NOTES, re.M)))
