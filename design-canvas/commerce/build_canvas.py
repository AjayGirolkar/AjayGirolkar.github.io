import gen, json
T = gen.T
kit = open("kit.html").read()
app = open("app.html").read()
OBJ = json.load(open("obj/meta.json"))

META = [
 ("01", "Editorial home", "Shop",
  "One object at 404pt with the headline set on the plate itself — the photograph is the layout, not an illustration of it",
  "Full-bleed plate · editorial headline · three-up new arrivals"),
 ("02", "Product grid", "Ceramics",
  "The 2-up grid breaks for a full-width banner: the rhythm resets mid-scroll instead of running uniform to the fold",
  "Product grid · category rail · sort/filter band · strikethrough + discount chip"),
 ("03", "Immersive detail", "Product page",
  "The photograph starts at the top of the glass and every piece of chrome collapses to two floating glyphs",
  "Full-bleed hero · glaze swatch row · size run with sold-out · sticky glass buy bar"),
 ("04", "Input moment", "Checkout",
  "The number you are actually deciding on is set at 42pt in the display face, against 13.5pt ledger rows",
  "Bag rows · steppers · address & payment rows · totals ledger"),
 ("05", "Empty state", "Empty bag",
  "An empty vessel is the illustration — no line-art cart, no shrugging mascot",
  "Object-as-illustration · single CTA · recently-viewed strip"),
 ("06", "Profile / orders", "Account",
  "Order rows carry the object's own photograph, so the history reads as a shelf rather than a table",
  "Order rows with status dot · hairline preference rows"),
]

AUDIT = [
 ("Concentric radii", "pass",
  "Screen 0 → product plate 12 → thumbnail 9 → size pill 12 → chip 8 → buy bar 19 with a 15 CTA nested inside it (r_child = R − p). No radius is reused across two levels."),
 ("Rhythm, not uniform spacing", "pass",
  "A 404pt plate on 01 against an 11pt-gutter three-up directly beneath it; on 04 a 42pt total against 7pt ledger rows. Gutters are 20 between groups, 4–9 within."),
 ("One accent, not purple", "pass",
  "Oxblood #8A3418, and deliberately narrow: full prices are ink, and the accent is reserved for a markdown, the cart badge, the delivery status dot and Sign out. The photography carries the colour, which is what the commerce lock asks for."),
 ("Plausible specific data", "pass",
  "₹50,000 subtotal = 31,500 + 18,500 exactly; +₹450 packing = the ₹50,450 total shown. −16% is the true reduction from ₹22,000 to ₹18,500. Order ids, dates and the two-studio ship estimate stay consistent across 04 and 06."),
 ("One bold move per screen", "pass",
  "Named per artboard above. Each is the only oversized element on its screen."),
 ("Domain vocabulary", "pass",
  "Product grid, glaze swatch row, size run with the sold-out size struck rather than hidden, strikethrough price with a discount chip, sticky glass buy bar, cart badge. No generic card appears anywhere in the set."),
 ("Real imagery", "pass",
  "Eighteen real object photographs, knocked off their studio sweeps and recomposited on the app's own sand. Rule 7 is not optional in this domain and no grey placeholder appears in the set."),
]

LOCK = [
 ("Ground", "Light grey #F2F2F7", "Near-black #07090A, locked",
  "Warm sand #F4EFE7, locked — paper is the identity, so there is no dark set"),
 ("Container model", "Inset grouped cards", "No cards; rings and zone bands are the surfaces",
  "No containers at all. Photographs sit directly on the ground at radius 12 with no border"),
 ("Chrome", "Floating glass pill tab bar on every screen", "Docked icon bar, absent during a workout",
  "Text-only dock — uppercase labels, no icons, no glass. One glass element in the whole app: the buy bar on 03"),
 ("Type personality", "SF Text, rounded reserved for money", "Oversized rounded numerals are the voice",
  "Fraunces display against 10pt uppercase labels tracked to .19em. Rounded is never used"),
 ("Density signature", "One hero number, then dense tabular rows", "Extreme alternation, giant metric against a dense grid",
  "Image-led and deliberately sparse: 20pt gutters, one dense band per screen as the counterweight"),
 ("Accent", "Deep teal #0F7B6C", "Mint #3DDC84",
  "Oxblood #8A3418 — 60° from the fitness mint, 150° from the fintech teal, and used on far less"),
]

boards = []
for num, arche, name, bold, widgets in META:      # keyed off num, not position
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
    f'<tr><td>{a}</td><td class="p-was">{f}</td><td class="p-was">{g}</td><td>{c}</td></tr>'
    for a, f, g, c in LOCK)

