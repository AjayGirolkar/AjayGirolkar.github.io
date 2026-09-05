"""
portfolio_app_pdf.py
--------------------
Renders a client-facing PDF case study for each demo app in the portfolio.

The PDF is the attachment that goes on an Upwork proposal: cover, case study,
every screen, and a hire page with contact details. A4 portrait, 4 pages.

Content is NOT duplicated in a per-app spec. Everything app-specific is parsed
out of index.html (the site is the single source of truth for app copy) and
merged with the shared seller copy in assets/portfolio-pdf/profile.json.

Usage:
    python3 tools/portfolio_app_pdf.py                 # every app
    python3 tools/portfolio_app_pdf.py gate wealthkit  # named apps
    python3 tools/portfolio_app_pdf.py --list          # what can be built
    python3 tools/portfolio_app_pdf.py gate --png      # + page PNGs, to eyeball layout
    python3 tools/portfolio_app_pdf.py gate --contact  # off-platform copy: prices + contact

Upwork forbids rates and off-platform contact details in proposal attachments, so the
default build carries neither. --contact adds both back for direct leads and email.

Requirements:
    pip install playwright beautifulsoup4 && playwright install chromium

Output:
    assets/portfolio-pdf/AjayGirolkar-<App>-iOS-case-study.pdf
"""

import base64
import json
import mimetypes
import re
import sys
from functools import lru_cache
from io import BytesIO
from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
SITE = ROOT / "index.html"
OUT_DIR = ROOT / "assets" / "portfolio-pdf"
PROFILE = OUT_DIR / "profile.json"

# A4 portrait at 96dpi. 1122 not 1123: Chromium rounds up and a 1123px page
# spills one pixel onto a blank fifth sheet.
PAGE_W, PAGE_H = 794, 1122
PHONE_RATIO = "1179 / 2556"


# ── Source data ────────────────────────────────────────────────────────────────

def parse_apps() -> dict:
    """Pull every app's copy out of the portfolio site."""
    soup = BeautifulSoup(SITE.read_text(), "html.parser")

    lines = {
        card["data-app"]: text(card.select_one(".work-card-line"))
        for card in soup.select("button.work-card")
    }

    apps = {}
    for demo in soup.select("div.app-demo"):
        slug = demo["data-app"]
        scara = [p for p in demo.select(".app-scara p")]
        apps[slug] = {
            "slug": slug,
            "name": text(demo.select_one(".app-demo-title h3")),
            "eyebrow": text(demo.select_one(".app-demo-title .eyebrow")),
            "line": lines.get(slug, ""),
            "problem": labelled(scara, "Problem"),
            "result": labelled(scara, "Result"),
            "features": [text(li) for li in demo.select("ul.app-features li")],
            "tech": [text(s) for s in demo.select(".app-tech span")],
            "screens": [
                {
                    "src": fig.select_one("img")["src"],
                    "caption": text(fig.select_one("figcaption")),
                }
                for fig in demo.select("figure.screen-shot")
            ],
        }
    return apps


def text(node) -> str:
    if not node:
        return ""
    for sup in node.select("sup"):
        # get_text() would flatten "saturation^1.5" into "saturation 1.5"
        sup.replace_with(f"^{sup.get_text(strip=True)}")
    joined = re.sub(r"\s+", " ", node.get_text(" ", strip=True))
    return re.sub(r"\s+([.,;:)])", r"\1", joined)


def labelled(paras, label: str) -> str:
    """The site writes '<strong>Problem:</strong> …' — return the body only."""
    for p in paras:
        strong = p.select_one("strong")
        if strong and strong.get_text(strip=True).rstrip(":").lower() == label.lower():
            strong.extract()
            return text(p).lstrip(": ").strip()
    return ""


# Screens render at 246px (cover) and ~160px (grid). Embedding the full 786px
# source at both sizes pushed one PDF past 8MB; 2x the render size is retina-sharp
# in print and roughly a quarter of the bytes.
@lru_cache(maxsize=512)
def screen_uri(rel: str, width: int) -> str:
    path = (ROOT / rel).resolve()
    if not path.exists():
        raise FileNotFoundError(f"asset missing: {path}")
    img = Image.open(path).convert("RGB")
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=86, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


