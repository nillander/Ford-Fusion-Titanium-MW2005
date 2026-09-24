import geo,numpy as np
def components(tris):
    parent={}
    def f(x):
        while parent.setdefault(x,x)!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    for a,b,c in tris:
        ra,rb,rc=f(a),f(b),f(c); parent[rb]=ra; parent[f(rc)]=ra
    lab=np.array([f(t[0]) for t in tris]); return lab
if __name__=='__main__':
    P={p['name']:p for p in geo.load('v2.dump')}
    p=P['MUSTANGGT_KIT00_BODY_A']; g=p['groups'][2]
    t=p['idx'][g['offset']:g['offset']+g['length']].astype(int).reshape(-1,3); V=p['v']['p']
    lab=components([tuple(x) for x in t])
    for l in np.unique(lab):
        tt=t[lab==l]; pts=V[tt.reshape(-1)]
        print(len(tt), 'min',pts.min(0).round(2),'max',pts.max(0).round(2))
