import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=2326,1058
FB="/System/Library/Fonts/Supplemental/Arial Bold.ttf"; FR="/System/Library/Fonts/Supplemental/Arial.ttf"
def font(sz,b=True): return ImageFont.truetype(FB if b else FR, sz)
RED=(255,72,72); GREEN=(64,230,120); WHITE=(245,245,245); DIM=(20,22,28)
n=[0]
def emit(im):
    n[0]+=1; im.save(f"out/{n[0]:05d}.jpg", quality=90)
def link(idx):
    n[0]+=1; os.symlink(os.path.abspath(f"src/{idx:05d}.jpg"), f"out/{n[0]:05d}.jpg")
def ease(t): return 0 if t<=0 else 1 if t>=1 else (1-math.cos(math.pi*t))/2
def bez(p0,p1,p2,t): 
    return ((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0],(1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1])
def curve(d,p0,p1,p2,t,color,w,dash=None):
    pts=[bez(p0,p1,p2,i/80*t) for i in range(81)]
    if dash is None: d.line(pts,fill=color,width=w,joint="curve")
    else:
        for i in range(0,80,dash*2):
            seg=pts[i:i+dash+1]
            if len(seg)>1: d.line(seg,fill=color,width=w)
def ring(d,c,r,color,w,a=1.0):
    d.ellipse([c[0]-r,c[1]-r*0.45,c[0]+r,c[1]+r*0.45],outline=color,width=w)
def glow(im,fn):
    layer=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(layer); fn(d)
    g=layer.filter(ImageFilter.GaussianBlur(10))
    im.alpha_composite(g); im.alpha_composite(layer)
