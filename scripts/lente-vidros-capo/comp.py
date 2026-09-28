import numpy as np
def comps(F,nv):
    par=np.arange(nv)
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for a,b,c in F:
        ra,rb,rc=f(a),f(b),f(c); par[rb]=ra; par[f(rc)]=ra
    r=np.array([f(x) for x in range(nv)]); return r
