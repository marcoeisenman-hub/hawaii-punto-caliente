import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
random.seed(7)
S=2                       # supermuestreo
W,H=7087*S,591*S          # 60 x 5 cm a 300 ppp
im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
MAR=int(250*S); FON=int(468*S)
def grad(y0,y1,c0,c1):
    for y in range(y0,y1):
        t=(y-y0)/max(1,y1-y0); d.line([(0,y),(W,y)],fill=tuple(int(c0[i]+(c1[i]-c0[i])*t) for i in range(3)))
grad(0,MAR,(150,196,226),(214,233,244))           # cielo
grad(MAR,FON,(38,128,168),(10,52,86))              # mar
grad(FON,H,(70,52,40),(44,30,24))                  # corteza / manto
# pluma del manto
PX=5650*S
for k in range(60,0,-1):
    t=k/60; w=int(520*S*t+40*S)
    c=(int(150+105*(1-t)),int(60+170*(1-t)),int(10+100*(1-t)))
    d.ellipse([PX-w,FON+4*S+int(60*S*t),PX+w,H+260*S],fill=c)
def fondo(x): return FON - 10*S*math.sin(x/(900*S)) - 6*S*math.sin(x/(260*S))
def volcan(cx,w,top,rug=0,seed=0):
    pts=[]
    for x in range(int(cx-w*1.8),int(cx+w*1.8),4*S):
        r=abs(x-cx)/w; f=math.exp(-(r**2.1)*.95)
        base=fondo(x); y=base-(base-top)*f
        if rug: y+= rug*S*(abs(math.sin(x/(37*S)+seed))**.5)*f*(1 if r>.1 else .3)
        pts.append((x,y))
    return pts
def poly(pts,col):
    d.polygon([(pts[0][0],fondo(pts[0][0])+2)]+pts+[(pts[-1][0],fondo(pts[-1][0])+2)],fill=col)
# 1 atolón: volcán hundido con arrecife en anillo
a=volcan(700*S,480*S,MAR+60*S); poly(a,(92,80,70))
for cx in (700*S-330*S,700*S+330*S):
    d.polygon([(cx-90*S,MAR+60*S),(cx-40*S,MAR-6*S),(cx+40*S,MAR-6*S),(cx+90*S,MAR+60*S)],fill=(232,214,170))
    d.polygon([(cx-40*S,MAR-6*S),(cx-20*S,MAR-14*S),(cx+25*S,MAR-12*S),(cx+40*S,MAR-6*S)],fill=(70,120,50))
d.rectangle([700*S-240*S,MAR+2*S,700*S+240*S,MAR+60*S],fill=(80,190,190))   # laguna turquesa
# 2 guyot: cima plana bajo el mar
g=volcan(2000*S,430*S,MAR+20*S); g=[(x,max(y,MAR+125*S)) for x,y in g]; poly(g,(92,80,70))
# 3 isla erosionada: verde con valles y tierra roja
e=volcan(3350*S,470*S,MAR-120*S,rug=34,seed=1.3); poly(e,(88,76,66))
dent=[(x,y) for x,y in e if y<MAR]
if dent:
    d.polygon(dent+[(dent[-1][0],MAR),(dent[0][0],MAR)],fill=(46,104,40))
    for x,y in dent[::9]:
        if random.random()<.35: d.line([(x,y+6*S),(x+8*S,min(MAR,y+60*S))],fill=(150,62,30),width=5*S)
    d.line([(dent[0][0],MAR),(dent[-1][0],MAR)],fill=(225,205,160),width=5*S)
