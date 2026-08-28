import gen
T = gen.T
kit = open("kit.html").read()
app = open("app.html").read()

META = [
 ("01", "Dashboard", "Studio",
  "The model picker is open. It is the screen's only glass, the only crafted surface, and a menu-open state is the kind of screen most portfolios never draw",
  "Model picker menu · resume block · hairline recents · context ledger"),
 ("02", "List", "Conversations",
  "Recency decides weight: today's threads carry a three-line excerpt at 16.5px, yesterday's two at 15px, earlier this week is a bare title. The list decays as you scroll",
  "Search · filter chips · day groups · excerpt rows · mono provenance"),
 ("03", "Immersive detail", "Streaming answer",
  "The answer is the screen, floor to ceiling, with no container around it. The only two bounded surfaces are the user's own turn and the code block — and they read as different objects",
  "User turn · citations · numbered steps · code block · soft caret · glass stop"),
 ("04", "Input moment", "Compose + tool run",
  "The composer has actually grown, to five real lines of a real follow-up with a caret in it, and the keyboard is drawn rather than implied — in the app's warm ink, not the stock iOS grey",
  "Tool-run chips · running underline · attachment pill · glass composer · keyboard"),
 ("05", "Empty / first run", "First run",
  "One 32px sentence with nothing beside it. No illustration, no robot, no sparkle — the three starters are three questions someone would genuinely type at 9am on a Tuesday",
  "Display sentence · starter rows · privacy foot · inert composer"),
 ("06", "Profile / settings", "Model & privacy",
  "The restraint screen. Full-bleed hairline rows, never an inset grouped card, and the only red in the whole app is on one row. The picker returns here as a list rather than a menu",
  "Model list + prices · switches · destructive row · mono build footer"),
]

AUDIT = [
 ("Concentric radii", "pass",
  "Menu 20 → its rows 0 with hairline dividers; composer 20 (tall) / 24 (single-line) → attachment pill 8 → send 17; code block 12 → its header rule 0; stop pill 22; tool chip 8; keyboard key 5. Message turns take 20/20/7/20 — the 7pt tail corner is the only asymmetric radius in the app and it exists to point the turn at its author."),
 ("Rhythm, not uniform spacing", "pass",
  "02 is the clearest case: 16.5px title + three-line excerpt for today, 15px + two lines for yesterday, bare 15.5px title for earlier — row heights run 118 / 96 / 44. 03 alternates a 96pt user turn, 8pt gaps inside the citation pair, 13pt between paragraphs and 3pt between a step and its body. Gutters are 20 at the margin, 8 within a chip stack."),
 ("One accent, not purple", "pass",
  "Citrine brass #DFC069, hue 46°. It clears WealthKit's teal by 126°, FitnessPro's mint by 101°, ShopEase's oxblood by 31° and SocialFlow's pink by 61°, and it is the one band no major AI product occupies — Claude is terracotta, ChatGPT mono green, Perplexity teal, Gemini blue-violet. Never a gradient. Per screen it appears on at most: the caret, one filled send, the citation numerals, the step numerals and one checkmark. Screen 02 spends it on a single filter chip; screen 03 has no filled control at all."),
 ("Plausible specific data", "pass",
  "The transcript is one real SwiftUI performance question with a real, correct answer: filtering inside body, value identity forcing a rebuild, and .searchable firing per character. The Swift compiles. Token counts scale with turn counts (14 turns / 31.2k, 22 / 47.8k, 6 / 9.4k), tool durations are ordered read < search < build (0.2s / 1.4s / 8.4s), the composer's counter reads 124 for a 124-character draft, and 214 conversations at 41.2 MB is 197 KB each."),
 ("One bold move per screen", "pass",
  "Named per artboard above. Each is the only oversized or the only crafted element on its screen; everything else drops to 16.5px or less."),
 ("Domain vocabulary", "pass",
  "Streaming response with a soft caret and no typewriter jitter; tool-run chips with icon, name, argument and duration, where running is a progress underline rather than a spinner; source citations as a superscript numeral with a row beneath; a model picker that is a menu on 01 and a list on 06, never a segmented control; a composer that grows to five lines with the accent fill earned by being non-empty; and message turns instead of cards. No card appears anywhere in the app."),
 ("Real imagery", "pass",
  "AI screens have no photography, so rule 7's answer is real CONTENT. Real API names (Task.sleep(for:), Task.isCancelled, @Observable, id: \\.self), a real WWDC session number, real source domains, real model names and prices, real file paths and line numbers, real build diagnostics. Not one 'Hello! How can I help you today?' anywhere — that sentence is what kills an AI screenshot."),
]

