import sys,numpy as np
sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts'); import geo
def soup(parts,select=lambda n:True):
    Ps=[];Fs=[];UV=[];part=[];grp=[];tex=[];off=0;N=[]
    for pi,p in enumerate(parts):
        if not select(p['name']): continue
        v=p['v']; Ps.append(v['p'].astype(np.float64)); N.append(v['n'].astype(np.float64)); UV.append(v['uv'].astype(np.float64))
        for gi,g in enumerate(p['groups']):
            seg=p['idx'][g['offset']:g['offset']+g['length']].astype(np.int64)
            # MW uses triangle strips? check flags
            t=seg[:len(seg)//3*3].reshape(-1,3)
            Fs.append(t+off); part+= [pi]*len(t); grp+=[gi]*len(t)
            ti=g['tex'][0]; tex+=[p['tex'][ti] if ti<len(p['tex']) else 0]*len(t)
        off+=len(v)
    return dict(P=np.concatenate(Ps),N=np.concatenate(N),UV=np.concatenate(UV),F=np.concatenate(Fs),part=np.array(part),grp=np.array(grp),tex=np.array(tex,np.uint64))
