from common import *
import sys
src=sys.argv[1]; out=sys.argv[2]
Pb=geo.load(src)
sel=lambda n: n.endswith('_A') and '_KIT00_' in n or n.endswith('BASE_A')
sel2=lambda n: sel(n) and not any(k in n for k in ['INTERIOR','DRIVER'])
B=mwsoup.soup(Pb,sel2)
L=np.array([-0.7,0.35,0.6]); L/=np.linalg.norm(L)
# per-vertex lighting (game-like smooth shading), averaged per triangle
V=np.array(B['N']); V/=np.linalg.norm(V,axis=1,keepdims=True)+1e-12
spec_dir=np.array([-0.8,-0.2,0.2]); spec_dir/=np.linalg.norm(spec_dir)
lit=0.25+0.75*np.clip(V@L,0,1)+0.35*np.clip(V@spec_dir,0,1)**12
base=np.where(np.isin(B["tex"],[0x9A8AAD9E,0xB637F71F])[:,None],np.array([0.55,0.75,0.78]),np.array([0.25,0.25,0.28]))
col=(base*lit[B['F']].mean(1)[:,None]).clip(0,1).astype(np.float32)
ims=[]
for az,el,c,s in ((180,8,(-2.25,0,0.72),1100),(205,15,(-2.2,0.2,0.72),1100),(180,5,(-2.2,0,0.62),480),(160,10,(-2.2,-0.25,0.72),1100)):
    im,_=rast.render(B['P'],B['F'],col,az=az,el=el,W=900,H=450,center=c,scale=s,shade=False)
    ims.append(Image.fromarray(im))
o=Image.new('RGB',(1800,900))
for i,m in enumerate(ims): o.paste(m,((i%2)*900,(i//2)*450))
o.save(out)
