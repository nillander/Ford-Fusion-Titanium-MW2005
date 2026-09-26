"""Item 29 (Fusion 2012): faróis "para dentro da carroceria".
Em cortes transversais o farol fica afundado: a borda de baixo da lente está 2–6 cm abaixo da lataria logo abaixo
(para-choque/paralama, com um degrau), e a de cima 1–2 cm abaixo da borda do capô. O farol inteiro (lente, interior,
LODs A–D) é empurrado para fora ao longo da normal média da lente, com deslocamento próprio em cada ponta:
- para cada fatia de 1 cm ao longo do farol (u): alvo em baixo = ponto mais externo da lataria 0,5–3,5 cm abaixo da
  lente; alvo em cima = idem acima (capô); deslocamento = alvo − lente − 3 mm (0 a 6 cm), suavizado ao longo de u;
- cada vértice recebe a interpolação linear entre o deslocamento de cima e o de baixo pela sua posição na altura."""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo,pickle
from partmesh import PartMesh
from bulge import samp,allF
from scipy.ndimage import gaussian_filter1d
CLEAR=0.003; DMAX=0.06; TOPK=float(__import__('os').environ.get('TOPK','1.0'))
def frame(gl):
    F=allF(gl); X=gl.P; F=F[X[F].mean(1)[:,2]>0.35]
    fn=np.cross(X[F[:,1]]-X[F[:,0]],X[F[:,2]]-X[F[:,0]]); n=fn.sum(0); n/=np.linalg.norm(n)
    if n[0]<0: n=-n
    a=np.cross(n,[0,0,1.]); a/=np.linalg.norm(a); b=np.cross(n,a); c0=X[np.unique(F)].mean(0)
    return F,n,a,b,c0
def field(gl,bodies,verbose=''):
    F,n,a,b,c0=frame(gl); pr=lambda Y: np.c_[(Y-c0)@a,(Y-c0)@b,(Y-c0)@n]
    L=pr(samp(gl.P,F,30)); B=np.concatenate([pr(samp(pm.P,allF(pm)[np.linalg.norm(pm.P[allF(pm)].mean(1)-c0,axis=1)<0.5],4)) for pm in bodies])
    B=B[np.abs(B[:,2])<0.15]
    us=np.arange(L[:,0].min(),L[:,0].max()+1e-9,0.01)
    rows=[]
    for u in us:
        l=L[np.abs(L[:,0]-u)<0.006]
        if len(l)<10: rows.append((np.nan,)*6); continue
        i0,i1=l[:,1].argmin(),l[:,1].argmax(); bmin,bmax=l[i0,1],l[i1,1]; nmin,nmax=l[i0,2],l[i1,2]
        bb=B[np.abs(B[:,0]-u)<0.006]
        lo=bb[(bb[:,1]>bmax+0.005)&(bb[:,1]<bmax+0.035)]; hi=bb[(bb[:,1]<bmin-0.005)&(bb[:,1]>bmin-0.035)]
        dlo=(lo[:,2].max()-nmax-CLEAR) if len(lo) else np.nan; dhi=(hi[:,2].max()-nmin-CLEAR) if len(hi) else np.nan
        rows.append((bmin,bmax,nmin,nmax,dhi,dlo))
    R=np.array(rows)
    for k in range(6):
        bad=np.isnan(R[:,k])
        if bad.all(): R[:,k]=0
        elif bad.any(): R[bad,k]=np.interp(us[bad],us[~bad],R[~bad,k])
    R[:,4:]=np.clip(R[:,4:],0,DMAX); R[:,4]=TOPK*gaussian_filter1d(R[:,4],3,mode='nearest'); R[:,5]=gaussian_filter1d(R[:,5],3,mode='nearest')
    if verbose: print(verbose,'desloc. em cima: mediana %.3f max %.3f | em baixo: mediana %.3f max %.3f'%(np.median(R[:,4]),R[:,4].max(),np.median(R[:,5]),R[:,5].max()))
    def disp(Y):
        Q=pr(Y); bm=np.interp(Q[:,0],us,R[:,0]); bM=np.interp(Q[:,0],us,R[:,1]); t=np.clip((Q[:,1]-bm)/np.maximum(bM-bm,1e-6),0,1)
        d=np.interp(Q[:,0],us,R[:,4])*(1-t)+np.interp(Q[:,0],us,R[:,5])*t
        return d[:,None]*n
    return disp,dict(us=us,R=R)
if __name__=='__main__':
    Z={p['name']:p for p in geo.load(sys.argv[1])}; recs=[]; dbg={}
    bodies=[PartMesh(Z['COBALTSS_KIT00_BODY_A']),PartMesh(Z['COBALTSS_KIT00_HOOD_A'])]
    for side,sg in (('LEFT',1),('RIGHT',-1)):
        disp,info=field(PartMesh(Z['COBALTSS_KIT00_%s_HEADLIGHT_GLASS_A'%side]),bodies,side); dbg[side]=info
        for Lv in 'ABCD':
            for part in ('HEADLIGHT','HEADLIGHT_GLASS'):
                pm=PartMesh(Z['COBALTSS_KIT00_%s_%s_%s'%(side,part,Lv)]); v=np.unique(allF(pm))
                v=v[(pm.P[v,2]>0.33)&(pm.P[v,0]>1.6)&(sg*pm.P[v,1]>0.3)]
                pm.P[v]+=disp(pm.P[v]); recs.append(pm)
    pickle.dump(dbg,open('build/hl29dbg.pkl','wb'))
    with open(sys.argv[2],'wb') as f:
        for pm in recs: b,nv=pm.record(); f.write(b)
