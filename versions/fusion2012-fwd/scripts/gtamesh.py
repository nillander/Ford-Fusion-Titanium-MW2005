import pickle,numpy as np
def soup(pkl,lod='high'):
    o=pickle.load(open(pkl,'rb')); B=o['bones']
    Ps=[];Ns=[];UVs=[];Fs=[];sh=[];bo=[];gid=[];off=0
    for m in o['models']:
        if m['lod']!=lod: continue
        for gi,g in enumerate(m['geoms']):
            v=g['v'];p=v['Position'].astype(np.float64)
            n=v['Normal'].astype(np.float64) if 'Normal' in v else np.zeros_like(p)
            uv=v['TexCoord0'].astype(np.float64) if 'TexCoord0' in v else np.zeros((len(p),2))
            bi=v.get('BlendIndices');bw=v.get('BlendWeights')
            if bi is not None:
                loc=bi[np.arange(len(p)),bw.argmax(1)]
                vb=g['bone_ids'][loc] if len(g['bone_ids']) else loc
            else: vb=np.full(len(p),m['bone'])
            I=g['idx'][:len(g['idx'])//3*3].reshape(-1,3).astype(np.int64)
            # triangle bone = majority
            tb=vb[I]; t=np.where(tb[:,1]==tb[:,2],tb[:,1],tb[:,0])
            Ps.append(p);Ns.append(n);UVs.append(uv);Fs.append(I+off);off+=len(p)
            sh.append(np.full(len(I),g['shader']));bo.append(t);gid.append(np.full(len(I),gi))
    return dict(P=np.concatenate(Ps),N=np.concatenate(Ns),UV=np.concatenate(UVs),F=np.concatenate(Fs),
                shader=np.concatenate(sh),bone=np.concatenate(bo),geom=np.concatenate(gid),
                bones=[b['name'] for b in B],shaders=o['shaders'])
