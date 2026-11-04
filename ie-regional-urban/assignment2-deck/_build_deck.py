"""Build the IDB Mexico and Central America deck (v3) in the 'Eight patents' visual style,
following the Assignment 2 suggested structure. Content and numbers: friend's deck V2.
Output: IDB_Mexico_Central_America_v3.html (single file, D3 from cdnjs)."""
import pathlib, json

OUT = pathlib.Path(__file__).with_name('IDB_Mexico_Central_America_v3.html')

SECTIONS = ['Regional context', 'Diagnostic', 'International benchmarks', 'Policy recommendations', 'Conclusion']
# slide list: (section index or None for title/exec, eyebrow, kind, body html, chart id or None, source)
S = []
def slide(sec, eyebrow, body, chart=None, source='', cls=''):
    S.append(dict(sec=sec, eyebrow=eyebrow, body=body, chart=chart, source=source, cls=cls))

def card(title, sub='', big='', bigcls='', biglab='', key='', keylab='KEY'):
    h = f'<div class="card">'
    h += f'<h1>{title}</h1>'
    if sub: h += f'<p class="sub">{sub}</p>'
    if big: h += f'<div class="rule"></div><div class="big {bigcls}{" sm" if len(big)>5 else ""}">{big}</div>'
    if biglab: h += f'<div class="biglab">{biglab}</div>'
    if key: h += f'<div class="keylab">{keylab}</div><p class="key">{key}</p>'
    h += '</div>'
    return h

def aside(t): return f'<p class="aside">{t}</p>'

# ---------- 1 TITLE ----------
slide(None, 'FOR THE INTER-AMERICAN DEVELOPMENT BANK', '''
<div class="title">
  <div class="dots8" id="dots8"></div>
  <div class="dotslab">FILED BY GUATEMALA'S 18.4 MILLION RESIDENTS IN 2024. NOT EIGHT THOUSAND.</div>
  <h1 class="huge">Eight patents</h1>
  <p class="tsub">What Mexico and Central America stopped buying, and what it cost them</p>
  <p class="tsub2">Growth diagnostic for the IDB · one subregion, different binding constraints</p>
  <div class="tfoot"><div><b>Group 1 · [Consulting firm] · IE University</b><br>[Presenter 1] · [Presenter 2] · [Presenter 3] · [Presenter 4] · [Presenter 5]</div><div>12 November 2026</div></div>
</div>''', cls='full')

# ---------- 2 EXECUTIVE SUMMARY ----------
slide(None, 'EXECUTIVE SUMMARY', card(
 'One subregion, different binding constraints.',
 'Seven economies, four stories. The money should follow the constraint, not the map.',
 '3', 'blue', 'PROGRAMMES, ONE ASK: FUND LINKAGES AND FORMALISATION IN MEXICO, STARTING IN 2027',
 'Evidence on slides 3 to 11, benchmarks on 12 to 13, programmes on 14 to 17.'),
 chart='exec', source='Summary of the deck · each claim is sourced on the slide that carries it')

# ---------- 3-6 REGIONAL CONTEXT ----------
slide(0, 'REGIONAL CONTEXT · 1 OF 4', card(
 'Seven economies, four different stories.',
 'Informality, tax, remittances and skills, against the OECD.',
 '~25%', 'red', 'OF GDP IS MONEY SENT HOME, IN HONDURAS, EL SALVADOR AND NICARAGUA',
 'Darker cells sit further behind the Latin American average. Costa Rica and Panama break the pattern in different ways.'),
 chart='heat', source='ILOSTAT · Revenue Statistics in LAC 2025 (2023 data) · WDI remittances 2024 · OECD PISA 2022')

slide(0, 'REGIONAL CONTEXT · 2 OF 4', card(
 'Since 1990, Mexico has grown slowest of all.',
 'Real income per person, average annual growth, 1990 to 2024.',
 '0.7%', 'orange', "A YEAR: MEXICO'S GROWTH IN INCOME PER PERSON SINCE 1990. VIETNAM: 5.3%",
 'Grey bars are benchmarks outside the subregion. Panama grew fastest in the subregion, on services. Costa Rica came second.'),
 chart='growth', source='World Bank WDI, NY.GDP.PCAP.KD, 1990 to 2024, compound annual rate · Honduras from 2000 (series break)')

slide(0, 'REGIONAL CONTEXT · 3 OF 4', card(
 'Latin America did not lack machines. It used them less well.',
 'Total factor productivity as a share of the US level, 1960 and 2013.',
 '54%', 'red', 'RICHER, HAD PRODUCTIVITY SIMPLY KEPT PACE WITH THE US',
 'Two lines, two regions. Chile is the only country in Latin America that closed any of the gap.'),
 chart='tfp', source='Grazzi and Pietrobelli (IDB, 2016) · Pagés (IDB, 2010) · Penn World Table 10.01')

slide(0, 'REGIONAL CONTEXT · 4 OF 4 · A SUPPORTING SIGNAL', card(
 'Patents tell the same story, more starkly.',
 'Resident patent applications per million people, 2024.',
 '420×', 'blue', "KOREA'S RESIDENT PATENTS PER PERSON AGAINST MEXICO'S. AGAINST GUATEMALA: 8,704×",
 "One dot is one patent per million people. Guatemala's is hollow because it is less than one. Patents undercount invention, since multinationals file abroad; we use them as one signal, not the measure."),
 chart='patents', source='World Bank WDI, IP.PAT.RESD and SP.POP.TOTL, 2024 · retrieved 17 Oct 2026')

# ---------- 7-11 DIAGNOSTIC ----------
slide(1, 'DIAGNOSTIC · 1 OF 5 · THE TEST', card(
 'Same test, different verdicts for Mexico and Guatemala.',
 'Four candidate constraints, one indicator each, scored against the Latin American average.',
 '1 vs 3', 'red', 'CONSTRAINTS THAT CLEARLY BIND, IN MEXICO AGAINST GUATEMALA. FINANCE BINDS IN NEITHER',
 "Mexico's binding constraint is appropriability: informality and missing supplier links. Guatemala's is the state itself."),
 chart='test', source='Framework after Hausmann, Rodrik and Velasco (2005) · WDI FS.AST.PRVT.GD.ZS, FR.INR.LNDP 2025; LP.LPI.OVRL.XQ 2022; EG.ELC.ACCS.ZS 2024 · OECD PISA 2022 · ILOSTAT · InSight Crime 2024 · Revenue Statistics in LAC 2025')

slide(1, 'DIAGNOSTIC · 2 OF 5 · MEXICO', card(
 'In Mexico, every formal hire carries a tax, so firms stay small.',
 'So firms stay small, stay hidden, and never learn to grow.',
 '55%', 'orange', 'OF MEXICAN WORKERS ARE INFORMAL. COSTA RICA: 37%. GUATEMALA: 83%',
 'Solid circles are the firm today. The dashed line is the moment the state can see it. Hollow circles are the growth that never comes. Levy puts the efficiency cost at 0.9% to 1.44% of GDP every year.'),
 chart='informal', source='ILOSTAT, latest year · mechanism after Levy (2008)')

slide(1, 'DIAGNOSTIC · 3 OF 5 · MEXICO', card(
 'The export poles buy abroad, and the south is left out.',
 'What Mexico exports is complex. The capability that makes it sits abroad.',
 '>70%', 'orange', "OF THE INPUTS USED BY MEXICO'S EXPORT FACTORIES ARE IMPORTED, EVERY YEAR SINCE 2013",
 "Mexico ranks 17th in economic complexity, yet its export factories buy fewer than 30% of inputs at home. Nuevo León's factories make 39% of all domestic IMMEX purchases. Chiapas, on the southern border, has six times its poverty rate."),
 chart='poles', source='Harvard Growth Lab, Atlas of Economic Complexity · INEGI IMMEX 2024 · INEGI poverty 2024 · El Financiero (2023) on IMMEX · Perroux, Myrdal, Hirschman')

slide(1, 'DIAGNOSTIC · 4 OF 5 · NORTHERN TRIANGLE AND NICARAGUA', card(
 'In the Northern Triangle, the state is too thin to provide the basics.',
 'Revenue, skills and safety, against the region and the OECD.',
 '14%', 'purple', "GUATEMALA'S TAX TAKE, % OF GDP. LATIN AMERICA: 21.3%. OECD: 34%",
 'Violence works as a second, private tax on growth, and it falls hardest on the periphery. Twenty PISA points equal about one school year.'),
 chart='state', source='Revenue Statistics in LAC 2025 · IDB on PISA 2022 · InSight Crime 2024')

