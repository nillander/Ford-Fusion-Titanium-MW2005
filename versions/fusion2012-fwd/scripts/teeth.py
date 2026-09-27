"""Item 41c (Fusion 2012 e 2018): "dentes" claros/escuros na faixa entre a borda de baixo do farol e o para-choque.
A lataria ali tem uma aba quase horizontal intercalada com as faces do para-choque; os vértices misturam normais
"para cima" e "para fora" e o sombreado vira dente de serra. Nas faces visíveis da pele a menos de RB da borda de
baixo da lente (e abaixo dela), a normal dos vértices passa a ser a média das faces vizinhas (raio 4 cm) viradas
para fora como o para-choque (menos de 40° da normal média dessas faces). Só normais, sem mexer na forma.
Uso: teeth.py in.dump out.spec PRE TAG"""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo,pickle,os
from partmesh import PartMesh
from hl29 import frame,samp
from scipy.spatial import cKDTree
RB=float(os.environ.get('RB','0.06'))
src,out,pre,tag=sys.argv[1:5]
P=geo.load(src); vis=pickle.load(open('build/vis%s.pkl'%tag,'rb')); Z={p['name']:(i,p) for i,p in enumerate(P)}
pi,_=Z[pre+'_KIT00_BODY_A']; sv=np.where(vis['seen'][(vis['part']==pi)&(vis['grp']==0)])[0]
pm0=PartMesh(Z[pre+'_KIT00_BODY_A'][1]); F=pm0.groups[0]['F'][sv]; T=pm0.P[F]
fn=np.cross(T[:,1]-T[:,0],T[:,2]-T[:,0]); ar=np.linalg.norm(fn,axis=1); fu=fn/np.maximum(ar,1e-15)[:,None]; C=T.mean(1); kd=cKDTree(C)
targets=[]; newN=[]
for side in ('LEFT','RIGHT'):
    gl=PartMesh(Z['%s_KIT00_%s_HEADLIGHT_GLASS_A'%(pre,side)][1]); Fg,n,a,b,c0=frame(gl)
    L=samp(gl.P,Fg,12); qa=(L-c0)@a; qb=(L-c0)@b
    # bottom edge: per 1 cm slice of a, the sample with largest b (b points down)
    edge=[]
    for u in np.arange(qa.min(),qa.max(),0.01):
        m=np.abs(qa-u)<0.005
        if m.any(): edge.append(L[m][np.argmax(qb[m])])
    edge=np.array(edge); ke=cKDTree(edge)
    vv=np.unique(F); d,j=ke.query(pm0.P[vv]); below=((pm0.P[vv]-edge[j])@b)>-0.002
    vv=vv[(d<RB)&below]
    # outward reference = mean normal of visible faces near the bottom edge that face like the bumper (not up)
    near=kd.query_ball_point(edge,0.06); near=np.unique(np.concatenate([np.array(x,int) for x in near]))
    up=np.array([0,0,1.]); ref=fu[near][(fu[near]@up)<0.75]; ref=(ref*ar[near][(fu[near]@up)<0.75,None]).sum(0); ref/=np.linalg.norm(ref)
    for v in vv:
        nb=np.array(kd.query_ball_point(pm0.P[v],0.04),int); m=(fu[nb]@ref)>np.cos(np.radians(40))
        s=fn[nb[m]].sum(0) if m.any() else ref; targets.append(v); newN.append(s/np.linalg.norm(s))
    print(side,'ref',np.round(ref,2),'verts',len(vv))
targets=np.array(targets); newN=np.array(newN); recs=[]
for k in ('KIT00','KIT01','KIT02','KIT04','KIT05'):
    nme='%s_%s_BODY_A'%(pre,k)
    if nme not in Z: continue
    pm=PartMesh(Z[nme][1]); ln=np.linalg.norm(pm.N[targets],axis=1,keepdims=True); pm.N[targets]=newN*ln; recs.append(pm)
with open(out,'wb') as f:
    for pm in recs: bb,nv=pm.record(); f.write(bb)
