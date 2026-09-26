import sys,pickle,numpy as np
sys.path.insert(0,'lib'); import mwsoup,geo
from scipy.spatial import cKDTree
P=geo.load('z10.dump')
body=[p for p in P if p['name']=='MUSTANGGT_KIT00_BODY_A'][0]
hood=[p for p in P if p['name']=='MUSTANGGT_KIT00_HOOD_A'][0]
T=np.concatenate([body['v']['p'],hood['v']['p']]).astype(float)
S=pickle.load(open('gta/oracle_soup.pkl','rb'))
paint=np.unique(S['F'][S['shader']==0])
G=S['P'][paint]
# initial: wheels. Mondeo wheel_lf y=1.588 z=-0.253 ; wheel_lr y=-1.353 z=-0.292
sx=(1.425+1.305)/(1.588+1.353); tx=1.425-1.588*sx
M0=np.c_[G[:,1]*sx+tx,-G[:,0],G[:,2]+0.27+0.15]
def fit(src,dst,w=None):
    # affine with diag scale + rotation (solve general affine then keep)
    A=np.c_[src,np.ones(len(src))]
    X,*_=np.linalg.lstsq(A,dst,rcond=None); return X
def icp(src,T,iters=40,region=None,affine='scale'):
    tree=cKDTree(T); cur=src.copy(); X_total=np.eye(4)
    for it in range(iters):
        d,j=tree.query(cur); thr=np.percentile(d,80)
        m=d<thr
        if region is not None: m&=region(cur)
        A=np.c_[cur[m],np.ones(m.sum())]; B=T[j[m]]
        if affine=='scale':
            # per-axis scale + translation only (no rotation)
            X=np.zeros((4,3))
            for k in range(3):
                a=np.c_[cur[m,k],np.ones(m.sum())]; s,t=np.linalg.lstsq(a,B[:,k],rcond=None)[0]
                X[k,k]=s; X[3,k]=t
        else:
            X,*_=np.linalg.lstsq(A,B,rcond=None)
        cur=np.c_[cur,np.ones(len(cur))]@X
        H=np.eye(4); H[:3,:3]=X[:3].T; H[:3,3]=X[3]; X_total=H@X_total
    d,j=tree.query(cur)
    return X_total,cur,d
H,cur,d=icp(M0,T,affine='scale')
print('global scale-only: median dist %.4f p90 %.4f'%(np.median(d),np.percentile(d,90)))
print(np.round(H,4))
Hf,curf,df=icp(M0,T,affine='full')
print('global affine: median %.4f p90 %.4f'%(np.median(df),np.percentile(df,90))); print(np.round(Hf,4))
pickle.dump(dict(sx=sx,tx=tx,H=H,Hf=Hf),open('align0.pkl','wb'))
# per region stats
for nm,f in [('front',lambda c:c[:,0]>1.3),('rear',lambda c:c[:,0]<-1.5),('mid',lambda c:abs(c[:,0])<1)]:
    m=f(curf); print(nm,'median %.4f p90 %.4f'%(np.median(df[m]),np.percentile(df[m],90)))