slide(1, 'DIAGNOSTIC · 5 OF 5 · INCLUSION', card(
 'Growth has not been shared, and the poorest farm on rain.',
 'Income inequality and the share of jobs in agriculture.',
 '~30%', 'purple', 'OF JOBS IN GUATEMALA AND NICARAGUA ARE IN FARMING, EXPOSED TO DROUGHT IN THE DRY CORRIDOR',
 'Guatemala, Honduras, El Salvador and Nicaragua share the Dry Corridor, where most farming depends on rain and droughts recur.'),
 chart='inclusion', source='WDI SI.POV.GINI, latest year 2023 to 2025 (Nicaragua 2014) · WDI SL.AGR.EMPL.ZS, 2025 (ILO modelled) · Dry Corridor: FAO and WFP regional assessments')

# ---------- 12-13 BENCHMARKS ----------
slide(2, 'INTERNATIONAL BENCHMARKS · 1 OF 2 · INSIDE THE SUBREGION', card(
 'Costa Rica grew on skills. Panama grew without inclusion.',
 'Two neighbours that broke the pattern, in opposite ways.',
 '44%', 'teal', "OF COSTA RICA'S GOODS EXPORTS IN 2024 WERE MEDICAL DEVICES, WITH ALMOST NO R&D OR PATENTS",
 'Panama grew fastest, on canal and financial services, but collects the least tax and leaves most workers informal.'),
 chart='crpa', source='WDI NY.GDP.PCAP.KD, GB.XPD.RSDV.GD.ZS, SI.POV.GINI · Revenue Statistics in LAC 2025 · ILOSTAT · PROCOMER 2025')

slide(2, 'INTERNATIONAL BENCHMARKS · 2 OF 2 · PRECEDENTS', card(
 'Each constraint has already been broken, close to home.',
 'Three precedents, one for each programme, each a narrow mandate held for a long time.',
 '3', 'blue', 'PRECEDENTS. A CAUTION: COSTA RICA CUT CINDE\'S PUBLIC FUNDING IN 2023. THESE INSTITUTIONS NEED A PROTECTED MANDATE',
 'None of it was luck. All of it was policy, done by a state that did one narrow thing for a long time.'),
 chart='precedents', source='UNIDO WP 5/2019 (Tong) · Vietnamese Ministry of Industry and Trade 2017 · Medellín city data, 99% Invisible · PROCOMER 2025')

# ---------- 14-17 POLICY ----------
slide(3, 'POLICY RECOMMENDATIONS · 1 OF 4 · PROGRAMME ONE · MEXICO', card(
 'Mexico: link the export plants to local firms, and lift the payroll wedge.',
 "Pay for the two steps of Perroux's growth pole that markets skip.",
 '<30%', 'orange', "DOMESTIC SHARE OF INPUTS IN MEXICO'S EXPORT FACTORIES: THE NUMBER THIS PROGRAMME MOVES",
 'Formalisation: move health and pensions from wages to general revenue, so firms can grow into suppliers. Modelled net cost: 0.34% of GDP.'),
 chart='prog1', source="Perroux's growth pole · Vietnam supplier development (UNIDO 2019) · Antón, Hernández and Levy (2012), IDB · IDB border integration programme")

slide(3, 'POLICY RECOMMENDATIONS · 2 OF 4 · PROGRAMME TWO · NORTHERN TRIANGLE', card(
 'Northern Triangle: build the state first, then connect the towns.',
 'Revenue, security and connectivity, in that order.',
 '14%', 'purple', "GUATEMALA'S TAX TAKE. EVERY OTHER FIX IS PAID FOR FROM THIS BASE",
 'Broader VAT base and e-invoicing first. A security component in every corridor. Roads, power and broadband to lagging towns.'),
 chart='prog2', source='Revenue Statistics in LAC 2025 · InSight Crime 2024 · WDI EG.ELC.ACCS.ZS · precedent: Medellín social urbanism')

slide(3, 'POLICY RECOMMENDATIONS · 3 OF 4 · PROGRAMME THREE · CAPABILITY', card(
 'Across the region: an agency that proves new industries, then leaves.',
 'Fund an agency that proves a new product works, hands it to firms, and makes itself unnecessary.',
 'US$35m', 'blue', "THE IDB LOAN THAT FUNDED COSTA RICA'S INNOVATION AND SKILLS PROGRAMME (CR-L1043, 2012): OUR SIZING BENCHMARK",
 'Blue is public money, orange is private firms. The agency\'s whole job is to make itself unnecessary.'),
 chart='prog3', source='Vernon 1966 · Hausmann and Rodrik 2003 · precedents: CINDE Costa Rica, Fundación Chile · IDB project CR-L1043')

slide(3, 'POLICY RECOMMENDATIONS · 4 OF 4 · SEQUENCING', card(
 'The cheap, visible programme goes first.',
 'Ten years, three programmes. Each one earns the credibility the next one spends.',
 '2', 'red', 'YEARS TO THE FIRST VISIBLE RESULT: LOCAL SUPPLIERS CERTIFIED IN MEXICO',
 'Each band begins only once the one before it has shown something. Timeline illustrative; gates to be calibrated with the IDB country teams.'),
 chart='seq', source='Timeline illustrative · gates to be calibrated with the IDB country teams')

# ---------- 18-19 CONCLUSION ----------
slide(4, 'CONCLUSION AND NEXT STEPS · 1 OF 2 · ACCOUNTABILITY', card(
 'We promise three counts, not a growth rate.',
 'Published every year, each with a baseline and a fair comparator.',
 '3', 'blue', 'COUNTS. TOP RISK: A US TRADE OR REMITTANCE SHOCK. PROGRAMME THREE ALSO TARGETS NON-US BUYERS',
 'Solid dots are where we are. Hollow dots are where we are aiming. Target levels to be set with the IDB country teams.'),
 chart='counts', source='Baselines: INEGI IMMEX, ILOSTAT, Revenue Statistics in LAC 2025 · targets set with the IDB country teams')

slide(4, 'CONCLUSION AND NEXT STEPS · 2 OF 2 · ONE ASK', '''
<div class="ask">
  <div class="askbar"></div>
  <h1 class="huge2">Fund linkages and formalisation.<br>In Mexico. <span class="red">Starting in 2027.</span></h1>
  <p class="tsub">Record investment is landing in Mexico now. Linkages decide whether it builds capability or only assembly lines.</p>
  <div class="steps3">
    <div><b>Months 0 to 3</b>Supplier scan in two corridors</div>
    <div><b>Months 3 to 9</b>Design the supplier programme, prepare the loan</div>
    <div><b>Months 9 to 12</b>Loan approval; formalisation groundwork</div>
  </div>
  <p class="aside">sixty-four years is long enough to wait for the second attempt</p>
</div>''', cls='full', source='Programme one of three · precedent: Vietnam supplier development · sizing benchmark: IDB border integration programme')

# ---------- APPENDIX ----------
slide(None, 'APPENDIX', '<div class="divider"><h1 class="huge">Backup</h1><p class="tsub">A1 to A4 · the evidence behind the story and answers for Q&amp;A</p></div>', cls='full dark')
slide(None, 'BACKUP · A1', '<h1 class="wide">Every indicator, every country</h1>', chart='a1', cls='wide', source='WDI series NY.GDP.PCAP.PP.CD, IP.PAT.RESD, GB.XPD.RSDV.GD.ZS, SP.POP.SCIE.RD.P6, BX.TRF.PWKR.DT.GD.ZS, retrieved 31 Oct 2026 · *official, contested · n.a. no reliable series · n.t. not tested')
slide(None, 'BACKUP · A2', '<h1 class="wide">The IDB projects we sized against</h1>', chart='a2', cls='wide', source='IDB project database, project CR-L1043 · IDB Border Integration Programme documents')
slide(None, 'BACKUP · A3 AND A4', '<h1 class="wide">Formalisation: the evidence, and the counterarguments</h1>', chart='a3', cls='wide', source='Levy (2008), Brookings · Antón, Hernández and Levy (2012), IDB · Fajnzylber et al. (2011) · Monteiro and Assunção (2012) · Piza (2018) · Secretaría de Economía, RNIE, 2025 FDI composition')

MAIN = sum(1 for s in S if not s['eyebrow'].startswith('BACKUP') and s['eyebrow'] != 'APPENDIX')

