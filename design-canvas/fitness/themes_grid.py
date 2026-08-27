import os, subprocess, importlib, sys
sys.path.insert(0, ".")
import themes, gen
from PIL import Image, ImageDraw, ImageFont

RENDER = os.path.expanduser("~/.claude/skills/ios-design-language/render.py")
OUT = "/private/tmp/claude-501/-Users-ajaygirolkar-Documents-AI-Agent-Claude-Code/7f9c58ca-46df-43da-9482-95d2c6be8e97/scratchpad"
kit = open("kit.html").read(); app = open("app.html").read()
src0 = open("s1.html").read()
for k, v in gen.T.items(): src0 = src0.replace("{{"+k+"}}", v)

for key, p in themes.PALETTES.items():
    ov = ("<style>.ios{--accent:%s;--accent-dim:%s;--accent-lift:%s;"
          "--z1:%s;--z2:%s;--z3:%s;--z4:%s;--z5:%s;}</style>"
          % (p["accent"], p["dim"], p["lift"], *p["zones"]))
    f = f"out/_t_{key}.html"
    open(f, "w").write('<!doctype html><meta charset="utf-8">'
        '<style>html,body{margin:0;background:#07090A}</style>' + kit + app + ov + src0)
    subprocess.run(["python3", RENDER, f, f"{OUT}/_t_{key}.png", "--scale", "1", "--dark"],
                   check=True, capture_output=True)

W, H, PAD, CAP = 393, 852, 22, 46
keys = list(themes.PALETTES)
COLS = 3
rows = (len(keys)+COLS-1)//COLS
sheet = Image.new("RGB", (COLS*(W+PAD)+PAD, rows*(H+CAP+PAD)+PAD), (10, 12, 13))
d = ImageDraw.Draw(sheet)
try: font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
except Exception: font = ImageFont.load_default()
for i, key in enumerate(keys):
    p = themes.PALETTES[key]
    x = PAD + (i % COLS)*(W+PAD); y = PAD + (i//COLS)*(H+CAP+PAD)
    d.rectangle([x, y+6, x+16, y+22], fill=p["accent"])
    d.text((x+26, y+4), f"{p['label']}", font=font, fill=(235, 240, 232))
    d.text((x+26, y+24), p["accent"], font=font, fill=(150, 158, 148))
    sheet.paste(Image.open(f"{OUT}/_t_{key}.png").convert("RGB"), (x, y+CAP))
sheet.save(f"{OUT}/themes.png")
print("sheet", sheet.size)
