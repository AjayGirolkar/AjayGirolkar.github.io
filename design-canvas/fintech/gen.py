import math,random,json,sys,os,re

def series(n,seed,drift,vol,shock=None):
    r=random.Random(seed); v=100.0; out=[]
    for i in range(n):
        v*= 1+drift+r.gauss(0,vol)
        if shock and i==shock[0]: v*=1+shock[1]
        out.append(v)
    return out

def smooth(pts,w,h,pad=2):
    """Catmull-Rom -> cubic bezier path through pts (list of y values)."""
    n=len(pts); lo=min(pts); hi=max(pts); rng=(hi-lo) or 1
    P=[(i*(w/(n-1)), pad+(1-(y-lo)/rng)*(h-2*pad)) for i,y in enumerate(pts)]
    d=f"M{P[0][0]:.1f},{P[0][1]:.1f}"
    for i in range(n-1):
        p0=P[i-1] if i>0 else P[0]; p1=P[i]; p2=P[i+1]; p3=P[i+2] if i+2<n else P[-1]
        c1=(p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6)
        c2=(p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6)
        d+=f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d,P

def area(d,P,h):
    return f"{d} L{P[-1][0]:.1f},{h} L{P[0][0]:.1f},{h} Z"

T={}
# dashboard intraday 1D, ends higher
s=series(46,7,0.0006,0.0035,shock=(28,0.004))
d,P=smooth(s,386,132,6); T["SPARK_D"]=d; T["SPARK_A"]=area(d,P,132)
T["SPARK_X"]=f"{P[-1][0]:.1f}"; T["SPARK_Y"]=f"{P[-1][1]:.1f}"

# fund detail 1Y hero
s=series(84,21,0.0022,0.011,shock=(52,-0.05))
d,P=smooth(s,384,178,8); T["HERO_D"]=d; T["HERO_A"]=area(d,P,214)
T["HERO_X"]=f"{P[-1][0]:.1f}"; T["HERO_Y"]=f"{P[-1][1]:.1f}"

# mini sparklines 60x22
for k,(sd,dr,vo) in {"M1":(3,0.004,0.012),"M2":(11,0.0015,0.009),"M3":(5,-0.003,0.010)}.items():
    d,_=smooth(series(22,sd,dr,vo),40,22,3); T["MINI_"+k]=d

# month spend bars (12 weeks) for feed screen
r=random.Random(9); vals=[r.uniform(.30,1.0) for _ in range(14)]; vals[-1]=.58; vals[-2]=.92
T["BARS"]="".join(
  f'<rect x="{i*25.8:.1f}" y="{(1-v)*52:.1f}" width="16" height="{max(v*52,4):.1f}" rx="5" '
  f'fill="{"var(--accent)" if i==13 else "color-mix(in srgb,var(--ink) 10%,transparent)"}"/>'
  for i,v in enumerate(vals))

r=random.Random(4)
cols=["#0F7B6C","#2FA396","#93CEC5","#C9A227","#0B5F55"]
pcs=[]
while len(pcs)<20:
    x=r.uniform(8,372); y=r.uniform(8,300)
    if (x-196)**2+(y-182)**2 < 138**2: continue      # keep clear of the ring
    w=r.uniform(5,9); h=r.uniform(9,15); rot=r.uniform(-60,60)
    pcs.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="2.5" '
               f'fill="{r.choice(cols)}" opacity="{r.uniform(.40,.85):.2f}" '
               f'transform="rotate({rot:.0f} {x+w/2:.1f} {y+h/2:.1f})"/>')
T["CONFETTI"]="".join(pcs)

T["SB"]=open("_sb.frag").read()

for f in sys.argv[1:]:
    src=open(f).read()
    for k,v in T.items(): src=src.replace("{{"+k+"}}",v)
    out=os.path.join("out",os.path.basename(f))
    kit=open("kit.html").read(); app=open("app.html").read()
    open(out,"w").write(
      '<!doctype html><meta charset="utf-8"><title>WealthKit</title>'
      '<style>html,body{margin:0;padding:0;background:#F2F2F7}'
      '@media(prefers-color-scheme:dark){html,body{background:#000}}</style>'
      +kit+app+src)
    print("built",out)
