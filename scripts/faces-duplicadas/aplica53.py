"""Item 53: remove faces duplicadas na mesma posição (todas as peças e LODs).
Uso: python aplica53.py GEO_in GEO_out kills.json
kills.json = {nome_do_solido: [indice_do_triangulo, ...]}. Cada triângulo listado vira degenerado
(três índices iguais); vértices, contagens e grupos não mudam."""
import sys,struct,json,numpy as np
gin,gout,kf=sys.argv[1:4]; K=json.load(open(kf)); b=bytearray(open(gin,'rb').read())
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
            elif t==0x00134B03: c['i']=(al(s,16),e)
        o=e
walk(0,len(b)); tot=0; seen=set()
for c in sol:
    n=c.get('n','')
    if n not in K: continue
    i0,ie=c['i']; idx=np.frombuffer(bytes(b[i0:ie]),'<u2').copy(); F=idx[:len(idx)//3*3].reshape(-1,3)
    k=np.array(K[n],int); F[k]=F[k,0:1]; idx[:len(F)*3]=F.ravel(); b[i0:ie]=idx.astype('<u2').tobytes()
    tot+=len(k); seen.add(n)
assert seen==set(K),set(K)-seen
open(gout,'wb').write(b); print('solidos',len(seen),'triangulos removidos',tot)
