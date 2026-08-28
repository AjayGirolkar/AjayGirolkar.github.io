"""ShopEase catalogue + the image tokens the screens interpolate.

Every product is a real CC0 plate from obj/ (Cleveland Museum of Art Open Access).
Names, makers, prices and stock are written for the mockup; the photography is the
only thing that has to be real, and rule 7 says it does.
"""
import json, os, objects as O

# id, key, product name, maker, price, was, category, glaze/finish swatches
P = [
 ("447764","kyusu",  "Bamboo Kyūsu",          "Anzai Ceramics",    8400,  None, "Ceramics"),
 ("447720","kiku",   "Kikū Side-Handle Pot",  "Anzai Ceramics",    6900,  8200, "Ceramics"),
 ("125978","tenmoku","Tenmoku Tea Bowl",      "Kuro Atelier",      4250,  None, "Ceramics"),
 ("520329","gu",     "Gu Carved Vase",        "Shirogane Studio", 12800,  None, "Ceramics"),
 ("447759","celadon","Celadon Crackle Vase",  "Mira Kaur Pottery", 9600,  None, "Ceramics"),
 ("122443","meiping","Meiping Lotus Vase",    "Blue Kiln Co.",    18500, 22000, "Ceramics"),
 ("300665","cameo",  "Marbled Cameo Vase",    "Verre Atelier",    24000,  None, "Glass"),
 ("94657", "fluted", "Fluted Glass Bowl",     "Verre Atelier",     7200,  None, "Glass"),
 ("370537","pulpit", "Jack-in-the-Pulpit",    "Favrile Works",    31500,  None, "Glass"),
 ("296873","globe",  "Patinated Globe Vase",  "Favrile Works",    27400,  None, "Glass"),
 ("93176", "ruffle", "Ruffled Rim Bowl",      "Favrile Works",    11900, 14500, "Glass"),
 ("136303","stem",   "Iridescent Stem Vase",  "Favrile Works",    16200,  None, "Glass"),
 ("93173", "inkwell","Mosaic Inkwell",        "Favrile Works",    21000,  None, "Glass"),
 ("144690","scroll", "Cinnabar Scroll Box",   "Red Lacquer House",14700,  None, "Lacquer"),
 ("169510","peony",  "Peony Round Box",       "Red Lacquer House", 9800,  None, "Lacquer"),
 ("97857", "coil",   "Coiled Figure Basket",  "Panamint Weavers", 13400,  None, "Baskets"),
 ("97847", "storage","Deep Storage Basket",   "Panamint Weavers", 10600,  None, "Baskets"),
 ("102980","binakol","Binakol Handloom Throw","Ilocos Handloom",   5900,  7400, "Textiles"),
]
BY_KEY = {k: dict(id=i, name=n, maker=m, price=p, was=w, cat=c) for i,k,n,m,p,w,c in P}

def rupees(n):
    s = f"{n:,}"                      # lakh grouping reads wrong below 1,00,000; these all are
    return "₹" + s

# key -> (plate size, inset). Heroes are only built for the screens that go full-bleed,
# because a 786px plate is ~4x the bytes of a tile and the canvas ships every one.
TILE = (460, 575)
# key -> (size, inset, align). A hero that carries a headline set on the plate needs the
# object high and small; a hero that IS the whole product page wants it big and centred.
HERO = {"pulpit":  ((786, 904), 0.70, 0.60),
        "cameo":   ((786, 900), 0.62, 0.16),
        "celadon": ((786, 900), 0.62, 0.16)}
# A wide break tile is not a tall hero cropped: object-fit:cover on a 900-tall plate
# shows the middle of the vase and nothing else. Wide plates get composed as wide.
# A banner is not a tall plate cropped -- cover crops the foot off the vase and the
# result reads as a mistake. Compose wide plates wide, and push the object off-centre
# so the caption has clean sand to sit on.
WIDE = {"meiping": ((786, 444), 0.94, 0.50, 0.74),
        "binakol": ((786, 444), 0.90, 0.50, 0.74),
        "scroll":  ((786, 444), 0.90, 0.50, 0.74)}

CACHE = "product_imgs.json"

def build(force=False):
    if os.path.exists(CACHE) and not force:
        return json.load(open(CACHE))
    T = {}
    for i, k, *_ in P:
        T["IMG_" + k.upper()] = O.b64(O.plate(f"obj/{i}.jpg", TILE, inset=0.78), q=74)
        if k in WIDE:
            sz, ins, al, hal = WIDE[k]
            T["WIDE_" + k.upper()] = O.b64(
                O.plate(f"obj/{i}.jpg", sz, inset=ins, align=al, halign=hal), q=76)
        if k in HERO:
            sz, ins, al = HERO[k]
            T["HERO_" + k.upper()] = O.b64(
                O.plate(f"obj/{i}.jpg", sz, inset=ins, align=al), q=76)
    json.dump(T, open(CACHE, "w"))
    return T

if __name__ == "__main__":
    T = build(force=True)
    print(f"{len(T)} images, {sum(len(v) for v in T.values())//1024} KB base64")
