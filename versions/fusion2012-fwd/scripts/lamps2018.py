"""2018 lamp volumes and triangle removal masks for any z10 part."""
from common import *
from footprint import Footprint
from islands import islands
LAMP_SOLIDS=('KIT00_RIGHT_HEADLIGHT_','KIT00_RIGHT_HEADLIGHT_GLASS_','KIT00_RIGHT_BRAKELIGHT_','KIT00_RIGHT_BRAKELIGHT_GLASS_')
def region_of(C):
    """label per triangle centroid: 'head','fog','tail' or '' (lamp-solid rule)"""
    r=np.full(len(C),'',dtype=object)
    r[(C[:,0]>1.6)&(C[:,2]>0.4)]='head'
    r[(C[:,0]>1.9)&(C[:,2]<0.3)&(np.abs(C[:,1])>0.5)]='fog'
    r[(C[:,0]<-1.75)&(C[:,2]>0.45)&(np.abs(C[:,1])>0.3)]='tail'
    return r
def part(name): return [q for q in Z if q['name']=='MUSTANGGT_'+name][0]
# footprints from LOD A lenses
_fps={}
def footprints():
    if _fps: return _fps
    for lens,kinds in (('KIT00_RIGHT_HEADLIGHT_GLASS_A',('head','fog')),('KIT00_RIGHT_BRAKELIGHT_GLASS_A',('tail',))):
        T=mwsoup.soup([part(lens)]); C=T['P'][T['F']].mean(1); r=region_of(C)
        for k in kinds:
            for s,nm in ((1,'L'),(-1,'R')):
                m=(r==k)&(C[:,1]*s>0)
                _fps[k+nm]=Footprint(T['P'],T['F'][m],dilate=0.008)
    return _fps
def removal_mask(p,depth=0.30,thr=0.9):
    """per-triangle removal mask (in soup order of the part) for a z10 part"""
    T=mwsoup.soup([p]); C=T['P'][T['F']].mean(1)
    short=p['name'][10:]
    if short.startswith(LAMP_SOLIDS):
        return T,region_of(C)!=''
    if short.startswith(('KIT00_BODY','KIT01_BODY','KIT02_BODY','KIT00_HOOD','STYLE')) or 'DECAL' in short:
        return T,np.zeros(len(C),bool)
    fps=footprints(); ok=np.zeros(len(C),bool)
    for k,fp in fps.items():
        inside,dz=fp.query(C); ok|=inside&(dz<=0.01)&(dz>=-depth)
    if not ok.any(): return T,ok
    n,lab=islands(T['P'],T['F'],tol=1e-4,split_by=T['grp'])
    tri=T['P'][T['F']]; area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)
    frac=np.bincount(lab,weights=area*ok,minlength=n)/np.maximum(np.bincount(lab,weights=area,minlength=n),1e-12)
    return T,frac[lab]>=thr
if __name__=='__main__':
    for p in Z:
        T,m=removal_mask(p)
        if m.any(): print(p['name'][10:].ljust(36),'remove',m.sum(),'of',len(m))
