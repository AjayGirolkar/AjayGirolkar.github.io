# Workflow — Publish an Upwork Project Catalog listing

**Objective:** turn one demo app in this repo into a live, fixed-price Upwork Project Catalog
listing with 6 compliant gallery images and paste-ready copy.

**Why this exists:** Project Catalog is a storefront, not bidding. Listings cost no Connects,
are free to create, and stay searchable 24/7 while you bid elsewhere. Expect 4–8 weeks before
organic traffic is steady, so the cost of publishing early is close to zero and the cost of
waiting is a month of ranking.

---

## Platform facts that constrain this workflow

| Constraint | Value |
|---|---|
| Live listings | 20 max, plus 20 more in review |
| Cost to create | Free. No Connects |
| Fee on a sale | Standard 10% freelancer service fee |
| Approval | Upwork reviews every listing before it publishes |
| Images | up to 20 per project · **4:3** · min 400×300 · recommended 1000×750 · max 4000×4000 · JPEG/PNG · <10MB |
| Video | 1 per project · ≤60s · MP4 · ≤100MB · English audio |
| Tiers | 3 (Starter / Standard / Premium). The middle tier converts most |
| Buyer requirements | Client has 48h to answer mandatory questions. Miss it and the order auto-cancels and refunds. **The delivery clock starts when they answer, not when they buy** |

**The trap this repo solves:** iPhone screenshots are 1179×2556 (9:19.5). Upwork wants 4:3.
Uploading a raw screenshot gets it letterboxed or cropped through the middle of the UI.
Every image must be composited onto a 4:3 canvas first. That is what the tool does.

---

## Inputs

- A demo app with 6+ screenshots under `assets/app-screenshots/<slug>/v<n>/`
- A spec at `assets/upwork/listings/<slug>.json`
- Copy at `assets/upwork/listings/<slug>.md` — title, description, tiers, FAQ, buyer
  requirements and project steps. Form-only fields live here, not in the JSON spec, because no
  card renders them.

## Tools

- `tools/upwork_catalog_cards.py` — renders the 6 gallery cards

---

## Step 1 — Write the spec

Copy an existing JSON in `assets/upwork/listings/` and edit. Required keys:

| Key | Notes |
|---|---|
| `slug` | must match the output folder name |
| `screens_dir` | repo-relative, e.g. `assets/app-screenshots/wealthkit/v2` |
| `hero_screens` | exactly 3 filenames — the strongest three, most visual in the middle |
| `grid_screens` | 6 filenames (the tool adapts to other counts, but 6 is the tuned layout) |
| `grid_captions` | optional; derived from filenames when omitted |
| `hero_headline` | `\n` forces the line break. Two lines, ≤26 chars per line |
| `eyebrow`, `hero_sub`, `deliverables`, `process`, `tiers`, `fit_good`, `fit_bad`, `footer` | see an existing spec |

Mark exactly one tier `"featured": true` — that is the "Most popular" ribbon, and it should be
the middle tier.

## Step 2 — Render the cards

```bash
python3 tools/upwork_catalog_cards.py <slug>                  # all 6
python3 tools/upwork_catalog_cards.py <slug> --cards hero      # iterate on one
python3 tools/upwork_catalog_cards.py                          # every spec
```

Output lands in `assets/upwork/cards/<slug>/`, 2000×1500 PNG:

| File | Job |
|---|---|
| `01-hero` | the thumbnail. The only image most buyers ever see. Get this one right |
| `02-deliverables` | what they get, as a checklist |
| `03-screens` | six screens with captions — the proof |
| `04-process` | day-by-day, kills "when will it be done" |
| `05-tiers` | price comparison so they self-select before clicking |
| `06-fit` | buy / don't buy. Filters bad orders and cuts refund risk |

**Open every card before uploading.** Long strings wrap differently than you expect; the
renderer will not warn you about overflow.

## Step 3 — Publish on Upwork

Go to **Find Work → Project Catalog → Manage Projects → Create a new project**
(the freelancer view of `upwork.com/nx/project-dashboard/`).