LOCK = [
 ("Ground", "Light grey #F2F2F7", "Near-black #07090A", "Warm sand #F4EFE7", "Pure black #000",
  "Warm ink #131211, locked. Deliberately not black — it is visibly lifted off SocialFlow's #000 and warm where FitnessPro's near-black is cold. A printed page, inverted."),
 ("Container model", "Inset grouped cards", "No cards; rings and zone bands are the surfaces",
  "No containers; photographs sit on the ground at radius 12",
  "No containers and no radius; media is edge to edge",
  "Message turns. The user's turn is compact, right-inset 76pt, on a lifted plate with a 7pt tail corner; the assistant's is full width with no plate, no border and no radius at all. The asymmetry is the entire container model, and there is not one card in the app."),
 ("Chrome", "Floating glass pill tab bar on every screen", "Docked icon bar, absent during a workout",
  "Text-only dock, one glass buy bar", "Disappears on scroll; a floating compose pill",
  "There is no tab bar. Navigation is a plain hairline top bar. Glass appears on exactly three things across six screens — the model menu, the composer, the stop button — and never two at once."),
 ("Type personality", "SF Text, rounded reserved for money", "Oversized rounded numerals",
  "Fraunces display + .19em uppercase labels", "Inter Tight, tight and large, never uppercased",
  "IBM Plex Sans set airy — 16px body, 1.56 leading, tracking at or near zero, the opposite of SocialFlow's −.035em — against IBM Plex Mono carrying every machine-generated fact: model names, durations, token counts, paths, code. Prose is sans; the machine is mono. Mono caps are tracked .06em, a terminal header, not ShopEase's .19em editorial label."),
 ("Density signature", "One hero number, then dense tabular rows", "Extreme alternation",
  "Image-led and sparse, 20pt gutters", "Quiet and even; the photography carries the variance",
  "Long-form vertical rhythm at a 20pt margin. Reading measure is ~34 characters, paragraphs are 13pt apart, and density is set by recency and by turn ownership rather than by section."),
 ("Accent", "Deep teal #0F7B6C", "Mint #3DDC84", "Oxblood #8A3418", "Hot pink #FF2E63",
  "Citrine brass #DFC069 — one flat colour, never a gradient, and never purple, which is the AI house style this domain had to avoid hardest."),
]

boards = []
for num, arche, name, bold, widgets in META:      # keyed off num, not list position
    body = open(f"s{int(num)}.html").read()
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
    f'<tr><td>{a}</td><td class="p-was">{f}</td><td class="p-was">{g}</td>'
    f'<td class="p-was">{c}</td><td class="p-was">{so}</td><td>{ai}</td></tr>'
    for a, f, g, c, so, ai in LOCK)