# ---------- HTML ----------
def render(i, s):
    n = i + 1
    is_app = s['eyebrow'].startswith('BACKUP') or s['eyebrow'] == 'APPENDIX'
    num = f'A{n-MAIN-1}' if is_app and s['eyebrow'] != 'APPENDIX' else ('' if s['eyebrow']=='APPENDIX' else f'{n:02d} / {MAIN}')
    prog = ''
    if not is_app:
        segs = ''.join(f'<i class="{"on" if s["sec"] is not None and j <= s["sec"] else ""} {"cur" if s["sec"]==j else ""}"></i>' for j in range(len(SECTIONS)))
        prog = f'<div class="prog">{segs}<span>{num}</span></div>'
    elif num:
        prog = f'<div class="prog"><span>{num}</span></div>'
    chart = f'<div class="viz" id="{s["chart"]}"></div>' if s['chart'] else ''
    return f'''<section class="slide {s['cls']}" data-i="{i}">
  <div class="eyebrow">{s['eyebrow']}</div>
  {s['body']}
  {chart}
  {prog}
  <div class="src">{s['source']}</div>
</section>'''

SLIDES = '\n'.join(render(i, s) for i, s in enumerate(S))

CSS = r'''
:root{
  --bg:#F3F1EB; --card:#FAF9F6; --line:#E3E0D7; --strip:#E9E6DE; --ink:#1C1B19; --muted:#78746D; --muted2:#A39F97;
  --blue:#1F6FD6; --orange:#C9541C; --purple:#6A3DB8; --teal:#0F8A7A; --magenta:#B5176B; --red:#E03A1C; --grey:#B9B5AC; --greyd:#8D8980;
  --display:'Archivo','Inter',Helvetica,Arial,sans-serif; --body:'Inter',Helvetica,Arial,sans-serif; --cond:'Archivo Narrow','Roboto Condensed',Arial,sans-serif; --serif:'Source Serif 4',Georgia,serif;
  color-scheme:light;
}
:root[data-theme="dark"]{--bg:#F3F1EB}
html,body{height:100%}
body{margin:0;background:#DCD9D1;color:var(--ink);font-family:var(--body);overflow:hidden;-webkit-font-smoothing:antialiased;padding-left:env(safe-area-inset-left,0px);padding-right:env(safe-area-inset-right,0px)}
#viewport{position:fixed;inset:0;display:grid;place-items:center;background:#DCD9D1}
#stage{position:relative;width:1920px;height:1080px;transform-origin:center center;background:var(--bg);box-shadow:0 20px 80px rgba(0,0,0,.18);overflow:hidden}
.slide{position:absolute;inset:0;display:none}
.slide.active{display:block}
.slide.active .card, .slide.active .viz, .slide.active .title, .slide.active .ask{animation:rise .55s cubic-bezier(.2,.75,.2,1) both}
.slide.active .viz{animation-delay:.12s}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){.slide.active *{animation:none!important}}
.eyebrow{position:absolute;left:104px;top:92px;font-family:var(--cond);font-size:20px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);font-weight:500}
.slide.full .eyebrow{left:104px;top:96px}
.slide.full .eyebrow::after{content:'';position:absolute;left:0;top:44px;width:1712px;height:1.5px;background:var(--line)}
.card{position:absolute;left:104px;top:150px;width:548px;height:808px;background:var(--card);border:1.5px solid var(--line);padding:40px 40px 36px;box-sizing:border-box;display:flex;flex-direction:column}
.card h1{font-family:var(--display);font-weight:800;font-size:56px;line-height:1.0;letter-spacing:-.035em;margin:0;text-wrap:balance}
.card .sub{font-size:24px;line-height:1.35;color:#3E3B36;margin:18px 0 0}
.card .rule{height:1.5px;background:var(--line);margin:26px 0 22px}
.card .big{font-family:var(--display);font-weight:800;font-size:112px;line-height:.9;letter-spacing:-.05em}
.card .big.sm{font-size:84px}
.card .big.blue{color:var(--blue)}.card .big.orange{color:var(--orange)}.card .big.purple{color:var(--purple)}.card .big.teal{color:var(--teal)}.card .big.red{color:var(--red)}
.card .biglab{font-family:var(--cond);font-size:19px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-top:16px;line-height:1.4}
.card .keylab{font-family:var(--cond);font-size:17px;letter-spacing:.2em;font-weight:700;margin-top:auto;padding-top:22px}
.card .key{font-size:19px;line-height:1.4;color:var(--muted);margin:8px 0 0}
.viz{position:absolute;left:740px;top:150px;width:1076px;height:808px}
.viz svg{width:100%;height:100%;display:block;overflow:visible}
.vlab{position:absolute;font-family:var(--cond);font-size:19px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted2)}
.aside{font-family:var(--serif);font-style:italic;font-size:30px;color:#4A4742;margin:0}
.aside.vz{position:absolute;left:0;bottom:40px;width:100%;padding-top:22px;border-top:1.5px solid var(--line)}
svg text{font-family:var(--body)}
.lbl{font-size:24px;font-weight:600;fill:var(--ink)}.lbl.m{fill:var(--muted);font-weight:500}
.cl{font-family:var(--cond);font-size:20px;letter-spacing:.14em;text-transform:uppercase;fill:var(--muted2)}
.num{font-family:var(--display);font-weight:800;letter-spacing:-.03em;fill:var(--ink)}
.ax text{font-size:20px;fill:var(--muted2)}.ax line,.ax path{stroke:var(--line)}
.src{position:absolute;left:0;right:0;bottom:0;height:54px;background:var(--strip);font-size:17px;color:var(--muted);line-height:54px;padding:0 104px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;box-sizing:border-box}
.slide.full .prog{bottom:60px}
.prog{position:absolute;right:104px;bottom:84px;display:flex;align-items:center;gap:10px;font-family:var(--cond);font-size:19px;color:var(--muted2);letter-spacing:.1em}
.prog i{display:block;width:56px;height:3px;background:var(--line)}
.prog i.on{background:var(--greyd)}.prog i.cur{background:var(--blue)}
.prog span{margin-left:10px}
/* full-bleed slides */
.title{position:absolute;left:104px;top:190px;width:1712px}
.dots8{display:flex;gap:18px;margin-bottom:22px}
.dots8 i{width:34px;height:34px;border-radius:50%;background:var(--purple);display:block;transform:scale(0)}
.slide.active .dots8 i{animation:pop .4s cubic-bezier(.3,1.5,.5,1) forwards}
@keyframes pop{to{transform:scale(1)}}
.dotslab{font-family:var(--cond);font-size:20px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:26px}
.huge{font-family:var(--display);font-weight:800;font-size:260px;line-height:.88;letter-spacing:-.05em;margin:0 0 30px}
.huge2{font-family:var(--display);font-weight:800;font-size:112px;line-height:1.0;letter-spacing:-.04em;margin:0 0 34px}
.huge2 .red{color:var(--red)}
.tsub{font-size:36px;line-height:1.3;margin:0 0 10px;max-width:1300px}
.tsub2{font-size:24px;color:var(--muted);margin:0}
.tfoot{position:absolute;left:0;top:690px;width:1712px;display:flex;justify-content:space-between;font-size:22px;color:var(--muted);line-height:1.5;border-top:1.5px solid var(--line);padding-top:24px}
.tfoot b{color:var(--ink);font-weight:700}
.ask{position:absolute;left:104px;top:200px;width:1712px}
.askbar{width:160px;height:12px;background:var(--red);margin-bottom:40px}
.steps3{display:grid;grid-template-columns:repeat(3,1fr);gap:40px;margin:60px 0 50px}
.steps3 div{border-top:3px solid var(--ink);padding-top:16px;font-size:24px;line-height:1.35;color:#3E3B36}
.steps3 b{display:block;font-weight:700;color:var(--ink);margin-bottom:4px}
.divider{position:absolute;left:104px;top:300px;width:1712px}
.slide.dark{background:var(--red)}
.slide.dark .huge,.slide.dark .tsub,.slide.dark .eyebrow{color:#fff}
.slide.dark .eyebrow::after{background:rgba(255,255,255,.4)}
.slide.dark .src{background:rgba(0,0,0,.15);color:#fff}
.slide.dark .huge{margin-top:30px;padding-top:40px;border-top:1.5px solid rgba(255,255,255,.4)}
/* wide (appendix) */
.slide.wide h1.wide{position:absolute;left:104px;top:166px;margin:0;font-family:var(--display);font-weight:800;font-size:60px;letter-spacing:-.03em}
.slide.wide .viz{left:104px;top:270px;width:1712px;height:700px}
table.t{border-collapse:collapse;width:100%;font-size:22px}
table.t th{font-family:var(--cond);font-size:19px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);text-align:left;padding:0 18px 12px 0;border-bottom:2px solid var(--ink);font-weight:500}
table.t td{padding:16px 18px 16px 0;border-bottom:1.5px solid var(--line);vertical-align:top;line-height:1.3}
table.t td.n{font-variant-numeric:tabular-nums}
.c-mex{color:var(--orange)}.c-gua{color:var(--purple)}.c-cr{color:var(--teal)}.c-kor{color:var(--blue)}.c-bra{color:var(--magenta)}
.hint{position:fixed;left:14px;top:12px;font-family:var(--cond);font-size:12px;color:#777;letter-spacing:.1em;z-index:5}
'''

