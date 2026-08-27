import re, subprocess, sys, os
sys.argv=["gen.py"]  # reuse gen's substitution table
src=open("gen.py").read().split('for f in sys.argv[1:]:')[0]
ns={}; exec(src, ns); T=ns["T"]

kit=open("kit.html").read()   # already scoped to .ios by the patched primitives kit
app=open("app.html").read()

META=[
 ("01","Data-dense dashboard","Oversized portfolio figure over an edge-to-edge intraday sparkline",
  "Hero figure · sparkline · allocation donut · ledger rows"),
 ("02","Rich scrolling feed","14-week spend histogram with only the current month in accent",
  "Category-coloured merchant tiles · day totals · tabular amounts"),
 ("03","Immersive detail","Full-bleed ink hero — the 1Y chart owns the top 40% of the screen",
  "Ink hero · 1Y area chart · stat grid · position P&L"),
 ("04","Input moment","₹45,000 set at 46px with a live caret; keypad fills the sheet",
  "Order sheet (38pt) · quick-amount chips · custom keypad"),
 ("05","Celebration state","A single 236pt ring closing at 100% with a check at 12 o'clock",
  "Goal ring · confetti · contribution split · next-goal nudge"),
 ("06","Profile / settings","Deliberately quiet — only the identity block carries weight",
  "Inset grouped lists · native toggles · KYC status chip"),
]
AUDIT=[
 ("Concentric radii","pass","sheet 38 → card 20 → control 12 → chip 8; no radius reused across levels"),
 ("Rhythm, not uniform spacing","pass","4/8 inside rows, 18–24 between sections; density visibly varies per screen"),
 ("One accent, not purple","pass","#0F7B6C throughout (#2FBFA8 in dark). Green/red confined to numbers and deltas"),
 ("Plausible specific data","pass","RELIANCE at ₹2,979.90, HDFC Bank 18 shares, Swiggy 1:12 PM; day totals sum correctly"),
 ("One bold move per screen","pass","Listed per artboard above; everything else held quiet"),
 ("Domain vocabulary","pass","Sparkline, allocation donut, ledger row, delta pill, order pad — no generic cards"),
 ("Real imagery","n/a","Fintech carries no photography; brand monograms stand in for logos, no grey placeholders"),
]

screens=[]
for i,(num,arche,bold,widgets) in enumerate(META,1):
    body=open(f"s{i}.html").read()
    for k,v in T.items(): body=body.replace("{{"+k+"}}",v)
    screens.append(f'''<figure class="p-board">
  <figcaption class="p-cap">
    <span class="p-num">{num}</span>
    <h3>{arche}</h3>
    <p class="p-bold"><span class="p-lbl">Bold move</span>{bold}</p>
    <p class="p-widg"><span class="p-lbl">Widgets</span>{widgets}</p>
  </figcaption>
  <div class="p-dev">{body}</div>
</figure>''')

rows="".join(
 f'<tr><td>{n}</td><td><span class="p-v p-v--{v}">{v}</span></td><td>{d}</td></tr>'
 for n,v,d in AUDIT)

