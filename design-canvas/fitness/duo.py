"""Build duotone exercise frame pairs as base64 WEBP data URIs.

Source: yuhonas/free-exercise-db (The Unlicense / public domain).
Each exercise ships exactly two frames -- start and end of the rep -- so a
crossfade between them reads as the movement without shipping a GIF.

The raw frames are red-walled stock gym photography, which is this domain's
first cliche. Mapping them onto the app's own accent ramp is what turns them
into a designed asset, so STOPS must move whenever the accent moves.
"""
from PIL import Image, ImageOps, ImageEnhance
import numpy as np, base64, io, json

STOPS = [(0.00,(7, 9, 10)), (0.42,(21, 64, 42)), (0.72,(53, 190, 115)), (1.00,(181, 242, 208))]

W, H = 320, 320          # square tile: holds upright and lying subjects alike

# Crop boxes as FRACTIONS of each source (l, t, r, b) -- the dataset mixes
# 850x567 landscape and 850x1275 portrait, so absolute pixels are not portable.
# Each box holds the figure across BOTH frames of the rep.
CROPS = {
 "rdl":    ("Romanian_Deadlift",               (0.280, 0.102, 0.767, 0.882)),
 "thrust": ("Barbell_Hip_Thrust",              (0.241, 0.030, 0.965, 0.988)),
 "curl":   ("Lying_Leg_Curls",                 (0.253, 0.194, 0.896, 0.961)),
 "gm":     ("Good_Morning",                    (0.298, 0.028, 0.935, 0.900)),
 "split":  ("Split_Squat_with_Dumbbells",      (0.000, 0.140, 1.000, 0.860)),
 "ext":    ("Hyperextensions_Back_Extensions", (0.170, 0.085, 0.722, 0.965)),
}

def build_lut(stops=None):
    stops = stops or STOPS
    lut = np.zeros((256, 3), dtype=np.uint8)
    for i in range(256):
        t = i/255
        for j in range(len(stops)-1):
            a, ca = stops[j]; b, cb = stops[j+1]
            if a <= t <= b:
                f = (t-a)/(b-a)
                lut[i] = [int(ca[k]+(cb[k]-ca[k])*f) for k in range(3)]
                break
    return lut

LUT = build_lut()

def _vignette(w, h, strength=0.72):
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w/2, h*0.48
    d = np.sqrt(((xx-cx)/(w*0.62))**2 + ((yy-cy)/(h*0.66))**2)
    return np.clip(1 - strength*np.clip(d-0.42, 0, None)**1.35, 0.06, 1)[..., None]

VIG = _vignette(W, H)

def build(src, frac, lut=None):
    lut = LUT if lut is None else lut
    im = Image.open(src).convert("RGB")
    w, h = im.size
    l, t, r, b = frac
    im = im.crop((int(l*w), int(t*h), int(r*w), int(b*h)))
    im = ImageOps.fit(im, (W, H), Image.LANCZOS)
    g  = ImageOps.autocontrast(im.convert("L"), cutoff=2)
    g  = ImageEnhance.Contrast(g).enhance(1.22)
    arr = lut[np.array(g)].astype(np.float32) * VIG
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")
    buf = io.BytesIO(); out.save(buf, "WEBP", quality=70, method=6)
    return out, buf.getvalue()

def build_all(stops=None):
    """-> {IMG_<KEY>_<frame>: data-uri} for every exercise, both frames."""
    lut = build_lut(stops) if stops else LUT
    imgs = {}
    for key, (name, frac) in CROPS.items():
        for f in (0, 1):
            _, raw = build(f"ex/{name}_{f}.jpg", frac, lut)
            imgs[f"IMG_{key.upper()}_{f}"] = "data:image/webp;base64," + base64.b64encode(raw).decode()
    return imgs

if __name__ == "__main__":
    imgs = build_all()
    json.dump(imgs, open("exercise_imgs.json", "w"))
    print(f"{len(imgs)} frames, {sum(len(v) for v in imgs.values())//1024} KB base64")
