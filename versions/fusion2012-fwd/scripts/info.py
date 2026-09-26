import pickle,numpy as np,sys
o=pickle.load(open(sys.argv[1],'rb'))
B=o['bones']
for m in o['models']:
  for gi,g in enumerate(m['geoms']):
    v=g['v'];p=v['Position']
    bi=v.get('BlendIndices');bw=v.get('BlendWeights')
    if bi is not None:
        loc=bi[np.arange(len(p)),bw.argmax(1)]
        mapped=g['bone_ids'][loc] if len(g['bone_ids']) else loc
        cnt=np.bincount(mapped.astype(int),minlength=len(B))
        top=[(B[k]['name'],int(cnt[k])) for k in np.argsort(-cnt)[:3] if cnt[k]]
    else: top=[]
    print(m['lod'],gi,'sh',g['shader'],o['shaders'][g['shader']]['tex'][0],len(p),len(g['idx'])//3,np.round(p.min(0),2),np.round(p.max(0),2),top)
