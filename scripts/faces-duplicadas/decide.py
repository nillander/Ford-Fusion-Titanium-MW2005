import numpy as np,mwgeo,collections,sys,pickle,re
from scan2 import pairs
from vis import idbuf,dirs
car=sys.argv[1]; P=mwgeo.load(car+'.BIN'); byname={p.get('name'):p for p in P if p.get('name')}
def base(n): return n.split('_',1)[1][:-2]
def lod(n): return n[-1]
SKIP=('DECAL','WINDOW')
def default_part(b):
    if any(k in b for k in SKIP): return False
    if b.startswith('STYLE'): return False
    if re.match(r'KIT0[1-5]_',b): return False
    if any(k in b for k in ('TIRE','BRAKE_','FRONT_BRAKE','REAR_BRAKE')): return False
    return True
def tris(p):
    v=p['vbs'][0]; F=p['idx'][:len(p['idx'])//3*3].reshape(-1,3); return v['p'].astype(np.float64)[F]
res={}
D=dirs()
for n,p in byname.items():
    o,s,_=pairs(p)
    if not o and not s: continue
    L=lod(n); b=base(n)
    alone=any(k in b for k in ('TIRE','FRONT_BRAKE','REAR_BRAKE'))
    occ=[]
    if not alone:
        for m,q in byname.items():
            if m==n or lod(m)!=L or not default_part(base(m)): continue
            bm=base(m)
            if 'BODY' in b and 'BODY' in bm: continue
            if 'HOOD' in b and 'HOOD' in bm: continue
            occ.append(tris(q))
    X=tris(p); allT=np.concatenate([X]+occ) if occ else X
    cnt=np.zeros(len(X))
    for d in D:
        ids=idbuf(allT,d); ids=ids[(ids>=0)&(ids<len(X))]
        cnt+=np.bincount(ids,minlength=len(X))
    res[n]=dict(opp=o,same=s,cnt=cnt)
    va=np.array([cnt[a] for a,b_ in o]) if o else np.zeros(0); vb=np.array([cnt[b_] for a,b_ in o]) if o else np.zeros(0)
    mx=np.maximum(va,vb); mn=np.minimum(va,vb)
    print('%-40s opp %5d (um lado %5d, dois lados %4d, nenhum %5d) same %4d'%(n,len(o),np.sum((mx>0)&(mn<=0.1*mx)),np.sum((mn>0.1*mx)&(mx>0)),np.sum(mx==0),len(s)),flush=True)
pickle.dump(res,open(car+'_vis.pkl','wb'))
