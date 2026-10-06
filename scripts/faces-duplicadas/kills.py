import pickle,numpy as np,json,sys,mwgeo,collections,re
car=sys.argv[1]; R=pickle.load(open(car+'_vis.pkl','rb'))
P={p.get('name'):p for p in mwgeo.load(car+'.BIN') if p.get('name')}
C0=np.array([0,0,0.6]); K={}; st=collections.Counter()
for n,r in R.items():
    p=P[n]; v=p['vbs'][0]; F=p['idx'][:len(p['idx'])//3*3].reshape(-1,3); X=v['p'].astype(np.float64)[F]
    nn=np.cross(X[:,1]-X[:,0],X[:,2]-X[:,0]); c=X.mean(1); out=(nn*(c-C0)).sum(1)
    cnt=r['cnt']; kill=set()
    for a,b in r['opp']:
        if a in kill or b in kill: continue
        if max(cnt[a],cnt[b])>0: k=a if cnt[a]<cnt[b] else b; st['visivel' if min(cnt[a],cnt[b])<=0.1*max(cnt[a],cnt[b]) else 'dois_lados']+=1
        else: k=a if out[a]<out[b] else b; st['escondido']+=1
        kill.add(int(k))
    for a,b in r['same']:
        if a in kill or b in kill: continue
        kill.add(int(min(a,b))); st['iguais']+=1
    if kill: K[n]=sorted(kill)
json.dump(K,open(car+'_kills.json','w')); print(car,dict(st),'total',sum(len(v) for v in K.values()),'solidos',len(K))