@lru_cache(maxsize=256)
def data_uri(rel: str) -> str:
    # set_content pages have an about:blank origin, so Chromium refuses file://
    # subresources. Every image has to be inlined.
    path = (ROOT / rel).resolve()
    if not path.exists():
        raise FileNotFoundError(f"asset missing: {path}")
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def esc(value) -> str:
    return (
        str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )


# ── Styles ─────────────────────────────────────────────────────────────────────

CSS = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
@page {{ size: A4; margin: 0; }}
:root {{
  --bg: #f5f6fb;
  --paper: #ffffff;
  --ink: #10131a;
  --ink-soft: #3d4557;
  --ink-muted: #657087;
  --dark: #0d1117;
  --on-dark: #f5f7fb;
  --on-dark-muted: #94a0b5;
  --accent: #1e6cff;
  --accent-soft: #6b7cff;
  --success: #0bb07b;
  --line: rgba(16, 19, 26, 0.10);
  --line-dark: rgba(255, 255, 255, 0.13);
}}
html, body {{ width: {PAGE_W}px; background: #fff; }}
body {{
  font-family: -apple-system, "SF Pro Text", "SF Pro Display", "Helvetica Neue", system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
  color: var(--ink);
  font-size: 12px;
  line-height: 1.5;
}}
.page {{
  width: {PAGE_W}px; height: {PAGE_H}px;
  position: relative; overflow: hidden;
  page-break-after: always; break-after: page;
  padding: 54px 56px 62px;
  display: flex; flex-direction: column;
  background: var(--bg);
}}
.page:last-child {{ page-break-after: auto; break-after: auto; }}
.page.dark {{
  background:
    radial-gradient(760px 460px at 84% -8%, rgba(30,108,255,0.34), transparent 62%),
    radial-gradient(620px 420px at 2% 104%, rgba(107,124,255,0.22), transparent 60%),
    var(--dark);
  color: var(--on-dark);
}}
.page.light {{
  background:
    radial-gradient(620px 380px at 96% -10%, rgba(30,108,255,0.09), transparent 62%),
    var(--bg);
}}

.eyebrow {{
  font-size: 10px; font-weight: 700; letter-spacing: 0.18em;
  text-transform: uppercase; color: var(--accent);
}}
.page.dark .eyebrow {{ color: var(--accent-soft); }}
h1 {{ font-size: 62px; line-height: 1.02; letter-spacing: -0.035em; font-weight: 700; }}
h2 {{ font-size: 27px; line-height: 1.12; letter-spacing: -0.025em; font-weight: 700; }}
h3 {{ font-size: 14px; letter-spacing: -0.01em; font-weight: 700; }}
p {{ color: var(--ink-soft); }}
.page.dark p {{ color: var(--on-dark-muted); }}
strong {{ color: var(--ink); font-weight: 650; }}
.page.dark strong {{ color: var(--on-dark); }}

/* running head + foot ------------------------------------------------------ */
.runhead {{
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10.5px; font-weight: 600; color: var(--ink-muted);
  padding-bottom: 14px; border-bottom: 1px solid var(--line);
  margin-bottom: 26px; flex: 0 0 auto;
}}
.page.dark .runhead {{ color: var(--on-dark-muted); border-color: var(--line-dark); }}
.runhead .who {{ color: var(--ink); font-weight: 700; letter-spacing: -0.01em; }}
.page.dark .runhead .who {{ color: var(--on-dark); }}
.runfoot {{
  position: absolute; left: 56px; right: 56px; bottom: 26px;
  display: flex; justify-content: space-between; align-items: center;
  font-size: 9.5px; color: var(--ink-muted);
  padding-top: 12px; border-top: 1px solid var(--line);
}}
.page.dark .runfoot {{ color: var(--on-dark-muted); border-color: var(--line-dark); }}
.runfoot a {{ color: inherit; text-decoration: none; }}

/* phones -------------------------------------------------------------------- */
.phone {{
  aspect-ratio: {PHONE_RATIO};
  border-radius: 18px; border: 1.5px solid rgba(255,255,255,0.16);
  box-shadow: 0 22px 44px rgba(4, 8, 18, 0.42);
  object-fit: cover; display: block; background: #000;
}}
.light .phone, .paper .phone {{
  border-color: rgba(16,19,26,0.12);
  box-shadow: 0 14px 30px rgba(28, 37, 56, 0.16);
}}

/* cover --------------------------------------------------------------------- */
.cover-body {{ flex: 1 1 auto; display: flex; flex-direction: column; }}
.cover-body h1 {{ margin: 12px 0 14px; }}
.cover-body h1.long {{ font-size: 46px; }}
.cover-facts {{ display: flex; gap: 10px; margin-top: 26px; }}
.cover-facts .f {{
  flex: 1; border: 1px solid var(--line-dark); border-radius: 12px;
  padding: 12px 14px; background: rgba(255,255,255,0.05);
}}
.cover-facts .f .k {{
  font-size: 9px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--accent-soft);
}}
.cover-facts .f .v {{ font-size: 12.5px; font-weight: 600; margin-top: 5px; line-height: 1.35; }}
.cover-lead {{ font-size: 15px; line-height: 1.5; max-width: 600px; }}
.fan {{
  margin-top: auto; margin-bottom: 22px;
  display: flex; justify-content: center; align-items: center;
}}
.fan .phone {{ width: 246px; height: auto; }}
.fan .phone + .phone {{ margin-left: -72px; }}
.fan .phone:nth-child(2) {{ z-index: 2; transform: translateY(-16px); }}
.fan .phone:nth-child(1), .fan .phone:nth-child(3) {{ transform: translateY(14px); }}
.cover-strip {{
  display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px;
}}
.chip {{
  font-size: 10px; font-weight: 600; letter-spacing: 0.01em;
  padding: 6px 12px; border-radius: 999px;
  border: 1px solid var(--line); color: var(--ink-soft); background: rgba(255,255,255,0.6);
}}
.page.dark .chip {{
  border-color: var(--line-dark); color: var(--on-dark);
  background: rgba(255,255,255,0.06);
}}
.disclosure {{
  font-size: 9.5px; line-height: 1.45; color: var(--ink-muted);
  border-left: 2px solid var(--accent); padding-left: 12px; max-width: 560px;
}}
.page.dark .disclosure {{ color: var(--on-dark-muted); border-color: var(--accent-soft); }}

/* stats --------------------------------------------------------------------- */
.stats {{ display: flex; gap: 10px; }}
.stat {{
  flex: 1; background: var(--paper); border: 1px solid var(--line);
  border-radius: 12px; padding: 12px 13px;
}}
.stat .v {{ font-size: 19px; font-weight: 700; letter-spacing: -0.03em; }}
.stat .l {{ font-size: 9.5px; color: var(--ink-muted); margin-top: 2px; line-height: 1.3; }}

/* case study ---------------------------------------------------------------- */
.split {{ display: flex; gap: 16px; }}
.block {{
  flex: 1; background: var(--paper); border: 1px solid var(--line);
  border-radius: 14px; padding: 18px 19px;
}}
.block.accent {{
  background: linear-gradient(160deg, rgba(30,108,255,0.07), rgba(107,124,255,0.04));
  border-color: rgba(30,108,255,0.22);
}}
.block h3 {{ margin-bottom: 8px; display: flex; align-items: center; gap: 7px; }}
.block h3 .dot {{
  width: 7px; height: 7px; border-radius: 50%; background: var(--ink-muted);
}}
.block.accent h3 .dot {{ background: var(--accent); }}
.block p {{ font-size: 11.5px; line-height: 1.55; }}
.block.transfer {{ flex: 0 0 auto; }}
.page.spread > * {{ flex: 0 0 auto; }}
.page.spread > * + * {{ margin-top: 18px; }}
.sec {{ flex: 0 0 auto; }}

.section-title {{
  display: flex; align-items: baseline; gap: 10px; margin-bottom: 14px;
}}
.section-title .n {{
  font-size: 10px; font-weight: 700; color: var(--accent); letter-spacing: 0.12em;
}}

ul.ticks {{ list-style: none; }}
ul.ticks li {{
  display: flex; gap: 10px; align-items: flex-start;
  font-size: 11.5px; line-height: 1.5; color: var(--ink-soft);
  padding: 7px 0; border-bottom: 1px solid var(--line);
}}
ul.ticks li:last-child {{ border-bottom: 0; }}
ul.ticks .tick {{
  flex: 0 0 auto; width: 16px; height: 16px; border-radius: 50%; margin-top: 1px;
  background: rgba(11,176,123,0.14); color: var(--success);
  display: flex; align-items: center; justify-content: center;
  font-size: 9px; font-weight: 800;
}}
ul.ticks.blue .tick {{ background: rgba(30,108,255,0.13); color: var(--accent); }}

.tech {{ display: flex; flex-wrap: wrap; gap: 7px; margin-top: 16px; }}
.tech span {{
  font-size: 10px; font-weight: 600; padding: 5px 11px; border-radius: 999px;
  background: rgba(16,19,26,0.05); border: 1px solid var(--line); color: var(--ink-soft);
}}

/* screen grid --------------------------------------------------------------- */
.grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px 14px; }}
.grid figure .phone {{ width: 100%; height: auto; }}
.grid figcaption {{
  font-size: 9.5px; line-height: 1.35; color: var(--ink-muted);
  margin-top: 8px; text-align: center;
}}

