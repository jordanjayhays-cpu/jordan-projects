"""Assemble PEPE_Energia_DataLens_v8.html: one design system, three modes (Panel, Historia, Ciudad).
Sources: v5 (panel), v6 (historia), v7 (ciudad). Each module keeps its own logic; this script
scopes CSS per module, renames colliding classes, wraps JS in its own scope, removes per-file
chrome and applies shared tokens. Data stays identical to v4."""
import re, pathlib

SRC = {
  'panel':   pathlib.Path('PEPE_Energia_DataLens_v5.html').read_text(),
  'historia':pathlib.Path('PEPE_Energia_Flow_v6.html').read_text(),
  'ciudad':  pathlib.Path('PEPE_Energia_Noche_v7.html').read_text(),
}

def part(html, a, b, last=False):
    i = html.rfind(a) if last else html.find(a); assert i >= 0, a
    j = html.find(b, i + len(a)); assert j >= 0, b
    return html[i + len(a):j]

def css_of(h): return part(h, '<style>', '</style>')
def body_of(h):
    b = part(h, '<body>', '</body>')
    return re.sub(r'<script\b[^>]*>.*?</script>', '', b, flags=re.S)
def js_of(h):
    return [m.group(1) for m in re.finditer(r'<script>(.*?)</script>', h, re.S)]

# ---------- CSS scoper ----------
DROP = ('*', 'html', 'body', 'html,body', 'button', 'button,input', 'a', ':root')
def scope_css(css, scope):
    out = []; i = 0; n = len(css)
    def parse(s, i, depth):
        res = []
        while i < n:
            j = s.find('{', i)
            if j < 0: break
            sel = s[i:j].strip()
            # find matching close
            k = j + 1; d = 1
            while k < n and d:
                if s[k] == '{': d += 1
                elif s[k] == '}': d -= 1
                k += 1
            body = s[j+1:k-1]
            if sel.startswith('@keyframes') or sel.startswith('@font-face'):
                res.append(f'{sel}{{{body}}}')
            elif sel.startswith('@media'):
                res.append(f'{sel}{{{parse_inner(body)}}}')
            else:
                sels = [x.strip() for x in sel.split(',')]
                keep = [x for x in sels if x and x not in DROP and not x.startswith(':root')]
                if keep:
                    res.append(', '.join(f'{scope} {x}' for x in keep) + '{' + body + '}')
            i = k
        return ''.join(res)
    def parse_inner(body):
        return parse(body, 0, 1)
    # strip comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    return parse(css, 0, 0)

# ---------- per-module transforms ----------
# PANEL (v5)
pc = scope_css(css_of(SRC['panel']), '#m-panel')
pb = body_of(SRC['panel'])
pb = re.sub(r'<header class="top">.*?</header>', lambda m: '<div class="subbar">' + re.search(r'<nav class="nav" id="nav">.*?</nav>', m.group(0), re.S).group(0) + '</div>', pb, flags=re.S)
pb = re.sub(r'<footer class="foot">.*?</footer>', '', pb, flags=re.S)
pj = [j for j in js_of(SRC['panel']) if 'const PLANTS' in j][0]
pj += "\nwindow.MODES.panel={activate(){ DRAW[cur].forEach(f=>f()); highlight(state.plant); }};\n"

# HISTORIA (v6)
hcss = css_of(SRC['historia']).replace('.card', '.sc')
hc = scope_css(hcss, '#m-historia')
hb = body_of(SRC['historia']).replace('class="card"', 'class="sc"')
hb = re.sub(r'<div class="bar">.*?</div>\n', '', hb, flags=re.S)
hb = re.sub(r'<footer>.*?</footer>', '', hb, flags=re.S)
hj = js_of(SRC['historia'])[0]
hj += "\nwindow.MODES.historia={activate(){ resize(); LAYOUT[step](); }};\n"

# CIUDAD (v7)
ccss = css_of(SRC['ciudad']).replace('.card', '.ccard')
cc = scope_css(ccss, '#m-ciudad')
cb = body_of(SRC['ciudad']).replace('class="card" id="card"', 'class="ccard" id="card"')
cb = re.sub(r'<span class="badge">.*?</span>', '', cb, flags=re.S)
cj = js_of(SRC['ciudad'])[0]
cj += "\nwindow.MODES.ciudad={activate(){ render(); }};\n"

for name, js in (('panel', pj), ('historia', hj), ('ciudad', cj)):
    assert 'const PLANTS' in js, name

