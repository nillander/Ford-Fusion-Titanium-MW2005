"""Aplica o layout51 (vidros: uma chapa por janela, UV 0-1 sem espelho) nos solidos
<SLOT>_KIT00_FRONT_WINDOW_A-D e REAR_WINDOW_A-D. Edita no lugar: mesmo numero de vertices e indices;
triangulos descartados viram degenerados no fim do ultimo grupo."""
import sys,struct,numpy as np
gin,gout,slot=sys.argv[1:4]
L=np.load('layout51.npz'); b=bytearray(open(gin,'rb').read())
def al(o,a): return (o+a-1)//a*a
sol=[]
def walk(o,end):
    while o+8<=end:
        t,l=struct.unpack_from('<Ii',b,o); s=o+8; e=s+l
        if t&0x80000000:
            if t==0x80134010: sol.append({})
            walk(s,e)
        else:
            c=sol[-1] if sol else None
            if t==0x00134011: c['n']=bytes(b[s+0xa0:e]).split(b'\0')[0].decode()
            elif t==0x00134B01: c.setdefault('v',[]).append((al(s,128),e))
            elif t==0x00134B02: c['g']=(al(s,16),e)
            elif t==0x00134B03: c['i']=(al(s,16),e)
        o=e
walk(0,len(b)); done=0
for c in sol:
    n=c.get('n','')
    for key in ('FRONT_WINDOW','REAR_WINDOW'):
        if n.startswith(slot+'_KIT00_'+key+'_') and n[-1] in 'ABCD':
            k=key+'_A'; vm=L[k+'_vmap']; uv=L[k+'_uv']; idx=L[k+'_idx']; G=L[k+'_groups']
            (vs,ve),=c['v']; nv=(ve-vs)//36; assert nv==len(vm),(n,nv,len(vm))
            old=np.frombuffer(bytes(b[vs:vs+nv*36]),np.uint8).reshape(nv,36).copy()
            new=old[vm].copy(); new[:,28:36]=uv.astype('<f4').view(np.uint8).reshape(-1,8)
            b[vs:vs+nv*36]=new.tobytes()
            i0,ie=c['i']; assert (ie-i0)//2>=len(idx); b[i0:i0+2*len(idx)]=idx.astype('<u2').tobytes()
            gs,ge=c['g']; assert (ge-gs)//104==6
            P=np.frombuffer(new[:,0:12].tobytes(),'<f4').reshape(-1,3)
            for gi,(v0,vc,ii,ic) in enumerate(G):
                p=gs+104*gi; used=idx[ii:ii+ic]; pp=P[np.unique(used)]
                struct.pack_into('<6f',b,p,*pp.min(0),*pp.max(0))
                struct.pack_into('<3i',b,p+60,int(vc),int(ic//3),int(ii)); struct.pack_into('<i',b,p+92,int(ic))
            done+=1; print('ok',n)
assert done==8,done
open(gout,'wb').write(b)
