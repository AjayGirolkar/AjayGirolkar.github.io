import sys, os, json, feed

# feed.build() re-grades and re-encodes 42 images (~8s), so cache it. Delete media.json
# after touching feed.py's CAST/POSTS/grids or the screens keep the stale crop.
if os.path.exists("media.json") and os.path.getmtime("media.json") > os.path.getmtime("feed.py"):
    T = json.load(open("media.json"))
else:
    T = feed.build()
    json.dump(T, open("media.json", "w"))

T["SB"] = open("_sb.frag").read()

# No chart generator here on purpose. Fintech's sparkline/donut and fitness's rings are
# spent, and social's whole vocabulary -- story rail, media post, engagement row, compose
# pill, 3-up grid -- is layout over photography. The only generated thing is the imagery.

if __name__ == "__main__" and len(sys.argv) > 1:
    os.makedirs("out", exist_ok=True)
    kit = open("kit.html").read(); app = open("app.html").read()
    for f in sys.argv[1:]:
        src = open(f).read()
        for k, v in T.items(): src = src.replace("{{"+k+"}}", v)
        out = os.path.join("out", os.path.basename(f))
        open(out, "w").write(
            '<!doctype html><meta charset="utf-8"><title>SocialFlow</title>'
            '<style>html,body{margin:0;padding:0;background:#000}</style>'
            + kit + app + src)
        print("built", out, os.path.getsize(out)//1024, "KB")