# provenance, straight out of the fetch manifest rather than retyped
prov = "".join(
    f'<tr><td>{m["title"]}</td><td class="p-was">{m["culture"] or "—"}</td>'
    f'<td class="p-was">{m["date"] or "—"}</td><td>{m["license"]}</td></tr>'
    for m in sorted(OBJ.values(), key=lambda m: m["title"]))

page = f'''<title>ShopEase Artboards</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap">
{kit}
{app}
<style>
/* ShopEase is light-locked, so this review page commits to one paper world too and
   paints every colour explicitly rather than inheriting the viewer's ground.
   NOTE: app.html's class names are NOT scoped to .ios, so everything here is p- and
   every bare element selector is scoped under .p-wrap. Unprefixed .grid / .rule /
   .price / .btn would leak straight into the embedded screens. */
:root{{
  --g-bg:#E6DED2; --g-panel:#F2ECE2; --g-card:#FBF8F3;
  --g-ink:#221D16; --g-ink-2:rgba(34,29,22,.62); --g-ink-3:rgba(34,29,22,.40);
  --g-rule:rgba(34,29,22,.16); --g-accent:#8A3418;
  --g-disp:"Fraunces","Iowan Old Style",Palatino,Georgia,serif;
  --g-body:"Inter","Helvetica Neue",Arial,sans-serif;
  --g-mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,monospace;
}}
html{{background:var(--g-bg)}}
body{{background:var(--g-bg);color:var(--g-ink);font-family:var(--g-body);
  font-size:16px;line-height:1.6;margin:0;-webkit-font-smoothing:antialiased}}
.p-wrap{{max-width:1240px;margin:0 auto;padding:0 26px 96px;
  display:flex;flex-direction:column;gap:64px}}
.p-wrap h1,.p-wrap h2,.p-wrap h3{{font-family:var(--g-disp);font-weight:400}}
.p-wrap table{{border-collapse:collapse}}

.p-head{{padding:60px 0 34px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,330px);
  gap:44px;align-items:end;border-bottom:1px solid var(--g-rule)}}
.p-eyebrow{{font-family:var(--g-mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--g-accent);margin:0 0 18px}}
.p-wrap h1{{font-size:clamp(52px,9vw,102px);letter-spacing:-.02em;line-height:.94;
  margin:0;text-wrap:balance}}
.p-wrap h1 em{{font-style:normal;color:var(--g-accent)}}
.p-lede{{color:var(--g-ink-2);margin:0;font-size:16px;max-width:46ch}}

.p-spec{{display:grid;grid-template-columns:repeat(auto-fit,minmax(158px,1fr));
  gap:1px;background:var(--g-rule);border:1px solid var(--g-rule)}}
.p-spec>div{{background:var(--g-bg);padding:16px 18px}}
.p-spec dt{{font-family:var(--g-mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--g-ink-3);margin:0}}
.p-spec dd{{font-family:var(--g-mono);font-size:13px;margin:8px 0 0;color:var(--g-ink);
  display:flex;align-items:center;gap:8px;font-variant-numeric:tabular-nums}}
.p-chip{{width:14px;height:14px;flex:none;background:var(--g-accent);border-radius:7px}}

.p-rail{{display:grid;grid-template-columns:repeat(auto-fit,minmax(316px,1fr));gap:52px 30px}}
.p-board{{margin:0;display:flex;flex-direction:column;gap:20px;min-width:0}}
.p-cap{{min-height:196px;border-top:2px solid var(--g-accent);padding-top:14px}}
.p-kicker{{font-family:var(--g-mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--g-ink-2);margin:0 0 10px;display:flex;gap:10px;align-items:baseline}}
.p-num{{color:var(--g-accent)}}
.p-cap h3{{font-size:28px;letter-spacing:-.01em;margin:0 0 10px;line-height:1.05}}
.p-bold{{margin:0 0 10px;font-size:14.5px;line-height:1.5;color:var(--g-ink)}}
.p-widg{{margin:0;font-family:var(--g-mono);font-size:11.5px;line-height:1.65;color:var(--g-ink-3)}}
.p-dev{{width:340px;height:737px;overflow:hidden;border-radius:33px;
  outline:1px solid var(--g-rule);outline-offset:-1px;
  box-shadow:0 22px 54px rgba(74,58,40,.26)}}
.p-dev .ios{{transform:scale(.865);transform-origin:top left}}

.p-sec{{display:flex;flex-direction:column;gap:18px}}
.p-wrap h2{{font-size:32px;letter-spacing:-.015em;margin:0;line-height:1.05}}
.p-sub{{margin:0;color:var(--g-ink-2);font-size:15.5px;max-width:70ch}}
.p-tablewrap{{overflow-x:auto;border:1px solid var(--g-rule);background:var(--g-card)}}
.p-tablewrap table{{width:100%;min-width:820px}}
.p-tablewrap th,.p-tablewrap td{{text-align:left;padding:14px 18px;
  border-bottom:1px solid var(--g-rule);font-size:14px;vertical-align:top;line-height:1.5}}
.p-tablewrap tr:last-child td{{border-bottom:0}}
.p-tablewrap th{{font-family:var(--g-mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--g-ink-3);font-weight:400;background:var(--g-panel)}}
.p-tablewrap td:first-child{{font-family:var(--g-disp);font-size:16px;
  letter-spacing:-.01em;white-space:nowrap;color:var(--g-ink)}}
.p-tablewrap td:last-child{{color:var(--g-ink)}}
.p-was{{color:var(--g-ink-3)}}
.p-v{{font-family:var(--g-mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;
  padding:4px 9px;display:inline-block}}
.p-v--pass{{color:#FBF8F3;background:var(--g-accent)}}
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
      <p class="p-eyebrow">Session 4 · Commerce · review gate · rev 1</p>
      <h1>Shop<em>Ease</em></h1>
    </div>
    <p class="p-lede">Six iOS 26 artboards, no two sharing a layout skeleton.
      Every screen is live HTML at 393 × 852 — type stays sharp at any zoom.</p>
  </header>

  <dl class="p-spec">
    <div><dt>Accent</dt><dd><span class="p-chip"></span>#8A3418</dd></div>
    <div><dt>Ground</dt><dd>#F4EFE7 · locked</dd></div>
    <div><dt>Canvas</dt><dd>393 × 852 @3×</dd></div>
    <div><dt>Radii</dt><dd>19 · 15 · 12 · 9 · 8</dd></div>
    <div><dt>Glass</dt><dd>1 element, 1 screen</dd></div>
    <div><dt>Photography</dt><dd>18 plates · CC0</dd></div>
  </dl>

  <div class="p-rail">
{"".join(boards)}
  </div>

  <section class="p-sec">
    <h2>How it diverges from WealthKit and FitnessPro</h2>
    <p class="p-sub">The S2 gate approved the process, not the visuals — each app has to read as a
      different product rather than a recolour. Two domains are now spent, so the divergence has to
      hold against both at once.</p>
    <div class="p-tablewrap"><table>
      <thead><tr><th>Axis</th><th>Fintech · spent</th><th>Fitness · spent</th><th>Commerce · this session</th></tr></thead>
      <tbody>{lock_rows}</tbody>
    </table></div>
    <p class="p-note">Also avoided, as the earlier domains have spent them:
      <b>inset grouped card lists</b>, a <b>floating glass pill tab bar</b>,
      <b>letter-monogram tiles standing in for logos</b>, the <b>sparkline + allocation-donut pair</b>,
      a <b>tabular hero number</b> as the opening move, and an <b>icon dock</b>.<br>
      Commerce clichés avoided: <b>grey placeholder blocks</b>, <b>five-star rows on every tile</b>,
      <b>"Flash Sale!!" banners</b>, a <b>card border around every product</b>, and
      <b>carousel dots as the only navigation</b>.</p>
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
    <h2>Where the photography comes from</h2>
    <p class="p-sub">Rule 7 is not optional in commerce — grey rectangles would have sunk the set.
      Every product is a real object photograph released into the public domain, verified by API
      rather than by assumption.</p>
    <p class="p-note">Source: <b>Cleveland Museum of Art Open Access</b>. Each object is fetched by
      id and its <b>share_license_status</b> asserted to equal <b>CC0</b> before it enters the build.<br>
      Treatment: CMA shoots on a graduated studio sweep, and the commerce identity lock says images
      sit <b>directly on the ground with no container</b> — so the backdrop is flooded out from the
      frame edge through low-gradient pixels, the object's outline acting as the barrier, and the
      object is recomposited on ShopEase's own sand with a new contact shadow. The knockout is what
      buys the containerless look; it is not a filter for its own sake.<br>
      Product names, makers, prices and stock are written for the mockup. The photography is the
      only part that had to be real, and it is.</p>
    <div class="p-tablewrap"><table>
      <thead><tr><th>Object</th><th>Origin</th><th>Date</th><th>Licence</th></tr></thead>
      <tbody>{prov}</tbody>
    </table></div>
  </section>

  <p class="p-note">Source artboards → <b>PortfolioProjectWebApp/design-canvas/commerce/</b><br>
    PNG exports @3× (1179 × 2556) → <b>assets/app-screenshots/shopease/v1/</b><br>
    One ground only: paper is the commerce identity lock, so there is no dark set to review.<br>
    Gate question: does this read as a third product, or as WealthKit and FitnessPro in a new colour?</p>
</div>
'''
open("canvas.html", "w").write(page)
print(len(page), "bytes")