page = f'''<title>NativeAIStudio Artboards</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
{kit}
{app}
<style>
/* NativeAIStudio is ink-locked, so this review page commits to the same warm ink and
   paints every colour explicitly rather than inheriting the viewer's ground.
   app.html's selectors ARE scoped under .ios in this domain (the first one that is), but
   the p- prefix is kept anyway: the kit's own .card / .row / .chip are not scoped, and an
   unprefixed rule here would still leak into the six embedded screens. */
:root{{
  --g-bg:#0E0D0C; --g-panel:#181615; --g-card:#131211;
  --g-ink:#F5F2ED; --g-ink-2:rgba(245,242,237,.62); --g-ink-3:rgba(245,242,237,.36);
  --g-rule:rgba(245,242,237,.14); --g-accent:#DFC069; --g-on:#17140F;
  --g-body:"IBM Plex Sans","Helvetica Neue",Arial,sans-serif;
  --g-mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,monospace;
}}
html{{background:var(--g-bg)}}
body{{background:var(--g-bg);color:var(--g-ink);font-family:var(--g-body);
  font-size:16px;line-height:1.6;margin:0;-webkit-font-smoothing:antialiased}}
.p-wrap{{max-width:1240px;margin:0 auto;padding:0 26px 96px;
  display:flex;flex-direction:column;gap:64px}}
.p-wrap h1,.p-wrap h2,.p-wrap h3{{font-family:var(--g-body);font-weight:600;
  letter-spacing:-.028em}}
.p-wrap table{{border-collapse:collapse}}

.p-head{{padding:60px 0 34px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,330px);
  gap:44px;align-items:end;border-bottom:1px solid var(--g-rule)}}
.p-eyebrow{{font-family:var(--g-mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--g-accent);margin:0 0 18px}}
.p-wrap h1{{font-size:clamp(50px,8.4vw,96px);letter-spacing:-.042em;line-height:.95;
  margin:0;font-weight:600;text-wrap:balance}}
.p-wrap h1 em{{font-style:normal;color:var(--g-accent)}}
.p-lede{{color:var(--g-ink-2);margin:0;font-size:16px;max-width:46ch}}

.p-spec{{display:grid;grid-template-columns:repeat(auto-fit,minmax(158px,1fr));
  gap:1px;background:var(--g-rule);border:1px solid var(--g-rule)}}
.p-spec>div{{background:var(--g-bg);padding:16px 18px}}
.p-spec dt{{font-family:var(--g-mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;
  color:var(--g-ink-3);margin:0}}
.p-spec dd{{font-family:var(--g-mono);font-size:13px;margin:8px 0 0;color:var(--g-ink);
  display:flex;align-items:center;gap:8px;font-variant-numeric:tabular-nums}}
.p-chip{{width:14px;height:14px;flex:none;background:var(--g-accent);border-radius:7px}}

.p-rail{{display:grid;grid-template-columns:repeat(auto-fit,minmax(316px,1fr));gap:52px 30px}}
.p-board{{margin:0;display:flex;flex-direction:column;gap:20px;min-width:0}}
.p-cap{{min-height:224px;border-top:2px solid var(--g-accent);padding-top:14px}}
.p-kicker{{font-family:var(--g-mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;
  color:var(--g-ink-2);margin:0 0 10px;display:flex;gap:10px;align-items:baseline}}
.p-num{{color:var(--g-accent)}}
.p-cap h3{{font-size:27px;margin:0 0 10px;line-height:1.08}}
.p-bold{{margin:0 0 10px;font-size:14.5px;line-height:1.52;color:var(--g-ink)}}
.p-widg{{margin:0;font-family:var(--g-mono);font-size:11.5px;line-height:1.65;color:var(--g-ink-3)}}
.p-dev{{width:340px;height:737px;overflow:hidden;border-radius:33px;
  outline:1px solid var(--g-rule);outline-offset:-1px;
  box-shadow:0 24px 60px rgba(0,0,0,.7)}}
.p-dev .ios{{transform:scale(.865);transform-origin:top left}}

.p-sec{{display:flex;flex-direction:column;gap:18px}}
.p-wrap h2{{font-size:31px;margin:0;line-height:1.1}}
.p-sub{{margin:0;color:var(--g-ink-2);font-size:15.5px;max-width:72ch}}
.p-tablewrap{{overflow-x:auto;border:1px solid var(--g-rule);background:var(--g-card)}}
.p-tablewrap table{{width:100%;min-width:1080px}}
.p-tablewrap th,.p-tablewrap td{{text-align:left;padding:14px 18px;
  border-bottom:1px solid var(--g-rule);font-size:14px;vertical-align:top;line-height:1.52}}
.p-tablewrap tr:last-child td{{border-bottom:0}}
.p-tablewrap th{{font-family:var(--g-mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;
  color:var(--g-ink-3);font-weight:400;background:var(--g-panel)}}
.p-tablewrap td:first-child{{font-size:15px;font-weight:600;letter-spacing:-.02em;color:var(--g-ink)}}
.p-tablewrap td:last-child{{color:var(--g-ink)}}
.p-was{{color:var(--g-ink-3)}}
.p-v{{font-family:var(--g-mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;
  padding:4px 9px;display:inline-block}}
.p-v--pass{{color:var(--g-on);background:var(--g-accent)}}
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
      <p class="p-eyebrow">Session 6 · AI · review gate · rev 1 · closes the set</p>
      <h1>NativeAI<em>Studio</em></h1>
    </div>
    <p class="p-lede">Six iOS 26 artboards, no two sharing a layout skeleton.
      Every screen is live HTML at 393 × 852 — type stays sharp at any zoom.</p>
  </header>

  <dl class="p-spec">
    <div><dt>Accent</dt><dd><span class="p-chip"></span>#DFC069</dd></div>
    <div><dt>Ground</dt><dd>#131211 · locked</dd></div>
    <div><dt>Canvas</dt><dd>393 × 852 @3×</dd></div>
    <div><dt>Radii</dt><dd>24 · 20 · 12 · 8 · 7 · 5</dd></div>
    <div><dt>Glass</dt><dd>3 elements, 1 per screen</dd></div>
    <div><dt>Type</dt><dd>Plex Sans + Plex Mono</dd></div>
  </dl>

  <div class="p-rail">
{"".join(boards)}
  </div>

  <section class="p-sec">
    <h2>How it diverges from the four apps already built</h2>
    <p class="p-sub">The S2 gate approved the process, not the visuals — each app has to read as a
      different product rather than a recolour. Four domains are spent, so this one has to hold
      against all four at once, on every axis, not just on hue.</p>
    <div class="p-tablewrap"><table>
      <thead><tr><th>Axis</th><th>Fintech</th><th>Fitness</th><th>Commerce</th><th>Social</th><th>AI · this session</th></tr></thead>
      <tbody>{lock_rows}</tbody>
    </table></div>
    <p class="p-note">Also avoided, as the earlier domains have spent them:
      <b>inset grouped card lists</b>, a <b>floating glass pill tab bar</b>,
      <b>letter-monogram tiles</b>, the <b>sparkline + allocation-donut pair</b>,
      a <b>tabular hero number</b> as the opening move, an <b>icon dock</b>,
      <b>.19em uppercase editorial labels</b>, and <b>edge-to-edge photography</b>.<br>
      AI clichés avoided: <b>purple or blue gradients</b> anywhere, a <b>sparkle glyph</b>
      on any button — there is deliberately no sparkle in the icon sheet — a <b>robot avatar</b>,
      <b>“AI is thinking…” with three bouncing dots</b>, a <b>chat bubble around the assistant's
      text</b> (bubbles belong to the user turn only), and <b>“Hello! How can I help you today?”</b>.</p>
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
    <h2>Rule 7 without photography</h2>
    <p class="p-sub">Every earlier domain answered “real imagery” with real licence-verified
      photographs. An AI product has none — so the thing that has to be real is the content, and
      it is the single highest-risk item in the whole session. A mockup chat that says
      “Hello! How can I help you today?” is dead on the slide.</p>
    <p class="p-note">The transcript is one real question — <b>a SwiftUI List dropping to 38 fps
      while filtering 4,200 rows</b> — with a real, correct, three-part answer: the filter running
      inside <b>body</b>, <b>id: \\.self</b> forcing a teardown instead of a move, and
      <b>.searchable</b> firing on every character. The Swift in the code block compiles.<br>
      The citations point at a real WWDC session and a real forum; the tool chips name real tools
      with ordered durations; the diagnostics name a real deprecation. The model names, context
      windows and per-million prices are the ones a 2026 build would actually show.<br>
      This is also why the icon sheet has no sparkle: four extra symbols were drawn for this
      domain — <b>doc</b>, <b>terminal</b>, <b>sessions</b>, <b>model</b> — and a sparkle was
      deliberately not one of them.</p>
  </section>

  <p class="p-note">Source artboards → <b>PortfolioProjectWebApp/design-canvas/ai/</b><br>
    PNG exports @3× (1179 × 2556) → <b>assets/app-screenshots/nativeaistudio/v1/</b><br>
    One ground only: warm ink is the AI identity lock, so there is no light set to review.<br>
    Gate question: does this read as a fifth product — and does the set of five read as one
    designer with five briefs, rather than one template in five colours?</p>
</div>
'''
open("canvas.html", "w").write(page)
print(len(page) // 1024, "KB")
