# Portfolio screen design — session handoff

Plan: `~/.claude/plans/we-have-portfolio-project-async-tarjan.md`
Skill: `/ios-design-language` (carries rules, metrics, icons, glass, domain vocab)
Boundary: **one domain per session.** Two domains blows context past 150k.

## Status

| S | Domain | State |
|---|---|---|
| 1 | Foundation | done — skill + primitives + domain-patterns |
| 2 | **Fintech (WealthKit)** | **done — gate PASSED 2026-08-27** |
| 3 | **Fitness (FitnessPro)** | **done — awaiting gate** |
| 4 | **Commerce (ShopEase)** | **done — awaiting gate** |
| 5 | **Social (SocialFlow)** | **done — awaiting gate** |
| 6 | **AI (NativeAIStudio)** + index rewire + Leonardo prompts deleted | **done 2026-08-28 — awaiting gate. Project complete.** |

## S2 output

Canvas: https://claude.ai/code/artifact/c423cb7c-7e64-4eca-bc19-51f675d0048b
PNGs @3x: `assets/app-screenshots/wealthkit/v2/` (light) and `v2/dark/` — 01-dashboard … 06-profile + _proof-sheet in each.
Canvas has an Auto / Light / Dark switch; the embedded live screens follow it.
Source: `design-canvas/fintech/` — `gen.py` builds `out/sN.html` from `kit.html` + `app.html` + `sN.html`;
`build_canvas.py` assembles the review canvas. Render: `python3 ~/.claude/skills/ios-design-language/render.py page.html out.png [--dark]`

Accent `#0F7B6C` / dark `#2FBFA8`. Widgets: sparkline, allocation donut, ledger row.
Self-audit: 6 rules pass, "real imagery" n/a (fintech has no photography).

## S3 output

Canvas: https://claude.ai/code/artifact/89d0c446-ee86-47df-a5ed-a62adc53c939
PNGs @3x: `assets/app-screenshots/fitnesspro/v1/` — 01-today … 06-you + 07-workout-detail + _proof-sheet.
**7 artboards** (6 archetypes + a workout-detail screen added in rev 2).
**One ground only.** FitnessPro is dark-locked by design (identity lock), so there is no light set.
Source: `design-canvas/fitness/` — same harness as fintech: `gen.py` builds `out/sN.html` from
`kit.html` + `app.html` + `sN.html`; `build_canvas.py` assembles the review canvas;
`proof.py` builds the 4x2 proof sheet; `duo.py` rebuilds the exercise demo frames.

Accent **`#3DDC84` mint** on ground `#07090A` (rev 3 — the original `#CBFF3C` lime read as glare;
it was near-max luminance *and* chroma on pure black). Zone ramp is now deliberately **desaturated
and held below the accent's chroma** so data colours never compete with the brand colour:
`#5E7C99 #3E9FA8 #7FB03F #D9922C #C0392B`.

**Changing the accent is one line.** `themes.py` derives `--accent-dim`, `--accent-lift` and the
4-stop photo ramp from a single accent hex; `duo.py` re-maps the exercise frames onto it. Nine
candidates are defined there, and `variants.py` renders any of them across s1/s7 for comparison.
Caveat recorded: mint sits **24° in hue from WealthKit's dark teal `#2FBFA8`** — closer than any
other candidate. That is acceptable only because ground, container model, chrome and type already
carry the identity separation; do not let a future domain narrow that gap further.
Widgets: progress ring, HR zone band, vertical zone bar, set/rep grid, weight ruler, rest bar,
streak strip, pace ladder, consistency matrix.
Self-audit: **all 7 rules pass** as of rev 2 (re-checked at rev 3 after the accent change) — "real imagery" was n/a in rev 1 and now passes.

