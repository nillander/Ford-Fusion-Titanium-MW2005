from common import *
sys.path.insert(0,'/home/claude/c12/lib'); from footprint import Footprint
lab=pickle.load(open('mondeo_islands.pkl','rb'))
M=S['M']; F=S['F']; sh=S['shader']; C=M[F].mean(1)
tri=M[F]; area=np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1)/2
key=np.round(np.sort(tri,axis=1).reshape(len(F),-1)/0.0005).astype(np.int64)
_,first,kinv=np.unique(key,axis=0,return_index=True,return_inverse=True); kinv=kinv.ravel()
uniq=np.zeros(len(F),bool); uniq[first]=True
def lamp(region,lensmask,depth=0.30,front=0.01,dil=0.015,thr=0.85):
    L=lensmask&region(C)
    fp=Footprint(M,F[L],dilate=dil)
    inside,dz=fp.query(C)
    ok=inside&(dz<=front)&(dz>=-depth)
    tot=np.bincount(lab,weights=area,minlength=lab.max()+1); good=np.bincount(lab,weights=area*ok,minlength=lab.max()+1)
    frac=good/np.maximum(tot,1e-12)
    sel=(frac[lab]>=thr)&(sh!=0)
    sel|=L
    sel&=uniq
    return sel,fp
side=lambda s:(lambda C:(C[:,1]*s>0.25))
out={}
for s,nm in ((1,'L'),(-1,'R')):
    out['head'+nm]=lamp(lambda C:side(s)(C)&(C[:,0]>1.55)&(C[:,2]>0.42),sh==15)
    out['tail'+nm]=lamp(lambda C:side(s)(C)&(C[:,0]<-1.75)&(C[:,2]>0.55),(sh==16)|(sh==15))
    out['fog'+nm]=lamp(lambda C:side(s)(C)&(C[:,0]>1.7)&(C[:,2]<0.47),sh==15,depth=0.2,dil=0.03)
import collections
for k,(sel,fp) in out.items(): print(k,sel.sum(),collections.Counter(sh[sel]).most_common())
pickle.dump(dict(sel={k:v[0] for k,v in out.items()},kinv=kinv),open('mondeo_lampsel.pkl','wb'))
if __name__=='__main__':
    col,tid=mcol(S)
    allsel=np.zeros(len(F),bool)
    for k,(s_,_) in out.items(): allsel|=s_
    selkeys=np.zeros(kinv.max()+1,bool); selkeys[kinv[allsel]]=True; rest=~selkeys[kinv]
    ims=[]
    for k,view in [('headL',(25,8,(1.95,0.62,0.55),900)),('tailL',(200,8,(-2.05,0.6,0.7),900)),('fogL',(15,5,(2.1,0.72,0.3),1500))]:
        sel=out[k][0]
        for m in (np.ones(len(F),bool),sel,rest):
            a,_=rast.render(M,F[m],col[m],uv=S['UV'],texid=tid[m],textures=[FARI,RED],az=view[0],el=view[1],W=600,H=400,center=view[2],scale=view[3],bg=(0.2,0.5,0.2))
            ims.append(Image.fromarray(a))
    o=Image.new('RGB',(1800,1200))
    for i,m in enumerate(ims): o.paste(m,((i%3)*600,(i//3)*400))
    o.save('mondeo_lamps.png')
