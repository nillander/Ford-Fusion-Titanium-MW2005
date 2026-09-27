import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
from xray import xcast
def faces(p,gsel=None):
    F=[]
    for gi,g in enumerate(p['groups']):
        if gsel is not None and not gsel(gi,p['tex'][g['tex'][0]]): continue
        seg=p['idx'][g['offset']:g['offset']+g['length']].astype(int); F.append(seg[:len(seg)//3*3].reshape(-1,3))
    return p['v']['p'].astype(float),(np.concatenate(F) if F else np.zeros((0,3),int))
def sub(P,F):
    C=P[F].mean(1); m=(C[:,0]>1.7)&(C[:,2]>0.2)&(C[:,2]<0.8)&(np.abs(C[:,1])<0.8); return P,F[m]
def maps(path,car,L='A'):
    Z={p['name']:p for p in geo.load(path)}
    ys=np.arange(-0.62,0.6201,0.005); zs=np.arange(0.28,0.68,0.005); YY,ZZ=np.meshgrid(ys,zs); Q=np.c_[YY.ravel(),ZZ.ravel()]
    def cast(parts,mode='max'):
        r=[xcast(*sub(*pf),Q,mode) for pf in parts]; r=np.stack(r)
        if mode=='max': r=np.where(np.isnan(r),-9,r).max(0); r[r<-8]=np.nan
        else: r=np.where(np.isnan(r),9,r).min(0); r[r>8]=np.nan
        return r.reshape(YY.shape)
    skinp=[faces(Z[f'{car}_KIT00_BODY_{L}']),faces(Z[f'{car}_KIT00_HOOD_{L}'])]+[faces(Z[n]) for n in Z if n.endswith('_'+L) and 'KIT00' in n and 'LIGHT' in n]
    gr=[faces(Z[f'{car}_BASE_{L}'],lambda gi,t: t in (0xE67A7FA5,0x5A00E244,0xE67A0B4A,0x5A006DE9))]
    if L=='A': gr.append(faces(Z[f'{car}_KIT00_RIGHT_SIDE_MIRROR_A']))
    return ys,zs,cast(skinp),cast(gr),cast(gr,'min'),Z
if __name__=='__main__':
    ys,zs,xs,xg,xgm,Z=maps(sys.argv[1],sys.argv[2])
    np.savez(sys.argv[3],ys=ys,zs=zs,xs=xs,xg=xg,xgm=xgm)
    for iz in range(len(zs)-1,-1,-4):
        print('%.3f '%zs[iz]+''.join(' ' if np.isnan(xs[iz,j]) else ('#' if not np.isnan(xg[iz,j]) and xg[iz,j]>xs[iz,j]-0.005 else '.') for j in range(0,len(ys),3)))
