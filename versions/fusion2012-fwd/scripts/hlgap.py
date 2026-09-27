import sys;sys.path.insert(0,'/home/claude/c12');sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo,pickle
from partmesh import PartMesh
from bulge import samp,allF
from hl29 import frame
from scipy.ndimage import binary_fill_holes,binary_closing,distance_transform_edt,label,binary_opening
RES=0.003
def masks(Z,side,dump=None):
    gl=PartMesh(Z['COBALTSS_KIT00_%s_HEADLIGHT_GLASS_A'%side]); F,n,a,b,c0=frame(gl)
    pr=lambda Y: np.c_[(Y-c0)@a,(Y-c0)@b,(Y-c0)@n]
    L=pr(samp(gl.P,F,30)); hd=PartMesh(Z['COBALTSS_KIT00_%s_HEADLIGHT_A'%side])
    u0,u1=L[:,0].min()-0.08,L[:,0].max()+0.08; v0,v1=L[:,1].min()-0.08,L[:,1].max()+0.08
    nu,nv=int((u1-u0)/RES)+1,int((v1-v0)/RES)+1
    def rast(P3,zmin=-9):
        m=np.zeros((nv,nu),bool); h=np.full((nv,nu),-9.0)
        iu=((P3[:,0]-u0)/RES).astype(int); iv=((P3[:,1]-v0)/RES).astype(int); ok=(iu>=0)&(iu<nu)&(iv>=0)&(iv<nv)&(P3[:,2]>zmin)
        np.maximum.at(h,(iv[ok],iu[ok]),P3[ok,2]); return h
    Lh=rast(L); lens=binary_closing(Lh>-8,iterations=2); from scipy.ndimage import binary_fill_holes; lens=binary_fill_holes(lens)
    import fit28
    fit28.RES=RES
    Bh=np.full((nv,nu),np.nan)
    for nm in ('COBALTSS_KIT00_BODY_A','COBALTSS_KIT00_HOOD_A','COBALTSS_BASE_A','COBALTSS_KIT00_RIGHT_SIDE_MIRROR_A'):
        pm=PartMesh(Z[nm]); FF=allF(pm); m=np.linalg.norm(pm.P[FF].mean(1)-c0,axis=1)<0.5; U=pr(pm.P)
        FF=FF[m]; FF=FF[(U[FF][:,:,2]>-0.035).all(1)]
        img=fit28.raster(U,FF,(u0,v0,nu,nv)); Bh=np.fmax(Bh,img)
    body=~np.isnan(Bh)
    dl=distance_transform_edt(~lens)*RES
    gap=(~body)&(~lens)&(dl<0.05)
    gap=binary_opening(gap,iterations=1)
    lab,nl=label(gap); sizes=np.bincount(lab.ravel()); keep=np.zeros_like(gap)
    for i in range(1,nl+1):
        if sizes[i]*RES*RES>2e-5: keep|=lab==i
    return dict(lens=lens,body=body,gap=keep,grid=(u0,v0,nu,nv),frame=(n,a,b,c0),Bh=Bh,Lh=Lh)
if __name__=='__main__':
    import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
    Z={p['name']:p for p in geo.load(sys.argv[1])}
    fig,ax=plt.subplots(2,1,figsize=(16,10))
    for axx,side in zip(ax,('LEFT','RIGHT')):
        d=masks(Z,side); im=np.zeros(d['lens'].shape+(3,)); im[d['body']]=(0.3,0.7,0.7); im[d['lens']]=(1,1,1); im[d['gap']]=(1,0,1)
        axx.imshow(im,origin='lower'); axx.set_title(side+' gap cm2 %.1f'%(d['gap'].sum()*RES*RES*1e4))
    plt.savefig(sys.argv[2] if len(sys.argv)>2 else 'build/hlgap.png',dpi=55,bbox_inches='tight')
