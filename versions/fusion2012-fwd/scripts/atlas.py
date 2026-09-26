import numpy as np
from PIL import Image
D='/mnt/user-data/uploads/fusion-mw2005/source/fusion-2016-dev/DEV Version/FordFusion/'
fari=np.asarray(Image.open(D+'fari.PNG').convert('RGBA')).astype(np.float32)
red=np.asarray(Image.open(D+'redglass.png').convert('RGBA')).astype(np.float32)
old=np.asarray(Image.open('z10tex/95DE5B23.dds').convert('RGBA').resize((512,512),Image.LANCZOS)).astype(np.float32)
print('fari alpha',fari[...,3].min(),fari[...,3].mean(),'red alpha',red[...,3].min(),red[...,3].mean(), 'red rgb mean',red[...,:3].mean((0,1)))
CELLS={'black':((0,0),(16,16,18,255),(16,16,18,255)),
       'chrome':((1,0),(196,198,204,255),(196,198,204,255)),
       'clear':((2,0),(215,222,230,255),(215,222,230,70)),
       'smoke':((3,0),(35,38,44,255),(35,38,44,200)),
       'white':((0,1),(235,235,235,255),(235,235,235,255)),
       'amber':((1,1),(255,140,20,255),(255,140,20,190)),
       'red':((2,1),(170,10,12,255),(170,10,12,215)),
       'dkgray':((3,1),(60,62,66,255),(60,62,66,255))}
def cell_uv(name):
    (i,j),_,_=CELLS[name]; return (0.5+0.125*i+0.0625, 0.5+0.125*j+0.0625)
def build():
    A=np.zeros((1024,1024,4),np.float32); A[...,3]=255
    red2=red.copy(); red2[...,:3]=np.clip(red[...,:3]*1.75+np.array([0,8,8]),0,255)
    A[0:512,0:512]=old; A[0:512,512:1024]=fari; A[512:1024,0:512]=red2
    B=A.copy()
    A[...,3]=255
    B[0:512,512:1024,3]=255
    B[512:1024,0:512,3]=190
    for name,((i,j),ca,cb) in CELLS.items():
        y0=512+128*j; x0=512+128*i
        A[y0:y0+128,x0:x0+128]=ca; B[y0:y0+128,x0:x0+128]=cb
    # chrome cell with a soft vertical gradient (reads as metal)
    g=np.linspace(1.12,0.78,128)[:,None,None]
    A[512:640,640:768,:3]=np.clip(np.array([196,198,204])*g,0,255); B[512:640,640:768,:3]=A[512:640,640:768,:3]
    return A.astype(np.uint8),B.astype(np.uint8)
if __name__=='__main__':
    A,B=build()
    Image.fromarray(A).save('tex/atlasA.png'); Image.fromarray(B).save('tex/atlasB.png')
    import sys; sys.path.insert(0,'/home/claude/v3/versions/v1prime/scripts'); import dxt
    dxt.write_dds_dxt1('z10tex/95DE5B23.dds','tex/HEADLIGHT_OFF.dds',A)
    dxt.write_dds_like('z10tex/95DE5B23.dds','tex/BRAKELIGHT_OFF.dds',B)
    print('ok')
