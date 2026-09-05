import gen
T = gen.T; kit = open("kit.html").read(); app = open("app.html").read()
bodies = []
for i in range(1, 8):
    b = open(f"s{i}.html").read()
    for k, v in T.items(): b = b.replace("{{"+k+"}}", v)
    bodies.append(f'<div class="cell">{b}</div>')
open("out/proof.html", "w").write(
 '<!doctype html><meta charset="utf-8"><title>GATE proof sheet</title>'
 '<style>html,body{margin:0;background:#08070A}'
 '.sheet{display:grid;grid-template-columns:repeat(4,393px);gap:26px;padding:26px;width:max-content}'
 '.cell{width:393px;height:852px;overflow:hidden;border-radius:38px}</style>'
 + kit + app + f'<div class="sheet">{"".join(bodies)}</div>')
print("ok")