/* hire page ----------------------------------------------------------------- */
.tiers {{ display: flex; gap: 12px; margin-bottom: 18px; }}
.tier {{
  flex: 1; border: 1px solid var(--line); border-radius: 14px;
  padding: 13px 14px 14px; background: var(--paper); position: relative;
}}
.tier.featured {{ border-color: var(--accent); box-shadow: 0 10px 26px rgba(30,108,255,0.13); }}
.tier .ribbon {{
  position: absolute; top: -9px; left: 15px; font-size: 8.5px; font-weight: 700;
  letter-spacing: 0.1em; text-transform: uppercase; color: #fff;
  background: var(--accent); padding: 3px 9px; border-radius: 999px;
}}
.tier .price {{ font-size: 20px; font-weight: 700; letter-spacing: -0.03em; margin-top: 6px; }}
.tier .scope {{
  font-size: 12.5px; font-weight: 650; color: var(--accent);
  margin-top: 6px; line-height: 1.3;
}}
.tier .delivery {{ font-size: 9.5px; color: var(--ink-muted); margin-bottom: 8px; }}
.tier p {{ font-size: 10.5px; line-height: 1.45; }}

.also {{ columns: 2; column-gap: 26px; list-style: none; margin-bottom: 4px; }}
.also li {{
  break-inside: avoid; font-size: 11px; line-height: 1.45; color: var(--ink-soft);
  padding-left: 14px; margin-bottom: 8px; position: relative;
}}
.also li::before {{
  content: ""; position: absolute; left: 0; top: 7px;
  width: 5px; height: 5px; border-radius: 50%; background: var(--accent);
}}

