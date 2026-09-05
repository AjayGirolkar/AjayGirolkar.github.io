# Portfolio PDF case studies

One 4-page A4 PDF per demo app — the file to attach to an Upwork proposal or email
to a lead.

```
profile.json                             shared seller copy: tiers, process, contact, per-app "transfer" lines
AjayGirolkar-<App>-iOS-case-study.pdf    the deliverable, ~1.1–1.5 MB each
_preview/<slug>/page-*.png               layout previews, only with --png (gitignored)
```

Page order, and the job each page does:

| Page | Job |
|---|---|
| 1 · Cover | Name, one-line pitch, scope/stack/standard facts, 3 screens, self-initiated disclosure |
| 2 · Case study | Problem → what I built → engineering decisions → tech → **what this transfers to your build** |
| 3 · Screens | Every screen in a phone frame with captions |
| 4 · Work with me | Deliverables, three engagement sizes, adjacent services, day-by-day process, CTA |

## Upwork rules this build obeys

Upwork forbids rates and off-platform contact details inside proposal attachments — an
email address, a phone number, a portfolio URL or a price in a PDF can get the proposal
removed and the account flagged. So the default build carries **no prices and no contact
details**, on any page, footers included. Tiers show scope and delivery time only, and the
closing CTA says "message me" without saying where.

```bash
python3 tools/portfolio_app_pdf.py gate --contact   # ...-contact.pdf, with prices and contact
```

Use `--contact` only off-platform: direct leads, email, your own site. Never attach a
`-contact.pdf` to an Upwork proposal.

## Regenerate

```bash
python3 tools/portfolio_app_pdf.py                 # all 9 apps
python3 tools/portfolio_app_pdf.py gate wealthkit  # named apps
python3 tools/portfolio_app_pdf.py --list          # what can be built
python3 tools/portfolio_app_pdf.py gate --png      # + page PNGs to eyeball layout
```

## Where the content comes from

**App copy is never duplicated here.** The tool parses `index.html` — eyebrow, name,
one-liner, Problem/Result, feature bullets, tech chips, screenshots and captions all come
from the site, so editing the site updates the PDFs. Only seller-side copy lives in
`profile.json`.

To change a price, a process step or an app's "what this transfers to your build"
paragraph, edit `profile.json` and re-run. To change how an app is described, edit
`index.html`.

## Rules learned

- **A4 is 1122px, not 1123.** Chromium rounds up and spills a blank fifth page.
- **`set_content` pages are `about:blank`,** so `file://` images are blocked — every
  screenshot is inlined as a data URI.
- **Downscale before embedding.** Full 786px sources at two sizes put SocialFlow past
  8 MB; 2x the render size (520px cover, 340px grid) is retina-sharp and ~1.3 MB.
- **The renderer warns on overflow but will not fix it.** `! <slug> page N overflows by
  Npx` means content is under the footer — trim copy or tighten that page's CSS.
- **Contact and price live behind `--contact`,** not in the default file. The platform-safe
  build is the one you reach for 9 times out of 10, so it is the default.
- **Page 2 slack is distributed at render time,** because apps say different amounts.
  Blocks spread up to 70px each rather than pooling a 250px hole above the last block.
