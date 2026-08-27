"""Nine accent directions for FitnessPro, on the locked near-black ground.

The HR zone ramp is held CONSTANT across all nine -- a desaturated cool->hot
scale -- so the only variable is the accent. Keeping the ramp lower in chroma
than every candidate is what stops the data colours fighting the brand colour.

Excluded on purpose: purple/indigo (the AI house style) and anything near
WealthKit's teal #0F7B6C / #2FBFA8.
"""
import colorsys

ZONES = ["#5E7C99", "#3E9FA8", "#7FB03F", "#D9922C", "#C0392B"]

def _rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))
def _hex(r): return "#%02X%02X%02X" % tuple(max(0, min(255, round(c*255))) for c in r)
def _mix(a, b, t): return tuple(a[i] + (b[i]-a[i])*t for i in range(3))

def derive(accent):
    """dim / lift / photo ramp, all derived from the one accent hex."""
    c = _rgb(accent)
    h, l, s = colorsys.rgb_to_hls(*c)
    dim  = colorsys.hls_to_rgb(h, max(0, l*0.44), s*0.92)
    lift = _mix(c, (1, 1, 1), 0.45)
    ground = (7/255, 9/255, 10/255)
    return dict(
        dim=_hex(dim), lift=_hex(lift),
        duo=[(0.00, tuple(round(v*255) for v in ground)),
             (0.42, tuple(round(v*255) for v in _mix(ground, c, 0.26))),
             (0.72, tuple(round(v*255) for v in _mix(ground, c, 0.86))),
             (1.00, tuple(round(v*255) for v in _mix(c, (1, 1, 1), 0.62)))])

CANDIDATES = [
 ("lime",     "#CBFF3C", "Volt lime — current"),
 ("volt",     "#A6D93B", "Volt, dialed down"),
 ("mint",     "#3DDC84", "Mint"),
 ("arctic",   "#4FC9F0", "Arctic"),
 ("ember",    "#FF5E3A", "Ember coral"),
 ("tangerine","#FF8A3D", "Tangerine"),
 ("solar",    "#FFB02E", "Solar gold"),
 ("magenta",  "#FF3D8B", "Magenta"),
 ("chalk",    "#E9EFE4", "Chalk — colour only in data"),
]

PALETTES = {}
for key, accent, label in CANDIDATES:
    PALETTES[key] = dict(label=label, accent=accent, zones=ZONES, **derive(accent))

# chalk is near-achromatic, so the generic derivation pushes its dim green.
PALETTES["chalk"]["dim"] = "#7C837A"
