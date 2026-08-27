"""Render s1 + s7 in every candidate accent, and tile them for comparison."""
import json, os, sys, subprocess, importlib
import themes as palettes, duo as duomod
from PIL import Image, ImageDraw, ImageFont

RENDER = os.path.expanduser("~/.claude/skills/ios-design-language/render.py")
OUT = "/private/tmp/claude-501/-Users-ajaygirolkar-Documents-AI-Agent-Claude-Code/7f9c58ca-46df-43da-9482-95d2c6be8e97/scratchpad"
SCREENS = ["s1", "s7"]
KEYS = sys.argv[1:] or ["lime", "volt", "ember", "chalk"]   # theme keys from themes.py

def override(p):
    z = p["zones"]
    return ("<style>.ios{--accent:%s;--accent-dim:%s;--accent-lift:%s;"
            "--z1:%s;--z2:%s;--z3:%s;--z4:%s;--z5:%s;"
            "--accent-soft:color-mix(in srgb,var(--accent) 14%%,transparent);}"
            ".demo{background:#0D1210}</style>") % (p["accent"], p["dim"], p["lift"], *z)

kit = open("kit.html").read(); app = open("app.html").read()

for key in KEYS:
    p = palettes.PALETTES[key]
    imgs = duomod.build_all(p["duo"])       # remap the photo ramp to this accent
    import gen; importlib.reload(gen)
    T = dict(gen.T); T.update(imgs)
    for s in SCREENS:
        src = open(f"{s}.html").read()
        for k, v in T.items(): src = src.replace("{{"+k+"}}", v)
        f = f"out/_{key}_{s}.html"
        open(f, "w").write('<!doctype html><meta charset="utf-8">'
            '<style>html,body{margin:0;background:#07090A}</style>'
            + kit + app + override(p) + src)
        subprocess.run(["python3", RENDER, f, f"{OUT}/_{key}_{s}.png",
                        "--scale", "1", "--dark"], check=True, capture_output=True)
    print("rendered", key)

# tile: one column per palette, one row per screen
W, H, PAD, CAP = 393, 852, 26, 62
keys = KEYS
sheet = Image.new("RGB", (len(keys)*(W+PAD)+PAD, CAP + len(SCREENS)*(H+PAD) + PAD), (10, 12, 13))
d = ImageDraw.Draw(sheet)
try: font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 21)
except Exception: font = ImageFont.load_default()
for c, key in enumerate(keys):
    x = PAD + c*(W+PAD)
    p = palettes.PALETTES[key]
    d.rectangle([x, 20, x+16, 36], fill=p["accent"])
    d.text((x+26, 18), f"{p['label']}  {p['accent']}", font=font, fill=(235, 240, 232))
    for r, s in enumerate(SCREENS):
        sheet.paste(Image.open(f"{OUT}/_{key}_{s}.png").convert("RGB"),
                    (x, CAP + r*(H+PAD)))
sheet.save(f"{OUT}/accents.png")
print("sheet", sheet.size)
