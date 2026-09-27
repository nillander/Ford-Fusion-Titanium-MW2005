"""Kits de carroceria com cintas de reboque (Fusion 2012 e 2018): os seis kits que o jogo já tem para o slot
(KIT00–KIT05; o KIT03 existia no carro original e faltava no Fusion). KIT00 sem cinta; KIT01–KIT05 com uma cinta
diferente cada (tex48.py), na dianteira (lado direito) e na traseira (lado esquerdo):
  KIT01 preta/vermelho 大吉大利  KIT02 vermelha/branco 出入平安  KIT03 laranja/preto 一路顺风
  KIT04 azul/amarelo F B I      KIT05 zebrada preta e amarela
Dianteira: y −0,33, z 0,148 → −0,03 (suporte até 0,183: só na parte preta do para-choque), 1 cm à frente.
Traseira: y +0,405, por dentro do escapamento, presa na faixa preta (z 0,215) → 0,015, 1 cm atrás.
Fundo escuro (1 e 5) 6,5 cm de largura, os demais 5 cm; suporte triangular preto no topo.
Uso: kits46.py in.dump out.spec PREFIXO"""
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts');sys.path.insert(0,'/home/claude/c12')
import numpy as np,geo
from partmesh import PartMesh
SHADER=0x0FEDEE40
from tex48 import SLOTS
CAR={'COBALTSS':dict(tex=0xC195B264,black=(0.5625,0.5625)),'MUSTANGGT':dict(tex=0x5A006DE9,black=(0.02,0.02))}
for c in CAR: CAR[c]['slots']=[(x/1024,(x+64)/1024,y/1024,(y+256)/1024) for x,y in SLOTS[c]]
WID={0:0.065,1:0.05,2:0.05,3:0.05,4:0.065}
FRONT=dict(Y=-0.33,ZT=0.148,ZB=-0.03,X=2.322,dirx=1.0)
REAR=dict(Y=0.405,ZT=0.215,ZB=0.015,X=-2.358,dirx=-1.0)
KITS={'KIT0%d'%(i+1):[(FRONT,i),(REAR,i)] for i in range(5)}
def strap_mesh(cfg,which,pos):
    u0,u1,v0,v1=cfg['slots'][which]; eu=(u1-u0)*0.03; ev=(v1-v0)*0.004; u0+=eu;u1-=eu;v0+=ev;v1-=ev
    Y,W,ZT,ZB,XF,dx=pos['Y'],WID[which],pos['ZT'],pos['ZB'],pos['X'],pos['dirx']
    # seen from outside, image-right is +y at the front and -y at the rear
    right=Y+W/2 if dx>0 else Y-W/2; left=Y-W/2 if dx>0 else Y+W/2
    n=8; P=[];N=[];UV=[];F=[]
    for side,nx in ((0,dx),(1,-dx)):
        o=len(P); x=XF if side==0 else XF-0.002*dx
        for i in range(n+1):
            t=i/n; z=ZT+(ZB-ZT)*t
            for yy,uu in ((right,u1),(left,u0)):
                P.append((x,yy,z)); N.append((nx,0,0)); UV.append((uu if side==0 else (u0+u1-uu),v0+(v1-v0)*t))
        for i in range(n):
            a,b,c,d=o+2*i,o+2*i+1,o+2*i+3,o+2*i+2; F+=[(a,b,c),(a,c,d)]
    for side,nx in ((0,dx),(1,-dx)):
        o=len(P); x=XF-0.001*dx if side==0 else XF-0.003*dx
        for q in ((Y+W/2+0.004,ZT+0.004),(Y-W/2-0.004,ZT+0.004),(Y,ZT+0.035)):
            P.append((x,q[0],q[1])); N.append((nx,0,0)); UV.append(cfg['black'])
        F+=[(o,o+1,o+2)]
    P=np.array(P,float);F=np.array(F);N=np.array(N,float);UV=np.array(UV,float)
    fn=np.cross(P[F[:,1]]-P[F[:,0]],P[F[:,2]]-P[F[:,0]])
    F=np.where(((fn*N[F[:,0]]).sum(1)<0)[:,None],F[:,[0,2,1]],F)
    return P,N,UV,F
def kit(Z,pre,L,k):
    pm=PartMesh(Z['%s_KIT00_BODY_%s'%(pre,L)]); pm.name='%s_%s_BODY_%s'%(pre,k,L); cfg=CAR[pre]
    ti=pm.tex_index(cfg['tex']); si=pm.sh_index(SHADER); g0=pm.groups[0]; F=[]
    for pos,which in KITS[k]:
        P,N,UV,Ff=strap_mesh(cfg,which,pos); o=pm.add_verts(P,N,UV,0xFFFFFFFF); F.append(Ff+o)
    pm.groups.append(dict(ti=ti,si=si,flags=g0['flags'],unk1=g0['unk1'],F=np.concatenate(F)))
    return pm
if __name__=='__main__':
    src,out,pre=sys.argv[1:4]; Z={p['name']:p for p in geo.load(src)}; recs=[]
    for k in KITS:
        for L in 'ABCDE':
            pm=kit(Z,pre,L,k); b,nv=pm.record('%s_KIT01_BODY_%s'%(pre,L)); recs.append(b)
            print('%-26s verts %d%s'%(pm.name,nv,' !!' if nv>65535 else ''))
            if nv>65535: raise SystemExit('limite')
        if not any(n.startswith('%s_%s_DECAL_'%(pre,k)) for n in Z):
            for n in [x for x in Z if x.startswith(pre+'_KIT01_DECAL_')]:
                pm=PartMesh(Z[n]); pm.name=n.replace('_KIT01_','_%s_'%k); b,nv=pm.record(n); recs.append(b); print('%-26s (decal)'%pm.name)
    open(out,'wb').write(b''.join(recs))
