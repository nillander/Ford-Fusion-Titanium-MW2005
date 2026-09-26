# Item 6 (Fusion 2012): para-choque traseiro, canto inferior no meio.
# Vértices do vinco inferior do para-choque (onde a face traseira encontra a face de baixo) que ficaram com a
# normal da face de baixo, mas são usados por triângulos grandes da face traseira -> triângulo escuro ("amassado").
# Troca só a normal desses vértices pela média (por área) das faces traseiras que os usam. Posição/UV intactas.
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
def candidates(p,region=(-2.28,0.35,0.22,0.36),rear=-0.85,minA=1e-4,ang=40):
    X=p['v']['p'].astype(float);N=p['v']['n'].astype(float)
    out={}
    for g in p['groups']:
        seg=p['idx'][g['offset']:g['offset']+g['length']].astype(int);F=seg[:len(seg)//3*3].reshape(-1,3)
        if not len(F): continue
        fn=np.cross(X[F[:,1]]-X[F[:,0]],X[F[:,2]]-X[F[:,0]]);A=np.linalg.norm(fn,axis=1)/2;fnu=fn/(2*A[:,None]+1e-12)
        c=X[F].mean(1)
        sel=(c[:,0]<region[0])&(np.abs(c[:,1])<region[1])&(c[:,2]>region[2])&(c[:,2]<region[3])&(fnu[:,0]<rear)
        acc={}
        for t in np.nonzero(sel)[0]:
            for i in F[t]: acc.setdefault(i,[np.zeros(3),0.0]); acc[i][0]+=fnu[t]*A[t]; acc[i][1]+=A[t]
        for i,(s,a) in acc.items():
            if a<minA: continue
            m=s/np.linalg.norm(s); cur=N[i]/ (np.linalg.norm(N[i])+1e-12)
            if np.degrees(np.arccos(np.clip(m@cur,-1,1)))>ang: out[i]=m
    return out
if __name__=='__main__':
    P=geo.load(sys.argv[1])
    for p in P:
        if 'BODY' not in p['name']: continue
        c=candidates(p)
        for i,m in c.items(): print(p['name'],i,np.round(p['v']['p'][i],4),'n',np.round(p['v']['n'][i],2),'->',np.round(m,2))
