"""Item 27 (Fusion 2012): a parte da lanterna na tampa do porta-malas com a mesma cor/camadas da parte externa.
Na tampa (|y| < 0,585) o interior da lanterna (KIT00_LEFT/RIGHT_BRAKELIGHT_A–D, atlas <CARRO>_KIT00_HEADLIGHT_OFF)
usava a célula preta (0,562; 0,562). Agora: o anel em "C" (continuação da faixa vermelha da parte externa) usa a
célula vermelha sólida (0,8125; 0,6875) = (173,8,8); a área da luz de ré (atrás da lente transparente) usa a célula
prata (0,6875; 0,5625), a mesma da moldura prata da parte externa. O contorno preto fica (nos LODs C e D, onde anel e contorno são uma peça só, tudo vermelho). Só os 8 bytes de UV mudam."""
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts')
import numpy as np,geo
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
RED=(0.8125,0.6875); SILVER=(0.6875,0.5625); BLACK=np.array((0.5625,0.5625))
def remap(p):
    X=p['v']['p'];uv=p['v']['uv'];F=p['idx'][:len(p['idx'])//3*3].astype(int).reshape(-1,3)
    lid=(np.abs(X[F][:,:,1])<0.585).all(1)&(X[F][:,:,2]>0.55).all(1)&(X[F][:,:,0]<-1.9).all(1)
    Fl=F[lid]
    key=np.round(X/1e-4).astype(np.int64);_,w=np.unique(key,axis=0,return_inverse=True);w=w.ravel()
    W=w[Fl];n=w.max()+1;r=np.r_[W[:,0],W[:,1],W[:,2]];c=np.r_[W[:,1],W[:,2],W[:,0]]
    _,lab=connected_components(coo_matrix((np.ones(len(r)),(r,c)),shape=(n,n)),directed=False);fl=lab[W[:,0]]
    red=set();sil=set();info=[]
    for L in np.unique(fl):
        v=np.unique(Fl[fl==L]); P=X[v]; ay=np.abs(P[:,1])
        black=(np.abs(uv[v]-BLACK).max(1)<0.01).mean()
        if ay.min()>=0.44 and P[:,2].min()>=0.675 and P[:,2].max()<=0.75:
            sil|=set(v.tolist()); info.append(('ré',len(v)))
        elif black>0.99 and ay.min()>0.36 and np.ptp(P[:,2])>0.06:
            red|=set(v.tolist()); info.append(('anel',len(v)))
        elif black>0.9 and p['name'][-1] in 'CD' and np.ptp(P[:,2])>0.1:
            # far LODs: ring and outline are one welded piece -> its black vertices go red
            vb=v[np.abs(uv[v]-BLACK).max(1)<0.01]
            red|=set(vb.tolist()); info.append(('anel+contorno',len(vb)))
    # vertices used by triangles outside the lid set are left alone
    out=np.zeros(len(X),bool); out[np.unique(F[~lid])]=True
    red=[v for v in red if not out[v]]; sil=[v for v in sil if not out[v]]
    return red,sil,info
if __name__=='__main__':
    src,dump,dst=sys.argv[1:4]
    b=bytearray(open(src,'rb').read());Z=geo.load(dump);pos=0
    for p in Z:
        vb=p['v'].tobytes(); o=b.find(vb[:36*8],pos)
        assert o>=0 and bytes(b[o:o+len(vb)])==vb,p['name']; pos=o+len(vb)
        if '_BRAKELIGHT_' not in p['name'] or 'GLASS' in p['name']: continue
        red,sil,info=remap(p)
        for v in red: b[o+36*v+28:o+36*v+36]=np.asarray(RED,'<f4').tobytes()
        for v in sil: b[o+36*v+28:o+36*v+36]=np.asarray(SILVER,'<f4').tobytes()
        print(p['name'],'red',len(red),'silver',len(sil),info)
    open(dst,'wb').write(b)
