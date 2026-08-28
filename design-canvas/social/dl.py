#!/usr/bin/env python3
"""Openverse CC0 pull for SocialFlow.

fetch_cc0.py cannot `pull` from Openverse (no by-id endpoint), so this keeps the same
contract locally: search -> assert the licence field per item -> download -> meta.json.
Openverse quality varies wildly, so everything lands in a labelled contact sheet
(`python3 dl.py sheet`) and nothing is chosen without looking at it.

    python3 dl.py search "street portrait,friends laughing"   # print candidates
    python3 dl.py grab   "street portrait" 12                 # download a term
    python3 dl.py sheet                                       # contact sheet -> src/_sheet.png
"""
import json, os, sys, urllib.request, urllib.parse
from PIL import Image, ImageDraw

UA = "design-canvas/1.0 (portfolio mockup; educational use)"
SRC = "src"


def _get(url):
    return json.load(urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": UA}), timeout=45))


def search(term, limit=20):
    d = _get("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(
        dict(q=term, license="cc0", page_size=limit, mature="false")))
    for a in d["results"]:
        yield dict(id=a["id"], title=a.get("title") or "untitled",
                   creator=a.get("creator") or "", licence=a["license"].upper(),
                   source=a.get("source") or "", img=a["url"],
                   w=a.get("width"), h=a.get("height"),
                   page=a.get("foreign_landing_url"), term=term)


def grab(term, limit=12):
    os.makedirs(SRC, exist_ok=True)
    meta = json.load(open(f"{SRC}/meta.json")) if os.path.exists(f"{SRC}/meta.json") else {}
    for m in search(term, limit):
        assert m["licence"] == "CC0", f"{m['id']}: licence {m['licence']}"
        p = f"{SRC}/{m['id']}.jpg"
        if not os.path.exists(p):
            try:
                with urllib.request.urlopen(urllib.request.Request(
                        m["img"], headers={"User-Agent": UA}), timeout=90) as r:
                    open(p, "wb").write(r.read())
                Image.open(p).verify()           # refuse anything that is not a real image
            except Exception as e:
                if os.path.exists(p):
                    os.remove(p)
                print("  skip", m["id"], type(e).__name__)
                continue
        meta[m["id"]] = {k: v for k, v in m.items() if k != "img"}
        print(" ", m["id"], m["title"][:52])
    json.dump(meta, open(f"{SRC}/meta.json", "w"), indent=1)
    print(f"{len(meta)} files in {SRC}/")


def sheet(cols=6, cell=260):
    meta = json.load(open(f"{SRC}/meta.json"))
    ids = [i for i in sorted(meta) if os.path.exists(f"{SRC}/{i}.jpg")]
    rows = (len(ids) + cols - 1) // cols
    out = Image.new("RGB", (cols * cell, rows * (cell + 22)), "#111")
    d = ImageDraw.Draw(out)
    for n, i in enumerate(ids):
        x, y = (n % cols) * cell, (n // cols) * (cell + 22)
        try:
            im = Image.open(f"{SRC}/{i}.jpg").convert("RGB")
        except Exception:
            continue
        im.thumbnail((cell - 8, cell - 8))
        out.paste(im, (x + 4, y + 4))
        lab = f"{n:02d} {meta[i]['title'][:26]}".encode("latin-1", "replace").decode("latin-1")
        d.text((x + 5, y + cell + 4), lab, fill="#bbb")
    out.save(f"{SRC}/_sheet.png")
    print(f"{len(ids)} -> {SRC}/_sheet.png")
    for n, i in enumerate(ids):
        print(n, i, meta[i]["term"], "|", meta[i]["title"][:44])


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "search":
        for t in sys.argv[2].split(","):
            print(f"\n===== {t} =====")
            for m in search(t.strip()):
                print(f"{m['id']}\t{m['w']}x{m['h']}\t{m['source'][:12]}\t{m['title'][:50]}")
    elif c == "grab":
        for t in sys.argv[2].split(","):
            print(f"===== {t} =====")
            grab(t.strip(), int(sys.argv[3]) if len(sys.argv) > 3 else 12)
    elif c == "sheet":
        sheet()
    else:
        sys.exit(__doc__)
