import gen, json, feed
T = gen.T
kit = open("kit.html").read()
app = open("app.html").read()
SRC = json.load(open("src/meta.json"))

# only the files that actually ship, not the 137 that were contact-sheeted
USED = ([c[2] for c in feed.CAST.values()] + [p[1] for p in feed.POSTS.values()]
        + [feed.HERO[1]] + [e[0] for e in feed.EXPLORE] + feed.GRID + feed.TRAY)
USED = sorted(set(USED))

META = [
 ("01", "List / feed", "Home",
  "One square photograph at 393pt with the caption set at 18px directly on the black — no card, no border, no radius. Everything else on the screen is 13.5px or smaller",
  "Story rail · media post · engagement row · compose pill"),
 ("02", "Immersive detail", "Post",
  "The photograph is the screen, floor to ceiling, and the like count is set at 36px over it. Chrome has fully dissolved — no tab rail, no compose pill",
  "Full-bleed media · oversized count · scrim type · inline comment"),
 ("03", "Input moment", "Compose",
  "The caption is mid-sentence with a live caret and a counter that has actually counted it — the one screen where type is being entered",
  "Wide picker plate · caret + counter · hairline rows · 4-up recents tray"),
 ("04", "Dense grid", "Explore",
  "A 2×2 anchor inside a 1pt-gutter mosaic, so the grid reads as one sheet of photography that one frame happens to be four times larger inside",
  "Search field · mosaic with 2×2 anchor · bare glyph rail"),
 ("05", "Empty state", "Quiet feed",
  "One 40px sentence with nothing beside it. The illustration is three real faces — a drawn spot illustration would be the only thing on screen that is not a photograph",
  "Solo story slot · display headline · suggestion rows · single CTA"),
 ("06", "Profile", "Grid",
  "The 3-up grid runs edge to edge at 1pt gutters, so the bottom two thirds is one continuous field. The accent does not appear on this screen at all",
  "Avatar + tabular stats · hairline controls · 3-up grid · segment"),
]

AUDIT = [
 ("Concentric radii", "pass",
  "The social lock forbids radius on CONTENT — media, mosaic tiles and grid tiles are all square, which is the point. The nesting lives in the chrome: compose pill 26 → its camera button 19; share pill 25; profile controls 8; avatars and story rings are circles. No radius is reused across two levels, and no radius touches a photograph."),
 ("Rhythm, not uniform spacing", "pass",
  "01 runs a 393pt photograph against a 46pt byline and an 11pt gap to the caption. 03 alternates a 296pt plate, 52pt hairline rows and a 1pt-gutter tray. 06 goes 82pt avatar → 34pt controls → 1pt gutters. Gutters are 16–34 between groups and 1–9 within."),
 ("One accent, not purple", "pass",
  "Hot pink #FF2E63, hue 342° — 174° from the WealthKit teal, 190° from the FitnessPro mint and 144° from the ShopEase oxblood. It appears only on a primary action: the liked heart, the compose button, Share, the empty state's one CTA and the story + badge. Counts, labels, status and section heads are all mono. Screen 06 has no accent on it at all."),
 ("Plausible specific data", "pass",
  "Likes ≫ comments > shares on every post (4,218 / 96 / 31 · 12,480 / 318 / 512 — the one inversion is the share-heavy city frame, which is how that content actually behaves). Timestamps ascend down the feed, 2h → 5h → 8h → 1d. The composer's counter reads 81 and the sentence is 81 characters. Handles, mutual counts and the 214 / 18.4k / 391 triple are internally consistent."),
 ("One bold move per screen", "pass",
  "Named per artboard above. Each is the only oversized element on its screen and every other element steps back to 15px or less."),
 ("Domain vocabulary", "pass",
  "Story rail with a 2.5pt gradient ring for unseen and a plain hairline for seen; full-bleed media post with no card; engagement row where the glyphs carry weight and the counts are secondary; a compose PILL, never a plus-in-a-circle; 3-up profile grid at 1pt gutters. No generic card appears anywhere in the set."),
 ("Real imagery", "pass",
  "Forty-two real photographs — twelve faces, four feed frames, a full-bleed hero, fourteen mosaic tiles, nine grid tiles and eight tray thumbnails. All CC0, licence asserted per item at download. No grey placeholder and no repeated stock face."),
]

