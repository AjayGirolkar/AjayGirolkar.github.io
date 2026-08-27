import gen
T = gen.T
kit = open("kit.html").read()
app = open("app.html").read()

META = [
 ("01", "Data-dense dashboard", "Today",
  "A single 236pt Move ring owns the upper half; the two lesser goals are deliberately rendered at a fraction of its weight",
  "Progress ring · HR zone band · streak strip · stat strip"),
 ("02", "Rich scrolling feed", "History",
  "Every row carries its own heart-rate trace, bled full-width into a lane beneath the text",
  "Vertical zone bar · HR trace row · week totals"),
 ("03", "Immersive detail", "Active workout",
  "42:07 set at 104pt with every piece of chrome removed — no nav bar, no tab bar, for the duration of the run",
  "Live HR trace · edge-to-edge zone band · pace ladder · one glass control"),
 ("07", "Workout detail", "Lower B",
  "Every row runs a live two-frame demo of its own movement — the list itself is the bold move",
  "Exercise rows · looping demos · set dots · resume bar"),
 ("04", "Input moment", "Set logger",
  "The value being edited is the screen: 88pt, sitting directly on the ruler that changes it",
  "Weight ruler · rep stepper · set/rep grid · rest bar"),
 ("05", "Celebration", "Streak closed",
  "The app inverts — mint floods the ground, ink goes black, and 18 runs at 224pt",
  "Closed-ring mark · outlined stat pills · milestone bar · PR line"),
 ("06", "Profile / settings", "You",
  "26 weeks of training rendered as one consistency matrix, with the current streak marked in place",
  "Consistency matrix · PR list · hairline preference rows"),
]

AUDIT = [
 ("Concentric radii", "pass",
  "Demo tile 14 → ruler control 12 → small demo tile 10 → chip/zone band 8 → dot 3, against a screen radius of 0. No radius is reused across two levels, and nothing in the set is a card."),
 ("Rhythm, not uniform spacing", "pass",
  "Extreme alternation by design: a 224pt numeral against 22pt ladder rows on 03, an 88pt weight against 40pt grid rows on 04. 4/8 within groups, 26/32 between."),
 ("One accent, not purple", "pass",
  "#3DDC84 only. The five-step zone ramp is deliberately held at lower chroma than the accent, so the data colours never compete with the brand colour; it appears solely inside zone bands and the row zone bar."),
 ("Plausible specific data", "pass",
  "Romanian deadlift 60/67.5/72.5 kg on a real progression; 7.42 km in 42:07 = the 5:40 avg shown, and the six splits sum back to that elapsed time."),
 ("One bold move per screen", "pass",
  "Named per artboard above. Each is the only oversized element on its screen."),
 ("Domain vocabulary", "pass",
  "Progress ring, HR zone band, set/rep grid, weight ruler, rest bar, streak strip, pace ladder, consistency matrix, looping movement demo. No generic card appears anywhere in the set."),
 ("Real imagery", "pass",
  "Every exercise carries a two-frame demo of its own movement, duotoned onto the accent ramp so it reads as a designed asset rather than the full-bleed stock gym photography that is this domain's first cliché. No grey placeholders anywhere."),
]

LOCK = [
 ("Ground", "Light grey #F2F2F7", "Near-black #07090A, dark-locked — the app ships one ground"),
 ("Container model", "Inset grouped cards", "No cards. Rings, zone bands and hairline rows are the surfaces"),
 ("Chrome", "Floating glass pill tab bar on every screen", "Docked bar with a hairline; gone entirely during a workout. One glass layer in the whole set"),
 ("Type personality", "SF Text, rounded reserved for money", "Rounded numerals at 88–224pt are the voice; SF Text is the support"),
 ("Density signature", "One hero number, then dense tabular rows", "Extreme alternation — a giant metric hard against a dense grid"),
 ("Accent", "Deep teal #0F7B6C", "Mint #3DDC84, on a desaturated zone ramp"),
]

boards = []
for num, arche, name, bold, widgets in META:      # keyed off num, not position,
    body = open(f"s{int(num)}.html").read()        # so META can be reordered safely
    for k, v in T.items():
        body = body.replace("{{" + k + "}}", v)
    boards.append(f'''<figure class="p-board">
  <figcaption class="p-cap">
    <p class="p-kicker"><span class="p-num">{num}</span>{arche}</p>
    <h3>{name}</h3>
    <p class="p-bold">{bold}</p>
    <p class="p-widg">{widgets}</p>
  </figcaption>
  <div class="p-dev">{body}</div>
</figure>''')

audit_rows = "".join(
    f'<tr><td>{n}</td><td><span class="p-v p-v--{v}">{v}</span></td><td>{d}</td></tr>'
    for n, v, d in AUDIT)
lock_rows = "".join(
    f'<tr><td>{a}</td><td class="p-was">{f}</td><td>{t}</td></tr>'
    for a, f, t in LOCK)

