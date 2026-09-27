"""Texturas das cintas de reboque (item 35), gravadas numa área livre do atlas <CARRO>_KIT00_HEADLIGHT_OFF (DXT1):
colunas 512–639, linhas 768–1023 (u 0,50–0,625, v 0,75–1,0), 64×256 px cada:
- cinta 1 (u 0,50–0,5625): preta com 大吉大利 bordado em vermelho;
- cinta 2 (u 0,5625–0,625): vermelha com 出入平安 em branco.
Costuras claras nas bordas; texto na fonte Noto Sans CJK JP Black."""
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
def strap(bg,fg,txt,W=64,H=256,size=44,step=54,y0=24):
    im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im)
    # woven texture
    a=np.asarray(im).astype(float); yy=np.arange(H)[:,None,None]; a*=1+0.06*((yy%4)<2); im=Image.fromarray(np.clip(a,0,255).astype(np.uint8)); d=ImageDraw.Draw(im)
    st=tuple(min(255,int(c*0.6+100)) for c in bg)
    for x in (3,W-4): 
        for y in range(4,H-4,6): d.line([(x,y),(x,y+3)],fill=st)
    f=ImageFont.truetype(FONT,size,index=0)
    y=y0
    for ch in txt:
        bb=d.textbbox((0,0),ch,font=f); w=bb[2]-bb[0]
        d.text(((W-w)/2-bb[0],y-bb[1]),ch,font=f,fill=fg); y+=step
    return im
def atlas_patch():
    s1=strap((18,18,18),(205,20,20),'大吉大利'); s2=strap((190,18,18),(245,240,235),'出入平安')
    o=Image.new('RGB',(128,256)); o.paste(s1,(0,0)); o.paste(s2,(64,0)); return o
def dxt1_encode(img):
    a=np.asarray(img).astype(np.float32); H,W,_=a.shape; out=bytearray()
    def to565(c): c=np.clip(np.round(c),0,255).astype(int); return ((c[0]>>3)<<11)|((c[1]>>2)<<5)|(c[2]>>3)
    def from565(v): return np.array([((v>>11)&31)*255/31,((v>>5)&63)*255/63,(v&31)*255/31])
    for by in range(0,H,4):
        for bx in range(0,W,4):
            blk=a[by:by+4,bx:bx+4].reshape(16,3); m=blk.mean(0); u,sv,vt=np.linalg.svd(blk-m); ax=vt[0]
            t=(blk-m)@ax; c0=m+ax*t.max(); c1=m+ax*t.min()
            e0,e1=to565(c0),to565(c1)
            if e0<e1: e0,e1=e1,e0
            if e0==e1:
                out+=np.array([e0,e1],'<u2').tobytes()+b'\0\0\0\0'; continue
            p0,p1=from565(e0),from565(e1); pal=np.array([p0,p1,(2*p0+p1)/3,(p0+2*p1)/3])
            idx=((blk[:,None,:]-pal[None])**2).sum(2).argmin(1); bits=0
            for i,k in enumerate(idx): bits|=int(k)<<(2*i)
            out+=np.array([e0,e1],'<u2').tobytes()+np.array([bits],'<u4').tobytes()
    return bytes(out)
def patch(texbin_path,ddsfile,out_path,x0=512,y0=768):
    b=bytearray(open(texbin_path,'rb').read()); d=open(ddsfile,'rb').read(); off=b.find(d[128:]); assert off>0 and b.count(d[128:])==1, 'data not unique'
    W=int.from_bytes(d[16:20],'little'); assert int.from_bytes(d[84:88],'little')==0x31545844  # DXT1
    img=atlas_patch(); enc=dxt1_encode(img); bw=img.size[0]//4; rowbytes=(W//4)*8
    for r in range(img.size[1]//4):
        src=enc[r*bw*8:(r+1)*bw*8]; dst=off+((y0//4)+r)*rowbytes+(x0//4)*8
        b[dst:dst+len(src)]=src
    open(out_path,'wb').write(b); img.save('build/strap_tex.png')
if __name__=='__main__':
    import sys; patch(*sys.argv[1:4])
