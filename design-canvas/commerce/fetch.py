"""Pull CC0 object photography from the Cleveland Museum of Art Open Access API.

CMA publishes its public-domain holdings under CC0 with a documented `share_license_status`
field, so provenance is machine-verifiable the same way the fitness set verified The Unlicense.
"""
import json, urllib.request, urllib.parse, sys

API = "https://openaccess-api.clevelandart.org/api/artworks/"
UA  = "portfolio-design-canvas/1.0 (educational mockup; contact ajaygirolkar@gmail.com)"

def q(**kw):
    kw.setdefault("cc0", 1); kw.setdefault("has_image", 1); kw.setdefault("limit", 12)
    url = API + "?" + urllib.parse.urlencode(kw)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return json.load(urllib.request.urlopen(req, timeout=40))["data"]

QUERIES = sys.argv[1:] or ["vase", "bowl", "teapot", "textile", "glass", "basket", "box"]
for term in QUERIES:
    print(f"\n===== {term} =====")
    for a in q(q=term):
        img = (a.get("images") or {}).get("web", {}).get("url")
        if not img: continue
        print(f"{a['id']}\t{a.get('share_license_status')}\t{a.get('type')}\t"
              f"{a['title'][:52]}\t{(a.get('culture') or [''])[0][:26]}\t{img}")
