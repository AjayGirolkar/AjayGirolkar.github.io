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
| 4 | Commerce (ShopEase) | not started |
| 5 | Social (SocialFlow) | not started |
| 6 | AI (NativeAIStudio) + rewire index.html + delete Leonardo prompts | not started |

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
Three gotchas for S4+:
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

## TODO — do these first next session

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

3. **Reference screenshots still missing.** `Resources/design-refs/{commerce,social,ai}/`
   all empty — S2 and S3 were both built from prose only. This was named the highest-leverage input in the plan.
   3–5 PNGs per domain from Mobbin / VP0 / Banani before the matching session.

4. **Notion S2 and S3 rows** not updated — they are gates, Ajay's call to close.

## S4 kickoff prompt

/ios-design-language
S4 commerce canvas. Read design-canvas/HANDOFF.md, then domain-patterns.md §3 AND the
Identity lock table at the end of that file.
Reuse design-canvas/fitness/{kit,app,gen,build_canvas,proof} as the build HARNESS only —
extract the kit between its KIT-START / KIT-END markers, and prefix/scope the review page's own
CSS so it does not leak into the embedded screens. Do not reuse fintech or fitness layout decisions.
Commerce must diverge: warm sand/paper ground, NO containers (images sit directly on the ground,
4:5, radius 12, no border), chrome nearly invisible with a sticky glass buy bar as the only chrome,
uppercase wide-tracked labels + an editorial display face, image-led and deliberately sparse.
Accent: warm-neutral, product photography carries the colour.
Widgets: product grid, colour swatch row, size run, strikethrough price, sticky buy bar.
Rule 7 (real imagery) is NOT optional here — commerce needs real base64 product photography,
not grey rectangles. Source or generate it before laying out.
6 artboards, same archetype grid, six different skeletons. Render + review 1-3, then 4-6, then publish.
