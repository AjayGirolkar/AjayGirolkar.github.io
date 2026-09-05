"""
upwork_catalog_cards.py
-----------------------
Renders Upwork Project Catalog listing images (4:3) from a JSON spec.

Upwork Project Catalog image rules this tool satisfies:
    - 4:3 aspect ratio, rendered at 2000x1500 (well above the 1000x750 recommendation,
      below the 4000x4000 max)
    - PNG, under 10 MB
    - up to 20 images per project; this tool emits 6

Raw iPhone screenshots are 9:19.5, so they cannot be uploaded directly without an
ugly crop or letterbox. Every card here composites them onto a 4:3 canvas instead.

Usage:
    python3 tools/upwork_catalog_cards.py                    # render every spec
    python3 tools/upwork_catalog_cards.py wealthkit          # render one spec
    python3 tools/upwork_catalog_cards.py wealthkit --cards hero,tiers

Requirements:
    pip install playwright && playwright install chromium

Output:
    assets/upwork/cards/{slug}/01-hero.png ... 06-fit.png
"""

import base64
import json
import sys
from functools import lru_cache
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
SPEC_DIR = ROOT / "assets" / "upwork" / "listings"
OUT_ROOT = ROOT / "assets" / "upwork" / "cards"

WIDTH, HEIGHT = 2000, 1500
PHONE_RATIO = "1179 / 2556"

# Brand tokens lifted from styles.css so cards match the portfolio site.
CSS_TOKENS = """
  --bg: #f5f6fb;
  --bg-soft: #ffffff;
  --ink: #10131a;
  --ink-soft: #3d4557;
  --ink-muted: #657087;
  --dark: #0d1117;
  --dark-soft: #141925;
  --on-dark: #f5f7fb;
  --on-dark-muted: #94a0b5;
  --accent: #1e6cff;
  --accent-soft: #6b7cff;
  --success: #0bb07b;
  --line: rgba(16, 19, 26, 0.10);
  --line-dark: rgba(255, 255, 255, 0.12);
"""