# ---------- shared shell ----------
TOKENS = """
:root{
  /* one palette: focus orange, good green, alert red, everything else grey */
  --bg:#0D0F14; --paper:#0D0F14; --panel:#141822; --bg2:#141822; --card:#171B26; --line:#262B38;
  --ink:#F2EFE6; --muted:#9AA0AE; --muted2:#6E7585;
  --orange:#F57C00; --orange-soft:#3B2612; --orange-deep:#FFA04D;
  --green:#43C97A; --green-soft:#163D28; --solar:#43C97A;
  --red:#F0524F; --red-soft:#3D1A1A; --alert:#F0524F;
  --grey:#4B5160; --grey-deep:#7B8294; --grey-soft:#232835; --slate:#7B8294;
  --gold:#FFC94D; --lamp:#FFC94D; --lamp2:#FFE7A3; --ember:#FF6A3D; --smoke:#9AA3B5; --grid:#6EA8FF;
  --sans:'Montserrat',-apple-system,'Segoe UI',Helvetica,Arial,sans-serif; --serif:var(--sans);
  --mono:'JetBrains Mono',ui-monospace,Menlo,Consolas,monospace;
  --hdr:56px;
  color-scheme:dark;
}
:root[data-theme="light"]{--bg:#0D0F14;--ink:#F2EFE6}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.5;-webkit-font-smoothing:antialiased;padding-left:env(safe-area-inset-left,0px);padding-right:env(safe-area-inset-right,0px)}
button,input{font-family:inherit}
a{color:inherit}
/* shell */
.shell{position:sticky;top:0;z-index:100;height:var(--hdr);display:flex;align-items:center;justify-content:space-between;gap:12px;padding:0 20px;background:rgba(13,15,20,.92);border-bottom:1px solid var(--line);backdrop-filter:blur(8px)}
.shell .brand{font-size:15px;font-weight:700;white-space:nowrap}
.shell .brand b{color:var(--orange);font-weight:800}
.shell .brand span{color:var(--muted);font-weight:500}
.modes{display:flex;gap:4px;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:3px}
.modes button{background:transparent;border:0;color:var(--muted);padding:7px 14px;border-radius:6px;font-size:13px;font-weight:600;cursor:pointer;display:flex;gap:8px;align-items:center;transition:background .15s,color .15s,transform .08s}
.modes button:active{transform:scale(.97)}
.modes button .k{font-family:var(--mono);font-size:10.5px;color:var(--muted2)}
.modes button.on{background:var(--orange);color:#1a1000}
.modes button.on .k{color:#1a1000}
.shell .badge{font-family:var(--mono);font-size:11px;letter-spacing:.08em;color:var(--gold);border:1px solid rgba(255,201,77,.4);padding:4px 9px;border-radius:3px;white-space:nowrap}
.mode{display:none}
.mode.on{display:block}
#m-ciudad.on{display:block;height:calc(100svh - var(--hdr));overflow:hidden}
.gfoot{max-width:1280px;margin:0 auto;padding:18px 20px 60px;font-family:var(--mono);font-size:11.5px;color:var(--muted);line-height:1.6;border-top:1px solid var(--line)}
.gfoot b{color:var(--ink);font-weight:500}
.shell .brand{min-width:0;overflow:hidden;text-overflow:ellipsis}
.modes{flex:none}
@media(max-width:820px){.shell{padding:0 10px;gap:8px}.shell .brand{font-size:13px}.shell .brand span{display:none}.modes button{padding:7px 9px;font-size:12px}.modes button .k{display:none}.shell .badge{display:none}}
"""

OVER = """
/* panel on the dark system: a few rules the light version set explicitly */
#m-panel .subbar{position:sticky;top:var(--hdr);z-index:50;background:rgba(13,15,20,.92);border-bottom:1px solid var(--line);backdrop-filter:blur(8px)}
#m-panel .subbar .nav{max-width:1280px;margin:0 auto;padding:10px 16px}
#m-panel .nav button{border-color:var(--line);color:var(--muted)}
#m-panel .nav button .n{color:var(--orange)}
#m-panel .nav button.active{background:var(--orange);border-color:var(--orange);color:#1a1000}
#m-panel .nav button.active .n{color:#1a1000}
#m-panel .kpi{border-top-color:var(--muted2)}
#m-panel .kpi.focus{border-top-color:var(--orange)}#m-panel .kpi.good{border-top-color:var(--green)}#m-panel .kpi.bad{border-top-color:var(--red)}
#m-panel .chip.on{color:var(--bg)}
#m-panel .decide{background:var(--card);border:1px solid var(--orange);color:var(--ink)}
#m-panel .decide li span{color:var(--muted)}
#m-panel .decide .k{color:var(--orange)}
#m-panel .decide li .n{color:#1a1000}
#m-panel #tip{background:var(--ink);color:var(--bg)}
#m-panel #tip b{color:var(--orange)}
#m-panel .chat .h{background:var(--panel)}
#m-panel .chat .i button{color:#1a1000}
#m-panel .chat-toggle{color:#1a1000}
#m-panel .rs::before{border-color:var(--card)}
#m-panel .tb th{color:var(--muted);border-bottom-color:var(--grey-deep)}
#m-panel .al{border-left-color:var(--grey-deep)}
#m-panel .al.crit{border-left-color:var(--red)}
#m-panel .lead .so{color:var(--muted)}
/* historia under the shell */
#m-historia .gfx{top:var(--hdr);height:calc(100vh - var(--hdr));height:calc(100svh - var(--hdr))}
#m-historia .rail{top:calc(50% + var(--hdr)/2)}
@media(max-width:900px){#m-historia .gfx{height:48svh}}
/* ciudad under the shell */
#m-ciudad .app{height:100%}
#m-ciudad header h1{font-family:var(--sans);font-weight:800}
#m-ciudad header h1 em{font-style:normal;color:var(--orange)}
#m-ciudad .now .big{font-family:var(--sans);font-weight:800}
#m-ciudad .ccard h2{font-family:var(--sans);font-weight:800}
#m-ciudad .play{color:#1a1000}
#m-ciudad .mode button.on.g{color:#032b14}
"""

