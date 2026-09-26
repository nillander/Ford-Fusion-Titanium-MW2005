from common import *
from scipy.spatial import cKDTree
M=S['M']; F=S['F']; sh=S['shader']; C=M[F].mean(1)
LS=pickle.load(open('mondeo_lampsel.pkl','rb')); kinv=LS['kinv']
tri=M[F]
uniq=np.zeros(len(F),bool); _,first=np.unique(kinv,return_index=True); uniq[first]=True
pt=cKDTree(M[np.unique(F[sh==0])])
# distance of triangle's 3 verts to paint verts (max)
dv,_=pt.query(M); dmax=dv[F].min(1)
def fogbox(s): return (C[:,0]>1.8)&(C[:,2]>0.12)&(C[:,2]<0.47)&(C[:,1]*s>0.45)
out={}
for s,nm in ((1,'L'),(-1,'R')):
    b=fogbox(s)&uniq
    pocket=b&(sh==4)&(dmax>0.003)
    parts=b&np.isin(sh,[9,10,14,15])
    out['fog'+nm]=pocket|parts
    print(nm,pocket.sum(),parts.sum())
if __name__=='__main__':
    col,tid=mcol(S)
    ims=[]
    for m in (np.ones(len(F),bool)&fogbox(1),out['fogL']):
        a,_=rast.render(M,F[m],col[m],uv=S['UV'],texid=tid[m],textures=[FARI,RED],az=15,el=5,W=700,H=420,center=(2.05,0.72,0.3),scale=1300,bg=(0.2,0.5,0.2))
        ims.append(Image.fromarray(a))
    row(ims,'fogsel.png')
    pickle.dump(out,open('fogsel.pkl','wb'))
from visible import visible
for s,nm in ((1,'L'),(-1,'R')):
    box=fogbox(s)
    c=M[F[box]].mean((0,1))
    vis=visible(M,F,[(a*s,e) for a in (0,20,40,60) for e in (-10,5,20)],center=c,scale=3500)
    out['fog'+nm]&=vis
    print(nm,'visible',out['fog'+nm].sum())
pickle.dump(out,open('fogsel.pkl','wb'))
col,tid=mcol(S); m=out['fogL']
a,_=rast.render(M,F[m],col[m],uv=S['UV'],texid=tid[m],textures=[FARI,RED],az=15,el=5,W=700,H=420,center=(2.05,0.72,0.3),scale=1300,bg=(0.2,0.5,0.2))
Image.fromarray(a).save('fogsel2.png')
from scipy import ndimage
for s,nm in ((1,'L'),(-1,'R')):
    az=18*s; ctr=np.array([2.05,0.72*s,0.3]); sc=1300
    paint=(sh==0)
    col1=np.ones((len(F),3),np.float32)
    _,ids=rast.render(M,F,col1,az=az,el=5,W=700,H=420,center=ctr,scale=sc,shade=False)
    ispaint=np.zeros(ids.shape,bool); v=ids>=0; ispaint[v]=paint[ids[v]]
    lens=out['fog'+nm]&(sh==15)
    # pixel of lens centre
    R,d=rast.view(az,5); cam=(M[F[lens]].mean((0,1)))@R.T; c0=ctr@R.T
    px=int(350+(cam[0]-c0[0])*sc); py=int(210-(cam[1]-c0[1])*sc)
    lab,_=ndimage.label(~ispaint)
    comp=lab==lab[py,px]
    comp=ndimage.binary_dilation(comp,iterations=3)
    # project candidate centroids
    cc=C@R.T; X=(350+(cc[:,0]-c0[0])*sc).astype(int); Y=(210-(cc[:,1]-c0[1])*sc).astype(int)
    ok=(X>=0)&(X<700)&(Y>=0)&(Y<420); inside=np.zeros(len(F),bool); inside[ok]=comp[Y[ok],X[ok]]
    out['fog'+nm]&=inside
    print(nm,'in pocket',out['fog'+nm].sum(), 'pix',comp.sum())
pickle.dump(out,open('fogsel.pkl','wb'))
m=out['fogL']
a,_=rast.render(M,F[m],col[m],uv=S['UV'],texid=tid[m],textures=[FARI,RED],az=15,el=5,W=700,H=420,center=(2.05,0.72,0.3),scale=1300,bg=(0.2,0.5,0.2))
m=out['fogR']
b,_=rast.render(M,F[m],col[m],uv=S['UV'],texid=tid[m],textures=[FARI,RED],az=-15,el=5,W=700,H=420,center=(2.05,-0.72,0.3),scale=1300,bg=(0.2,0.5,0.2))
row([Image.fromarray(a),Image.fromarray(b)],'fogsel3.png')
