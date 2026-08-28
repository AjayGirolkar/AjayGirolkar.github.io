import sys, os

# No image pipeline here, and that is the domain's whole rule-7 story. AI screens have no
# photography -- the thing that has to be REAL is the CONTENT: a real technical question,
# a real specific answer, real tool names, real source domains, real compiling Swift.
# "Hello! How can I help you today?" kills the screenshot.

SB = ('<div class="island"></div>'
      '<div class="statusbar"><span>9:41</span><span class="glyphs">'
      '<span class="sb-sig"><i></i><i></i><i></i><i></i></span>'
      '<svg width="17" height="12" viewBox="0 0 17 12" fill="currentColor">'
      '<path d="M8.5 10.6 10.7 8.3a3.1 3.1 0 0 0-4.4 0ZM4.6 6.7l1.3 1.3a4.9 4.9 0 0 1 5.2 0'
      'l1.3-1.3a6.7 6.7 0 0 0-7.8 0ZM1.6 3.6 2.9 5a9.3 9.3 0 0 1 11.2 0l1.3-1.4a11.1 11.1 0 0 0-13.8 0Z"/>'
      '</svg><span class="sb-bat"><b></b></span></span></div>')

T = {"SB": SB}

if __name__ == "__main__" and len(sys.argv) > 1:
    os.makedirs("out", exist_ok=True)
    kit = open("kit.html").read(); app = open("app.html").read()
    for f in sys.argv[1:]:
        src = open(f).read()
        for k, v in T.items(): src = src.replace("{{"+k+"}}", v)
        out = os.path.join("out", os.path.basename(f))
        open(out, "w").write(
            '<!doctype html><meta charset="utf-8"><title>NativeAIStudio</title>'
            '<style>html,body{margin:0;padding:0;background:#131211}</style>'
            + kit + app + src)
        print("built", out, os.path.getsize(out)//1024, "KB")