# 4 volcán escudo activo
v=volcan(4750*S,620*S,MAR-175*S); poly(v,(60,52,48))
sobre=[(x,y) for x,y in v if y<MAR]
d.polygon(sobre+[(sobre[-1][0],MAR),(sobre[0][0],MAR)],fill=(30,27,26))
cima=min(v,key=lambda p:p[1])
for k,(sgn,prof) in enumerate([(-1,14),(1,20),(-1,48),(1,60),(1,34)]):
    x0,y0=cima; path=[]
    for i in range(80):
        x=x0+sgn*i*14*S
        yy=fondo(x)-(fondo(x)-(MAR-175*S))*math.exp(-((abs(x-4750*S)/(620*S))**2.1)*.95)
        yy+= prof*S*min(1,i/8) + 6*S*math.sin(i*.9+k)
        if yy>=MAR-2*S: path.append((x,MAR)); break
        path.append((x,yy))
    if len(path)>2:
        d.line(path,fill=(200,60,10),width=13*S); d.line(path,fill=(255,140,30),width=8*S); d.line(path,fill=(255,225,120),width=3*S)
d.ellipse([cima[0]-26*S,cima[1]-8*S,cima[0]+26*S,cima[1]+10*S],fill=(255,170,60))
for i in range(14):                                           # humo
    r=(24+i*7)*S; x=cima[0]-i*28*S; y=cima[1]-20*S-i*9*S
    d.ellipse([x-r,y-r*.7,x+r,y+r*.7],fill=(150+i*4,148+i*4,146+i*4))
# 5 volcán submarino joven
s=volcan(6300*S,330*S,MAR+95*S); poly(s,(70,60,54))
sc=min(s,key=lambda p:p[1])
for i in range(16):
    x=sc[0]+random.uniform(-30,30)*S; y=sc[1]-random.uniform(10,170)*S
    if y>MAR+6*S: r=random.uniform(4,9)*S; d.ellipse([x-r,y-r,x+r,y+r],outline=(210,240,255),width=2*S)
# conductos de magma
for tx,ty in ((cima[0],cima[1]+10*S),(sc[0],sc[1]+6*S)):
    d.line([(PX+(tx-PX)*.25,FON+20*S),(tx,ty)],fill=(255,110,20),width=7*S); d.line([(PX+(tx-PX)*.25,FON+20*S),(tx,ty)],fill=(255,210,110),width=2*S)
# línea del mar
d.line([(0,MAR),(W,MAR)],fill=(230,245,250),width=3*S)
im=im.resize((W//S,H//S),Image.LANCZOS); d=ImageDraw.Draw(im)
F='/System/Library/Fonts/Supplemental/'
fb=ImageFont.truetype(F+'Arial Bold.ttf',44); fr=ImageFont.truetype(F+'Arial.ttf',34); ft=ImageFont.truetype(F+'Arial Bold.ttf',52)
def etq(x,y,t1,t2,col=(15,47,69)):
    w1=d.textlength(t1,font=fb); w2=d.textlength(t2,font=fr)
    d.text((x-w1/2,y),t1,font=fb,fill=col); d.text((x-w2/2,y+50),t2,font=fr,fill=col)
etq(700,40,'Atolón','arrecife de coral en anillo')
etq(2000,40,'Monte submarino','se hundió y se aplanó')
etq(3350,40,'Isla erosionada','la lluvia talla valles')
etq(5600,40,'Volcán escudo','sobre el punto caliente')
etq(6420,140,'Volcán submarino','está naciendo',(255,255,255))
d.text((60,300),'MÁS VIEJO',font=fb,fill=(255,255,255))
t='MÁS JOVEN'; d.text((7087-60-d.textlength(t,font=fb),300),t,font=fb,fill=(255,255,255))
t='←  La placa del Pacífico se mueve al noroeste'; d.text((120,505),t,font=ft,fill=(255,236,214))
t='Punto caliente (fijo)'; d.text((5650+260,525),t,font=fb,fill=(255,236,214))
d.text((2650,505),'La vida de una isla hawaiana',font=ft,fill=(255,236,214))
im.save('dibujo_completo.png')
# 4 piezas de 15 x 5 cm
pw=7087//4+1
for i in range(4):
    p=im.crop((i*pw,0,min(7087,(i+1)*pw),591)); c=Image.new('RGB',(p.width+0,p.height),'white'); c.paste(p,(0,0))
    dd=ImageDraw.Draw(c); dd.text((10,560),f'pieza {i+5}',font=ImageFont.truetype(F+'Arial.ttf',22),fill=(255,255,255))
    c.save(f'pieza{i+5}.png')
print(im.size)
