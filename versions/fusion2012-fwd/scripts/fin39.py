"""Item 36b (Fusion 2012 e 2018): divisão em "V" no fundo da traseira reta da antena tubarão.
O triângulo que fechava o "V" (fin36) tem lados retos, mas a borda de baixo da face achatada é uma linha quebrada:
entre as duas ficavam frestas finas (o teto aparecia) e no jogo se via a divisão. Aqui a parte de baixo da face é
preenchida por uma faixa de quadriláteros, coluna a coluna (2 mm em y), do teto (3 mm para dentro dele) até 1,5 mm
acima da borda de baixo real da face — sobreposto e no mesmo plano, mesma normal (−1,0,0), UV e cor da face, então
não há emenda. KIT00/01/02/04/05_BODY_A–E."""
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts');sys.path.insert(0,'/home/claude/c12')
import numpy as np,geo
from partmesh import PartMesh
SKINS=(0xB637F71F,0x9A8AAD9E)   # 2012, 2018 paint
def lower_env(T2,ys):
    """T2 (n,3,2) triangles in (y,z); lowest z covered at each y"""
    out=np.full(len(ys),np.nan)
    for t in T2:
        for k in range(3):
            a,b=t[k],t[(k+1)%3]
            if abs(b[0]-a[0])<1e-9: continue
            m=(ys>=min(a[0],b[0]))&(ys<=max(a[0],b[0]))
            z=a[1]+(ys[m]-a[0])*(b[1]-a[1])/(b[0]-a[0])
            out[m]=np.fmin(out[m],z)
    return out
def fix(pm):
    P=pm.P; best=None
    for g in pm.groups:
        F=g['F']
        if not len(F) or pm.tex[g["ti"]] not in SKINS: continue
        T=P[F]; fin=(np.abs(T[:,:,1]).max(1)<0.1)&(T[:,:,2].min(1)>1.1)&(T[:,:,0].max(1)<-0.9)&(T[:,:,0].min(1)>-1.2)
        if not fin.any(): continue
        Nf=pm.N[F]; isb=(Nf[:,:,0]<-0.999).all(1)&fin
        if isb.sum()<3: continue
        xs=np.round(T[isb][:,:,0].ravel(),4); u,cn=np.unique(xs,return_counts=True); xb=u[cn.argmax()]
        back=fin&(np.abs(T[:,:,0]-xb)<2e-4).all(1)
        if back.sum()<3: continue
        best=(g,xb,F[back]); break
    if best is None: return 0
    g,xb,Fb=best; T2=P[Fb][:,:,1:]
    # leave out fin36's notch triangle (spans the whole width): its straight edges are what left the cracks
    sp=T2[:,:,0].max(1)-T2[:,:,0].min(1); T2=T2[sp<0.7*(T2[:,:,0].max()-T2[:,:,0].min())]
    y0,y1=T2[:,:,0].min(),T2[:,:,0].max(); ys=np.linspace(y0,y1,max(8,int((y1-y0)/0.002))+1)
    env=lower_env(T2,ys)
    # roof height under the back face: skin triangles just behind/under the fin, not part of it
    F=np.concatenate([gg['F'] for gg in pm.groups if len(gg['F']) and pm.tex[gg["ti"]] in SKINS]); T=P[F]; C=T.mean(1)
    fn=np.cross(T[:,1]-T[:,0],T[:,2]-T[:,0]); fn/=np.maximum(np.linalg.norm(fn,axis=1),1e-12)[:,None]
    r=(np.abs(C[:,0]-xb)<0.05)&(np.abs(C[:,1])<0.08)&(C[:,2]>1.1)&(C[:,2]<env[~np.isnan(env)].min()+0.01)&(np.abs(fn[:,2])>0.8)
    if r.sum()>=3:
        c=np.polyfit(C[r,1],C[r,2],2); roof=np.polyval(c,ys)
    else: roof=np.full(len(ys),np.nanmin(env))
    bot=np.minimum(roof-0.003,env-0.001); top=env+0.0015
    ok=~np.isnan(env)
    ys,bot,top=ys[ok],bot[ok],top[ok]
    n=len(ys); Pv=np.zeros((2*n,3)); Pv[:,0]=xb; Pv[:n,1]=ys; Pv[:n,2]=bot; Pv[n:,1]=ys; Pv[n:,2]=top
    ref=Fb[0,0]
    o=pm.add_verts(Pv,np.tile((-1.0,0,0),(2*n,1)),np.tile(pm.UV[ref],(2*n,1)),np.full(2*n,pm.C[ref]))
    tris=[]
    for i in range(n-1):
        a,b,c_,d=o+i,o+i+1,o+n+i+1,o+n+i
        tris+=[(a,b,c_),(a,c_,d)]
    tris=np.array(tris)
    t0=pm.P[tris[0]]; fnx=np.cross(t0[1]-t0[0],t0[2]-t0[0])[0]
    if fnx>0: tris=tris[:,[0,2,1]]
    g['F']=np.r_[g['F'],tris]
    return len(tris)
if __name__=='__main__':
    src,out,pre=sys.argv[1:4]; Z={p['name']:p for p in geo.load(src)}; recs=[]
    for k in ('KIT00','KIT01','KIT02','KIT04','KIT05'):
        for L in 'ABCDE':
            n='%s_%s_BODY_%s'%(pre,k,L)
            if n not in Z: continue
            pm=PartMesh(Z[n]); c=fix(pm); recs.append(pm); print(n,c)
    with open(out,'wb') as f:
        for pm in recs: b,nv=pm.record(); f.write(b)
