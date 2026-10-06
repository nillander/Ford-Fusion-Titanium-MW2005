import numpy as np,mwgeo,sys,collections
def tris(p):
    v=p['vbs'][0]; F=p['idx'][:len(p['idx'])//3*3].reshape(-1,3)
    ok=(F[:,0]!=F[:,1])&(F[:,1]!=F[:,2])&(F[:,0]!=F[:,2]); return v,F,ok
def pairs(p,tol=0.0005):
    v,F,ok=tris(p); P=v['p'].astype(np.float64)
    A,B,C=P[F[:,0]],P[F[:,1]],P[F[:,2]]; n=np.cross(B-A,C-A); ar=np.linalg.norm(n,axis=1)/2
    q=np.round(P/tol).astype(np.int64)
    key=np.sort(q[F].reshape(len(F),3,3).view([('a','<i8'),('b','<i8'),('c','<i8')]).reshape(len(F),3),axis=1)
    d=collections.defaultdict(list)
    for i in np.nonzero(ok&(ar>1e-10))[0]: d[key[i].tobytes()].append(i)
    opp=[];same=[]
    for ids in d.values():
        if len(ids)<2: continue
        for a in range(len(ids)):
            for b in range(a+1,len(ids)):
                (opp if np.dot(n[ids[a]],n[ids[b]])<0 else same).append((ids[a],ids[b]))
    return opp,same,len(np.nonzero(ok)[0])
if __name__=='__main__':
    P=mwgeo.load(sys.argv[1]); to=ts=0; per=collections.Counter()
    for p in P:
        n=p.get('name','')
        if not n or not p.get('vbs'): continue
        o,s,nt=pairs(p)
        if o or s:
            to+=len(o); ts+=len(s); base=n.split('_',1)[1][:-2]; per[base]+=len(o)
            if n.endswith('_A'): print('%-42s tris %6d opostos %6d iguais %5d'%(n,nt,len(o),len(s)))
    print('TOTAL opostos',to,'iguais',ts)