**Exercise demos (rev 2).** `duo.py` builds 12 lime-duotone WEBP frames from
[yuhonas/free-exercise-db](https://github.com/yuhonas/free-exercise-db) — 873 exercises,
**The Unlicense (public domain), verified via the GitHub API**. Every exercise ships exactly
two frames (start + end of the rep), so s7/s4 crossfade them into a loop instead of shipping a GIF;
the animation is gated behind `prefers-reduced-motion: no-preference`, which is why render.py
stills freeze on frame one. Frames go into `exercise_imgs.json` as base64 data URIs and are merged
into gen.py's token table as `IMG_<KEY>_0/_1`. Canvas is ~310 KB, far under the 16 MB artifact cap.
Crop boxes in duo.py are **fractional, not pixel** — the dataset mixes 850×567 landscape and
850×1275 portrait sources, and absolute boxes silently mis-crop the portrait ones.
Raw, these are red-walled stock gym photos; the duotone + vignette is what stops them from
being the domain's #1 cliché. Do not embed them untreated.
Divergence from fintech is tabled on the canvas against every identity-lock axis.

Kit extraction between KIT-START / KIT-END worked with no string surgery — the S2 patch holds.
**But extract on the exact marker lines.** `primitives.html` line 4 is a doc comment that *mentions*
both markers, so `sed -n '/KIT-START/,/KIT-END/p'` grabs it and the comment's `-->` renders as body
text at the top of every screen. Use:
`awk '/^<!-- KIT-START -->$/{f=1} f{print} /^<!-- KIT-END -->$/{f=0}' primitives.html > kit.html`
Four gotchas for S5+:
1. `app.html` class names are **not** scoped to `.ios`, so the review page must prefix its own
   classes (`p-`) and scope bare element selectors (`h1`, `h2`, `table`) under `.p-wrap`, or they
   leak into the embedded screens.
2. `build_canvas.py`'s board loop is now keyed off each entry's `num`, not its list position —
   it used to open `s{i}.html` by index, so reordering META silently paired captions with the
   wrong screens. Keep it keyed off `num`.
3. **Never hardcode the accent inside a screen.** Rev 1 buried lime hexes in the s1 ring gradient,
   the s1/s2/s3 HR-trace gradients and the gen.py consistency matrix and ruler, so the first
   accent comparison rendered coral numerals against a still-lime ring. Everything now goes
   through `var(--accent)` / `--accent-dim` / `--accent-lift` / `--z1..--z5`, including the s3
   ambient glow. Check with:
   `grep -o '#[0-9A-Fa-f]\{6\}' s*.html gen.py | sort | uniq -c`

## S4 output

Canvas: https://claude.ai/code/artifact/df0ae719-e3cc-4449-bd33-980386ffd4a5
PNGs @3x: `assets/app-screenshots/shopease/v1/` — 01-shop … 06-account + _proof-sheet.
**One ground only.** ShopEase is light-locked: warm sand `#F4EFE7` IS the commerce identity lock,
so there is no dark set. `--dark` renders pixel-identical (verified), because app.html re-pins the
kit's dark tokens *and* its dark `.glass` variant — without that second pin the buy bar goes dark
glass on paper.
Source: `design-canvas/commerce/` — same harness as fitness: `gen.py` builds `out/sN.html` from
`kit.html` + `app.html` + `sN.html`; `build_canvas.py` assembles the review canvas; `proof.py`
builds the 3x2 proof sheet. Plus two new ones: `dl.py` fetches the source photography and
`objects.py`/`catalog.py` turn it into image tokens.

Accent **oxblood `#8A3418`** on paper, and used on far less than the earlier domains: full prices
are ink, and the accent is reserved for a markdown, the cart badge, the delivery status dot and
Sign out. Display face is **Fraunces** (Google Fonts, allowed by the artifact CSP) over
`"Iowan Old Style", Palatino, Georgia`; labels are 10pt uppercase tracked to .19em. Chrome is a
**text-only dock — no icons, no glass**; the whole app has exactly one glass element, the PDP buy bar.
Widgets: product grid, glaze swatch row, size run with sold-out struck, strikethrough + discount
chip, sticky buy bar, cart badge.
Self-audit: **all 7 rules pass.**

**Photography (the session's real work).** 18 CC0 object plates from the
[Cleveland Museum of Art Open Access API](https://openaccess-api.clevelandart.org/) —
`dl.py` fetches each by id and **asserts `share_license_status == "CC0"`** before it enters the
build. Chosen after the Met's Costume Institute turned out to publish **zero** public-domain
images (`isPublicDomain=true` returns 0 for every clothing query — designer rights).
The store is therefore a curated-objects shop: ceramics, glass, lacquer, basketry, textile.

Gotchas that cost real time here, in order of nastiness:

1. **Both the CMA API and its CDN 403 on urllib's default User-Agent.** Send one on every request.
2. **`objects.py` is a backdrop knockout, not a filter.** CMA shoots on a graduated studio sweep;
   the commerce lock says images sit directly on the ground with no container, so the sweep has to
   go. Three algorithms were needed and the first two are recorded in the file because they are the
   obvious things to try:
   - flat colour-distance from the border → stops partway up the gradient, leaves a grey rectangle
     behind every object;
   - **edge-energy flood** (the sweep is smooth, the outline is a hard step) → works, but walks
     straight through a pale porcelain shoulder and eats the object;
   - **+ a per-row backdrop colour model, refit from confirmed background and re-flooded** → tracks
     the sweep inward without crossing the outline. This is the shipped one.
3. **Over-cutting is unrecoverable, under-cutting reads as the object's own shadow.** Seed tight.
   Pale bodies get `tol=10, passes=8, edge=2.5`; everything else takes the defaults. Per-object
   overrides live in `objects.PARAMS`, chosen from the grids in `obj/_grid*.png`.
4. **Cutout defects are invisible on a contact sheet and glaring at tile size.** Two plates shipped
   into a rendered screen with bites out of them before anyone saw it. Always check at final scale.
5. **A wide banner is not a tall plate cropped.** `object-fit:cover` on a 900-tall plate shows the
   middle of the vase and cuts its foot. `catalog.WIDE` composes wide plates wide, and `halign`
   pushes the object off-centre so the caption has clean sand to sit on.
6. **A hero that carries type must leave clean ground for it.** `catalog.HERO` carries
   `(size, inset, align)` per key for exactly this; a tall object at a high `align` still crosses
   the headline, and the Dynamic Island will crop the crown if `align` is too low.

Divergence from fintech and fitness is tabled on the canvas against every identity-lock axis,
now three columns wide since two domains are spent.

**Promoted into `/ios-design-language` after the S4 review** — do not re-derive these:
- `references/design-registers.md` — the register concept (domain gives vocabulary, register
  gives voice) with **editorial-paper** documented in full: type pairing + Google-Fonts/CSP
  mechanics + the `text-indent == letter-spacing` tracking fix, the paper/plate ground pair,
  containerless photography, the chrome budget, "the accent is savings, not price", density.
- `references/register-editorial-paper.html` — that register as a working CSS layer, between
  `REGISTER-START` / `REGISTER-END`. Load after the primitives kit. Verified to reproduce the
  ShopEase screens.
- `references/real-imagery.md` — the rule-7 workflow, licence-verified sources, the three
  knockout algorithms and why the first two fail, the tuning rules, the framing rules.
- `scripts/fetch_cc0.py` — CMA / Openverse / Wikimedia search + pull, licence asserted per item.
- `scripts/plates.py` — the generalised knockout + composite (`Plates(ground=...)`), plus
  `sheet` and `grid` CLI views. Verified to reproduce the ShopEase plates exactly.

## S5 output

Canvas: https://claude.ai/code/artifact/c8514ab0-449b-4812-9f8a-a0219748e4a1
PNGs @3x: `assets/app-screenshots/socialflow/v1/` — 01-feed … 06-profile + _proof-sheet.
**One ground only.** SocialFlow is dark-locked: the lock says "pure mono, black or white",
and black is the ground that leaves the photography as the only colour on the screen.
A white social app would also have landed on top of ShopEase's paper. `--dark` and the
light request render identically — `app.html` re-pins the kit's light tokens *and* its
light `.glass` variant, the mirror image of the fix ShopEase needed.
Source: `design-canvas/social/` — same harness: `gen.py` builds `out/sN.html` from
`kit.html` + `app.html` + `sN.html`; `build_canvas.py` assembles the review canvas;
`proof.py` builds the 3x2 proof sheet. Plus `dl.py` (Openverse search/pull/contact sheet)
and `feed.py` (the cast, the captions, the counts, and the image tokens).

Accent **hot pink `#FF2E63`** (hue 342°) on `#000` — 174° from the WealthKit teal, 190°
from the FitnessPro mint, 144° from the ShopEase oxblood, so the four-way hue separation
is now the widest it has been. Used on a primary action only: the liked heart, the compose
button, Share, the empty state's CTA, the story + badge. Screen 06 carries no accent at all.
Type is **Inter Tight** (Google Fonts) set tight and large — 17px body, 1.26 leading,
−.02 to −.045em tracking — and **nothing is ever uppercased**, which is the one type rule
the other three domains do not have.
Widgets: story rail (2.5pt gradient ring unseen / hairline seen), full-bleed media post,
engagement row, compose pill, 1pt-gutter mosaic with a 2x2 anchor, 3-up profile grid.
Self-audit: **all 7 rules pass.**

**Photography (again the session's real work).** 42 CC0 frames from **Openverse**,
`licence` asserted per item before the file is written. 137 candidates were pulled and
contact-sheeted; 42 ship. CMA is useless here — social needs faces, and CMA is objects.

Gotchas, in order of nastiness:

1. **Openverse's anonymous API starts returning HTTP 403 after a few hundred requests
   from one IP.** It is a quota, not a ban, and it clears — but it lands mid-session with
   no warning and you cannot pull one more file. Source the imagery FIRST (real-imagery.md
   already says so; this is the failure mode it protects against), and register a client
   id if a session needs more than ~150 files.
2. **`fetch_cc0.py` cannot `pull` from Openverse** — there is no by-id endpoint, so the
   skill script only searches. `social/dl.py` keeps the same contract locally:
   search → assert the licence field → download → `src/meta.json`. Fold it back into the
   skill if another people-led domain comes up.
3. **No knockout was needed and that is the point.** Social's lock says media is
   edge-to-edge, so there is no ground to composite onto and `plates.py` never runs. What
   *is* needed is a single shared **grade** — every black lifted to the same cool 6/255,
   every highlight warmed the same, saturation −8%. 42 files from 42 shoots dropped on one
   black ground read as a scrapbook without it. Keep it mild: social is the register where
   the photography has to stay louder than the treatment.
4. **Openverse quality varies wildly and the search terms lie.** "young woman portrait
   face" returns Renaissance panel paintings and Fayum mummy portraits; "pottery hands
   clay" returns museum vases. Contact-sheet everything and look — two rounds of picking
   were needed and half the first round was thrown out.
5. **A 4:5 opening post does not fit a feed screen that also has a story rail.** 59 status
   + 52 header + 105 rail + 46 byline + 491 media + 34 engagement leaves nothing for the
   caption, and the compose pill then lands on top of it. The opener is 1:1; the immersive
   4:5-and-taller moment belongs on the post-detail artboard, which is the right division
   of labour anyway.
6. **Chrome that "disappears on scroll" needs the content to disappear under it.** Without
   a bottom fade the next post's byline sits half-behind the compose pill and reads as a
   layout bug rather than as a scroll position. `.fade-b` is that fade.

Divergence from fintech, fitness and commerce is tabled on the canvas against every
identity-lock axis, now four columns wide.

**Promoted into `/ios-design-language` after S5** — do not re-derive these:
- `references/design-registers.md` — **mono-feed** documented in full alongside
  editorial-paper: the one-grotesk type rule (and the never-uppercase rule that separates
  the two at a glance), the mono ground and the dark-lock glass re-pin, no-containers-AND-
  no-radius with the concentric nesting moved into the chrome, the two chrome states and
  why the bottom fade is structural, the one-hot-accent discipline, the even density, the
  copy voice, and six failure modes including the 4:5-opener trap.
- `references/register-mono-feed.html` — that register as a working CSS layer, between
  `REGISTER-START` / `REGISTER-END`. Load after the primitives kit.
- `references/real-imagery.md` — new §2a: how to tell whether the register needs a
  **knockout** or a **shared grade**, with the grade's LUT; plus the Openverse quota-403,
  the no-by-id-endpoint fact, and the "search terms lie" warning.
- `scripts/fetch_cc0.py` — `pull` now works for Openverse via `pull openverse "<term>" [ids]`,
  licence still asserted per item, so the next people-led domain needs no local dl.py.

## S6 output — the last one

Canvas: https://claude.ai/code/artifact/f2ba2b4e-628c-431a-aad8-19c68f8e7bbf
PNGs @3x: `assets/app-screenshots/nativeaistudio/v1/` — 01-studio … 06-settings + _proof-sheet.
**One ground only.** NativeAIStudio is ink-locked. `app.html` re-pins the kit's light tokens
*and* its light `.glass`, so `--dark` and the light request render identically — the same
fix ShopEase and SocialFlow each needed, in the same place.
Source: `design-canvas/ai/` — same harness: `gen.py` builds `out/sN.html` from
`kit.html` + `app.html` + `sN.html`; `build_canvas.py` assembles the review canvas;
`proof.py` builds the 3x2 proof sheet. **No `dl.py` and no image pipeline** — see rule 7 below.

Accent **citrine brass `#DFC069`** (hue 46°) on warm ink `#131211`. It clears the teal by
126°, the mint by 101°, the oxblood by 31° and the pink by 61°, and it is the one band no
major AI product occupies — Claude is terracotta ~18°, ChatGPT mono green, Perplexity teal,
Gemini blue-violet. Flat, never a gradient, never purple.
Ground is **deliberately not black**: `#000` is social's and `#07090A` is fitness's, so warm
ink at `#131211` is what keeps a third dark app from landing on the first two.
Type is **IBM Plex Sans + IBM Plex Mono**, one superfamily, split by a rule that carries
meaning: **prose is sans, every machine-generated fact is mono** — model names, durations,
token counts, paths, prices, diagnostics, code. Sans is set airy (16px, 1.56 leading,
tracking ~0 — the opposite of social's −.035em); mono caps are tracked **.06em**, a terminal
header, not commerce's .19em editorial label.
Container model is **message turns**: user compact and right-inset 76pt on a lifted plate
with a 7pt tail corner; assistant full width with no plate, no border and no radius at all.
**There is not one card in the app, and no tab bar on any screen.**
Widgets: streaming response with a soft caret, tool-run chip with progress underline,
source citation (superscript + row), model picker as both a glass menu and a settings list,
composer that grows to five lines, drawn software keyboard.
Self-audit: **all 7 rules pass.**

**Rule 7 was the session's real work, and it was not photography.** AI screens have none,
so the thing that had to be real was the CONTENT: one real SwiftUI performance question
(a List dropping 60 → 38 fps while filtering 4,200 rows) with a correct three-part answer —
the filter running inside `body`, `id: \.self` forcing a teardown instead of a move, and
`.searchable` firing per character — real API names, a real WWDC session number, real
source domains, and Swift in the code block that compiles. This is now written up as
`real-imagery.md` §0.

Gotchas, in order of nastiness:

1. **The primitives kit never reset block margins.** S2–S5 got away with it because none of
   them used a bare `<p>`; the first prose register hit it immediately and every row was
   ~32pt too tall. **Fixed inside `primitives.html`** — `.ios p,h1..h3,ul,ol,pre,figure{margin:0}`.
2. **An unclosed `</div>` is invisible in a single-screen render and fatal in the proof
   sheet.** The browser auto-closes at EOF, so `out/s3.html` looked perfect while s4/s5/s6
   rendered *blank* inside their proof-sheet cells — they had nested into s3's
   `overflow:hidden` cell. Check with
   `for f in s*.html; do echo $f $(grep -o '<div' $f|wc -l) $(grep -o '</div>' $f|wc -l); done`
   before building the sheet, not after.
3. **A streaming screen cannot show a completed sources block.** Citations were moved
   *above* the prose (Perplexity's arrangement, and Perplexity is in the domain's
   "look at" list) — retrieval ran first, so the sources legitimately exist before the
   answer does. It also bought the ~150pt that made the caret fit.
4. **Long-form content overruns 852pt fast.** Three fit passes were needed on s3. Budget
   ~749pt below the status bar and nav, and lay input screens out *from the bottom up*:
   keyboard 262 + composer ~160 leaves ~240 for the transcript.
5. **Floating chrome needs the content to disappear under it.** The composer's fade has to
   be sized to the composer, not to a fixed 70pt — otherwise the paragraph behind it is
   half-visible and reads as a layout bug. Same structural fix social's compose pill needed.
6. **`--on-accent` has to be a token.** The ink that sits *on* an accent fill is
   accent-derived; hardcoding it is the S3 lime-ring failure in a new costume.
   Check with `grep -o '#[0-9A-Fa-f]\{6\}' s*.html` — the screens should return nothing.
7. **zsh arrays are 1-indexed.** A `for i in 1..6; do cp out/s$i.png $D/${names[$((i-1))]}.png`
   loop shifted every export by one and produced a file literally named `.png`.
8. **`render.py --reduce-transparency` is broken on this machine's Playwright build** —
   `Page.emulate_media() got an unexpected keyword argument 'reduced_transparency'`. Not
   fixed here because it is a skill-wide change; work around it by injecting the fallback
   rules with `add_style_tag` and screenshotting. Done for S6: the glass menu holds as a
   solid `#26221F` panel with the hierarchy intact, so the glass was not decoration.

Verified before publishing: dark and light render **pixel-identical** (ink is locked),
`register-ink-transcript.html` reproduces the shipped s3 render **pixel-identical**, and
`grep -o '#[0-9A-Fa-f]\{6\}' s*.html` returns nothing — no accent is hardcoded in a screen.

**app.html is scoped under `.ios` for the first time** — every earlier domain left its app
layer unscoped, which is why each review page had to prefix its own classes. The `p-` prefix
is still used on the canvas because the *kit's* `.card` / `.row` / `.chip` are unscoped.

Divergence from all four earlier domains is tabled on the canvas, five columns wide.

**Promoted into `/ios-design-language` after S6** — do not re-derive these:
- `references/design-registers.md` — **ink-transcript** documented in full: the
  prose-is-sans / machine-is-mono rule and the three-way tracking split that keeps it clear
  of the other two registers, the not-black ink ground, message turns and the tail corner,
  the no-tab-bar chrome budget and the composer→stop-button substitution, the flat
  iridescent accent, recency-driven density, the copy voice, and six failure modes.
  Plus an **Ink transcript · component markup** section.
- `references/register-ink-transcript.html` — that register as a working CSS layer between
  `REGISTER-START` / `REGISTER-END`, including the four extra symbols (`doc`, `term`,
  `sessions`, `model`) and the drawn keyboard. **Verified pixel-identical** to the shipped
  s3 render.
- `references/real-imagery.md` — new **§0**: how to tell whether a domain has photography at
  all, and what rule 7 becomes when it does not, with the image-led ↔ text-led table.
- `references/primitives.html` — the block-margin reset (gotcha 1).
- `references/domain-patterns.md` — the Identity lock table's AI row filled in as spent, the
  accent locked, and a new **"Spent by the later four"** block. All five domains are now spent.
- `SKILL.md` — rule 7 restated to cover text-led domains; the register table lists the new file.

## Index rewire (same session)

`index.html` now ships the five design-canvas apps instead of the old Leonardo set:
**WealthKit · FitnessPro · ShopEase · SocialFlow · NativeAIStudio** (PaySwift and AppMarket
are gone). Each tab links to its own canvas artifact, and the ShopEase copy that still said
"Amazon / Meesho style E-Commerce" is rewritten as the editorial curated-objects shop that
S4 actually built.
Images: the @3x PNGs stay the deliverable; the site loads **786px WEBP** copies written to
`<app>/<ver>/web/` (1.9 MB for all 31 frames, lazy-loaded). Hero phones and the two preloads
now point at `wealthkit/v2/web/01-dashboard.webp` and `nativeaistudio/v1/web/03-answer.webp`.
`docs/app-screenshot-prompts.md` — the Leonardo prompt sheet — is **deleted**, and `docs/`
with it.


## TODO

1. ~~Gate decision on S2~~ — **PASSED.** Ajay approved the fintech canvas. Proceed S3–S6 on the
   same process. Standing note: screen 02 (brand-colour merchant tiles) was the weakest of the six.

   **The approval covers the process, not the visuals.** Each remaining app must read as a
   different product, not a recolour of WealthKit. The binding constraint is the
   **Identity lock** table at the end of `references/domain-patterns.md`: every domain diverges
   on ground, container model, chrome and type personality — and the list of moves fintech has
   already spent is off-limits as another domain's default.

2. ~~Patch 3 skill bugs found in S2~~ — **DONE 2026-08-27.** `references/primitives.html` now has
   `<!-- KIT-START -->` / `<!-- KIT-END -->` extraction markers, `.ios svg text{font-family:var(--f-sys)}`
   plus a `.rnd` rounded class, and all tokens scoped to `.ios` instead of `:root`.
   Backup at `primitives.html.bak`. SKILL.md kit table updated to name the markers.
   S3+ should extract between the markers — no string surgery needed.

3. ~~Reference screenshots~~ — **never used.** All six sessions were built from prose plus the
   skill's own references. `Resources/design-refs/` was empty the whole way through and the set
   still passed its own audit six times. Worth recording as a finding rather than as debt: the
   highest-leverage input turned out to be the **identity-lock table**, not reference PNGs.

4. **Notion rows for S2–S6** not updated — they are gates, Ajay's call to close.

5. ~~ShopEase copy~~ — **DONE.** Rewritten in `index.html`; the prompt sheet that carried the
   other copy is deleted.

## Open items — what a next session would pick up

1. **Gate S3, S4, S5 and S6.** Four canvases are published and unreviewed. S2 is the only
   one that has actually been through a gate.
2. **Nothing here is SwiftUI yet.** Thirty artboards exist as HTML. `/mockup-to-swiftui`
   is the bridge, and WealthKit is the obvious first port — it is the one with a signed-off
   gate and a light *and* dark set.
3. **A sixth domain has nowhere to stand.** All five identity-lock rows are spent; see the
   new "Spent by the later four" block in `domain-patterns.md`.

## S6 kickoff prompt — the one that was run (kept for the record)

/ios-design-language
S6 AI canvas, and it closes the project. Read design-canvas/HANDOFF.md, then
domain-patterns.md §5 AND the Identity lock table at the end of that file.
Reuse design-canvas/social/{kit,app,gen,build_canvas,proof} as the build HARNESS only —
extract the kit on the EXACT marker lines (awk one-liner above), and prefix/scope the
review page's own CSS so it does not leak into the embedded screens. Do not reuse
fintech, fitness, commerce or social layout decisions.
AI must diverge: ink ground · MESSAGE TURNS, not cards (user compact and right-inset,
assistant full-width and airy — the asymmetry is the whole container model) · glass on
the composer and the stop button ONLY · mono for tool chips against an airy sans body ·
long-form vertical rhythm. Accent: a single restrained iridescent, NEVER purple and never
a gradient — and it has to clear teal 168°, mint 152°, oxblood 18° and social's pink 342°.
Widgets: streaming response with a soft caret, tool-run chip with icon + name + duration,
source citation (superscript + row beneath), model picker menu, prompt composer that grows
to ~5 lines.
Rule 7 is the one that will bite: AI screens have no photography, so the "real imagery"
answer is real CONTENT — a real technical question with a real specific answer, real tool
names, real source domains. "Hello! How can I help you today?" kills the screenshot.
Openverse is quota-limited (see S5 gotcha 1) but you should not need it.
6 artboards, same archetype grid, six different skeletons. Render + review 1-3, then 4-6,
then publish.

Then, in the SAME session (it is cheap once the canvas is done):
- rewire `index.html` to the five new canvases and the v1/v2 screenshot folders;
- **rewrite the ShopEase copy** — `index.html` and `docs/app-screenshot-prompts.md` still
  say "Amazon / Meesho style E-Commerce"; S4 built the editorial version the identity lock
  requires (TODO 5 above);
- delete the Leonardo prompts.