page=f'''<title>WealthKit Fintech Canvas</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700&family=IBM+Plex+Mono:wght@400;500&family=Literata:opsz,wght@7..72,400;7..72,500&display=swap">
{kit}
{app}
<style>
:root{{
  --p-bg:#E9EAEC; --p-surface:#FFFFFF; --p-ink:#141A19; --p-ink-2:#5D6866;
  --p-line:rgba(20,26,25,.12); --p-accent:#0F7B6C; --p-accent-soft:rgba(15,123,108,.10);
  --p-ok:#1C8C4B; --p-na:#7C8481;
  --p-disp:"Archivo","Helvetica Neue",sans-serif;
  --p-body:"Literata",Georgia,serif;
  --p-mono:"IBM Plex Mono",ui-monospace,monospace;
}}
@media (prefers-color-scheme:dark){{
  :root:not([data-theme="light"]){{
    --p-bg:#0D1211; --p-surface:#161D1B; --p-ink:#EDF1F0; --p-ink-2:#96A29F;
    --p-line:rgba(237,241,240,.14); --p-accent:#2FBFA8; --p-accent-soft:rgba(47,191,168,.14);
    --p-ok:#30D158; --p-na:#8A9golf;
  }}
}}
:root[data-theme="dark"]{{
  --p-bg:#0D1211; --p-surface:#161D1B; --p-ink:#EDF1F0; --p-ink-2:#96A29F;
  --p-line:rgba(237,241,240,.14); --p-accent:#2FBFA8; --p-accent-soft:rgba(47,191,168,.14);
  --p-ok:#30D158; --p-na:#8A9491;
}}
body{{background:var(--p-bg);color:var(--p-ink);font-family:var(--p-body);
  font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased;margin:0}}
.p-wrap{{max-width:1180px;margin:0 auto;padding:56px 28px 80px;
  display:flex;flex-direction:column;gap:44px}}
.p-eyebrow{{font-family:var(--p-mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--p-accent);margin:0 0 10px}}
h1{{font-family:var(--p-disp);font-weight:700;font-size:clamp(38px,6vw,60px);
  letter-spacing:-.035em;line-height:1;margin:0;text-wrap:balance}}
.p-sub{{color:var(--p-ink-2);max-width:62ch;margin:14px 0 0;font-size:17px}}
.p-tokens{{display:flex;flex-wrap:wrap;gap:0;border:1px solid var(--p-line);
  border-radius:14px;overflow:hidden;background:var(--p-surface)}}
.p-tok{{flex:1 1 172px;padding:15px 18px;border-right:1px solid var(--p-line)}}
.p-tok:last-child{{border-right:0}}
.p-tok dt{{font-family:var(--p-mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--p-ink-2)}}
.p-tok dd{{font-family:var(--p-mono);font-size:14px;margin:6px 0 0;
  display:flex;align-items:center;gap:8px;font-variant-numeric:tabular-nums}}
.p-swatch{{width:15px;height:15px;border-radius:5px;background:#0F7B6C;
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.16);flex:none}}
.p-rail{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));
  gap:40px 34px;padding:4px 0 8px}}
.p-board{{margin:0;display:flex;flex-direction:column;gap:16px;min-width:0}}
.p-cap{{min-height:132px}}
.p-num{{font-family:var(--p-mono);font-size:11px;letter-spacing:.1em;color:var(--p-accent);
  display:block;margin-bottom:7px}}
.p-cap h3{{font-family:var(--p-disp);font-weight:700;font-size:21px;letter-spacing:-.02em;
  margin:0 0 9px;text-wrap:balance}}
.p-cap p{{margin:0 0 7px;font-size:13.5px;line-height:1.5;color:var(--p-ink-2)}}
.p-lbl{{font-family:var(--p-mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--p-ink);display:block;margin-bottom:2px}}
.p-dev{{width:340px;height:737px;border-radius:33px;overflow:hidden;
  box-shadow:0 1px 2px rgba(0,0,0,.10),0 18px 44px rgba(0,0,0,.16);
  outline:1px solid var(--p-line);outline-offset:-1px}}
.p-dev .ios{{transform:scale(.865);transform-origin:top left}}
h2{{font-family:var(--p-disp);font-weight:700;font-size:26px;letter-spacing:-.025em;margin:0 0 6px}}
.p-tablewrap{{overflow-x:auto;border:1px solid var(--p-line);border-radius:14px;background:var(--p-surface)}}
table{{border-collapse:collapse;width:100%;min-width:620px}}
th,td{{text-align:left;padding:12px 18px;border-bottom:1px solid var(--p-line);font-size:14.5px;vertical-align:top}}
tr:last-child td{{border-bottom:0}}
th{{font-family:var(--p-mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--p-ink-2);font-weight:500}}
td:first-child{{font-family:var(--p-disp);font-weight:500;white-space:nowrap}}
td:last-child{{color:var(--p-ink-2)}}
.p-v{{font-family:var(--p-mono);font-size:11px;letter-spacing:.09em;text-transform:uppercase;
  padding:3px 8px;border-radius:6px}}
.p-v--pass{{color:var(--p-ok);background:color-mix(in srgb,var(--p-ok) 13%,transparent)}}
.p-v--na{{color:var(--p-na);background:color-mix(in srgb,var(--p-na) 15%,transparent)}}
.p-note{{font-family:var(--p-mono);font-size:12.5px;color:var(--p-ink-2);line-height:1.7;
  border-left:2px solid var(--p-accent);padding-left:16px}}
.p-themebar{{display:flex;align-items:center;gap:10px;margin-top:22px}}
.p-themebar span{{font-family:var(--p-mono);font-size:10.5px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--p-ink-2)}}
.p-seg{{display:flex;gap:2px;background:var(--p-surface);border:1px solid var(--p-line);
  border-radius:9px;padding:2px}}
.p-seg button{{font-family:var(--p-mono);font-size:12px;color:var(--p-ink-2);
  background:none;border:0;border-radius:7px;padding:5px 13px;cursor:pointer}}
.p-seg button[aria-pressed="true"]{{background:var(--p-accent-soft);color:var(--p-accent)}}
.p-seg button:focus-visible{{outline:2px solid var(--p-accent);outline-offset:1px}}
@media (max-width:640px){{.p-wrap{{padding:36px 18px 60px}}}}
</style>

<div class="p-wrap">
  <header>
    <p class="p-eyebrow">Session 2 · Fintech · review gate</p>
    <h1>WealthKit</h1>
    <p class="p-sub">Six iOS 26 artboards, one per archetype in the portfolio grid — no two share a
      layout skeleton.
      Screens are live HTML at 393 × 852, so text stays sharp at any zoom and both themes
      are painted from tokens — switch below and the six screens follow.</p>
    <div class="p-themebar">
      <span>Theme</span>
      <div class="p-seg" role="group" aria-label="Theme">
        <button type="button" data-t="auto" aria-pressed="true">Auto</button>
        <button type="button" data-t="light" aria-pressed="false">Light</button>
        <button type="button" data-t="dark" aria-pressed="false">Dark</button>
      </div>
    </div>
  </header>

  <dl class="p-tokens">
    <div class="p-tok"><dt>Accent</dt><dd><span class="p-swatch"></span>#0F7B6C</dd></div>
    <div class="p-tok"><dt>Dark accent</dt><dd><span class="p-swatch" style="background:#2FBFA8"></span>#2FBFA8</dd></div>
    <div class="p-tok"><dt>Canvas</dt><dd>393 × 852 @3×</dd></div>
    <div class="p-tok"><dt>Radii</dt><dd>38 · 20 · 12 · 8</dd></div>
    <div class="p-tok"><dt>Glass</dt><dd>chrome only, 1 layer</dd></div>
    <div class="p-tok"><dt>Icons</dt><dd>43 inline SVG</dd></div>
  </dl>

  <div class="p-rail">
{"".join(screens)}
  </div>

  <section>
    <h2>Self-audit — the seven anti-generic rules</h2>
    <p class="p-sub" style="margin:0 0 18px">Scored before publishing, per the skill's workflow.</p>
    <div class="p-tablewrap"><table>
      <thead><tr><th>Rule</th><th>Verdict</th><th>Evidence</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
  </section>

  <p class="p-note">PNG exports @3× (1179 × 2556) →
    PortfolioProjectWebApp/assets/app-screenshots/wealthkit/v2/ (light) and /dark/<br>
    Source artboards → PortfolioProjectWebApp/design-canvas/fintech/<br>
    Gate question: does this read as a real product, or as a template?</p>
</div>

<script>
(function(){{
  var root=document.documentElement, seg=document.querySelector(".p-seg");
  function apply(t){{
    if(t==="auto") root.removeAttribute("data-theme"); else root.dataset.theme=t;
    seg.querySelectorAll("button").forEach(function(b){{
      b.setAttribute("aria-pressed", String(b.dataset.t===t));
    }});
    try{{ localStorage.setItem("wk-theme", t); }}catch(e){{}}
  }}
  var saved="auto";
  try{{ saved=localStorage.getItem("wk-theme")||"auto"; }}catch(e){{}}
  apply(saved);
  seg.addEventListener("click", function(e){{
    var b=e.target.closest("button"); if(b) apply(b.dataset.t);
  }});
}})();
</script>
'''
page=page.replace("#8A9golf","#8A9491")
open("canvas.html","w").write(page)
print(len(page),"bytes")
