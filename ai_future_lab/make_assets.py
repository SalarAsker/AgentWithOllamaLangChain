"""Generera stiliserade lokala affischbilder; inga externa bildtjänster behövs."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random
from careers import CAREERS

OUT=Path(__file__).parent/'assets'
OUT.mkdir(exist_ok=True)
W,H=1000,750
font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
if not Path(font_path).exists():
    font_path='C:/Windows/Fonts/arialbd.ttf'
try:
    font_big=ImageFont.truetype(font_path,64)
    font_small=ImageFont.truetype(font_path,27)
except OSError:
    font_big=ImageFont.load_default();font_small=ImageFont.load_default()

def rgb(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def build(key,title,c1,c2,idx):
    random.seed(idx+123)
    a,b=rgb(c1),rgb(c2)
    im=Image.new('RGB',(W,H)); pix=im.load()
    for y in range(H):
        for x in range(W):
            t=y/H
            radial=max(0,1-math.hypot((x-W*.68)/W,(y-H*.4)/H)*1.3)
            pix[x,y]=tuple(int(min(255,8+(a[k]*.24+b[k]*.20)*radial + (a[k]*.11+b[k]*.13)*t)) for k in range(3))
    d=ImageDraw.Draw(im,'RGBA')
    for _ in range(65):
        x=random.randint(0,W);y=random.randint(0,H)
        r=random.randint(1,3)
        d.ellipse((x-r,y-r,x+r,y+r),fill=(180,220,255,random.randint(50,180)))
    # futuristic city / technology skyline
    for i in range(18):
        x=i*60+random.randint(-10,10)
        h=random.randint(90,260)
        d.rounded_rectangle((x,H-115-h,x+random.randint(35,75),H-80),radius=5,fill=(*a,55),outline=(*a,110),width=2)
        for yy in range(H-110-h,H-100,28):
            d.line((x+12,yy,x+28,yy),fill=(*b,170),width=3)
    # circular hologram rings
    cx,cy=690,300
    for r in (90,140,200,248):
        d.arc((cx-r,cy-r,cx+r,cy+r),15+idx*9,315+idx*9,fill=(*a,180),width=5)
    for angle in range(0,360,30):
        rad=math.radians(angle+idx*13)
        x=cx+210*math.cos(rad);y=cy+210*math.sin(rad)
        d.ellipse((x-5,y-5,x+5,y+5),fill=(*b,240))
    # distinctive geometric hologram symbol
    n=5+(idx%4)
    pts=[(cx+110*math.cos(2*math.pi*i/n-.5),cy+110*math.sin(2*math.pi*i/n-.5)) for i in range(n)]
    d.polygon(pts,fill=(*b,65),outline=(*a,255),width=7)
    d.ellipse((cx-48,cy-48,cx+48,cy+48),outline=(*b,255),width=8)
    d.line((cx-55,cy,cx+55,cy),fill=(240,250,255,230),width=5)
    d.line((cx,cy-55,cx,cy+55),fill=(240,250,255,230),width=5)
    d.rounded_rectangle((42,45,350,93),radius=18,fill=(10,19,45,180),outline=(*a,180),width=2)
    d.text((62,56),'AI FUTURE LAB 2035',font=font_small,fill=(224,244,255))
    d.rounded_rectangle((42,560,958,708),radius=23,fill=(7,14,34,225),outline=(*a,180),width=3)
    d.text((68,580),title,font=font_big,fill=(244,248,255),stroke_width=1)
    d.text((70,667),'FRAMTIDEN ÄR DIN ATT SKAPA',font=font_small,fill=(174,207,242))
    im.save(OUT/(key+'.png'),optimize=True)

for i,(key,c) in enumerate(CAREERS.items()):
    build(key,c['title'],*c['colors'],i)
build('cover','UPPTÄCK DIN FRAMTID','#00d4ff','#ad5cff',99)
print('Created',len(CAREERS)+1,'images')
