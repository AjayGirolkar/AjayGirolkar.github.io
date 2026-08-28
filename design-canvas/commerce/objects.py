"""Composite CC0 museum object photography onto ShopEase's own sand ground.

Source: Cleveland Museum of Art Open Access (CC0 1.0). Every object is fetched by id
and its `share_license_status` asserted == "CC0" in dl.py before it lands in obj/.

Why any processing at all: CMA shoots on graduated studio grey or on black. Dropped
straight into the layout those rectangles read as pasted-in stock, and the black-ground
ones fight the sand page. Commerce's identity lock says images sit DIRECTLY on the
ground with no container, so the backdrop has to become the ground -- the knockout is
what buys the containerless look, not a filter for its own sake.

Method: flood the backdrop from the frame border (it is near-uniform in every CMA
plate), feather the matte, drop the object on a sand gradient with a contact shadow.
"""
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np, base64, io, json, sys
from collections import deque

# --- ShopEase ground ---------------------------------------------------------
SAND_TOP = (238, 232, 222)
SAND_BOT = (227, 217, 202)

def _backdrop(arr, edge=5.0, tol=56, passes=4, grow=2):
    """Mask of the studio backdrop.

    CMA plates are shot on a GRADUATED sweep, so a flat colour-distance threshold from
    the border stops partway up the gradient and leaves a grey rectangle behind the
    object -- that was the first attempt and it failed on every plate. What actually
    separates backdrop from object here is edge energy: the sweep is smooth everywhere,
    the object outline is a hard step. So flood the border through LOW-GRADIENT pixels
    and let the outline itself be the barrier.
    """
    g = np.array(Image.fromarray(arr).convert("L").filter(
        ImageFilter.GaussianBlur(1.1)), dtype=np.float32)
    gx = np.zeros_like(g); gy = np.zeros_like(g)
    gx[:, 1:-1] = g[:, 2:] - g[:, :-2]
    gy[1:-1, :] = g[2:, :] - g[:-2, :]
    smooth = np.hypot(gx, gy) < edge

    # Edge energy alone is not enough: on a pale porcelain body the outline step is
    # soft, so the flood walks straight through the object and eats it. Second gate --
    # the sweep is a VERTICAL gradient, so model it per row from the outer columns and
    # require backdrop pixels to still look like the backdrop at their own height.
    a = arr.astype(np.int16)
    k = 7
    ref = np.median(np.concatenate([a[:, :k], a[:, -k:]], axis=1), axis=1)   # (h,3)
    near = np.abs(a - ref[:, None, :]).sum(axis=2) <= tol
    free = smooth & near

    def flood(free):
        m = np.zeros_like(free)
        m[0], m[-1], m[:, 0], m[:, -1] = True, True, True, True
        m &= free
        while True:                              # shift-dilate until stable
            n = m.copy()
            n[1:] |= m[:-1]; n[:-1] |= m[1:]; n[:, 1:] |= m[:, :-1]; n[:, :-1] |= m[:, 1:]
            n &= free
            if n.sum() == m.sum():
                return m
            m = n

    m = flood(free)

    # Refit and re-flood. The outer columns only sample the sweep where it meets the
    # frame; on a black-to-grey sweep the colour a third of the way in is already past
    # `tol`, which is what left grey wedges parked behind the darker objects. Re-deriving
    # each row's backdrop colour from the pixels ALREADY proven to be backdrop tracks the
    # sweep inward, and the edge barrier still stops it at the object outline.
    for _ in range(passes):
        rows = np.where(m.any(axis=1))[0]
        if not len(rows):
            break
        r2 = ref.copy()
        for y in rows:
            r2[y] = np.median(a[y][m[y]], axis=0)
        n2 = np.abs(a - r2[:, None, :]).sum(axis=2) <= tol
        m2 = flood(smooth & (near | n2))
        if m2.sum() <= m.sum():
            break
        m, near = m2, (near | n2)

    for _ in range(grow):                        # eat the outline ring itself
        n = m.copy()
        n[1:] |= m[:-1]; n[:-1] |= m[1:]; n[:, 1:] |= m[:, :-1]; n[:, :-1] |= m[:, 1:]
        m = n
    return m

def cutout(path, edge=5.0, tol=56, passes=4, open_px=0, feather=1.5):
    im = Image.open(path).convert("RGB")
    im.thumbnail((900, 900), Image.LANCZOS)
    arr = np.array(im)
    bg = _backdrop(arr, edge, tol, passes=passes)
    alpha = Image.fromarray(((~bg) * 255).astype(np.uint8))
    if open_px:                                  # morphological opening kills speckle
        alpha = alpha.filter(ImageFilter.MinFilter(open_px)).filter(
                             ImageFilter.MaxFilter(open_px))
    alpha = alpha.filter(ImageFilter.GaussianBlur(feather))
    im.putalpha(alpha)
    return im.crop(im.getchannel("A").getbbox())

