"""Item 35 + item 34: kits de carroceria = carroceria de fábrica (KIT00) + cinta de reboque no para-choque dianteiro.
KIT01 "Street": cinta preta 大吉大利; KIT02 "Race": cinta vermelha 出入平安; KIT04 (carro do Razor/cutscenes: presets
RAZORMUSTANG, OPM_MUSTANG_VERSION2 e CS_CAR_14) e KIT05 (preset BL8) — que o Fusion não tinha e por isso sumia a
lataria — com a cinta vermelha e a preta. Os decalques de porta (KITxx_DECAL_*) são copiados do KIT01.
Cinta: 5 × 20 cm, pendurada à direita da grade inferior (y −0,33), de z 0,17 a −0,03, 1 cm à frente do para-choque,
dupla face; suporte triangular preto no topo. Grupo próprio na carroceria com a textura <atlas> e shader 0x0FEDEE40
(o mesmo das peças pretas opacas)."""
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts');sys.path.insert(0,'/home/claude/c12')
import numpy as np,geo
from partmesh import PartMesh
SHADER=0x0FEDEE40
CAR={'COBALTSS':dict(tex=0xC195B264,black=(0.5625,0.5625),u=[(0.5,0.5625),(0.5625,0.625)],v=(0.75,1.0)),
     'MUSTANGGT':dict(tex=0x5A006DE9,black=(0.02,0.02),u=[(0.75,0.8125),(0.8125,0.875)],v=(0.0,0.25))}
Y=-0.33; W=0.05; ZT=0.17; ZB=-0.03; XF=2.322
def strap_mesh(cfg,which):
    u0,u1=cfg['u'][which]; v0,v1=cfg['v']; eu=(u1-u0)*0.03; ev=(v1-v0)*0.004; u0+=eu;u1-=eu;v0+=ev;v1-=ev
    n=8; P=[];N=[];UV=[];F=[]
    for side,nx in ((0,1.0),(1,-1.0)):
        o=len(P); x=XF if side==0 else XF-0.002
        for i in range(n+1):
            t=i/n; z=ZT+(ZB-ZT)*t
            for j,(yy,uu) in enumerate(((Y+W/2,u1),(Y-W/2,u0))):
                P.append((x,yy,z)); N.append((nx,0,0)); UV.append((uu if side==0 else (u0+u1-uu),v0+(v1-v0)*t))
        for i in range(n):
            a,b,c,d=o+2*i,o+2*i+1,o+2*i+3,o+2*i+2
            F+= [(a,b,c),(a,c,d)] if side==0 else [(a,c,b),(a,d,c)]
    # bracket: triangle plate above the strap (black), both faces
    for side,nx in ((0,1.0),(1,-1.0)):
        o=len(P); x=XF-0.001 if side==0 else XF-0.003
        for q in ((Y+W/2+0.004,ZT+0.004),(Y-W/2-0.004,ZT+0.004),(Y,ZT+0.035)):
            P.append((x,q[0],q[1])); N.append((nx,0,0)); UV.append(cfg['black'])
        # strip under the strap top (ring hole look): small bar
        F+= [(o,o+1,o+2)] if side==1 else [(o,o+2,o+1)]
    P=np.array(P,float);F=np.array(F);N=np.array(N,float);UV=np.array(UV,float)
    fn=np.cross(P[F[:,1]]-P[F[:,0]],P[F[:,2]]-P[F[:,0]])
    F=np.where(((fn*N[F[:,0]]).sum(1)<0)[:,None],F[:,[0,2,1]],F)
    return P,N,UV,F
def kit(Z,pre,src_name,dst_name,which):
    pm=PartMesh(Z[src_name]); pm.name=dst_name; cfg=CAR[pre]
    P,N,UV,F=strap_mesh(cfg,which); o=pm.add_verts(P,N,UV,0xFFFFFFFF)
    ti=pm.tex_index(cfg['tex']); si=pm.sh_index(SHADER); g0=pm.groups[0]
    pm.groups.append(dict(ti=ti,si=si,flags=g0['flags'],unk1=g0['unk1'],F=F+o))
    return pm
if __name__=='__main__':
    src,out,pre=sys.argv[1:4]; Z={p['name']:p for p in geo.load(src)}; recs=[]
    for k,which in (('KIT01',0),('KIT02',1),('KIT04',1),('KIT05',0)):
        tmpl_body=pre+'_KIT01_BODY_%s'
        for L in 'ABCDE':
            pm=kit(Z,pre,'%s_KIT00_BODY_%s'%(pre,L),'%s_%s_BODY_%s'%(pre,k,L),which); recs.append((pm,tmpl_body%L))
        if k in ('KIT04','KIT05'):
            for n in [x for x in Z if x.startswith(pre+'_KIT01_DECAL_')]:
                pm=PartMesh(Z[n]); pm.name=n.replace('_KIT01_','_%s_'%k); recs.append((pm,n))
    with open(out,'wb') as f:
        for pm,t in recs:
            b,nv=pm.record(t); f.write(b); print('%-44s verts %d%s'%(pm.name,nv,' !!' if nv>65535 else ''))
