import json, urllib.request, os, sys
UA = "portfolio-design-canvas/1.0 (educational mockup; contact ajaygirolkar@gmail.com)"
IDS = [447764,447720,125978,520329,447759,122443,300665,94657,
       370537,296873,93176,136303,169510,144690,97857,97847,102980,93173]
os.makedirs("obj", exist_ok=True)
meta = {}
for i in IDS:
    url = f"https://openaccess-api.clevelandart.org/api/artworks/{i}"
    a = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":UA}), timeout=40))["data"]
    assert a["share_license_status"] == "CC0", (i, a["share_license_status"])
    src = a["images"]["web"]["url"]
    p = f"obj/{i}.jpg"
    if not os.path.exists(p):
        # the CDN 403s on urllib's default UA just like the API does
        with urllib.request.urlopen(urllib.request.Request(src, headers={"User-Agent":UA}), timeout=60) as r:
            open(p, "wb").write(r.read())
    meta[str(i)] = {"title": a["title"], "type": a["type"],
                    "culture": (a.get("culture") or [""])[0], "date": a.get("creation_date"),
                    "url": a["url"], "license": a["share_license_status"]}
    print(i, a["type"], a["title"][:44])
json.dump(meta, open("obj/meta.json","w"), indent=1)
