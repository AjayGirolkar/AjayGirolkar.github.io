import sys, os, catalog

T = dict(catalog.build())
T["SB"] = open("_sb.frag").read()

# Commerce needs no chart generator -- fintech's sparkline/donut pair is spent, and the
# vocabulary here (grid, swatches, size run, strikethrough, buy bar) is all layout.
# What does belong in the token table is price copy, so a price change is one edit.
for k, p in catalog.BY_KEY.items():
    T[f"PR_{k.upper()}"]   = catalog.rupees(p["price"])
    T[f"WAS_{k.upper()}"]  = catalog.rupees(p["was"]) if p["was"] else ""
    T[f"OFF_{k.upper()}"]  = (f"-{round(100*(p['was']-p['price'])/p['was'])}%"
                              if p["was"] else "")
    T[f"NM_{k.upper()}"]   = p["name"]
    T[f"MK_{k.upper()}"]   = p["maker"]

if __name__ == "__main__" and len(sys.argv) > 1:
    os.makedirs("out", exist_ok=True)
    kit = open("kit.html").read(); app = open("app.html").read()
    for f in sys.argv[1:]:
        src = open(f).read()
        for k, v in T.items(): src = src.replace("{{"+k+"}}", v)
        out = os.path.join("out", os.path.basename(f))
        open(out, "w").write(
            '<!doctype html><meta charset="utf-8"><title>ShopEase</title>'
            '<style>html,body{margin:0;padding:0;background:#F4EFE7}</style>'
            + kit + app + src)
        print("built", out)