.steps {{ display: flex; gap: 10px; margin-bottom: 20px; }}
.step {{
  flex: 1; border-top: 2px solid var(--accent); padding-top: 10px;
}}
.step .k {{
  font-size: 9px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--accent); margin-bottom: 3px;
}}
.step h3 {{ font-size: 12px; margin-bottom: 4px; }}
.step p {{ font-size: 10px; line-height: 1.4; }}

.cta {{
  margin-top: auto; border-radius: 16px; padding: 19px 22px;
  background:
    radial-gradient(420px 260px at 88% -30%, rgba(30,108,255,0.42), transparent 64%),
    var(--dark);
  color: var(--on-dark);
  display: flex; gap: 20px; align-items: center;
}}
.cta .who-shot {{
  flex: 0 0 auto; width: 72px; height: 72px; border-radius: 50%;
  object-fit: cover; border: 2px solid rgba(255,255,255,0.22);
}}
.cta h2 {{ font-size: 19px; margin-bottom: 6px; }}
.cta p {{ font-size: 11px; color: var(--on-dark-muted); line-height: 1.5; }}
.contact {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }}
.contact a {{
  font-size: 10.5px; font-weight: 650; text-decoration: none; color: var(--on-dark);
  border: 1px solid var(--line-dark); border-radius: 999px; padding: 6px 12px;
  background: rgba(255,255,255,0.07);
}}
.contact a.primary {{ background: var(--accent); border-color: var(--accent); color: #fff; }}
"""


# ── Pages ──────────────────────────────────────────────────────────────────────

def runhead(app: dict, profile: dict, right: str) -> str:
    return f"""
    <div class="runhead">
      <span class="who">{esc(profile['name'])} · {esc(profile['role'])}</span>
      <span>{esc(app['name'])} — {esc(right)}</span>
    </div>"""


def runfoot(app: dict, profile: dict, page: int, total: int) -> str:
    return f"""
    <div class="runfoot">
      <span>{esc(profile['name'])} · {esc(profile['role'])} · {esc(profile['years'])}</span>
      <span>{esc(app['name'])} · iOS case study · {page} / {total}</span>
    </div>"""


def page_cover(app: dict, profile: dict, total: int) -> str:
    picks = pick_hero(app)
    phones = "".join(f'<img class="phone" src="{screen_uri(s["src"], 520)}">' for s in picks)
    chips = "".join(f"<span class='chip'>{esc(t)}</span>" for t in app["tech"][:5])
    facts = [
        ("Scope", f"{len(app['screens'])} screens, built and shot on device"),
        ("Stack", "SwiftUI · Swift 6 · async/await · iOS 26"),
        ("Standard", "Light + dark · Dynamic Type · VoiceOver"),
    ]
    fact_html = "".join(
        f"<div class='f'><div class='k'>{esc(k)}</div><div class='v'>{esc(v)}</div></div>"
        for k, v in facts
    )
    long = " long" if len(app["name"]) > 10 else ""
    return f"""
    <div class="page dark">
      <div class="runhead">
        <span class="who">{esc(profile['name'])} · {esc(profile['role'])}</span>
        <span>iOS case study · {esc(profile['location'])}</span>
      </div>
      <div class="cover-body">
        <div class="eyebrow">{esc(app['eyebrow'])}</div>
        <h1 class="{long.strip()}">{esc(app['name'])}</h1>
        <p class="cover-lead">{esc(app['line'])}</p>
        <div class="cover-facts">{fact_html}</div>
        <div class="fan">{phones}</div>
        <div class="cover-strip">{chips}</div>
        <p class="disclosure">{esc(profile['disclosure'])}</p>
      </div>
      {runfoot(app, profile, 1, total)}
    </div>"""


def page_case(app: dict, profile: dict, total: int) -> str:
    stats = list(profile["stats"])
    stats[3] = {"value": str(len(app["screens"])), "label": "Screens in this build"}
    tiles = "".join(
        f"<div class='stat'><div class='v'>{esc(s['value'])}</div>"
        f"<div class='l'>{esc(s['label'])}</div></div>"
        for s in stats
    )
    feats = "".join(
        f"<li><span class='tick'>&#10003;</span><span>{esc(f)}</span></li>"
        for f in app["features"]
    )
    tech = "".join(f"<span>{esc(t)}</span>" for t in app["tech"])
    transfer = (
        profile.get("apps", {}).get(app["slug"], {}).get("transfer")
        or profile["transfer_fallback"]
    )
    return f"""
    <div class="page light spread">
      {runhead(app, profile, "Case study")}
      <div class="stats">{tiles}</div>
      <div class="split">
        <div class="block">
          <h3><span class="dot"></span>The problem</h3>
          <p>{esc(app['problem'])}</p>
        </div>
        <div class="block accent">
          <h3><span class="dot"></span>What I built</h3>
          <p>{esc(app['result'])}</p>
        </div>
      </div>
      <div class="sec">
        <div class="section-title">
          <span class="n">02</span><h2>Engineering decisions</h2>
        </div>
        <ul class="ticks blue">{feats}</ul>
        <div class="tech">{tech}</div>
      </div>
      <div class="block accent transfer">
        <h3><span class="dot"></span>{esc(profile['transfer_title'])}</h3>
        <p>{esc(transfer)}</p>
      </div>
      {runfoot(app, profile, 2, total)}
    </div>"""


def page_screens(app: dict, profile: dict, total: int) -> str:
    cells = "".join(
        f'<figure><img class="phone" src="{screen_uri(s["src"], 340)}">'
        f"<figcaption>{esc(s['caption'])}</figcaption></figure>"
        for s in app["screens"][:8]
    )
    return f"""
    <div class="page light paper">
      {runhead(app, profile, "Screens")}
      <div class="section-title">
        <span class="n">03</span><h2>Every screen, shipped</h2>
      </div>
      <p style="font-size:11.5px;margin-bottom:20px;max-width:640px;">
        {len(app['screens'])} screens, built in SwiftUI and captured on device. Light and dark,
        Dynamic Type and VoiceOver labels are wired on each one.
      </p>
      <div class="grid">{cells}</div>
      {runfoot(app, profile, 3, total)}
    </div>"""


def page_hire(app: dict, profile: dict, total: int, contact: bool = False) -> str:
    proof = "".join(
        f"<li><span class='tick'>&#10003;</span><span>{esc(p)}</span></li>"
        for p in profile["proof"][:4]
    )
    tiers = "".join(
        f"<div class='tier{' featured' if t.get('featured') else ''}'>"
        f"{'<span class=ribbon>Most picked</span>' if t.get('featured') else ''}"
        f"<h3>{esc(t['name'])}</h3>"
        + (f"<div class='price'>{esc(t['price'])}</div>" if contact else
           f"<div class='scope'>{esc(t['scope'])}</div>")
        + f"<div class='delivery'>{esc(t['delivery'])}</div>"
        f"<p>{esc(t['body'])}</p></div>"
        for t in profile["services"]
    )
    also = "".join(f"<li>{esc(a)}</li>" for a in profile["also"])
    steps = "".join(
        f"<div class='step'><div class='k'>{esc(st['step'])}</div>"
        f"<h3>{esc(st['title'])}</h3><p>{esc(st['body'])}</p></div>"
        for st in profile["process"]
    )
    if contact:
        wa_digits = re.sub(r"\D", "", profile["whatsapp"])
        cta_links = f"""
          <div class="contact">
            <a class="primary" href="mailto:{esc(profile['email'])}?subject=iOS%20project">{esc(profile['email'])}</a>
            <a href="https://wa.me/{wa_digits}">WhatsApp {esc(profile['whatsapp'])}</a>
            <a href="{esc(profile['site_url'])}">Portfolio</a>
            <a href="https://{esc(profile['linkedin'])}">LinkedIn</a>
          </div>"""
        cta_body = profile["cta_body"]
    else:
        cta_links = ""
        cta_body = profile["cta_body_platform"]
    return f"""
    <div class="page light">
      {runhead(app, profile, "Work with me")}
      <div class="section-title">
        <span class="n">04</span><h2>{esc(profile['proof_title'])}</h2>
      </div>
      <ul class="ticks" style="margin-bottom:18px;">{proof}</ul>
      <div class="section-title"><span class="n">05</span><h2>{esc(profile['services_title'])}</h2></div>
      <div class="tiers">{tiers}</div>
      <div class="section-title"><span class="n">06</span><h2>{esc(profile['also_title'])}</h2></div>
      <ul class="also">{also}</ul>
      <div class="section-title" style="margin-top:16px;">
        <span class="n">07</span><h2>{esc(profile['process_title'])}</h2>
      </div>
      <div class="steps">{steps}</div>
      <div class="cta">
        <img class="who-shot" src="{data_uri(profile['profile_image'])}">
        <div>
          <h2>{esc(profile['cta_title'])}</h2>
          <p>{esc(cta_body)}</p>{cta_links}
        </div>
      </div>
      {runfoot(app, profile, 4, total)}
    </div>"""


def pick_hero(app: dict) -> list:
    """Three screens for the cover fan, strongest in the middle."""
    shots = app["screens"]
    if len(shots) >= 3:
        return [shots[1], shots[0], shots[2]]
    return shots


def document(app: dict, profile: dict, contact: bool = False) -> str:
    total = 4
    pages = (
        page_cover(app, profile, total)
        + page_case(app, profile, total)
        + page_screens(app, profile, total)
        + page_hire(app, profile, total, contact)
    )
    return f"<!doctype html><meta charset='utf-8'><style>{CSS}</style>{pages}"


# ── Render ─────────────────────────────────────────────────────────────────────

# Apps say different amounts, so page 2 ends up with anywhere from 0 to ~250px of
# slack. Pool it all at the bottom and the page reads unfinished; this spreads it
# between the blocks, capped so a thin page does not turn into a sparse one.
DISTRIBUTE = """
() => {
  document.querySelectorAll('.page.spread').forEach(page => {
    const foot = page.querySelector('.runfoot');
    const kids = [...page.children].filter(c => c !== foot);
    const last = kids[kids.length - 1];
    const slack = foot.offsetTop - (last.offsetTop + last.offsetHeight) - 20;
    const gaps = kids.length - 2;
    if (slack <= 0 || gaps <= 0) return;
    const add = Math.min(70, slack / gaps);
    kids.slice(2).forEach(k => {
      k.style.marginTop = (parseFloat(getComputedStyle(k).marginTop) + add) + 'px';
    });
  });
}
"""

OVERFLOW_PROBE = """
() => [...document.querySelectorAll('.page')].map((p, i) => {
  const foot = p.querySelector('.runfoot');
  const limit = foot ? foot.getBoundingClientRect().top - p.getBoundingClientRect().top : p.clientHeight;
  const content = [...p.children].filter(c => !c.classList.contains('runfoot'));
  const bottom = Math.max(...content.map(c => c.offsetTop + c.offsetHeight));
  return { page: i + 1, overflow: Math.round(bottom - limit) };
})
"""


def render(slugs, apps: dict, profile: dict, png: bool = False, contact: bool = False) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": PAGE_W, "height": PAGE_H})
        for slug in slugs:
            app = apps[slug]
            page.set_content(document(app, profile, contact), wait_until="load")
            page.emulate_media(media="print")
            page.evaluate(DISTRIBUTE)

            for probe in page.evaluate(OVERFLOW_PROBE):
                if probe["overflow"] > 0:
                    print(f"  ! {slug} page {probe['page']} overflows by {probe['overflow']}px")

            suffix = "-contact" if contact else ""
            out = OUT_DIR / f"AjayGirolkar-{app['name']}-iOS-case-study{suffix}.pdf"
            page.pdf(
                path=str(out),
                width=f"{PAGE_W}px",
                height=f"{PAGE_H}px",
                print_background=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            )
            size = out.stat().st_size / 1024
            print(f"  {out.relative_to(ROOT)}  ({size:.0f} KB)")

            if png:
                shots = OUT_DIR / "_preview" / slug
                shots.mkdir(parents=True, exist_ok=True)
                for i, el in enumerate(page.query_selector_all(".page"), start=1):
                    el.screenshot(path=str(shots / f"page-{i}.png"))
                print(f"  {shots.relative_to(ROOT)}/page-*.png")
        browser.close()


def main() -> None:
    apps = parse_apps()
    args = [a for a in sys.argv[1:] if not a.startswith("-")]

    if "--list" in sys.argv:
        for slug, app in apps.items():
            print(f"{slug:16} {app['name']:16} {len(app['screens'])} screens")
        return

    unknown = [a for a in args if a not in apps]
    if unknown:
        sys.exit(f"unknown app(s): {', '.join(unknown)}. Try --list")

    profile = json.loads(PROFILE.read_text())
    slugs = args or list(apps)
    print(f"Rendering {len(slugs)} PDF case stud{'y' if len(slugs) == 1 else 'ies'}…")
    render(
        slugs, apps, profile,
        png="--png" in sys.argv,
        contact="--contact" in sys.argv,
    )


if __name__ == "__main__":
    main()