LOCK = [
 ("Ground", "Light grey #F2F2F7", "Near-black #07090A", "Warm sand #F4EFE7",
  "Pure black #000, locked — mono is the lock, and black is what leaves the photography as the only colour"),
 ("Container model", "Inset grouped cards", "No cards; rings and zone bands are the surfaces",
  "No containers; photographs sit on the ground at radius 12",
  "No containers AND no radius. Media is edge-to-edge and square-cornered; grids run at 1pt gutters"),
 ("Chrome", "Floating glass pill tab bar on every screen", "Docked icon bar, absent during a workout",
  "Text-only dock, one glass buy bar",
  "Disappears on scroll. When it shows it is five bare glyphs on the ground — no bar, no labels. The only floating element is a compose pill, and it is the app's one glass surface"),
 ("Type personality", "SF Text, rounded reserved for money", "Oversized rounded numerals",
  "Fraunces display + .19em uppercase labels",
  "Inter Tight throughout, set tight (−.02 to −.045em) and large (17px body, 1.26 leading). Nothing is ever uppercased — the one rule the other three do not have"),
 ("Density signature", "One hero number, then dense tabular rows", "Extreme alternation",
  "Image-led and sparse, 20pt gutters",
  "Quiet and even. The variance comes from the photography, not from the layout — which is why the grids are 1pt and the type scale is narrow"),
 ("Accent", "Deep teal #0F7B6C", "Mint #3DDC84", "Oxblood #8A3418",
  "Hot pink #FF2E63 — primary action only, at most one filled control per screen"),
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
    f'<tr><td>{a}</td><td class="p-was">{f}</td><td class="p-was">{g}</td>'
    f'<td class="p-was">{c}</td><td>{s}</td></tr>'
    for a, f, g, c, s in LOCK)
prov = "".join(
    f'<tr><td>{SRC[i]["title"][:64]}</td><td class="p-was">{SRC[i]["creator"][:28] or "—"}</td>'
    f'<td class="p-was">{SRC[i]["source"] or "—"}</td><td>{SRC[i]["licence"]}</td></tr>'
    for i in sorted(USED, key=lambda i: SRC[i]["title"].lower()))

