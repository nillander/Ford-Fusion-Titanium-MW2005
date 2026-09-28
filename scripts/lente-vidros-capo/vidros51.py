"""Vidros (item 51): uma chapa por janela e UV continua 0-1 por janela, sem espelho.
Entrada: vidros2018.npz (FRONT_WINDOW_A / REAR_WINDOW_A; LODs B-D e o 2012 sao identicos).
Saida: layout51.npz com, por solido, mapa de vertices (slot -> vertice original + UV nova), indices e grupos."""
import numpy as np
from scipy.spatial import cKDTree
exec(open('win.py').read())
NV={'FRONT_WINDOW_A':7304,'REAR_WINDOW_A':4553}; NI={'FRONT_WINDOW_A':35979,'REAR_WINDOW_A':24000}
kept={}   # solid -> list of (tri index, class)
samples=[]
info={}
for k in NV:
    P,F,n,ar,c,s,T=tri_info(k); lab=pieces(F,s>0.3,len(P)); info[k]=(P,F,n,ar,c,s,T,lab)
# pieces list with samples for coverage test
pcs=[]
for k,(P,F,n,ar,c,s,T,lab) in info.items():
    for L in np.unique(lab[lab>=0]):
        m=np.nonzero(lab==L)[0]; A,B,C=P[F[m,0]],P[F[m,1]],P[F[m,2]]
        pts=np.concatenate([A+(B-A)*a+(C-A)*b for a,b in [(i/6,j/6) for i in range(7) for j in range(7-i)]])
        pcs.append(dict(k=k,L=L,m=m,area=ar[m].sum(),pts=pts))
pcs.sort(key=lambda d:-d['area'])
keep=[]
for p in pcs:
    if keep:
        allk=np.concatenate([q['pts'] for q in keep]); d,_=cKDTree(allk).query(p['pts'])
        if np.mean(d<0.006)>0.9: p['drop']=True; continue
    keep.append(p)
print('pecas externas',len(pcs),'mantidas',len(keep),'descartadas (cobertas)',len(pcs)-len(keep))
def klass(nm,cm):
    if abs(nm[1])>0.6:
        left=cm[1]>0; front=cm[0]>-0.05
        return {(True,True):2,(False,True):3,(True,False):4,(False,False):5}[(left,front)]
    return 0 if cm[0]>0 else 1
tris={k:[] for k in NV}
for p in keep:
    P,F,n,ar,c,s,T,lab=info[p['k']]; m=p['m']
    nm=(n[m]*ar[m,None]).sum(0); nm/=np.linalg.norm(nm); cm=(c[m]*ar[m,None]).sum(0)/ar[m].sum()
    cl=klass(nm,cm); p['cl']=cl
    tris[p['k']]+= [(t,cl) for t in m]
# UV per class, over both solids
names=['WINDOW_FRONT','WINDOW_REAR','WINDOW_LEFT_FRONT','WINDOW_RIGHT_FRONT','WINDOW_LEFT_REAR','WINDOW_RIGHT_REAR']
uvfun={}
for cl in range(6):
    pts=[];nrm=[]
    for k in NV:
        P,F,n,ar,c,s,T,lab=info[k]; ts=[t for t,c_ in tris[k] if c_==cl]
        if ts: pts.append(P[F[ts]].reshape(-1,3)); nrm.append((n[ts]*ar[ts,None]).sum(0))
    X=np.concatenate(pts); nm=np.sum(nrm,0); nm/=np.linalg.norm(nm)
    up=np.array([0,0,1.])-nm[2]*nm; up/=np.linalg.norm(up)
    if cl==0: hz=np.array([0,1.,0])    # visto de frente: esquerda da imagem = lado direito do carro (-y)
    elif cl==1: hz=np.array([0,-1.,0]) # visto de tras: esquerda da imagem = lado esquerdo (+y)
    elif cl in (2,4): hz=np.array([-1.,0,0]) # lado esquerdo visto de fora: esquerda da imagem = frente
    else: hz=np.array([1.,0,0])        # lado direito visto de fora: esquerda da imagem = traseira
    hz=hz-np.dot(hz,nm)*nm-np.dot(hz,up)*up; hz/=np.linalg.norm(hz)
    a=X@hz; b=X@up
    uvfun[cl]=(hz,up,a.min(),a.max(),b.min(),b.max())
    print(names[cl],'normal',nm.round(2),'largura %.2f m altura %.2f m'%(a.max()-a.min(),b.max()-b.min()))
def uv_of(cl,p):
    hz,up,a0,a1,b0,b1=uvfun[cl]; e=0.004
    u=e+(1-2*e)*(p@hz-a0)/(a1-a0); v=e+(1-2*e)*(b1-p@up)/(b1-b0)   # v=0 na borda de cima
    return np.stack([u,v],-1)
out={}
for k in NV:
    P,F,n,ar,c,s,T,lab=info[k]
    vmap=[];vuv=[];idx=[];groups=[]
    for cl in range(6):
        ts=[t for t,c_ in tris[k] if c_==cl]; start=len(vmap); istart=len(idx)
        if ts:
            f=F[ts]; uniq,inv=np.unique(f.ravel(),return_inverse=True)
            vmap+=list(uniq); vuv+=list(uv_of(cl,P[uniq])); idx+=list(inv+start)
        else:
            vmap.append(0); vuv.append(np.array([0.5,0.5])); idx+=[start]*3
        groups.append([start,len(vmap)-start,istart,len(idx)-istart])
    # padding: vertices and degenerate tris go to the last group
    padv=NV[k]-len(vmap); padi=NI[k]-len(idx); assert padv>=0 and padi>=0 and padi%3==0,(padv,padi)
    last=vmap[-1]; vmap+=[last]*padv; vuv+=[vuv[-1]]*padv; groups[-1][1]+=padv
    idx+=[len(vmap)-1]*padi; groups[-1][3]+=padi
    out[k+'_vmap']=np.array(vmap,np.int32); out[k+'_uv']=np.array(vuv,np.float32); out[k+'_idx']=np.array(idx,np.uint16); out[k+'_groups']=np.array(groups,np.int32)
    kept_t=sum(1 for _ in tris[k]); print(k,'triangulos mantidos',kept_t,'de',len(F),'| vertices usados',NV[k]-padv,'de',NV[k], '| grupos',groups)
np.savez('layout51.npz',**out)
if __name__=='__main__':
    ka=sum(p['area'] for p in keep); da=sum(p['area'] for p in pcs if p.get('drop'))
    print('area mantida %.4f m2, descartada %.4f m2'%(ka,da))
    for p in keep: print('  mantida',p['k'][:5],p['L'],'%.4f'%p['area'],names[p['cl']])
    big=[p for p in pcs if p.get('drop') and p['area']>0.0005]
    for p in big: print('  descartada grande',p['k'][:5],p['L'],'%.4f'%p['area'])