page = f'''<title>FitnessPro Artboards</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;600&family=Roboto+Mono:wght@400;500&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&display=swap">
{kit}
{app}
<style>
/* The product is dark-locked by design, so this review page commits to the same
   single visual world rather than inverting under the viewer's theme. Every
   colour below is painted explicitly so the page holds on either host ground. */
:root{{
  --g-bg:#0A0C0D; --g-panel:#121618; --g-panel-2:#171C1E;
  --g-ink:#EDF2E8; --g-ink-2:#8E9A89; --g-ink-3:#5D665B;
  --g-rule:rgba(237,242,232,.13); --g-accent:#3DDC84;
  --g-ok:#3DDC84; --g-na:#7E8A7A;
  --g-disp:"Oswald","Haettenschweiler","Arial Narrow",sans-serif;
  --g-body:"Source Sans 3","Helvetica Neue",Arial,sans-serif;
  --g-mono:"Roboto Mono",ui-monospace,SFMono-Regular,monospace;
}}
html{{background:var(--g-bg)}}
body{{background:var(--g-bg);color:var(--g-ink);font-family:var(--g-body);
  font-size:16.5px;line-height:1.6;margin:0;-webkit-font-smoothing:antialiased}}
.p-wrap{{max-width:1180px;margin:0 auto;padding:0 26px 96px;
  display:flex;flex-direction:column;gap:64px}}

/* ---- masthead ---- */
.p-head{{padding:60px 0 0;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,320px);
  gap:44px;align-items:end;border-bottom:1px solid var(--g-rule);padding-bottom:34px}}
.p-eyebrow{{font-family:var(--g-mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--g-accent);margin:0 0 16px}}
.p-wrap h1{{font-family:var(--g-disp);font-weight:600;font-size:clamp(52px,9vw,104px);
  letter-spacing:.005em;line-height:.92;margin:0;text-transform:uppercase;text-wrap:balance}}
.p-wrap h1 em{{font-style:normal;color:var(--g-accent)}}
.p-lede{{color:var(--g-ink-2);margin:0;font-size:16px;max-width:46ch}}

/* ---- spec strip ---- */
.p-spec{{display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));
  gap:1px;background:var(--g-rule);border:1px solid var(--g-rule)}}
.p-spec>div{{background:var(--g-bg);padding:16px 18px}}
.p-spec dt{{font-family:var(--g-mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--g-ink-3);margin:0}}
.p-spec dd{{font-family:var(--g-mono);font-size:13.5px;margin:8px 0 0;color:var(--g-ink);
  display:flex;align-items:center;gap:8px;font-variant-numeric:tabular-nums}}
.p-chip{{width:14px;height:14px;flex:none;background:var(--g-accent)}}

/* ---- artboards ---- */
.p-rail{{display:grid;grid-template-columns:repeat(auto-fit,minmax(316px,1fr));gap:52px 30px}}
.p-board{{margin:0;display:flex;flex-direction:column;gap:20px;min-width:0}}
.p-cap{{min-height:190px;border-top:2px solid var(--g-accent);padding-top:14px}}
.p-kicker{{font-family:var(--g-mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--g-ink-2);margin:0 0 10px;display:flex;gap:10px;align-items:baseline}}
.p-num{{color:var(--g-accent)}}
.p-cap h3{{font-family:var(--g-disp);font-weight:600;font-size:27px;letter-spacing:.01em;
  text-transform:uppercase;margin:0 0 10px;line-height:1.05}}
.p-bold{{margin:0 0 10px;font-size:14.5px;line-height:1.5;color:var(--g-ink)}}
.p-widg{{margin:0;font-family:var(--g-mono);font-size:11.5px;line-height:1.65;color:var(--g-ink-3)}}
.p-dev{{width:340px;height:737px;overflow:hidden;border-radius:33px;
  outline:1px solid var(--g-rule);outline-offset:-1px;
  box-shadow:0 24px 60px rgba(0,0,0,.55)}}
.p-dev .ios{{transform:scale(.865);transform-origin:top left}}

/* ---- sections & tables ---- */
.p-sec{{display:flex;flex-direction:column;gap:18px}}
.p-wrap h2{{font-family:var(--g-disp);font-weight:600;font-size:30px;letter-spacing:.01em;
  text-transform:uppercase;margin:0;line-height:1}}
.p-sub{{margin:0;color:var(--g-ink-2);font-size:15.5px;max-width:66ch}}
.p-tablewrap{{overflow-x:auto;border:1px solid var(--g-rule)}}
.p-tablewrap table{{border-collapse:collapse;width:100%;min-width:660px}}
.p-tablewrap th,.p-tablewrap td{{text-align:left;padding:14px 18px;
  border-bottom:1px solid var(--g-rule);font-size:14.5px;vertical-align:top;line-height:1.5}}
.p-tablewrap tr:last-child td{{border-bottom:0}}
.p-tablewrap th{{font-family:var(--g-mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--g-ink-3);font-weight:400;background:var(--g-panel)}}
.p-tablewrap td:first-child{{font-family:var(--g-disp);font-weight:400;font-size:16px;
  text-transform:uppercase;letter-spacing:.02em;white-space:nowrap;color:var(--g-ink)}}
.p-tablewrap td:last-child{{color:var(--g-ink-2)}}
.p-was{{color:var(--g-ink-3);font-style:italic}}
.p-v{{font-family:var(--g-mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;
  padding:4px 9px;display:inline-block}}
.p-v--pass{{color:#0A0C0D;background:var(--g-ok)}}
.p-v--na{{color:var(--g-na);border:1px solid var(--g-na)}}
.p-note{{font-family:var(--g-mono);font-size:12.5px;color:var(--g-ink-2);line-height:1.9;
  border-left:2px solid var(--g-accent);padding:2px 0 2px 18px;margin:0}}
.p-note b{{color:var(--g-ink);font-weight:500}}
@media (max-width:680px){{
  .p-head{{grid-template-columns:1fr;gap:24px}}
  .p-wrap{{padding:0 18px 64px;gap:48px}}
}}
</style>

<div class="p-wrap">
  <header class="p-head">
    <div>
      <p class="p-eyebrow">Session 3 · Health &amp; fitness · review gate · rev 3</p>
      <h1>Fitness<em>Pro</em></h1>
    </div>
    <p class="p-lede">Seven iOS 26 artboards, no two sharing a layout skeleton.
      Every screen is live HTML at 393 × 852 — type stays sharp at any zoom.</p>
  </header>

  <dl class="p-spec">
    <div><dt>Accent</dt><dd><span class="p-chip"></span>#3DDC84</dd></div>
    <div><dt>Ground</dt><dd>#07090A · locked</dd></div>
    <div><dt>Canvas</dt><dd>393 × 852 @3×</dd></div>
    <div><dt>Radii</dt><dd>14 · 12 · 10 · 8 · 3</dd></div>
    <div><dt>Glass</dt><dd>1 element, 1 screen</dd></div>
    <div><dt>Demos</dt><dd>12 frames, duotoned</dd></div>
  </dl>

  <div class="p-rail">
{"".join(boards)}
  </div>

  <section class="p-sec">
    <h2>How it diverges from WealthKit</h2>
    <p class="p-sub">The S2 gate approved the process, not the visuals — each app has to read as a
      different product rather than a recolour. These are the axes the identity lock forces apart.</p>
    <div class="p-tablewrap"><table>
      <thead><tr><th>Axis</th><th>Fintech · spent</th><th>Fitness · this session</th></tr></thead>
      <tbody>{lock_rows}</tbody>
    </table></div>
    <p class="p-note">Also avoided, as fintech has spent them: <b>inset grouped card lists</b>,
      a <b>floating glass pill tab bar</b>, <b>letter-monogram tiles standing in for logos</b>,
      the <b>sparkline + allocation-donut pair</b>, a <b>tabular hero number</b> as the opening move,
      and <b>confetti</b> on the celebration screen.</p>
  </section>

  <section class="p-sec">
    <h2>Self-audit · the seven rules</h2>
    <p class="p-sub">Scored before publishing, per the skill's workflow.</p>
    <div class="p-tablewrap"><table>
      <thead><tr><th>Rule</th><th>Verdict</th><th>Evidence</th></tr></thead>
      <tbody>{audit_rows}</tbody>
    </table></div>
  </section>

  <section class="p-sec">
    <h2>Where the demos come from</h2>
    <p class="p-sub">Each exercise ships exactly two frames — the start and the end of the rep — so
      crossfading them reads as the movement without shipping a GIF. The loop is paused for anyone
      with Reduce Motion on, which is why the stills above are frozen on frame one.</p>
    <p class="p-note">Source: <b>yuhonas/free-exercise-db</b> — 873 exercises, released under
      <b>The Unlicense</b> (public domain).<br>
      Treatment: cropped per exercise, desaturated, mapped onto a four-stop ramp derived from the accent and vignetted,
      so the original red-walled gym photography folds into the palette instead of fighting it.<br>
      Nothing here is traced from, or derived from, another designer's work.</p>
  </section>

  <p class="p-note">Source artboards → <b>PortfolioProjectWebApp/design-canvas/fitness/</b><br>
    PNG exports @3× (1179 × 2556) → <b>assets/app-screenshots/fitnesspro/v1/</b><br>
    One ground only: FitnessPro ships dark, so there is no light set to review.<br>
    Gate question: does this read as a different product from WealthKit, or as a recolour?</p>
</div>
'''
open("canvas.html", "w").write(page)
print(len(page), "bytes")
