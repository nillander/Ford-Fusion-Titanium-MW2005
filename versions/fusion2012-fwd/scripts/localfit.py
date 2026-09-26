from common import *
from scipy.spatial import cKDTree
L=pickle.load(open('mondeo_lampsel.pkl','rb')); sel=L['sel']
M=S['M']; F=S['F']; sh=S['shader']; C=M[F].mean(1)
body=[p for p in Z if p['name'] in ('MUSTANGGT_KIT00_BODY_A','MUSTANGGT_KIT00_HOOD_A')]
T=np.concatenate([p['v']['p'] for p in body]).astype(float)
tree=cKDTree(T)
paintv=np.unique(F[sh==0]); PV=M[paintv]
fits={}
for k in ['headL','headR','tailL','tailR','fogL','fogR']:
    lamp_c=M[np.unique(F[sel[k]])]
    lo=lamp_c.min(0)-0.25; hi=lamp_c.max(0)+0.25
    m=np.all((PV>lo)&(PV<hi),1)
    src=PV[m]
    # exclude points very near lamp (inside opening edges)
    X=np.eye(4)
    cur=src.copy()
    for it in range(30):
        d,j=tree.query(cur); thr=min(np.percentile(d,85),0.03); w=d<thr
        A=np.c_[cur[w],np.ones(w.sum())]; Bt=T[j[w]]
        # translation + per-axis scale around lamp centre (robust, small)
        c0=cur[w].mean(0); c1=Bt.mean(0)
        t=c1-c0
        H=np.eye(4); H[:3,3]=t
        cur=cur+t; X=H@X
    d,j=tree.query(cur)
    d0,_=tree.query(src)
    print(k,'n',len(src),'before med %.4f after med %.4f p80 %.4f'%(np.median(d0),np.median(d),np.percentile(d,80)),'t',np.round(X[:3,3],4))
    fits[k]=X
pickle.dump(fits,open('localfit.pkl','wb'))
