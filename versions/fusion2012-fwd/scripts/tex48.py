"""Cinco cintas de reboque (64×256 cada, DXT1) gravadas numa área livre do atlas das cintas:
 1 preta com 大吉大利 vermelho   2 vermelha com 出入平安 branco   3 laranja com 一路顺风 preto
 4 azul com F B I amarelo (uma letra embaixo da outra)   5 zebrada preta e amarela (fita de contenção), sem texto
2012 (<CARRO>_KIT00_HEADLIGHT_OFF): x 512, 576, 640, 704, 768 na linha y 768.
2018 (<CARRO>_LOGO): x 768, 832, 896, 960 na linha y 0 e x 768 na linha y 256.
Uso: tex48.py TEXTURES.BIN atlas.dds CARRO out"""
import sys;sys.path.insert(0,'/home/claude/c12')
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from strap_tex import strap,dxt1_encode
SLOTS={'COBALTSS':[(512,768),(576,768),(640,768),(704,768),(768,768)],
       'MUSTANGGT':[(768,0),(832,0),(896,0),(960,0),(768,256)]}
def fbi(W=64,H=256):
    im=strap((22,52,150),(250,215,20),'')
    d=ImageDraw.Draw(im); f=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc',58,index=0)
    y=30
    for ch in 'FBI':
        bb=d.textbbox((0,0),ch,font=f); w=bb[2]-bb[0]
        d.text(((W-w)/2-bb[0],y-bb[1]),ch,font=f,fill=(250,215,20)); y+=72
    return im
def zebra(W=64,H=256,period=64):
    yy,xx=np.mgrid[0:H,0:W]; band=((yy+xx)//(period//2))%2
    a=np.where(band[...,None]==0,np.array([28,26,10]),np.array([245,215,20])).astype(np.uint8)
    return Image.fromarray(a)
def designs():
    return [strap((18,18,18),(205,20,20),'大吉大利'),strap((190,18,18),(245,240,235),'出入平安'),
            strap((235,118,18),(15,12,10),'一路顺风'),fbi(),zebra()]
def patch(texbin,ddsfile,car,out):
    b=bytearray(open(texbin,'rb').read()); d=open(ddsfile,'rb').read(); off=b.find(d[128:]); assert off>0 and b.count(d[128:])==1
    W=int.from_bytes(d[16:20],'little'); assert int.from_bytes(d[84:88],'little')==0x31545844
    rowbytes=(W//4)*8; ims=designs()
    for img,(x0,y0) in zip(ims,SLOTS[car]):
        enc=dxt1_encode(img); bw=img.size[0]//4
        for r in range(img.size[1]//4):
            src=enc[r*bw*8:(r+1)*bw*8]; dst=off+((y0//4)+r)*rowbytes+(x0//4)*8; b[dst:dst+len(src)]=src
    open(out,'wb').write(b)
    o=Image.new('RGB',(5*64+40,256),'white')
    for i,im in enumerate(ims): o.paste(im,(i*72,0))
    o.save(out+'.cintas.png')
if __name__=='__main__': patch(*sys.argv[1:5])
