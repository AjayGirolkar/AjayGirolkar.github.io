# Upwork Project Catalog assets

Everything needed to publish a fixed-price listing on Upwork's Project Catalog.

```
listings/<slug>.json   spec — feeds the card renderer
listings/<slug>.md     paste-ready copy for the Upwork form
cards/<slug>/*.png     6 gallery images, 2000×1500 (4:3), upload in filename order
```

Regenerate cards:

```bash
python3 tools/upwork_catalog_cards.py            # every listing
python3 tools/upwork_catalog_cards.py wealthkit  # one listing
```

Full procedure, platform limits and upload steps: [`workflows/upwork_project_catalog.md`](../../workflows/upwork_project_catalog.md)

## Live listings

| Slug | Listing | Status |
|---|---|---|
| `wealthkit` | Fintech / investment iOS app in SwiftUI | ready to publish |
| `nativeaistudio` | AI chat feature in an iOS app (Claude / GPT) | ready to publish |
| `shopease` | E-commerce iOS app in SwiftUI | ready to publish |

Six more demo apps are waiting on specs: `fitnesspro`, `socialflow`, `gate`, `nocturne`,
`lingo`, `wayfare`. Publish the three above first and clone whichever format ranks.