def ground(w, h):
    g = np.linspace(0, 1, h)[:, None, None]
    a = np.array(SAND_TOP)[None, None, :] * (1-g) + np.array(SAND_BOT)[None, None, :] * g
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8).repeat(w, axis=1), "RGB")

def plate(path, size=(560, 700), inset=0.80, align=0.52, halign=0.5,
          edge=None, tol=None, passes=None, open_px=None, warm=1.0):
    """Object on sand, sized to `inset` of the frame, with a soft contact shadow."""
    W, H = size
    ov = PARAMS.get(path.split("/")[-1].split(".")[0], {})
    edge = ov.get("edge", 5.0) if edge is None else edge
    tol  = ov.get("tol", 56)   if tol  is None else tol
    passes = ov.get("passes", 4) if passes is None else passes
    open_px = ov.get("open_px", 0) if open_px is None else open_px
    ob = cutout(path, edge, tol, passes, open_px)
    ob = ImageOps.contain(ob, (int(W*inset), int(H*inset)), Image.LANCZOS)
    if warm != 1.0:
        ob = Image.merge("RGBA", (*ImageEnhance.Color(ob.convert("RGB")).enhance(warm).split(),
                                  ob.getchannel("A")))
    bgp = ground(W, H)
    # `align` is where the object sits vertically. Heroes push it high so the lower
    # third stays clean sand -- the display headline is set ON the plate, and type
    # crossing the object's own shadow reads as an accident.
    x, y = int((W - ob.width)*halign), int((H - ob.height)*align)

    sh = Image.new("L", (W, H), 0)                     # contact shadow, not a drop shadow
    a = ob.getchannel("A").resize((ob.width, max(6, ob.height//9)), Image.LANCZOS)
    sh.paste(a, (x, y + ob.height - a.height//2))
    sh = sh.filter(ImageFilter.GaussianBlur(11))
    bgp = Image.composite(Image.new("RGB", (W, H), (176, 164, 146)), bgp,
                          sh.point(lambda v: int(v*0.42)))
    bgp.paste(ob, (x, y), ob)
    return unify(bgp)

# Per-object overrides. The grid in obj/_grid.png is how these were chosen: anything
# not listed cuts cleanly at the defaults.
PARAMS = {
    # Pale bodies get passes=0: the refit tracks the sweep inward, and on a white
    # porcelain body against a light sweep it eventually decides the object IS the
    # backdrop and takes a bite out of the silhouette. Visible only at tile size.
    # Pale bodies: a wide colour gate walks straight through the soft shoulder edge and
    # takes a bite out of the silhouette -- invisible on a contact sheet, glaring at tile
    # size. Seed them tight (tol 10) and let the refit passes track the sweep instead.
    "447764": dict(tol=10, passes=8, edge=2.5),
    "447759": dict(tol=10, passes=8, edge=2.5),
    "520329": dict(tol=10, passes=8, edge=2.5),
    "93176":  dict(tol=10, passes=8, edge=2.5),
    "447720": dict(tol=26, passes=0, edge=1.5, open_px=5),
    "97857": dict(edge=5.0, tol=96),      # basket rim halos at t56
    "97847": dict(edge=5.0, tol=96),
    "102980": dict(edge=0.0),             # textile fills its frame -- no backdrop to cut
    "370537": dict(edge=8.0, tol=150, passes=8),  # hard two-tone backdrop, not a sweep;
                                                 # a tight cut leaves its cast shadow as a
                                                 # black ellipse floating behind the stem
    "296873": dict(edge=9.0),
    "94657":  dict(edge=9.0),
}

def unify(im, warm=0.055, contrast=1.03):
    """Pull every plate onto one set. The objects come from four different CMA shoots,
    so their residual shadows sit at four different neutrals; a shared warm bias is what
    makes them read as one catalogue rather than as found images."""
    a = np.asarray(im).astype(np.float32)
    a = a*(1-warm) + np.array(SAND_BOT, np.float32)*warm*(a/255.0)*1.6
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")
    return ImageEnhance.Contrast(im).enhance(contrast)


def b64(im, q=76):
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=q, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()

if __name__ == "__main__":
    ids = json.load(open("obj/meta.json")).keys()
    from PIL import ImageDraw
    S = 200
    sheet = Image.new("RGB", (6*S, ((len(ids)+5)//6)*(S+16)), (255,255,255))
    d = ImageDraw.Draw(sheet)
    for n, i in enumerate(ids):
        p = ImageOps.contain(plate(f"obj/{i}.jpg"), (S-8, S-8))
        sheet.paste(p, ((n%6)*S+4, (n//6)*(S+16)+4))
        d.text(((n%6)*S+6, (n//6)*(S+16)+S-8), str(i), fill=(0,0,0))
    sheet.save("obj/_cut.png"); print("ok")
