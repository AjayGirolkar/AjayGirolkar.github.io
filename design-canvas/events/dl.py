#!/usr/bin/env python3
"""Wikimedia Commons search/pull with a per-item licence assert.

Why not the skill's fetch_cc0.py: Openverse (its people-photography source) was
UNREACHABLE this session -- api.openverse.org times out on connect, sandboxed and not,
while CMA and Commons both answer 200. CMA is objects, and this domain needs stages,
crowds and faces. So Commons is the fallback, and it needs its own puller because the
skill script only knows Commons for by-title lookups, not search+licence-gate.

  python3 dl.py search "rock concert stage"        # titles + licence, nothing written
  python3 dl.py pull "File:A.jpg" "File:B.jpg"     # -> src/<slug>.jpg + src/meta.json
  python3 dl.py sheet                              # contact sheet of everything in src/

NOTE: commons.wikimedia.org is blocked by the Bash sandbox. Run every command here with
dangerouslyDisableSandbox, or it fails with a bare connect timeout that looks like an outage.
"""
import json, os, re, subprocess, sys, urllib.parse

UA = "design-canvas/1.0 (portfolio mockup; educational use)"
API = "https://commons.wikimedia.org/w/api.php?"
# Only licences that need no permission to reproduce. CC-BY* is allowed but recorded so
# the canvas can carry the credit line; anything else is refused outright.
OK = re.compile(r"(cc0|public domain|cc[- ]by)", re.I)


def _curl(url, path=None):
    """curl, not urllib. urllib's TLS handshake to Commons is RESET on this machine while
    curl to the same host returns 200 -- a proxy/TLS difference, not an outage. Cost 20 min."""
    # -4 and the retry block are load-bearing: TLS to Commons from here resets at random,
    # roughly 2 calls in 3, and the failure surfaces as curl exit 35 / HTTP 000.
    cmd = ["curl", "-sSL", "-4", "-m", "180", "--retry", "8", "--retry-all-errors",
           "--retry-delay", "2", "-A", UA, url]
    if path:
        subprocess.run(cmd + ["-o", path], check=True)
        return path
    return subprocess.run(cmd, check=True, capture_output=True).stdout


def _get(params):
    return json.loads(_curl(API + urllib.parse.urlencode(dict(params, format="json"))))


def _meta(p):
    ii = (p.get("imageinfo") or [{}])[0]
    ex = ii.get("extmetadata") or {}
    g = lambda k: re.sub(r"<[^>]+>", "", (ex.get(k) or {}).get("value", "") or "").strip()
    return dict(title=p["title"], licence=g("LicenseShortName") or g("License"),
                author=g("Artist"), credit=g("Credit"), desc=g("ImageDescription")[:120],
                url=ii.get("url"), thumb=ii.get("thumburl"),
                w=ii.get("width"), h=ii.get("height"),
                page="https://commons.wikimedia.org/wiki/" + urllib.parse.quote(p["title"]))


def search(term, limit=24):
    d = _get(dict(action="query", generator="search", gsrsearch=f'filetype:bitmap {term}',
                  gsrnamespace=6, gsrlimit=limit, prop="imageinfo",
                  iiprop="url|extmetadata|size", iiurlwidth=400))
    for p in (d.get("query", {}).get("pages") or {}).values():
        yield _meta(p)


def pull(titles, out="src", width=1600):
    os.makedirs(out, exist_ok=True)
    d = _get(dict(action="query", titles="|".join(titles), prop="imageinfo",
                  iiprop="url|extmetadata|size", iiurlwidth=width))
    meta = json.load(open(f"{out}/meta.json")) if os.path.exists(f"{out}/meta.json") else {}
    for p in (d.get("query", {}).get("pages") or {}).values():
        m = _meta(p)
        # the assert: provenance, not a hopeful comment
        assert OK.search(m["licence"] or ""), f"REFUSED {m['title']}: licence={m['licence']!r}"
        slug = re.sub(r"[^a-z0-9]+", "-", m["title"][5:].rsplit(".", 1)[0].lower()).strip("-")[:44]
        path = f"{out}/{slug}.jpg"
        _curl(m["thumb"] or m["url"], path)
        meta[slug] = dict(m, file=path)
        print(f"ok  {slug:46s} {m['licence'][:24]:24s} {os.path.getsize(path)//1024}KB")
    json.dump(meta, open(f"{out}/meta.json", "w"), indent=1)


def sheet(out="src", path="_sheet.png", cols=6, cell=260):
    from PIL import Image, ImageDraw
    meta = json.load(open(f"{out}/meta.json"))
    keys = sorted(meta)
    rows = (len(keys) + cols - 1) // cols
    sh = Image.new("RGB", (cols * cell, rows * (cell + 18)), "#111")
    d = ImageDraw.Draw(sh)
    for i, k in enumerate(keys):
        im = Image.open(meta[k]["file"]).convert("RGB")
        s = cell / min(im.size)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        im = im.crop(((im.width - cell) // 2, (im.height - cell) // 2,
                      (im.width - cell) // 2 + cell, (im.height - cell) // 2 + cell))
        x, y = (i % cols) * cell, (i // cols) * (cell + 18)
        sh.paste(im, (x, y))
        d.text((x + 4, y + cell + 3), k[:40], fill="#bbb")
    sh.save(path)
    print("sheet", path, len(keys), "frames")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "search":
        for t in sys.argv[2:]:
            print(f"\n===== {t} =====")
            for m in search(t):
                print(f"  {(m['licence'] or '?')[:22]:22s} {m['w']}x{m['h']:<6} {m['title'][5:80]}")
    elif cmd == "pull":
        pull(sys.argv[2:])
    elif cmd == "sheet":
        sheet()
