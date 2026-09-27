"""Chapa preta atrás da grade superior (Fusion 2012 e 2018): impede ver o interior do carro pela grade.
Superfície x = a - b*y^2 acompanhando a curva da grade, 12 mm atrás da face de trás das barras cromadas;
contorno = abertura da lataria (vista de frente) + 2,5 cm por trás da lataria (fora dos faróis).
Textura <CARRO>_LOGO em UV de área preta sólida (0,1; 0,45). Grupo novo em BASE_A–E (vale para todos os kits)."""
import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo,gmap
from xray import xcast
from partmesh import PartMesh
from scipy.ndimage import binary_dilation,binary_fill_holes,label
src,car,out=sys.argv[1],sys.argv[2],sys.argv[3]
LOGO={'COBALTSS':0xE67A0B4A,'MUSTANGGT':0x5A006DE9}[car]; MISC={'COBALTSS':0xE67A7FA5,'MUSTANGGT':0x5A00E244}[car]
BACK=0.012; UV=(0.1,0.45)
Z={p['name']:p for p in geo.load(src)}
# 1. curva das barras: mínimo x por faixa de 5 cm de y (cromado da grade, z .37-.50)
P,F=gmap.faces(Z[f'{car}_KIT00_RIGHT_SIDE_MIRROR_A'],lambda i,t:t==MISC); C=P[F].mean(1)
m=(C[:,0]>2.0)&(C[:,2]>0.3)&(C[:,2]<0.6)&(np.abs(C[:,1])<0.6); V=P[np.unique(F[m])]
V=V[(V[:,2]>0.37)&(V[:,2]<0.50)&(np.abs(V[:,1])<0.53)]
yb=[];xb=[]
for y0 in np.arange(-0.53,0.53,0.03):
    s=(V[:,1]>=y0)&(V[:,1]<y0+0.03)
    if s.sum()>2: yb.append(V[s,1].mean()); xb.append(V[s,0].min())
yb=np.array(yb);xb=np.array(xb)
A=np.c_[np.ones_like(yb),yb**2]; c,*_=np.linalg.lstsq(A,xb,rcond=None)
c[0]-=max(0,(A@c-xb).max()); c[0]-=BACK
fx=lambda y: c[0]+c[1]*y**2
print('curva x = %.4f %+.4f y^2   (y=0: %.3f, y=0.55: %.3f)'%(c[0],c[1],fx(0),fx(0.55)))
# 2. contorno pela vista de frente
RES=0.005
ys=np.arange(-0.66,0.6601,RES); zs=np.arange(0.28,0.64,RES); YY,ZZ=np.meshgrid(ys,zs); Q=np.c_[YY.ravel(),ZZ.ravel()]
def cast(parts):
    r=np.stack([xcast(*gmap.sub(*pf),Q,'max') for pf in parts]); r=np.where(np.isnan(r),-9,r).max(0); r[r<-8]=np.nan; return r.reshape(YY.shape)
body=cast([gmap.faces(Z[f'{car}_KIT00_BODY_A']),gmap.faces(Z[f'{car}_KIT00_HOOD_A'])])
lamps=cast([gmap.faces(Z[n]) for n in Z if n.endswith('_A') and 'KIT00' in n and 'LIGHT' in n])
xp=fx(YY)
hole=np.isnan(body)&(ZZ>0.31)&(ZZ<0.57)&(np.abs(YY)<0.62)
lab,n=label(hole); keep=lab[np.abs(ys-0).argmin()//1 if False else (np.abs(zs-0.44)).argmin(),np.abs(ys).argmin()]
hole=lab==keep
hole=binary_fill_holes(hole)
covered=(body>xp+0.004)&np.isnan(lamps)            # plate hidden behind the skin here
region=hole.copy()
for it in range(int(0.025/RES)): region=region|(binary_dilation(region)&covered)
region&=np.isnan(lamps)|hole
print('hole cells %d, region cells %d; y %.3f..%.3f z %.3f..%.3f'%(hole.sum(),region.sum(),YY[region].min(),YY[region].max(),ZZ[region].min(),ZZ[region].max()))
np.savez(out+'.mask.npz',ys=ys,zs=zs,hole=hole,region=region,body=body,lamps=lamps)
# 3. malha: células com os 4 cantos na região, por LOD
def mesh(step):
    k=int(round(step/RES)); R=region[::k,::k]; y=ys[::k]; z=zs[::k]
    R=binary_dilation(R)  # garante cobertura na malha grossa
    idx=-np.ones(R.shape,int); vid=0; Pv=[]
    cells=R[:-1,:-1]&R[1:,:-1]&R[:-1,1:]&R[1:,1:]
    need=np.zeros_like(R); need[:-1,:-1]|=cells; need[1:,:-1]|=cells; need[:-1,1:]|=cells; need[1:,1:]|=cells
    for i,j in zip(*np.nonzero(need)): idx[i,j]=vid; vid+=1; Pv.append((fx(y[j]),y[j],z[i]))
    T=[]
    for i,j in zip(*np.nonzero(cells)):
        a,b,cc,d=idx[i,j],idx[i,j+1],idx[i+1,j+1],idx[i+1,j]; T+= [(a,b,cc),(a,cc,d)]
    Pv=np.array(Pv); T=np.array(T)
    fn=np.cross(Pv[T[:,1]]-Pv[T[:,0]],Pv[T[:,2]]-Pv[T[:,0]]); T=np.where((fn[:,0]<0)[:,None],T[:,[0,2,1]],T)
    N=np.c_[np.ones(len(Pv)),-2*c[1]*Pv[:,1],np.zeros(len(Pv))]; N/=np.linalg.norm(N,axis=1,keepdims=True)
    return Pv,N,T
# cor de vértice/flags do grupo preto existente
g1=Z[f'{car}_KIT00_RIGHT_SIDE_MIRROR_A']; gi=[i for i,g in enumerate(g1['groups']) if g1['tex'][g['tex'][0]]==LOGO][0]; gg=g1['groups'][gi]
seg=g1['idx'][gg['offset']:gg['offset']+gg['length']]; col=int(np.bincount(g1['v']['c'][seg].astype(np.int64)&0xFFFFFFFF).argmax()) if False else int(np.median(g1['v']['c'][seg].astype(np.int64)&0xFFFFFFFF))
print('flags %d unk1 %d shader-idx %d color %08X'%(gg['flags'],gg['unk1'],gg['shader'],col))
STEP={'A':0.01,'B':0.015,'C':0.02,'D':0.03,'E':0.03}
recs=[];geom={}
for L in 'ABCDE':
    pm=PartMesh(Z[f'{car}_BASE_{L}'])
    Pv,N,T=mesh(STEP[L]); geom[L]=(Pv,T)
    o=pm.add_verts(Pv,N,np.tile(UV,(len(Pv),1)),col)
    ti=pm.tex_index(LOGO)
    si=g1['shaders'][gg['shader']]; si=pm.sh_index(si)
    pm.groups.append(dict(ti=ti,si=si,flags=gg['flags'],unk1=gg['unk1'],F=T+o))
    b,nv=pm.record(); recs.append(b); print('%s verts %d (+%d) tris +%d'%(pm.name,nv,len(Pv),len(T)))
with open(out,'wb') as f:
    for b in recs: f.write(b)
np.save(out+'.A.npy',np.c_[geom['A'][0]]); np.save(out+'.AT.npy',geom['A'][1])