page = f'''<title>SocialFlow Artboards</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
{kit}
{app}
<style>
/* SocialFlow is dark-locked, so this review page commits to one mono world too and paints
   every colour explicitly rather than inheriting the viewer's ground.
   NOTE: app.html's class names are NOT scoped to .ios, so everything here is p- and every
   bare element selector is scoped under .p-wrap. An unprefixed .media / .cap / .sub / .act
   would leak straight into the six embedded screens. */
:root{{
  --g-bg:#0B0B0C; --g-panel:#141416; --g-card:#0F0F11;
  --g-ink:#F4F4F5; --g-ink-2:rgba(244,244,245,.62); --g-ink-3:rgba(244,244,245,.36);
  --g-rule:rgba(244,244,245,.15); --g-accent:#FF2E63;
  --g-body:"Inter Tight","Helvetica Neue",Arial,sans-serif;
  --g-mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,monospace;
}}
html{{background:var(--g-bg)}}
body{{background:var(--g-bg);color:var(--g-ink);font-family:var(--g-body);
  font-size:16px;line-height:1.58;margin:0;-webkit-font-smoothing:antialiased}}
.p-wrap{{max-width:1240px;margin:0 auto;padding:0 26px 96px;
  display:flex;flex-direction:column;gap:64px}}
.p-wrap h1,.p-wrap h2,.p-wrap h3{{font-family:var(--g-body);font-weight:600;
  letter-spacing:-.035em}}
.p-wrap table{{border-collapse:collapse}}

.p-head{{padding:60px 0 34px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,330px);
  gap:44px;align-items:end;border-bottom:1px solid var(--g-rule)}}
.p-eyebrow{{font-family:var(--g-mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--g-accent);margin:0 0 18px}}
.p-wrap h1{{font-size:clamp(52px,9vw,104px);letter-spacing:-.05em;line-height:.92;
  margin:0;font-weight:700;text-wrap:balance}}
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
.p-cap{{min-height:214px;border-top:2px solid var(--g-accent);padding-top:14px}}
.p-kicker{{font-family:var(--g-mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--g-ink-2);margin:0 0 10px;display:flex;gap:10px;align-items:baseline}}
.p-num{{color:var(--g-accent)}}
.p-cap h3{{font-size:28px;margin:0 0 10px;line-height:1.05}}
.p-bold{{margin:0 0 10px;font-size:14.5px;line-height:1.5;color:var(--g-ink)}}
.p-widg{{margin:0;font-family:var(--g-mono);font-size:11.5px;line-height:1.65;color:var(--g-ink-3)}}
.p-dev{{width:340px;height:737px;overflow:hidden;border-radius:33px;
  outline:1px solid var(--g-rule);outline-offset:-1px;
  box-shadow:0 24px 60px rgba(0,0,0,.75)}}
.p-dev .ios{{transform:scale(.865);transform-origin:top left}}

.p-sec{{display:flex;flex-direction:column;gap:18px}}
.p-wrap h2{{font-size:32px;margin:0;line-height:1.05}}
.p-sub{{margin:0;color:var(--g-ink-2);font-size:15.5px;max-width:70ch}}
.p-tablewrap{{overflow-x:auto;border:1px solid var(--g-rule);background:var(--g-card)}}
.p-tablewrap table{{width:100%;min-width:940px}}
.p-tablewrap th,.p-tablewrap td{{text-align:left;padding:14px 18px;
  border-bottom:1px solid var(--g-rule);font-size:14px;vertical-align:top;line-height:1.5}}
.p-tablewrap tr:last-child td{{border-bottom:0}}
.p-tablewrap th{{font-family:var(--g-mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--g-ink-3);font-weight:400;background:var(--g-panel)}}
.p-tablewrap td:first-child{{font-size:15px;font-weight:600;letter-spacing:-.02em;color:var(--g-ink)}}
.p-tablewrap td:last-child{{color:var(--g-ink)}}
.p-was{{color:var(--g-ink-3)}}
.p-v{{font-family:var(--g-mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;
  padding:4px 9px;display:inline-block}}
.p-v--pass{{color:#0B0B0C;background:var(--g-accent)}}
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
      <p class="p-eyebrow">Session 5 · Social · review gate · rev 1</p>
      <h1>Social<em>Flow</em></h1>
    </div>
    <p class="p-lede">Six iOS 26 artboards, no two sharing a layout skeleton.
      Every screen is live HTML at 393 × 852 — type stays sharp at any zoom.</p>
  </header>

  <dl class="p-spec">
    <div><dt>Accent</dt><dd><span class="p-chip"></span>#FF2E63</dd></div>
    <div><dt>Ground</dt><dd>#000 · locked</dd></div>
    <div><dt>Canvas</dt><dd>393 × 852 @3×</dd></div>
    <div><dt>Radii</dt><dd>26 · 25 · 19 · 8 · 0</dd></div>
    <div><dt>Glass</dt><dd>1 element, 1 screen</dd></div>
    <div><dt>Photography</dt><dd>42 frames · CC0</dd></div>
  </dl>

  <div class="p-rail">
{"".join(boards)}
  </div>

  <section class="p-sec">
    <h2>How it diverges from WealthKit, FitnessPro and ShopEase</h2>
    <p class="p-sub">The S2 gate approved the process, not the visuals — each app has to read as a
      different product rather than a recolour. Three domains are now spent, so the divergence has
      to hold against all three at once.</p>
    <div class="p-tablewrap"><table>
      <thead><tr><th>Axis</th><th>Fintech</th><th>Fitness</th><th>Commerce</th><th>Social · this session</th></tr></thead>
      <tbody>{lock_rows}</tbody>
    </table></div>
    <p class="p-note">Also avoided, as the earlier domains have spent them:
      <b>inset grouped card lists</b>, a <b>floating glass pill tab bar</b>,
      <b>letter-monogram tiles</b>, the <b>sparkline + allocation-donut pair</b>,
      a <b>tabular hero number</b> as the opening move, an <b>icon dock</b>, and
      <b>uppercase tracked labels</b>.<br>
      Social clichés avoided: <b>a card with a shadow around every post</b>,
      <b>blue verified checks everywhere</b>, <b>Lorem ipsum captions</b>,
      <b>the same stock face in every avatar</b>, <b>three identical grey outline glyphs</b>
      for like/comment/share, and a <b>plus-in-a-circle</b> compose button.</p>
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
    <p class="p-sub">Social is the domain where rule 7 is the whole design — remove the photographs
      and there is nothing left but a black rectangle and a pink button. Every frame is a real
      CC0 photograph, verified by API field rather than by assumption.</p>
    <p class="p-note">Source: <b>Openverse</b>, filtered to <b>CC0</b>, each item's
      <b>licence</b> field asserted before the file is written.
      A hundred and thirty-seven candidates were pulled and contact-sheeted;
      <b>{len(USED)}</b> survived and ship.<br>
      Treatment: one shared grade, and only one. Every black is lifted to the same cool 6/255,
      every highlight warmed the same amount, saturation pulled back 8%. Without it, files from
      {len(USED)} different shoots dropped edge-to-edge on one black ground read as a scrapbook of
      found images rather than as one feed. It is deliberately mild — social is the register where
      the photography has to stay louder than the treatment.<br>
      Handles, captions, counts and locations are written for the mockup. The photography is the
      only part that had to be real, and it is.</p>
    <div class="p-tablewrap"><table>
      <thead><tr><th>Frame</th><th>Creator</th><th>Provider</th><th>Licence</th></tr></thead>
      <tbody>{prov}</tbody>
    </table></div>
  </section>

  <p class="p-note">Source artboards → <b>PortfolioProjectWebApp/design-canvas/social/</b><br>
    PNG exports @3× (1179 × 2556) → <b>assets/app-screenshots/socialflow/v1/</b><br>
    One ground only: pure mono is the social identity lock, so there is no light set to review.<br>
    Gate question: does this read as a fourth product, or as the first three in a new colour?</p>
</div>
'''
open("canvas.html", "w").write(page)
print(len(page) // 1024, "KB")
