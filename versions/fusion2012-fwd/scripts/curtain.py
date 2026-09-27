"""Piso preto sob a borda de baixo de cada farol do 2012: tapa a visão para dentro do carro pela fresta entre a
carcaça do farol e o para-choque. Faixa a 2 mm abaixo da borda inferior da lente, de 3 mm atrás dela até 9 cm para
dentro (−x), dupla face, na cor da pintura (grupo da pele de fundo de BASE_A–E, UV da pintura mais próxima). Uso: curtain.py in.dump out.spec"""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
from partmesh import PartMesh
from gapmeas import slice_pts
from scipy.spatial import cKDTree
BLACK=0xE67A0B4A; UV=(0.1,0.45)
Z={p['name']:p for p in geo.load(sys.argv[1])}
strips=[]
for side,sg in (('LEFT',1),('RIGHT',-1)):
    gl=PartMesh(Z['COBALTSS_KIT00_%s_HEADLIGHT_GLASS_A'%side]); pts=[]
    for y in np.arange(0.505,0.87,0.006):
        G=slice_pts(gl,sg*y)
        if len(G)<3: continue
        lo=G[np.argmin(G[:,2])]; pts.append(lo)
    pts=np.array(pts)
    k=np.ones(5)/5; zs=np.convolve(np.r_[pts[:2,2],pts[:,2],pts[-2:,2]],k,'valid'); xs=np.convolve(np.r_[pts[:2,0],pts[:,0],pts[-2:,0]],k,'valid')
    C=np.c_[xs-0.003,pts[:,1],zs-0.002]
    B=C-np.array([0.07,0,0.06])
    strips.append((C,B))
    print(side,len(C),'z %.3f..%.3f'%(C[:,2].min(),C[:,2].max()))
def mesh(C,B):
    n=len(C); P=np.r_[C,B]; F=[]
    for i in range(n-1): F+=[(i,i+1,n+i+1),(i,n+i+1,n+i)]
    F=np.array(F); F=np.r_[F,F[:,[0,2,1]]]
    N=np.tile((0,0,1.0),(len(P),1)); return P,N,F
tmpl=[g for g in PartMesh(Z['COBALTSS_BASE_A']).groups]
recs=[]
for L in 'ABCDE':
    pm=PartMesh(Z['COBALTSS_BASE_%s'%L])
    g=[g for g in pm.groups if pm.tex[g['ti']]==0xB637F71F][0]
    fi=np.unique(g['F'].ravel()); kd=cKDTree(pm.P[fi])
    for C,Bk in strips:
        P,N,F=mesh(C,Bk); _,nn=kd.query(P)
        N=np.c_[np.ones(len(P))*0.6,np.sign(P[:,1])*0.3,np.ones(len(P))*0.75]; N/=np.linalg.norm(N,axis=1,keepdims=True)
        o=pm.add_verts(P,N,pm.UV[fi[nn]],pm.C[fi[nn]]); g['F']=np.r_[g['F'],F+o]
    b,nv=pm.record(); recs.append(b); print(pm.name,'verts',nv)
open(sys.argv[2],'wb').write(b''.join(recs))
