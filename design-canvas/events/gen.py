import sys, os, poster

# Rule 7 here is BOTH photography and content. The plates are CC0 Unsplash frames pulled
# from Wikimedia Commons with the licence asserted per item (dl.py); the copy is a real
# gig -- real running order with real set times, a real venue capacity, a real ticket
# policy (face-value resale, the thing that actually distinguishes this product category).
# "Amazing Artist / Live Tonight / Buy Now" kills the screenshot.

SB = ('<div class="island"></div>'
      '<div class="statusbar"><span>9:41</span><span class="glyphs">'
      '<span class="sb-sig"><i></i><i></i><i></i><i></i></span>'
      '<svg width="17" height="12" viewBox="0 0 17 12" fill="currentColor">'
      '<path d="M8.5 10.6 10.7 8.3a3.1 3.1 0 0 0-4.4 0ZM4.6 6.7l1.3 1.3a4.9 4.9 0 0 1 5.2 0'
      'l1.3-1.3a6.7 6.7 0 0 0-7.8 0ZM1.6 3.6 2.9 5a9.3 9.3 0 0 1 11.2 0l1.3-1.4a11.1 11.1 0 0 0-13.8 0Z"/>'
      '</svg><span class="sb-bat"><b></b></span></span></div>')

def qr(seed="GATE-ANTIPODES-14MAR26-A7F2", n=21):
    """A 21x21 block matrix with real finder squares, alignment block and quiet timing
    rows, filled deterministically from a hash of the order id.

    Drawn rather than shipped as an image on purpose: a random noise square reads as
    placeholder art the second anyone looks at the screenshot, and a REAL scannable code
    in a portfolio is a live payload pointing at nothing. Structure without a payload is
    the honest middle."""
    import hashlib
    h = hashlib.sha256(seed.encode()).digest() * 12
    g = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            g[i][j] = (h[(i * n + j) % len(h)] >> ((i + j) % 7)) & 1
    def finder(r, c):
        for i in range(7):
            for j in range(7):
                g[r + i][c + j] = 1 if (i in (0, 6) or j in (0, 6)
                                        or (2 <= i <= 4 and 2 <= j <= 4)) else 0
        for i in range(-1, 8):                      # quiet separator
            for j in range(-1, 8):
                if 0 <= r + i < n and 0 <= c + j < n and (i in (-1, 7) or j in (-1, 7)):
                    g[r + i][c + j] = 0
    finder(0, 0); finder(0, n - 7); finder(n - 7, 0)
    for i in range(8, n - 8):                       # timing rows
        g[6][i] = g[i][6] = (i + 1) % 2
    for i in range(5):                              # alignment block
        for j in range(5):
            g[n - 9 + i][n - 9 + j] = 1 if (i in (0, 4) or j in (0, 4) or (i == 2 and j == 2)) else 0
    return "".join('<s style="grid-area:%d/%d"></s>' % (i + 1, j + 1)
                   for i in range(n) for j in range(n) if g[i][j])


T = {"SB": SB, "QR": qr()}
T.update(poster.build()[0])

if __name__ == "__main__" and len(sys.argv) > 1:
    os.makedirs("out", exist_ok=True)
    kit = open("kit.html").read(); app = open("app.html").read()
    for f in sys.argv[1:]:
        src = open(f).read()
        for k, v in T.items(): src = src.replace("{{"+k+"}}", v)
        out = os.path.join("out", os.path.basename(f))
        open(out, "w").write(
            '<!doctype html><meta charset="utf-8"><title>GATE</title>'
            '<style>html,body{margin:0;padding:0;background:#000}</style>'
            + kit + app + src)
        print("built", out, os.path.getsize(out)//1024, "KB")