def pill(d,xy,text,color,sz=30):
    f=font(sz); tw=d.textlength(text,font=f); x,y=xy
    d.rounded_rectangle([x,y,x+tw+44,y+sz+22],radius=(sz+22)//2,fill=color)
    d.text((x+22,y+9),text,fill=(15,15,20),font=f)
def mark(d,xy,ok,r=16):
    x,y=xy; col=GREEN if ok else RED
    d.ellipse([x-r,y-r,x+r,y+r],fill=col)
    if ok: d.line([(x-8,y),(x-2,y+7),(x+9,y-7)],fill=(15,15,20),width=5)
    else: d.line([(x-7,y-7),(x+7,y+7)],fill=(15,15,20),width=5); d.line([(x-7,y+7),(x+7,y-7)],fill=(15,15,20),width=5)
def caption(d,y,text,ok,alpha):
    if alpha<=0: return
    f=font(40); tw=d.textlength(text,font=f); x=740
    d.rounded_rectangle([x,y,x+tw+110,y+80],radius=16,fill=(12,14,20,int(215*alpha)))
    col=GREEN if ok else RED
    d.ellipse([x+24,y+22,x+60,y+58],fill=col+(int(255*alpha),))
    cx,cy=x+42,y+40
    if ok: d.line([(cx-8,cy),(cx-2,cy+7),(cx+9,cy-7)],fill=(15,15,20),width=5)
    else: d.line([(cx-7,cy-7),(cx+7,cy+7)],fill=(15,15,20),width=5); d.line([(cx-7,cy+7),(cx+7,cy-7)],fill=(15,15,20),width=5)
    d.text((x+82,y+18),text,fill=WHITE+(int(255*alpha),),font=f)

def card(lines,frames,sub=None,fade=12):
    for i in range(frames):
        a=min(1,i/fade,(frames-1-i)/fade)
        im=Image.new("RGB",(W,H),DIM); d=ImageDraw.Draw(im)
        y=H//2-sum(sz*1.45 for _,sz,_ in lines)/2
        for j,(txt,sz,col) in enumerate(lines):
            f=font(sz); tw=d.textlength(txt,font=f)
            c=tuple(int(v*a+DIM[k]*(1-a)) for k,v in enumerate(col))
            d.text(((W-tw)/2,y),txt,fill=c,font=f); y+=sz*1.45
        emit(im)

# ---------- INTRO ----------
card([("PACO",120,(233,245,58)),("Así se ve tu partido analizado",78,WHITE),("Un punto real · Mundial FIP 2024 · reconstruido por IA",40,(170,175,190))],72)

# ---------- CLIP part 1 ----------
F1,F2=233,417
for i in range(1,F1+1): link(i)

# ---------- FREEZE 1: shot selection ----------
base=Image.open(f"src/{F1:05d}.jpg").convert("RGBA")
P0,PC,P1=(1362,395),(1750,325),(2100,385)   # actual volley -> right rival
G0,GC,G1=(1362,395),(1540,355),(1730,418)   # better: drop to the middle, near the net
for i in range(135):
    im=base.copy(); ov=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    tr=ease((i-5)/25); tg=ease((i-55)/30); pulse=0.5+0.5*math.sin(i/4)
    if i>=3: pill(d,(740,40),"ERROR 1 · SELECCIÓN DE TIRO",RED)
    if i>=55: pill(d,(740,112),"MEJOR OPCIÓN",GREEN)
    def draw(dd):
        if tr>0: curve(dd,P0,PC,P1,tr,RED+(255,),9)
        if tr>=1: ring(dd,P1,48+12*pulse,RED+(230,),6); mark(dd,(P1[0],P1[1]-70),False)
        if tg>0: curve(dd,G0,GC,G1,tg,GREEN+(255,),9,dash=3)
        if tg>=1: ring(dd,G1,55+14*pulse,GREEN+(230,),6); mark(dd,(G1[0],G1[1]+70),True)
    glow(im,draw)
    caption(d,870,"Volea al cuerpo del rival: llega cómodo y devuelve",False,ease((i-30)/10))
    caption(d,960,"Bajada al medio, corta: ninguno de los dos llega",True,ease((i-85)/10))
    im.alpha_composite(ov); emit(im.convert("RGB"))

# ---------- CLIP part 2 ----------
for i in range(F1+1,F2+1): link(i)

# ---------- FREEZE 2: positioning ----------
base=Image.open(f"src/{F2:05d}.jpg").convert("RGBA")
WL,WR=(1404,616),(1611,633)          # where they are (glued to the net)
GL,GR=(1350,712),(1600,748)          # one step back
for i in range(135):
    im=base.copy(); ov=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    tr=ease((i-5)/20); tg=ease((i-50)/30); pulse=0.5+0.5*math.sin(i/4)
    if i>=3: pill(d,(740,40),"ERROR 2 · POSICIÓN",RED)
    if i>=50: pill(d,(740,112),"MEJOR OPCIÓN",GREEN)
    def draw(dd):
        if tr>0:
            for c in (WL,WR): ring(dd,c,(60+14*pulse)*tr,RED+(230,),7)
            if tr>=1: mark(dd,(WL[0]-90,WL[1]),False); mark(dd,(WR[0]+90,WR[1]),False)
        if tg>0:
            for a,b in ((WL,GL),(WR,GR)):
                e=(a[0]+(b[0]-a[0])*tg, a[1]+(b[1]-a[1])*tg)
                dd.line([a,e],fill=GREEN+(255,),width=8)
                if tg>=1:
                    ang=math.atan2(b[1]-a[1],b[0]-a[0])
                    dd.polygon([b,(b[0]-30*math.cos(ang-0.5),b[1]-30*math.sin(ang-0.5)),(b[0]-30*math.cos(ang+0.5),b[1]-30*math.sin(ang+0.5))],fill=GREEN+(255,))
                    ring(dd,b,60+14*pulse,GREEN+(230,),7)
            if tg>=1: mark(dd,(GL[0]-90,GL[1]),True); mark(dd,(GR[0]+90,GR[1]),True)
    glow(im,draw)
    caption(d,870,"Los dos pegados a la red: el globo pasa por encima",False,ease((i-25)/10))
    caption(d,960,"Un paso atrás y en diagonal: el globo se defiende",True,ease((i-80)/10))
    im.alpha_composite(ov); emit(im.convert("RGB"))

# ---------- CLIP part 3 ----------
for i in range(F2+1,493): link(i)

# ---------- OUTRO ----------
card([("PACO",120,(233,245,58)),("Tu partido. Tus errores. Cómo corregirlos.",78,WHITE),("Video de 10-15 min + estadísticas + informe, 24 h después de jugar",40,(170,175,190)),("Los primeros 100 reciben el análisis de un partido gratis",52,GREEN)],111)
print("frames",n[0])