SHELL_HTML = """
<div class="shell">
  <div class="brand"><b>PEPE</b> Energía · DataLens <span>· eficiencia energética 2025</span></div>
  <div class="modes" role="tablist">
    <button role="tab" data-m="panel"><span class="k">1</span>Panel</button>
    <button role="tab" data-m="historia"><span class="k">2</span>Historia</button>
    <button role="tab" data-m="ciudad"><span class="k">3</span>Ciudad</button>
  </div>
  <span class="badge">v8 · DATOS DE DEMOSTRACIÓN</span>
</div>
"""

GFOOT = """
<footer class="gfoot"><b>Datos:</b> conjunto de demostración de PEPE Energía (febrero 2026), idénticos en los tres modos y a la versión 4 original. <b>Referencias sectoriales:</b> IDAE, Eurostat, AENOR. <b>2026 a 2028:</b> escenarios del plan, no datos observados. <b>Modos:</b> Panel para analizar, Historia para contar, Ciudad para sentir. Un mismo sistema: naranja es el foco, gris el contexto, rojo la alerta, verde el objetivo. Rediseño sobre el trabajo original de fiovana DataLens.</footer>
"""

SHELL_JS = """
window.MODES=window.MODES||{};
(function(){
  const names=['panel','historia','ciudad'];
  let cur=null;
  function setMode(m,push=true){
    if(!names.includes(m))m='panel';
    cur=m;
    document.querySelectorAll('.mode').forEach(s=>s.classList.toggle('on',s.id==='m-'+m));
    document.querySelectorAll('.modes button').forEach(b=>b.classList.toggle('on',b.dataset.m===m));
    document.getElementById('gfoot').style.display=(m==='ciudad')?'none':'';
    document.body.style.overflow=(m==='ciudad')?'hidden':'';
    window.scrollTo(0,0);
    if(push){ try{history.replaceState(null,'','#'+m);}catch(e){} try{localStorage.setItem('pepe-v8-mode',m);}catch(e){} }
    requestAnimationFrame(()=>{ const mod=window.MODES[m]; if(mod&&mod.activate) mod.activate(); });
  }
  document.querySelectorAll('.modes button').forEach(b=>b.addEventListener('click',()=>setMode(b.dataset.m)));
  window.addEventListener('hashchange',()=>setMode(location.hash.slice(1),false));
  document.addEventListener('keydown',e=>{ if(e.target.closest('input,textarea'))return; if(e.key==='1')setMode('panel'); if(e.key==='2')setMode('historia'); if(e.key==='3')setMode('ciudad'); });
  let start=location.hash.slice(1); if(!names.includes(start)){ try{start=localStorage.getItem('pepe-v8-mode')||'panel';}catch(e){start='panel';} }
  window.__setMode=setMode; window.__start=start;
})();
"""

OUT = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>PEPE Energía DataLens</title>
<meta name="description" content="Un sistema, tres modos: Panel para analizar, Historia para contar, Ciudad para sentir. Eficiencia energética de PEPE Energía, 2025.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap">
<style>
{TOKENS}
/* ===== PANEL (from v5) ===== */
{pc}
/* ===== HISTORIA (from v6) ===== */
{hc}
/* ===== CIUDAD (from v7) ===== */
{cc}
/* ===== SHELL OVERRIDES (after modules so they win) ===== */
{OVER}
</style>
</head>
<body>
{SHELL_HTML}
<section class="mode" id="m-panel">
{pb}
</section>
<section class="mode" id="m-historia">
{hb}
</section>
<section class="mode" id="m-ciudad">
{cb}
</section>
<div id="gfoot">{GFOOT}</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script>
{SHELL_JS}
</script>
<script>
/* ===== PANEL ===== */
(function(){{
{pj}
}})();
</script>
<script>
/* ===== HISTORIA ===== */
(function(){{
{hj}
}})();
</script>
<script>
/* ===== CIUDAD ===== */
(function(){{
{cj}
}})();
</script>
<script>window.__setMode(window.__start,false);</script>
</body>
</html>
"""
pathlib.Path('PEPE_Energia_DataLens_v8.html').write_text(OUT)
print('wrote v8', len(OUT.splitlines()), 'lines')