1. **Category** — pick the one in the `.md`. Category drives search placement, so match the
   buyer's mental model, not your job title.
2. **Title** — paste from the `.md`. It follows "I will …". Front-load the deliverable: buyers
   scan the first three words, and titles get indexed by Google.
3. **Search tags** — 5 from the `.md`.
4. **Scope / tiers** — enter the three tiers from the `.md` table: price, delivery days,
   revisions, and the feature checkboxes. Keep tiers clearly distinct; when Standard and
   Premium overlap, buyers fall back to Starter.
5. **Add-ons** — enter the optional extras from the `.md`. These raise average order value
   without touching the headline price that got the click.
6. **Description** — paste from the `.md`. Keep the "About the screenshots" paragraph. If the
   field truncates, cut from the middle, never the first paragraph or that disclosure.
7. **FAQ** — paste every Q&A. This field is the most-skipped one on the platform and the one
   that removes the last objection before purchase.
8. **Requirements** — paste the numbered questions and mark **all of them mandatory**. This is
   the single most valuable setting in the form: it starts your delivery clock only once the
   client has actually given you what you need.
9. **Project steps** — paste the numbered steps from the `.md`. Upwork owns steps 1 and 2
   ("client purchases and sends requirements", "you complete the project"); everything you add
   sits between them and becomes a checkbox in the project workroom. Rules: 4–6 steps, one
   client-visible outcome each ("you get a build to run", never "refactor the view models"), one
   list that fits all three tiers, first step says the clock starts on *their* requirements, last
   step is the revision round so revisions land before the order is marked complete.
10. **Gallery** — upload `01-hero` … `06-fit` in order. `01-hero` becomes the thumbnail.
11. **Video** — optional, add later (Step 6).
12. Submit for review. Upwork approves or rejects before it goes live.

## Step 4 — First 30 days

Ranking is driven by reviews and clicks, and there are none on day one.

- Discount the Starter tier ~30% for the first 30 days. Raise it after 3 reviews.
- Route any client you get elsewhere through the catalog link so the order and review land
  on the listing.
- Share the listing URL on LinkedIn. External traffic counts and is the fastest lever you own.
- Read the pre-purchase questions buyers send. Every repeated question is a hole in the
  description — patch it, in the FAQ.

## Step 5 — Read the dashboard

| Symptom | Diagnosis | Fix |
|---|---|---|
| Low impressions | title / tags / category | rewrite the title in buyer language |
| Impressions, no clicks | thumbnail | rebuild `01-hero`, bolder headline |
| Clicks, no orders | price, scope or proof | check `05-tiers` and `06-fit`, add the video |
| Orders, painful delivery | scope too loose | tighten Step 1 spec and the requirements questions |

## Step 6 — Add the video

One per listing, ≤60s. Spend it on your best-performing listing first: screen-record the demo
app running, narrate what the buyer gets. Autoplay video meaningfully lifts both views and
purchases.

---

## Rules learned

- **Never upload a raw phone screenshot.** 9:19.5 into a 4:3 slot always looks broken.
- **Always disclose that demo apps are self-initiated.** They are your own design work, which
  is fine to show — but implying client work risks a rejection in review, and rejection costs
  weeks of ranking.
- **Pad every timeline 2x.** These are evenings-and-weekends builds against a day job. A late
  delivery damages JSS, which is far more expensive than a longer quoted timeline.
- **Publish 3, not 9.** Ship the three strongest, learn which format ranks, then clone it.
  Nine mediocre listings rank worse than three good ones and are nine times the maintenance.
- **Refresh monthly.** Stale listings get demoted.
- **Don't stop bidding.** Catalog is the background track, not a replacement.

## Backlog

- [ ] Listings 4–9 from the remaining demo apps: `fitnesspro`, `socialflow`, `gate`,
      `nocturne`, `lingo`, `wayfare`
- [ ] Service listings with no demo app of their own (iOS audit, App Store launch, SwiftUI
      migration). These need different card types — the deliverable itself becomes the image:
      run `ios-audit` against a public open-source iOS repo, screenshot the real report, and
      use before/after splits and annotated screenshots as the gallery.