JS = r'''
const C=getComputedStyle(document.documentElement), col=n=>C.getPropertyValue(n).trim();
const INK=col('--ink'),MU=col('--muted'),MU2=col('--muted2'),LINE=col('--line'),BLUE=col('--blue'),OR=col('--orange'),PU=col('--purple'),TE=col('--teal'),MG=col('--magenta'),RD=col('--red'),GR=col('--grey'),GRD=col('--greyd');
const CC={Mexico:OR,Guatemala:PU,'Costa Rica':TE,'South Korea':BLUE,Korea:BLUE,Brazil:MG};
const cc=n=>CC[n]||INK;
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches, dur=ms=>RM?0:ms;
const svg=(id,w=1076,h=808)=>{const el=document.getElementById(id); el.innerHTML=''; return d3.select(el).append('svg').attr('viewBox',`0 0 ${w} ${h}`);};
const html=(id,h)=>{document.getElementById(id).innerHTML=h;};
const vlab=(s,x,y,t)=>s.append('text').attr('x',x).attr('y',y).attr('class','cl').text(t);
const asideIn=(id,t)=>{const el=document.getElementById(id); const p=document.createElement('p'); p.className='aside vz'; p.textContent=t; el.appendChild(p);};
const grow=(sel,attr,to,delay=0,ms=700)=>sel.transition().delay(dur(delay)).duration(dur(ms)).ease(d3.easeCubicOut).attr(attr,to);

const DRAW={};
/* title dots */
DRAW.dots8=()=>{ const d=document.getElementById('dots8'); d.innerHTML=''; for(let i=0;i<8;i++){ const e=document.createElement('i'); e.style.animationDelay=(i*70)+'ms'; d.appendChild(e);} };

/* exec summary table */
DRAW.exec=()=>{ html('exec',`<table class="t" style="margin-top:10px"><thead><tr><th style="width:300px">Group</th><th>Binding constraint</th><th style="width:330px">What fits</th></tr></thead><tbody>
<tr><td class="c-mex" style="font-family:var(--display);font-weight:800;font-size:30px">Mexico</td><td>Missing supplier linkages and the informality wedge</td><td style="color:var(--red);font-weight:700">Linkages and formalisation</td></tr>
<tr><td style="font-family:var(--display);font-weight:800;font-size:30px">Northern Triangle and Nicaragua</td><td>State capacity and violence; people are the main export</td><td style="color:var(--red);font-weight:700">Revenue, security and connectivity</td></tr>
<tr><td class="c-cr" style="font-family:var(--display);font-weight:800;font-size:30px">Costa Rica</td><td>Contrast: grew on FDI plus skills, without R&amp;D or patents</td><td style="color:var(--red);font-weight:700">The model for capability-building</td></tr>
<tr><td style="font-family:var(--display);font-weight:800;font-size:30px">Panama</td><td>Contrast: fast growth on services, low tax, high informality</td><td style="color:var(--red);font-weight:700">Growth that was not inclusive</td></tr>
</tbody></table>`); asideIn('exec','the money should follow the constraint, not the map'); };

/* heat table */
DRAW.heat=()=>{ const rows=[['Mexico',55.5,17.7,3.7,395],['Guatemala',83.2,14.0,19.1,344],['Honduras',82.6,21.0,25.7,null],['El Salvador',66.5,22.8,24.3,343],['Nicaragua',63.0,27.5,26.6,null],['Costa Rica',37.4,24.9,0.7,385],['Panama',58.7,11.9,0.6,357]];
 const sc=[[30,85,true],[34,11,false],[0,27,true],[472,340,false]]; // [good,bad,higherIsWorse] mapped to 0..1 badness
 const bad=(v,i)=>{ const [g,b]=sc[i]; return Math.max(0,Math.min(1,(v-g)/(b-g))); };
 const fill=t=>t<.25?'#FBEDE9':t<.5?'#F6C9BB':t<.75?'#EC8F74':'#C9341C';
 const tx=t=>t>=.75?'#fff':INK;
 let h='<table class="t"><thead><tr><th></th><th>Informal jobs %</th><th>Tax % of GDP</th><th>Remittances % GDP</th><th>PISA maths</th></tr></thead><tbody>';
 rows.forEach(r=>{ h+=`<tr><td style="font-weight:700;color:${cc(r[0])}">${r[0]}</td>`; r.slice(1).forEach((v,i)=>{ if(v==null){h+='<td style="background:#EEECE6;color:var(--muted2);text-align:center">n.t.</td>';return;} const t=bad(v,i); h+=`<td class="n" style="background:${fill(t)};color:${tx(t)};font-weight:600;text-align:center;padding:16px 10px">${i===3?v:v.toLocaleString('en',{minimumFractionDigits:1,maximumFractionDigits:1})}</td>`; }); h+='</tr>'; });
 h+='<tr><td style="font-weight:700;border-top:2px solid var(--ink)">OECD</td><td style="border-top:2px solid var(--ink)"></td><td class="n" style="text-align:center;border-top:2px solid var(--ink)">34.0</td><td style="border-top:2px solid var(--ink)"></td><td class="n" style="text-align:center;border-top:2px solid var(--ink)">472</td></tr></tbody></table>';
 html('heat',h); asideIn('heat','darker cells sit further behind the Latin American average'); };

/* growth bars */
DRAW.growth=()=>{ const d=[['Vietnam',5.3,GR],['South Korea',4.0,GR],['Panama',3.8,INK],['Costa Rica',2.7,TE],['El Salvador',2.0,INK],['Nicaragua',1.8,INK],['Honduras*',1.5,INK],['Guatemala',1.5,PU],['LAC average',1.3,GR],['Mexico',0.7,OR]];
 const s=svg('growth'); vlab(s,0,24,'Real income per person, average annual growth, 1990 to 2024');
 const y=d3.scaleBand().domain(d.map(e=>e[0])).range([70,690]).padding(.35), x=d3.scaleLinear().domain([0,5.8]).range([230,1040]);
 d.forEach(([n,v,c],i)=>{ const yy=y(n); s.append('text').attr('x',210).attr('y',yy+y.bandwidth()/2+8).attr('text-anchor','end').attr('class','lbl').attr('fill',c===GR?MU:c).text(n);
  const r=s.append('rect').attr('x',230).attr('y',yy).attr('height',y.bandwidth()).attr('width',0).attr('fill',c); grow(r,'width',x(v)-230,i*50);
  s.append('text').attr('x',x(v)+12).attr('y',yy+y.bandwidth()/2+8).attr('class','lbl').text(v.toFixed(1)+'%').attr('opacity',0).transition().delay(dur(500+i*50)).attr('opacity',1); });
 asideIn('growth','grey bars are benchmarks outside the subregion'); };

/* TFP slope */
DRAW.tfp=()=>{ const s=svg('tfp'); vlab(s,0,24,'Total factor productivity, % of the US level');
 const x=d3.scaleLinear().domain([1960,2013]).range([160,900]), y=d3.scaleLinear().domain([40,80]).range([640,110]);
 [40,50,60,70,80].forEach(v=>{ s.append('line').attr('x1',160).attr('x2',900).attr('y1',y(v)).attr('y2',y(v)).attr('stroke',LINE); s.append('text').attr('x',140).attr('y',y(v)+7).attr('text-anchor','end').attr('class','ax').attr('font-size',20).attr('fill',MU2).text(v+'%'); });
 [[1960,'1960'],[2013,'2013']].forEach(([v,t])=>s.append('text').attr('x',x(v)).attr('y',680).attr('text-anchor','middle').attr('font-size',22).attr('fill',MU).text(t));
 [['Latin America',73,51,OR],['East Asia',49,64,BLUE]].forEach(([n,a,b,c],i)=>{ const l=s.append('line').attr('x1',x(1960)).attr('y1',y(a)).attr('x2',x(1960)).attr('y2',y(a)).attr('stroke',c).attr('stroke-width',5); l.transition().delay(dur(200)).duration(dur(1000)).attr('x2',x(2013)).attr('y2',y(b));
  [[1960,a],[2013,b]].forEach(([yr,v],k)=>{ s.append('circle').attr('cx',x(yr)).attr('cy',y(v)).attr('r',0).attr('fill',c).transition().delay(dur(k*1000+200)).duration(dur(300)).attr('r',9); s.append('text').attr('x',x(yr)+(k?22:-22)).attr('y',y(v)+(i?(k?-14:30):(k?30:-14))).attr('text-anchor',k?'start':'end').attr('class','num').attr('font-size',32).attr('fill',c).text(v+'%'); });
  s.append('text').attr('x',x(2013)+22).attr('y',y(b)+(i?18:60)).attr('class','lbl').attr('fill',c).text(n); });
 asideIn('tfp','Chile is the only country in the region that closed any of the gap'); };

/* patents dots */
DRAW.patents=()=>{ const d=[['Guatemala',0.4],['Costa Rica',2.9],['Mexico',9.0],['Chile',19.7],['Brazil',27.1],['South Korea',3783]];
 const s=svg('patents'); vlab(s,0,24,'Resident patents per million people, 2024 · 1 dot = 1 per million');
 d.forEach(([n,v],i)=>{ const yy=90+i*95; const c=cc(n)===INK?GR:cc(n); s.append('text').attr('x',200).attr('y',yy+9).attr('text-anchor','end').attr('class','lbl').attr('fill',cc(n)).text(n);
  s.append('text').attr('x',214).attr('y',yy+9).attr('class','lbl m').text(v.toLocaleString('en'));
  const x0=320; const nd=Math.min(Math.round(v),40);
  if(v<1){ s.append('circle').attr('cx',x0+12).attr('cy',yy).attr('r',11).attr('fill','none').attr('stroke',c).attr('stroke-width',2.5); }
  for(let k=0;k<nd;k++){ s.append('circle').attr('cx',x0+12+k*19).attr('cy',yy).attr('r',0).attr('fill',c).transition().delay(dur(i*120+k*12)).duration(dur(250)).attr('r',8.5); }
  if(v>40){ s.append('text').attr('x',x0+12+40*19+6).attr('y',yy+10).attr('font-size',30).attr('fill',c).text('→'); } });
 s.append('rect').attr('x',320).attr('y',628).attr('width',560).attr('height',58).attr('fill','none').attr('stroke',INK).attr('stroke-width',1.5);
 s.append('text').attr('x',340).attr('y',665).attr('font-size',22).attr('fill',INK).text("1980: Mexico 704, Korea 1,241. Korea's whole lead was 1.8×.");
 asideIn('patents',"Korea's row keeps going for another 55 slide widths"); };

/* constraint test table */
DRAW.test=()=>{ const tag=(t)=>t==='Binds'?`<span style="background:#C9341C;color:#fff;padding:3px 9px;font-size:18px;font-weight:700">Binds</span>`:t==='Partly'?`<span style="background:#F6C9BB;color:#7A1F0E;padding:3px 9px;font-size:18px;font-weight:700">Partly binds</span>`:`<span style="background:#EEECE6;color:var(--muted);padding:3px 9px;font-size:18px">Does not bind</span>`;
 const rows=[['Finance','Private credit, % of GDP · lending spread, points','35.5 · 6.2','No','37.2 · 7.7','No','52.9 · 6.1'],['Human capital','PISA 2022 maths score (OECD 472)','395','Partly','344','Binds','n/a'],['Infrastructure','Logistics index, 1 to 5 · electricity access, %','2.9 · 99.8','No','2.6 · 90.9','Binds','2.7 · 98.0'],['Appropriability','Informal jobs % · homicides per 100k · tax % of GDP','55.5 · 19.3 · 17.7','Binds','83.2 · 16.1 · 14.0','Binds','n/a · 20.2 · 21.3']];
 let h='<table class="t"><thead><tr><th>Constraint</th><th>Indicator</th><th class="c-mex">Mexico</th><th class="c-gua">Guatemala</th><th>LAC</th></tr></thead><tbody>';
 rows.forEach(r=>{ h+=`<tr><td style="font-weight:700">${r[0]}</td><td style="color:#3E3B36;font-size:20px">${r[1]}</td><td class="n" style="font-weight:700">${r[2]}<br>${tag(r[3])}</td><td class="n" style="font-weight:700">${r[4]}<br>${tag(r[5])}</td><td class="n" style="color:var(--muted)">${r[6]}</td></tr>`; });
 html('test',h+'</tbody></table>'); asideIn('test','finance is not the problem in either country. what is missing differs.'); };

/* informality */
DRAW.informal=()=>{ const s=svg('informal'); vlab(s,0,24,'Why firms never get big');
 [[110,45,OR,1],[200,55,OR,1],[310,70,OR,1]].forEach(([x,r,c],i)=>s.append('circle').attr('cx',x).attr('cy',200).attr('r',0).attr('fill',c).transition().delay(dur(i*120)).duration(dur(400)).attr('r',r));
 s.append('line').attr('x1',430).attr('x2',430).attr('y1',80).attr('y2',330).attr('stroke',MG).attr('stroke-width',4).attr('stroke-dasharray','12 10');
 s.append('text').attr('x',445).attr('y',76).attr('font-size',22).attr('fill',MG).attr('font-weight',600).text('the state sees you');
 [[530,45],[660,70],[830,95]].forEach(([x,r],i)=>s.append('circle').attr('cx',x).attr('cy',200).attr('r',r).attr('fill','none').attr('stroke',GR).attr('stroke-width',2.5).attr('stroke-dasharray','6 6'));
 s.append('text').attr('x',210).attr('y',345).attr('text-anchor','middle').attr('class','cl').attr('fill',OR).text('Stays small'); s.append('text').attr('x',680).attr('y',345).attr('text-anchor','middle').attr('class','cl').text('Never happens');
 vlab(s,0,430,'Informal share of workers, ILO harmonised');
 const x=d3.scaleLinear().domain([0,100]).range([60,1000]); s.append('line').attr('x1',60).attr('x2',1000).attr('y1',560).attr('y2',560).attr('stroke',INK).attr('stroke-width',1.5);
 [0,100].forEach(v=>{ s.append('line').attr('x1',x(v)).attr('x2',x(v)).attr('y1',552).attr('y2',568).attr('stroke',INK); s.append('text').attr('x',x(v)).attr('y',600).attr('text-anchor','middle').attr('font-size',20).attr('fill',MU).text(v+'%'); });
 [['Costa Rica',37.4,-1],['Mexico',55.5,1],['Panama',58.7,-1],['Nicaragua',63.0,2],['El Salvador',66.5,-2],['Honduras',82.6,1],['Guatemala',83.2,-1]].forEach(([n,v,side],i)=>{ const c=cc(n)===INK?GRD:cc(n); s.append('circle').attr('cx',x(v)).attr('cy',560).attr('r',0).attr('fill',c).transition().delay(dur(300+i*80)).duration(dur(300)).attr('r',10);
  const yy=560+(side<0?-26*Math.abs(side)-10:30*side+10); s.append('text').attr('x',x(v)).attr('y',yy+(side>0?12:0)).attr('text-anchor','middle').attr('font-size',21).attr('font-weight',700).attr('fill',cc(n)).text(n+' ').append('tspan').attr('font-weight',500).attr('fill',MU).text(v); });
 asideIn('informal','about half the workforce lives to the left of that line'); };

/* export poles */
DRAW.poles=()=>{ const s=svg('poles'); vlab(s,0,24,'IMMEX inputs, 2024'); vlab(s,560,24,'Multidimensional poverty, % of people, 2024');
 const r1=s.append('rect').attr('x',0).attr('y',70).attr('width',380).attr('height',0).attr('fill',GR); grow(r1,'height',330,0,900);
 const r2=s.append('rect').attr('x',0).attr('y',400).attr('width',380).attr('height',0).attr('fill',OR); grow(r2,'height',140,300,700);
 s.append('text').attr('x',24).attr('y',130).attr('class','num').attr('font-size',56).attr('fill',INK).text('>70%'); s.append('text').attr('x',24).attr('y',165).attr('font-size',22).attr('fill',INK).text('imported');
 s.append('text').attr('x',24).attr('y',470).attr('class','num').attr('font-size',56).attr('fill','#fff').text('<30%'); s.append('text').attr('x',24).attr('y',505).attr('font-size',22).attr('fill','#fff').text('domestic');
 s.append('text').attr('x',0).attr('y',590).attr('font-size',22).attr('fill',MU).text('Economic Complexity Index:');
 s.append('text').attr('x',0).attr('y',620).attr('font-size',22).attr('fill',MU).text('Mexico ranks 17th of 133.');
 s.append('text').attr('x',0).attr('y',650).attr('font-size',22).attr('fill',MU).text('The capability sits abroad.');
 const x=d3.scaleLinear().domain([0,70]).range([560,1040]);
 [['Chiapas · southern border',66.0,INK],['Mexico · national',29.6,GR],['Nuevo León · industrial north',10.6,BLUE]].forEach(([n,v,c],i)=>{ const yy=90+i*150; s.append('text').attr('x',560).attr('y',yy).attr('font-size',22).attr('font-weight',700).attr('fill',c===GR?INK:c).text(n);
  const r=s.append('rect').attr('x',560).attr('y',yy+16).attr('height',44).attr('width',0).attr('fill',c); grow(r,'width',x(v)-560,i*120);
  s.append('text').attr('x',x(v)+14).attr('y',yy+48).attr('class','num').attr('font-size',34).text(v.toFixed(1)); });
 s.append('rect').attr('x',560).attr('y',578).attr('width',480).attr('height',96).attr('fill','none').attr('stroke',BLUE).attr('stroke-width',1.5);
 s.append('text').attr('x',578).attr('y',616).attr('font-size',21).attr('fill',INK).text("Nuevo León's export factories buy 39% of all"); s.append('text').attr('x',578).attr('y',646).attr('font-size',21).attr('fill',INK).text("domestic inputs purchased by Mexico's IMMEX firms.");
 asideIn('poles','a factory that imports its parts exports wages, not know-how'); };

/* northern triangle state: three panels */
DRAW.state=()=>{ const s=svg('state'); const panels=[['REVENUE','Tax revenue|% of GDP, 2023',[['Panama',11.9],['Guatemala',14.0],['Mexico',17.7],['Costa Rica',24.9],['LAC avg.',21.3],['OECD avg.',34.0]],36],['SKILLS','Years of schooling behind the OECD|PISA 2022 maths',[['Mexico',4],['Costa Rica',4],['Panama',6],['Guatemala',6],['El Salvador',6]],7],['SAFETY','Homicides per 100,000 people|2024',[['Honduras',25.3],['Mexico',19.3],['Costa Rica',16.6],['Guatemala',16.1],['LAC median',20.2]],28]];
 panels.forEach(([t,sub,rows,max],p)=>{ const x0=p*365; s.append('text').attr('x',x0).attr('y',24).attr('class','cl').attr('fill',INK).text(t); s.append('line').attr('x1',x0).attr('x2',x0+330).attr('y1',40).attr('y2',40).attr('stroke',INK).attr('stroke-width',1.5);
  s.append('text').attr('x',x0).attr('y',80).attr('font-size',20).attr('fill',MU).text(sub.split('|')[0]); s.append('text').attr('x',x0).attr('y',106).attr('font-size',20).attr('fill',MU).text(sub.split('|')[1]);
  const x=d3.scaleLinear().domain([0,max]).range([x0+150,x0+320]);
  rows.forEach(([n,v],i)=>{ const yy=150+i*62; const bench=/avg|median/.test(n); s.append('text').attr('x',x0+140).attr('y',yy+22).attr('text-anchor','end').attr('font-size',21).attr('font-weight',bench?500:600).attr('fill',bench?MU:cc(n)).text(n);
   const r=s.append('rect').attr('x',x0+150).attr('y',yy).attr('height',30).attr('width',0).attr('fill',bench?GR:(cc(n)===INK?INK:cc(n))); grow(r,'width',x(v)-x0-150,p*150+i*60);
   s.append('text').attr('x',x(v)+10).attr('y',yy+23).attr('font-size',21).attr('font-weight',700).text((p===1?'~':'')+v); }); });
 asideIn('state','violence works as a second, private tax on growth'); };

/* inclusion */
DRAW.inclusion=()=>{ const s=svg('inclusion'); const L=[['Panama',49.7],['Nicaragua*',46.2],['Honduras',45.7],['Costa Rica',45.5],['Guatemala',45.2],['Mexico',42.6],['El Salvador',39.8]], R=[['Nicaragua',30.5],['Guatemala',29.1],['Honduras',22.4],['Panama',16.0],['El Salvador',13.9],['Costa Rica',11.5],['Mexico',11.4]];
 const draw=(d,x0,title,max,fmt)=>{ vlab(s,x0,24,title); s.append('line').attr('x1',x0).attr('x2',x0+500).attr('y1',40).attr('y2',40).attr('stroke',INK).attr('stroke-width',1.5); const x=d3.scaleLinear().domain([0,max]).range([x0+160,x0+440]);
  d.forEach(([n,v],i)=>{ const yy=80+i*72; const c=cc(n.replace('*',''))===INK?INK:cc(n.replace('*','')); s.append('text').attr('x',x0+150).attr('y',yy+24).attr('text-anchor','end').attr('font-size',22).attr('font-weight',600).attr('fill',c).text(n);
   const r=s.append('rect').attr('x',x0+160).attr('y',yy).attr('height',34).attr('width',0).attr('fill',c); grow(r,'width',x(v)-x0-160,i*60); s.append('text').attr('x',x(v)+12).attr('y',yy+25).attr('font-size',22).attr('font-weight',700).text(fmt(v)); }); };
 draw(L,0,'Income inequality, Gini index',55,v=>v.toFixed(1)); draw(R,560,'Jobs in agriculture, % of employment',35,v=>v.toFixed(1)+'%');
 asideIn('inclusion','has anyone in or near the region broken these walls?'); };

/* costa rica vs panama */
DRAW.crpa=()=>{ const rows=[['Growth a year since 1990','2.7%','3.8%'],['R&D, % of GDP','0.34','0.20'],['Tax, % of GDP','24.9','11.9'],['Informal jobs','37%','59%'],['Gini index','45.5','49.7']];
 let h='<table class="t" style="font-size:26px"><thead><tr><th></th><th class="c-cr">Costa Rica</th><th>Panama</th></tr></thead><tbody>'; rows.forEach(r=>h+=`<tr><td style="color:#3E3B36">${r[0]}</td><td class="n" style="font-family:var(--display);font-weight:800;font-size:40px;letter-spacing:-.02em">${r[1]}</td><td class="n" style="font-family:var(--display);font-weight:800;font-size:40px;letter-spacing:-.02em">${r[2]}</td></tr>`); html('crpa',h+'</tbody></table>'); asideIn('crpa','same geography, opposite choices, opposite results'); };

/* precedents */
DRAW.precedents=()=>{ const d=[['4 → 29','Vietnam · supplier development, 2014 to 2017',"Samsung's local tier-1 suppliers rose sevenfold in three years.",'Mexico',OR],['−90%','Medellín · social urbanism, 2004 onward','Transport and public buildings went to the poorest comunas first. Homicides fell about 90% from 1991.','Northern Triangle',PU],['44%','Costa Rica · CINDE, 1982','Targeted investment promotion plus skills: medical devices reached 44% of goods exports.','Capability',BLUE]];
 let h='<div style="display:flex;flex-direction:column;gap:0;margin-top:20px">'; d.forEach(([n,t,sub,tag,c])=>{ h+=`<div style="display:grid;grid-template-columns:300px 1fr 230px;gap:30px;align-items:center;padding:34px 0;border-top:1.5px solid var(--line)"><div style="font-family:var(--display);font-weight:800;font-size:72px;letter-spacing:-.04em;color:${c}">${n}</div><div><div style="font-size:26px;font-weight:700">${t}</div><div style="font-size:22px;color:#3E3B36;margin-top:6px;line-height:1.35">${sub}</div></div><div style="justify-self:end;background:#FBEDE9;color:var(--red);font-weight:700;font-size:20px;padding:6px 14px">${tag}</div></div>`; }); html('precedents',h+'<div style="border-top:1.5px solid var(--line)"></div></div>'); asideIn('precedents','none of it was luck. all of it was policy.'); };

/* programme blocks */
const progFoot=(items)=>`<div style="position:absolute;left:0;bottom:120px;width:100%;display:grid;grid-template-columns:repeat(3,1fr);gap:40px">${items.map(([k,v])=>`<div style="border-top:2px solid var(--ink);padding-top:14px"><div style="font-family:var(--cond);font-size:19px;letter-spacing:.18em;color:var(--red);font-weight:700">${k}</div><div style="font-size:23px;line-height:1.35;margin-top:8px">${v}</div></div>`).join('')}</div>`;
DRAW.prog1=()=>{ const steps=[['01','A big factory arrives',0],['02 · fund','Local firms learn to supply it',1],['03','Skills spread',0],['04','It runs on its own',0],['05 · fund','Roads reach the towns outside',1]];
 let h='<div class="vlab" style="left:0;top:0">Linkages: pay for the two steps markets skip</div><div style="position:absolute;top:60px;left:0;width:100%;display:grid;grid-template-columns:repeat(5,1fr);gap:18px">'; steps.forEach(([n,t,f])=>h+=`<div><div style="height:8px;background:${f?'var(--red)':'var(--line)'}"></div><div style="font-family:var(--cond);font-size:19px;letter-spacing:.14em;color:${f?'var(--red)':'var(--muted2)'};font-weight:700;margin-top:12px">${n.toUpperCase()}</div><div style="font-size:${f?24:22}px;line-height:1.3;margin-top:6px;color:${f?'var(--ink)':'var(--muted)'};font-weight:${f?700:400}">${t}</div></div>`);
 h+='</div><p style="position:absolute;top:260px;left:0;width:100%;font-size:24px;line-height:1.4;margin:0"><b>Formalisation:</b> move health and pensions from wages to general revenue, so firms can grow into suppliers. Modelled net cost: <b>0.34% of GDP</b>.</p>';
 h+=progFoot([['PILOT','Nuevo León pole to Chiapas'],['IDB INSTRUMENT','Investment loan, IDB Invest supply-chain finance, then a policy-based loan'],['MEASURED BY','Domestic share of export inputs, now under 30%']]);
 html('prog1',h); asideIn('prog1','record investment is landing in Mexico now. linkages decide what it builds.'); };
DRAW.prog2=()=>{ const cols=[['REVENUE','14.0%','tax take, Guatemala, 2023','Broader VAT base and e-invoicing'],['SECURITY','25.3','homicides per 100k, Honduras, 2024','A security component in every corridor'],['CONNECTIVITY','88.7%','electricity access, Nicaragua, 2024','Roads, power and broadband to lagging towns']];
 let h='<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:40px;margin-top:10px">'; cols.forEach(([k,n,s,t])=>h+=`<div style="border-top:2px solid var(--ink);padding-top:14px"><div style="font-family:var(--cond);font-size:19px;letter-spacing:.18em;color:var(--red);font-weight:700">${k}</div><div style="font-family:var(--display);font-weight:800;font-size:64px;letter-spacing:-.04em;margin-top:10px">${n}</div><div style="font-size:20px;color:var(--muted);margin-top:4px">${s}</div><div style="font-size:24px;font-weight:600;margin-top:18px;line-height:1.3">${t}</div></div>`);
 h+='</div>'+progFoot([['PILOT','Guatemala first'],['IDB INSTRUMENT','Policy-based loan for revenue, investment loans for corridors'],['MEASURED BY','Tax take, homicides, travel time to the nearest town']]);
 html('prog2',h); asideIn('prog2','every other fix is paid for from this base'); };
DRAW.prog3=()=>{ let h='<div class="vlab" style="left:0;top:0">Who carries the risk, over time</div><div style="position:absolute;top:60px;left:0;width:100%;display:grid;grid-template-columns:1fr 40px 1fr 40px 1fr;gap:0;align-items:center">';
 const box=(parts,lab,labc)=>`<div><div style="display:flex;height:150px">${parts.map(([c,f])=>`<div style="flex:${f};background:${c}"></div>`).join('')}</div><div style="font-family:var(--cond);font-size:20px;letter-spacing:.14em;margin-top:14px;color:${labc};font-weight:700">${lab}</div></div>`;
 h+=box([[BLUE,1]],'AGENCY PROVES IT',BLUE)+'<div style="text-align:center;font-size:30px;color:var(--muted2)">→</div>'+box([[BLUE,1],[OR,1]],'HANDS IT TO FIRMS',INK)+'<div style="text-align:center;font-size:30px;color:var(--muted2)">→</div>'+box([[OR,1]],'AGENCY LEAVES',OR)+'</div>';
 h+=progFoot([['MODEL','CINDE, Costa Rica, 1982'],['PILOT','One Mexican export state, then the isthmus'],['MEASURED BY','Two new export products by year five']]);
 html('prog3',h); asideIn('prog3','factories are leaving China right now. they have to land somewhere.'); };

/* sequencing */
DRAW.seq=()=>{ const s=svg('seq'); vlab(s,0,24,'Ten years, three programmes'); const x=d3.scaleLinear().domain([0,10]).range([0,1040]);
 const bands=[['Mexico: linkages and formalisation · years 0 to 8',0,8,OR,null],['Northern Triangle: revenue, then corridors · revenue years 0 to 3, corridors from year 3',0,10,PU,3],['Capability agency · years 3 to 10',3,10,BLUE,null]];
 bands.forEach(([t,a,b,c,split],i)=>{ const yy=90+i*140; s.append('text').attr('x',0).attr('y',yy).attr('font-size',23).attr('font-weight',700).text(t.split(' · ')[0]).append('tspan').attr('font-weight',400).attr('fill',MU).text(' · '+t.split(' · ').slice(1).join(' · '));
  if(split!=null){ const p=s.append('rect').attr('x',x(a)).attr('y',yy+20).attr('height',40).attr('width',0).attr('fill',c).attr('opacity',.45); grow(p,'width',x(split)-x(a),i*200); const q=s.append('rect').attr('x',x(split)).attr('y',yy+20).attr('height',40).attr('width',0).attr('fill',c); grow(q,'width',x(b)-x(split),i*200+400); }
  else { const r=s.append('rect').attr('x',x(a)).attr('y',yy+20).attr('height',40).attr('width',0).attr('fill',c); grow(r,'width',x(b)-x(a),i*200,900); } });
 s.append('line').attr('x1',0).attr('x2',1040).attr('y1',520).attr('y2',520).attr('stroke',INK).attr('stroke-width',1.5);
 [[0,'Year 0'],[10,'Year 10']].forEach(([v,t])=>s.append('text').attr('x',x(v)).attr('y',555).attr('text-anchor',v?'end':'start').attr('font-size',21).attr('fill',MU).text(t));
 [[2,'Year 2','first certified local suppliers'],[3,'Year 3',"Guatemala's tax up one point"],[5,'Year 5','first new export product']].forEach(([v,t,sub],i)=>{ s.append('path').attr('d',`M${x(v)} 508 l12 12 l-12 12 l-12 -12 z`).attr('fill',RD); s.append('text').attr('x',x(v)).attr('y',555).attr('text-anchor','middle').attr('font-size',21).attr('font-weight',700).attr('fill',RD).text(v); s.append('text').attr('x',0).attr('y',605+i*36).attr('font-size',22).attr('font-weight',700).attr('fill',RD).text((i+1)+' · '+t+' ').append('tspan').attr('font-weight',400).attr('fill',INK).text(sub); });
 asideIn('seq','a plan that ignores the electoral calendar never happens'); };

/* three counts */
DRAW.counts=()=>{ const d=[['Linkages · Mexico',1,5,'<30%','domestic share of export-factory inputs, 2024',"Against Vietnam's 20% to 25% localisation",BLUE],['Formal jobs · Mexico',2,5,'55.5%','of workers informal','Against Costa Rica, 37.4%',OR],['State capacity · Guatemala',1,5,'14.0%','tax take, % of GDP, 2023','Against the LAC average, 21.3%',PU]];
 let h='<div class="vlab" style="left:0;top:0">The three counts, with baselines · solid = today · hollow = where we are aiming</div><div style="position:absolute;top:70px;left:0;width:100%;display:grid;grid-template-columns:repeat(3,1fr);gap:40px">';
 d.forEach(([t,on,n,big,sub,cmp,c])=>{ h+=`<div style="border-top:2px solid var(--ink);padding-top:16px"><div style="font-size:24px;font-weight:700;min-height:66px">${t}</div><div style="display:flex;gap:10px;margin:10px 0 18px">${Array.from({length:n},(_,k)=>`<span style="width:22px;height:22px;border-radius:50%;display:block;${k<on?`background:${c}`:`border:2.5px solid ${c}`}"></span>`).join('')}</div><div style="font-family:var(--display);font-weight:800;font-size:72px;letter-spacing:-.04em;color:${c}">${big}</div><div style="font-size:21px;margin-top:6px;line-height:1.3">${sub}</div><div style="font-size:20px;color:var(--muted);margin-top:10px;line-height:1.3">${cmp}</div></div>`; });
 html('counts',h+'</div>'); asideIn('counts','a number we cannot defend is worth less than an honest blank'); };

/* appendix */
DRAW.a1=()=>{ const H=['Indicator','Mexico','Guatemala','Honduras','El Salvador','Nicaragua','Costa Rica','Panama','Year · source'];
 const R=[['GDP per head, PPP US$','25,820','14,393','7,503','13,258','8,721','31,552','41,430','2024 · WDI'],['Resident patent filings','1,172','8','8 (2018)','6','1 (2014)','15','11','2024 · WDI'],['R&D spending, % of GDP','0.25','0.01 (2023)','0.06 (2019)','0.10 (2023)','0.11 (2015)','0.34 (2023)','0.20','2024 · WDI'],['Researchers per million','438','1.4 (2023)','188 (2019)','55 (2023)','71 (1997)','508 (2023)','250','2024 · WDI'],['Informal jobs, % of workers','55.5','83.2','82.6','66.5','63.0','37.4','58.7','Latest · ILOSTAT'],['Tax revenue, % of GDP','17.7','14.0','21.0','22.8','27.5','24.9','11.9','2023 · Rev. Stats LAC'],['Remittances, % of GDP','3.7','19.1','25.7','24.3','26.6','0.7','0.6','2024 · WDI'],['Homicides per 100,000','19.3','16.1','25.3','1.9*','n.a.','16.6','12.9','2024 · InSight Crime'],['PISA maths score','395','344','n.t.','343','n.t.','385','357','2022 · OECD PISA']];
 const cls=['','c-mex','c-gua','','','','c-cr','',''];
 let h='<table class="t" style="font-size:21px"><thead><tr>'+H.map((x,i)=>`<th class="${cls[i]}" style="${i?'text-align:right':''}${cls[i]?';color:var(--'+(cls[i]==='c-mex'?'orange':cls[i]==='c-gua'?'purple':'teal')+')':''}">${x}</th>`).join('')+'</tr></thead><tbody>';
 R.forEach(r=>h+='<tr>'+r.map((v,i)=>`<td class="${i?'n':''}" style="${i?'text-align:right':'font-weight:600'};padding:12px 18px 12px 0;${i===8?'color:var(--muted)':''}">${v}</td>`).join('')+'</tr>'); html('a1',h+'</tbody></table>'); };
DRAW.a2=()=>{ const R=[['CR-L1043 · Innovation and Human Capital for Competitiveness','Costa Rica, 2012','US$35m','Programme 3, capability agency'],['Border Integration Programme','Costa Rica','US$100m','Programme 2, corridor works'],['Border Integration Programme','Nicaragua','US$55m','Programme 2, corridor works'],['A recent programmatic policy-based loan','Mexico or Guatemala','From the IDB project database','Programme 1, budget support']];
 let h='<table class="t" style="font-size:24px"><thead><tr><th>Project</th><th>Country, year</th><th>Amount</th><th>Benchmark for</th></tr></thead><tbody>'; R.forEach(r=>h+=`<tr><td style="padding:24px 18px 24px 0">${r[0]}</td><td>${r[1]}</td><td style="font-family:var(--display);font-weight:800;font-size:32px;${/^From/.test(r[2])?'font-family:var(--body);font-weight:400;font-size:22px;color:var(--muted)':''}">${r[2]}</td><td>${r[3]}</td></tr>`); html('a2',h+'</tbody></table>'); };
DRAW.a3=()=>{ html('a3',`<div style="display:grid;grid-template-columns:1fr 1fr 1.2fr;gap:50px;margin-top:10px">
<div style="border-top:2px solid var(--ink);padding-top:16px"><div style="font-family:var(--display);font-weight:800;font-size:56px;letter-spacing:-.04em;color:var(--red)">0.9% to 1.44%</div><div style="font-family:var(--cond);font-size:19px;letter-spacing:.14em;color:var(--muted);margin:6px 0 12px">OF GDP EVERY YEAR</div><div style="font-size:22px;line-height:1.4">Levy's estimate of the static efficiency cost of Mexico's formal-informal wedge (Levy, 2008).</div></div>
<div style="border-top:2px solid var(--ink);padding-top:16px"><div style="font-family:var(--display);font-weight:800;font-size:56px;letter-spacing:-.04em;color:var(--red)">0.34%</div><div style="font-family:var(--cond);font-size:19px;letter-spacing:.14em;color:var(--muted);margin:6px 0 12px">OF GDP, NET FISCAL COST</div><div style="font-size:22px;line-height:1.4">Antón, Hernández and Levy (2012, IDB): universal social insurance funded from general revenue, a uniform 16% VAT, and compensation for poor households.</div></div>
<div style="border-top:2px solid var(--ink);padding-top:16px"><div style="font-size:25px;font-weight:700;margin-bottom:12px">Brazil's SIMPLES: three studies, three answers</div><table class="t" style="font-size:22px"><tr><td>Fajnzylber, Maloney and Montes-Rojas (2011)</td><td style="font-weight:700">Large</td></tr><tr><td>Monteiro and Assunção (2012)</td><td style="font-weight:700">Limited</td></tr><tr><td>Piza (2018)</td><td style="font-weight:700">None</td></tr></table><div style="font-size:21px;color:var(--muted);margin-top:12px;line-height:1.4">Simplifying paperwork alone is not enough, so programme one removes the wage wedge itself.</div></div></div>
<div style="margin-top:60px"><div style="font-family:var(--cond);font-size:19px;letter-spacing:.18em;color:var(--muted);border-bottom:2px solid var(--ink);padding-bottom:10px">COUNTERARGUMENTS WE CONSIDERED</div><table class="t" style="font-size:23px">
<tr><td style="font-family:var(--display);font-weight:800;font-size:30px;width:420px">“It is geography.”</td><td>Costa Rica shares the geography, and it is the outlier on almost every indicator on slide 3.</td></tr>
<tr><td style="font-family:var(--display);font-weight:800;font-size:30px">“It is corruption.”</td><td>It is a component of weak state capacity, rather than a separate cause.</td></tr>
<tr><td style="font-family:var(--display);font-weight:800;font-size:30px">“Nearshoring will fix it.”</td><td>Mexico's record 2025 FDI was 67.7% reinvested earnings and only 18% new investment, and assembly without linkages repeats the maquila pattern.</td></tr></table></div>`); };

/* nav */
const slides=[...document.querySelectorAll('.slide')], N=slides.length; let i=0;
function show(k){ i=Math.max(0,Math.min(N-1,k)); slides.forEach((s,j)=>s.classList.toggle('active',j===i)); const s=slides[i]; const v=s.querySelector('.viz'); if(v&&DRAW[v.id]) DRAW[v.id](); if(s.querySelector('#dots8')) DRAW.dots8(); try{localStorage.setItem('idb-v3',String(i));}catch(e){} }
document.addEventListener('keydown',e=>{ if(['ArrowRight','ArrowDown',' ','PageDown'].includes(e.key)){e.preventDefault();show(i+1);} else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();show(i-1);} else if(e.key==='Home')show(0); else if(e.key==='End')show(N-1); });
const vp=document.getElementById('viewport'); vp.addEventListener('click',e=>{ const r=vp.getBoundingClientRect(); show(e.clientX-r.left>r.width/2?i+1:i-1); });
let tx=null; vp.addEventListener('touchstart',e=>{tx=e.touches[0].clientX},{passive:true}); vp.addEventListener('touchend',e=>{ if(tx===null)return; const dx=e.changedTouches[0].clientX-tx; if(Math.abs(dx)>40)show(dx<0?i+1:i-1); tx=null; });
function fit(){ const sc=Math.min(window.innerWidth/1920,window.innerHeight/1080); document.getElementById('stage').style.transform=`scale(${sc})`; } window.addEventListener('resize',fit); fit();
let start=0; try{ const v=parseInt(localStorage.getItem('idb-v3')); if(!isNaN(v)&&v<N)start=v; }catch(e){} show(start); window.show=show;
'''

OUT.write_text(f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Eight Patents IDB</title>
<meta name="description" content="Growth diagnostic for Mexico and Central America, for the Inter-American Development Bank. Group 1, IE University.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800&family=Archivo+Narrow:wght@500;700&family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@1,8..60,400&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="hint">← → SPACE · {MAIN} SLIDES + 4 BACKUP</div>
<div id="viewport"><div id="stage">
{SLIDES}
</div></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script>{JS}</script>
</body>
</html>''')
print('wrote', OUT.name, 'slides', len(S), 'main', MAIN)
