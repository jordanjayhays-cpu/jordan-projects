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

S14 = """
<!-- 14 (new) -->
<section class="slide" data-i="13">
  <div class="panel">
    <div class="eyebrow">Part 3 · Policy · <b>What to order instead</b></div>
    <div class="bar" style="margin-top:18px"></div>
    <h1 class="sm">Same meal, a fraction of the sugar</h1>
    <p class="lede">Three common orders. Keep the main item, change the cup and the side. Nothing new has to go on the menu.</p>
    <div class="stat"><span class="lbl">Sugar cubes saved, three meals</span><span class="num" id="savedCubes">–</span></div>
    <div class="key">
      <div class="kh">KEY</div>
      <div class="row"><span class="sw" style="background:var(--grey-deep)"></span><span>What people order</span></div>
      <div class="row"><span class="sw" style="background:var(--gold)"></span><span>Order this instead</span></div>
      <div class="row"><span class="sw sq" style="background:var(--pink)"></span><span>One sugar cube, 4g</span></div>
      <div class="howto">Meals follow McDonald's own combos: main item, fries, drink. Nutrition from the same 260-item dataset.</div>
    </div>
  </div>
  <div class="chart" id="c14"></div>
</section>
"""
rep("\n<!-- 9 (new) -->\n", "\n" + S14 + "\n<!-- 15 -->\n")
rep('<div class="twho">Presenter 3 · 5 slides</div>', '<div class="twho">Presenter 3 · 6 slides</div>')

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
 ["Three real orders. Big Mac meal: keep the Big Mac, small fries, Diet Coke, and fourteen cubes of sugar disappear. Chicken meal: grilled instead of crispy, small fries, Diet Coke. Breakfast: the caramel syrup alone is eight cubes, a plain latte keeps the coffee. Nothing new on the menu. (Point at the gold rows only.)", "<b>Knaflic:</b> before/after side by side · <b>Session 7:</b> make the solution concrete · <b>Yau:</b> unit cubes, counts you can feel"],
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

/* ---------- new: 14 what to order instead ---------- */
(function(){
  const s = svg('c14');
  const by = new Map(DATA.map(d=>[d.item,d]));
  const get = n => { const d=by.get(n); if(!d) throw new Error('missing '+n); return d; };
  const meals = [
    {name:'Big Mac Meal', before:['Big Mac','Medium French Fries','Coca-Cola Classic (Medium)'], after:['Big Mac','Small French Fries','Diet Coke (Medium)'], why:'Keep the Big Mac. Small fries, a no-sugar drink.'},
    {name:'Crispy chicken meal', before:['Premium Crispy Chicken Classic Sandwich','Medium French Fries','Coca-Cola Classic (Medium)'], after:['Premium Grilled Chicken Classic Sandwich','Small French Fries','Diet Coke (Medium)'], why:'Grilled instead of crispy. Same sandwich, same bun.'},
    {name:'Breakfast run', before:['Sausage McMuffin with Egg','Hash Brown','Caramel Latte (Medium)'], after:['Egg McMuffin','Hash Brown','Latte (Medium)'], why:'The caramel syrup alone is 8 cubes. Keep the latte, lose the syrup.'}
  ];
  const sum = (names,k) => d3.sum(names.map(n=>get(n)[k]));
  const short = n => n.replace('Coca-Cola Classic (Medium)','medium Coke').replace('Diet Coke (Medium)','medium Diet Coke').replace('Medium French Fries','medium fries').replace('Small French Fries','small fries').replace('Premium Crispy Chicken Classic Sandwich','Crispy chicken sandwich').replace('Premium Grilled Chicken Classic Sandwich','Grilled chicken sandwich').replace('Caramel Latte (Medium)','medium caramel latte').replace('Latte (Medium)','medium latte');
  const CU=17, G=3, cx=720, rowH=300, top=40;
  let saved=0;
  meals.forEach((m,i)=>{
    const y = top+i*rowH;
    s.append('text').attr('x',0).attr('y',y+26).attr('class','ann-t').attr('font-size',26).text(`${i+1} · ${m.name}`);
    s.append('text').attr('x',0).attr('y',y+54).attr('class','ann-s').text(m.why);
    if(i<2) s.append('line').attr('x1',0).attr('x2',1170).attr('y1',y+rowH-28).attr('y2',y+rowH-28).attr('stroke',GREYS);
    const b = {cal:sum(m.before,'cal'), sug:sum(m.before,'sugar')};
    [['before',GREYD],['after',GOLD]].forEach(([k,c],j)=>{
      const yy = y+88+j*92;
      const cal=sum(m[k],'cal'), sug=sum(m[k],'sugar'), sod=sum(m[k],'sodium'), cubes=sug/4;
      saved += (k==='before'?cubes:-cubes);
      s.append('circle').attr('cx',10).attr('cy',yy+12).attr('r',9).attr('fill',c);
      s.append('text').attr('x',30).attr('y',yy+18).attr('class','ann-t').attr('font-size',20).text(m[k].map(short).join(' · '));
      s.append('text').attr('x',30).attr('y',yy+44).attr('class','ann-s').attr('font-size',17).text(`${d3.format(',')(cal)} cal · ${sug}g sugar · ${d3.format(',')(sod)}mg sodium`);
      const full=Math.floor(cubes), frac=cubes-full;
      for(let q=0;q<full;q++) s.append('rect').attr('x',cx+q*(CU+G)).attr('y',yy+2).attr('width',CU).attr('height',CU).attr('rx',3).attr('fill',PINK);
      if(frac>.12) s.append('rect').attr('x',cx+full*(CU+G)).attr('y',yy+2).attr('width',CU*frac).attr('height',CU).attr('rx',3).attr('fill',PINK);
      s.append('text').attr('x',cx+Math.ceil(cubes)*(CU+G)+10).attr('y',yy+18).attr('class','ann-t').attr('font-size',19).attr('fill',k==='before'?INK:GOLD).text(`${Math.round(cubes)} cube${Math.round(cubes)===1?'':'s'}`);
      if(k==='after') s.append('text').attr('x',cx).attr('y',yy+50).attr('class','ann-t').attr('font-size',19).attr('fill',GOLD).text(`saves ${d3.format(',')(b.cal-cal)} calories and ${b.sug-sug}g of sugar`);
    });
  });
  s.append('text').attr('x',cx).attr('y',top+22).attr('class','ann-s').attr('font-size',15).attr('letter-spacing','.14em').text('SUGAR IN THE MEAL · ONE CUBE = 4G');
  document.getElementById('savedCubes').textContent = Math.round(saved);
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
assert k[0]+1 == 15, k
assert html.count('["') >= 14
OUT.write_text(html)
print('wrote', OUT, 'slides', k[0]+1, 'notes', len(re.findall(r'^ \["', NOTES, re.M)))
