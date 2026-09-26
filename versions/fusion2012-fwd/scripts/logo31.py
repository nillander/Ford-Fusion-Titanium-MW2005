"""Item 31: logotipo Ford da tampa do porta-malas com a escrita e o aro prata, como na frente (Fusion 2012 e 2018).
O oval traseiro (BASE_A–E, textura <CARRO>_MISC) tinha a escrita "Ford" e o aro com UV (0,0) = borda preta da
textura (8,8,8); o da frente usa a célula prata (0,17; 0,25) = (148,150,156) para escrita/aro e uma célula preta para
o fundo. Aqui: peças soltas do oval traseiro (soldadas por posição) exceto o fundo (maior área vista de trás) e a
base (profundidade > 1,2 cm) recebem UV (0,17; 0,25); o fundo e a base passam para a área preta (0,88; 0,75),
como o fundo do oval da frente (antes (0,34; 0), na borda da textura: preto e cinza alternando). Só os 8 bytes de UV de cada vértice mudam (tamanho igual)."""
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts');sys.path.insert(0,'/home/claude/c12')
import numpy as np,geo
from ov2 import comps
CHROME=(0.17,0.25)
BLACK=(0.88,0.75)   # solid black area used by the front oval's background
BOX=lambda c:(c[:,0]<-2.2)&(np.abs(c[:,1])<0.06)&(c[:,2]>0.745)&(c[:,2]<0.81)
def chrome_verts(p):
    X=p['v']['p'];out=set();blk=set();info=[]
    allF=p['idx'][:len(p['idx'])//3*3].astype(int)
    for gi,g in enumerate(p['groups']):
        try: m,Fm,fl=comps(p,gi,BOX)
        except Exception: continue
        if not len(Fm): continue
        labs=np.unique(fl); yz=[];dx=[]
        for L in labs:
            T=X[Fm[fl==L]]; a=T[:,1,1:]-T[:,0,1:]; b=T[:,2,1:]-T[:,0,1:]
            yz.append(np.abs(a[:,0]*b[:,1]-a[:,1]*b[:,0]).sum()/2); dx.append(T[:,:,0].max()-T[:,:,0].min())
        face=labs[int(np.argmax(yz))]
        for L,d in zip(labs,dx):
            if L==face or d>0.012: blk.update(Fm[fl==L].ravel().tolist()); continue
            out|=set(Fm[fl==L].ravel().tolist())
        info.append((gi,len(labs),face))
    # never touch a vertex also used by a triangle outside the chrome set
    g=np.zeros(len(X),bool); g[list(out)]=True
    F=p['idx'].astype(int)
    for gg in p['groups']:
        seg=F[gg['offset']:gg['offset']+gg['length']].reshape(-1,3)
        # triangles touching chrome verts but not entirely chrome -> unsafe verts
        part=g[seg].any(1)&~g[seg].all(1)
        if part.any():
            for v in np.unique(seg[part].ravel()): g[v]=False if v in out and not all(g[seg[(seg==v).any(1)]].all(1)) else g[v]
    return np.nonzero(g)[0],np.array(sorted(blk-out),int),info
if __name__=='__main__':
    src,dump,dst,pre=sys.argv[1:5]
    b=bytearray(open(src,'rb').read());P=geo.load(dump);pos=0;n=0
    for p in P:
        vb=p['v'].tobytes(); o=b.find(vb[:36*8],pos)
        assert o>=0 and bytes(b[o:o+len(vb)])==vb,p['name']; pos=o+len(vb)
        if not p['name'].startswith(pre+'_BASE_'): continue
        vs,vb2,info=chrome_verts(p)
        for v in vs: b[o+36*v+28:o+36*v+36]=np.asarray(CHROME,'<f4').tobytes()
        for v in vb2: b[o+36*v+28:o+36*v+36]=np.asarray(BLACK,'<f4').tobytes()
        n+=len(vs); print(p['name'],'chrome verts',len(vs),'black verts',len(vb2),info)
    open(dst,'wb').write(b); print('total',n)
