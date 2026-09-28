import numpy as np,mwgeo,sys,collections
def scan(path,lods='A'):
    P=mwgeo.load(path); res=[]
    for p in P:
        n=p.get('name','')
        if not n or n[-1] not in lods or not p.get('vbs'): continue
        v=p['vbs'][0]; F=p['idx'][:len(p['idx'])//3*3].reshape(-1,3)
        F=F[(F[:,0]!=F[:,1])&(F[:,1]!=F[:,2])&(F[:,0]!=F[:,2])]
        if len(F)==0: continue
        q=np.round(v['p']*2000).astype(np.int64)  # 0.5 mm
        T=q[F]  # t,3,3
        key=np.sort(T.view([('a','<i8'),('b','<i8'),('c','<i8')]).reshape(len(F),3),axis=1)
        A,B,C=v['p'][F[:,0]],v['p'][F[:,1]],v['p'][F[:,2]]; nn=np.cross(B-A,C-A)
        d=collections.defaultdict(list)
        for i,k in enumerate(map(bytes,key)): d[k].append(i)
        opp=0; same=0; oppidx=set()
        for k,ids in d.items():
            if len(ids)<2: continue
            for a in range(len(ids)):
                for b in range(a+1,len(ids)):
                    s=np.dot(nn[ids[a]],nn[ids[b]])
                    if s<0: opp+=1; oppidx.add(ids[b])
                    else: same+=1
        if opp or same: res.append((n,len(F),opp,same))
    return res
if __name__=='__main__':
    for r in scan(sys.argv[1]): print('%-45s tris %6d  pares opostos %6d  pares iguais %5d'%r)