BASE_CSS = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{ {CSS_TOKENS} }}
html, body {{ width: {WIDTH}px; height: {HEIGHT}px; overflow: hidden; }}
body {{
  font-family: -apple-system, "SF Pro Display", "Helvetica Neue", system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
  color: var(--ink);
  background: var(--bg);
}}
.card {{
  width: {WIDTH}px; height: {HEIGHT}px;
  padding: 96px 110px;
  display: flex; flex-direction: column;
  position: relative; overflow: hidden;
}}
.card.dark {{
  background:
    radial-gradient(1200px 700px at 82% -10%, rgba(30,108,255,0.30), transparent 62%),
    radial-gradient(900px 620px at 6% 108%, rgba(107,124,255,0.20), transparent 60%),
    var(--dark);
  color: var(--on-dark);
}}
.card.light {{
  background:
    radial-gradient(1000px 620px at 92% -12%, rgba(30,108,255,0.10), transparent 60%),
    var(--bg);
}}
.eyebrow {{
  font-size: 30px; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--accent-soft);
}}
.card.light .eyebrow {{ color: var(--accent); }}
h1 {{ font-size: 104px; line-height: 1.03; letter-spacing: -0.035em; font-weight: 700; }}
h2 {{ font-size: 76px; line-height: 1.06; letter-spacing: -0.03em; font-weight: 700; }}
.sub {{ font-size: 36px; line-height: 1.42; font-weight: 400; color: var(--ink-soft); }}
.card.dark .sub {{ color: var(--on-dark-muted); }}
.phone {{
  aspect-ratio: {PHONE_RATIO};
  border-radius: 44px;
  border: 3px solid rgba(255,255,255,0.14);
  box-shadow: 0 40px 90px rgba(4, 8, 18, 0.45);
  object-fit: cover; display: block; background: #000;
  flex: 0 0 auto;
}}
.card.light .phone {{
  border-color: rgba(16,19,26,0.10);
  box-shadow: 0 34px 80px rgba(28, 37, 56, 0.20);
}}
.footer {{
  position: absolute; left: 110px; right: 110px; bottom: 52px;
  display: flex; justify-content: space-between; align-items: center;
  font-size: 26px; font-weight: 500; color: var(--ink-muted);
}}
.card.dark .footer {{ color: var(--on-dark-muted); }}
.footer .badge {{
  padding: 10px 24px; border-radius: 999px;
  border: 2px solid var(--line); font-weight: 600;
}}
.card.dark .footer .badge {{ border-color: var(--line-dark); }}
"""


def esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def multiline(text: str) -> str:
    return esc(text).replace("\n", "<br>")


@lru_cache(maxsize=256)
def data_uri(path: Path) -> str:
    # Pages are loaded via set_content, so their origin is about:blank and Chromium
    # blocks file:// subresources. Inline every screenshot instead.
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def phone_img(spec: dict, filename: str, style: str = "") -> str:
    path = (ROOT / spec["screens_dir"] / filename).resolve()
    if not path.exists():
        raise FileNotFoundError(f"screenshot missing: {path}")
    attr = f' style="{style}"' if style else ""
    return f'<img class="phone"{attr} src="{data_uri(path)}">'


def footer(spec: dict, badge: str = "") -> str:
    right = f'<span class="badge">{esc(badge)}</span>' if badge else "<span></span>"
    return f'<div class="footer"><span>{esc(spec["footer"])}</span>{right}</div>'


# ── Card templates ─────────────────────────────────────────────────────────────

def card_hero(spec: dict) -> str:
    offsets = ["translateY(34px)", "translateY(-38px)", "translateY(34px)"]
    phones = "".join(
        phone_img(spec, name, f"transform:{offsets[i % 3]}")
        for i, name in enumerate(spec["hero_screens"][:3])
    )
    return f"""
    <style>
      .card {{ padding: 80px; flex-direction: row; align-items: center; gap: 50px; }}
      .hero-text {{ flex: 1 1 auto; min-width: 0; }}
      .hero-text h1 {{ font-size: 72px; margin: 24px 0 26px; }}
      .hero-text .sub {{ font-size: 32px; }}
      .fan {{
        flex: 0 0 990px; display: flex; align-items: center;
        justify-content: flex-end;
      }}
      /* 400 + 2*(400-105) = 990, so the fan lands flush inside its column.
         105px overlap hides ~26% of each outer screen — enough to read, tight enough to group. */
      .fan .phone {{ width: 400px; height: auto; }}
      .fan .phone + .phone {{ margin-left: -105px; }}
      .fan .phone:nth-child(2) {{ z-index: 2; }}
    </style>
    <div class="card dark">
      <div class="hero-text">
        <div class="eyebrow">{esc(spec["eyebrow"])}</div>
        <h1>{multiline(spec["hero_headline"])}</h1>
        <p class="sub">{multiline(spec["hero_sub"])}</p>
      </div>
      <div class="fan">{phones}</div>
    </div>
    """


def card_deliverables(spec: dict) -> str:
    items = "".join(
        f'<li><span class="tick">&#10003;</span><span>{multiline(item)}</span></li>'
        for item in spec["deliverables"]
    )
    return f"""
    <style>
      .card {{ justify-content: center; }}
      h2 {{ margin-bottom: 56px; }}
      ul {{ list-style: none; columns: 2; column-gap: 90px; }}
      li {{
        break-inside: avoid; display: flex; gap: 24px; align-items: flex-start;
        font-size: 38px; line-height: 1.34; font-weight: 500;
        margin-bottom: 40px; color: var(--ink-soft);
      }}
      .tick {{
        flex: 0 0 auto; width: 52px; height: 52px; border-radius: 50%;
        background: rgba(11,176,123,0.14); color: var(--success);
        display: flex; align-items: center; justify-content: center;
        font-size: 28px; font-weight: 700;
      }}
    </style>
    <div class="card light">
      <div class="eyebrow">{esc(spec["eyebrow"])}</div>
      <h2>{multiline(spec["deliverables_title"])}</h2>
      <ul>{items}</ul>
      {footer(spec, "Fixed scope · fixed price")}
    </div>
    """


def caption_for(filename: str) -> str:
    stem = Path(filename).stem
    if "-" in stem and stem.split("-", 1)[0].isdigit():
        stem = stem.split("-", 1)[1]
    return stem.replace("-", " ").title()


def card_screens(spec: dict) -> str:
    shots = spec["grid_screens"]
    captions = spec.get("grid_captions") or [caption_for(s) for s in shots]
    gap = 22
    cells = "".join(
        f'<figure>{phone_img(spec, name)}<figcaption>{esc(cap)}</figcaption></figure>'
        for name, cap in zip(shots, captions)
    )
    return f"""
    <style>
      .card {{ padding-bottom: 130px; }}
      .strip {{
        flex: 1; display: flex; align-items: center; justify-content: center;
        gap: {gap}px; margin-top: 40px;
      }}
      .strip figure {{
        width: calc((100% - {gap * (len(shots) - 1)}px) / {len(shots)});
      }}
      .strip .phone {{ border-radius: 28px; border-width: 2px; width: 100%; height: auto; }}
      .strip figcaption {{
        margin-top: 26px; text-align: center; font-size: 26px; font-weight: 600;
        letter-spacing: 0.01em; color: var(--on-dark-muted);
      }}
    </style>
    <div class="card dark">
      <div class="eyebrow">{esc(spec["eyebrow"])}</div>
      <h2 style="margin-top:22px">{multiline(spec["grid_title"])}</h2>
      <div class="strip">{cells}</div>
      {footer(spec, "Every screen shipped, not mocked")}
    </div>
    """


def card_process(spec: dict) -> str:
    steps = "".join(
        f"""<div class="step">
              <div class="when">{esc(s["step"])}</div>
              <div class="dot"></div>
              <div class="title">{multiline(s["title"])}</div>
              <div class="body">{multiline(s["body"])}</div>
            </div>"""
        for s in spec["process"]
    )
    return f"""
    <style>
      .card {{ justify-content: center; }}
      h2 {{ margin-bottom: 80px; }}
      .rail {{ display: flex; gap: 44px; position: relative; }}
      .rail::before {{
        content: ""; position: absolute; left: 0; right: 0; top: 96px; height: 4px;
        background: linear-gradient(90deg, var(--accent), var(--accent-soft));
        opacity: 0.28;
      }}
      .step {{ flex: 1; }}
      .when {{ font-size: 30px; font-weight: 700; color: var(--accent); letter-spacing: 0.02em; }}
      .dot {{
        width: 30px; height: 30px; border-radius: 50%; background: var(--accent);
        margin: 22px 0 34px; box-shadow: 0 0 0 12px rgba(30,108,255,0.14);
      }}
      .step .title {{ font-size: 44px; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 18px; }}
      .step .body {{ font-size: 30px; line-height: 1.45; color: var(--ink-muted); font-weight: 450; }}
    </style>
    <div class="card light">
      <div class="eyebrow">{esc(spec["eyebrow"])}</div>
      <h2>{multiline(spec["process_title"])}</h2>
      <div class="rail">{steps}</div>
      {footer(spec, "Milestones you can see")}
    </div>
    """


def card_tiers(spec: dict) -> str:
    cols = ""
    for tier in spec["tiers"]:
        featured = " featured" if tier.get("featured") else ""
        ribbon = '<div class="ribbon">Most popular</div>' if tier.get("featured") else ""
        items = "".join(f"<li>{multiline(i)}</li>" for i in tier["items"])
        cols += f"""
        <div class="tier{featured}">
          {ribbon}
          <div class="name">{esc(tier["name"])}</div>
          <div class="price">{esc(tier["price"])}</div>
          <div class="delivery">{esc(tier["delivery"])}</div>
          <ul>{items}</ul>
        </div>"""
    return f"""
    <style>
      .card {{ justify-content: center; }}
      h2 {{ margin-bottom: 54px; }}
      .tiers {{ display: flex; gap: 36px; align-items: stretch; }}
      .tier {{
        flex: 1; background: var(--bg-soft); border: 3px solid var(--line);
        border-radius: 34px; padding: 46px 42px; position: relative;
      }}
      .tier.featured {{
        border-color: var(--accent);
        box-shadow: 0 34px 80px rgba(30,108,255,0.18);
      }}
      .ribbon {{
        position: absolute; top: -22px; left: 42px; background: var(--accent);
        color: #fff; font-size: 24px; font-weight: 700; letter-spacing: 0.06em;
        text-transform: uppercase; padding: 10px 22px; border-radius: 999px;
      }}
      .name {{ font-size: 34px; font-weight: 700; letter-spacing: 0.02em; color: var(--ink-muted); }}
      .price {{ font-size: 78px; font-weight: 700; letter-spacing: -0.035em; margin: 12px 0 6px; }}
      .delivery {{ font-size: 28px; font-weight: 600; color: var(--accent); margin-bottom: 32px; }}
      .tier ul {{ list-style: none; }}
      .tier li {{
        font-size: 28px; line-height: 1.4; color: var(--ink-soft);
        padding-left: 34px; margin-bottom: 20px; position: relative; font-weight: 450;
      }}
      .tier li::before {{
        content: "\\2022"; position: absolute; left: 8px; top: -2px;
        color: var(--accent); font-size: 34px;
      }}
    </style>
    <div class="card light">
      <div class="eyebrow">{esc(spec["eyebrow"])}</div>
      <h2>{multiline(spec["tiers_title"])}</h2>
      <div class="tiers">{cols}</div>
      {footer(spec, "Prices exclude Upwork fees")}
    </div>
    """


def card_fit(spec: dict) -> str:
    good = "".join(f"<li>{multiline(i)}</li>" for i in spec["fit_good"])
    bad = "".join(f"<li>{multiline(i)}</li>" for i in spec["fit_bad"])
    return f"""
    <style>
      .card {{ justify-content: center; }}
      h2 {{ margin-bottom: 56px; }}
      .split {{ display: flex; gap: 48px; align-items: stretch; }}
      .pane {{
        flex: 1; border-radius: 34px; padding: 48px 46px;
        border: 3px solid var(--line); background: var(--bg-soft);
      }}
      .pane.yes {{ border-color: rgba(11,176,123,0.45); }}
      .pane .head {{
        display: flex; align-items: center; gap: 18px;
        font-size: 38px; font-weight: 700; margin-bottom: 34px; letter-spacing: -0.01em;
      }}
      .pane .mark {{
        width: 56px; height: 56px; border-radius: 50%; display: flex;
        align-items: center; justify-content: center; font-size: 30px; font-weight: 700;
      }}
      .yes .mark {{ background: rgba(11,176,123,0.14); color: var(--success); }}
      .no  .mark {{ background: rgba(16,19,26,0.08); color: var(--ink-muted); }}
      .pane ul {{ list-style: none; }}
      .pane li {{
        font-size: 31px; line-height: 1.4; color: var(--ink-soft);
        margin-bottom: 24px; padding-left: 30px; position: relative; font-weight: 450;
      }}
      .pane li::before {{
        content: "\\2014"; position: absolute; left: 0; color: var(--ink-muted);
      }}
      .no li {{ color: var(--ink-muted); }}
    </style>
    <div class="card light">
      <div class="eyebrow">{esc(spec["eyebrow"])}</div>
      <h2>{multiline(spec["fit_title"])}</h2>
      <div class="split">
        <div class="pane yes">
          <div class="head"><span class="mark">&#10003;</span>Buy this if</div>
          <ul>{good}</ul>
        </div>
        <div class="pane no">
          <div class="head"><span class="mark">&#10005;</span>Don't buy this if</div>
          <ul>{bad}</ul>
        </div>
      </div>
      {footer(spec, "Scope stated up front")}
    </div>
    """


CARDS = {
    "hero": ("01-hero", card_hero),
    "deliverables": ("02-deliverables", card_deliverables),
    "screens": ("03-screens", card_screens),
    "process": ("04-process", card_process),
    "tiers": ("05-tiers", card_tiers),
    "fit": ("06-fit", card_fit),
}


def render(spec: dict, only: list[str] | None = None) -> list[Path]:
    out_dir = OUT_ROOT / spec["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)
    wanted = only or list(CARDS)
    written = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT})
        for key in wanted:
            if key not in CARDS:
                raise KeyError(f"unknown card '{key}'. known: {', '.join(CARDS)}")
            filename, builder = CARDS[key]
            html = f"<!doctype html><meta charset='utf-8'><style>{BASE_CSS}</style>{builder(spec)}"
            page.set_content(html)
            page.wait_for_load_state("networkidle")

            # The card is a fixed 4:3 box with overflow hidden, so anything too long is
            # silently clipped. Measure it instead of eyeballing 18 PNGs.
            overflow = page.evaluate(
                """() => {
                    const card = document.querySelector('.card');
                    return {
                        h: card.scrollHeight - card.clientHeight,
                        w: card.scrollWidth - card.clientWidth,
                    };
                }"""
            )

            target = out_dir / f"{filename}.png"
            page.screenshot(path=str(target))
            written.append(target)

            flag = ""
            if overflow["h"] > 1 or overflow["w"] > 1:
                flag = f"  ⚠ clipped by {overflow['h']}px tall / {overflow['w']}px wide"
            print(f"  ✓ {target.relative_to(ROOT)}{flag}")
        browser.close()
    return written


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    only = None
    for a in sys.argv[1:]:
        if a.startswith("--cards"):
            only = a.split("=", 1)[1].split(",") if "=" in a else None
    if "--cards" in sys.argv:
        idx = sys.argv.index("--cards")
        if idx + 1 < len(sys.argv):
            only = sys.argv[idx + 1].split(",")
            args = [a for a in args if a != sys.argv[idx + 1]]

    specs = sorted(SPEC_DIR.glob("*.json"))
    if args:
        specs = [SPEC_DIR / f"{slug}.json" for slug in args]

    if not specs:
        sys.exit(f"no specs found in {SPEC_DIR}")

    for path in specs:
        if not path.exists():
            sys.exit(f"spec not found: {path}")
        spec = json.loads(path.read_text())
        print(f"\n{spec['slug']} — {spec['title']}")
        render(spec, only)

    print(f"\nDone. Cards in {OUT_ROOT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
