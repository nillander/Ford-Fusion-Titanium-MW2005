"""Capo (item 52): o capo do GTA tem cada triangulo repetido com a face virada para baixo, na mesma posicao.
Capo de fabrica (KIT00_HOOD): toda face virada para dentro que for copia sai (coincidente ou deslocada; o verso do capo nunca e visto de cima).
Capos da loja (STYLExx_HOOD): so a copia virada para baixo em superficie quase horizontal; paredes de entradas de ar ficam.
O jogo original descarta o verso e nao mostra; com mods que desenham os dois lados, a copia (normal para baixo,
escura) briga com a pintura e o capo fica preto. Em cada par oposto coincidente, o triangulo virado para dentro
(normal contra o vetor que sai de um ponto abaixo do capo) vira degenerado. Edita no lugar."""
import sys,struct,numpy as np,mwgeo,collections
gin,gout,slot=sys.argv[1:4]
b=bytearray(open(gin,'rb').read())
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
            elif t==0x00134B03: c['i']=(al(s,16),e)
        o=e
walk(0,len(b)); C0=np.array([1.2,0,0.2]); tot=0
for c in sol:
    n=c.get('n','')
    if not (n.startswith(slot+'_') and '_HOOD_' in n and n[-1] in 'ABCDE'): continue
    stock='_KIT00_HOOD_' in n
    (vs,ve),=c['v']; nv=(ve-vs)//36
    V=np.frombuffer(bytes(b[vs:vs+nv*36]),dtype=np.dtype([('p','<3f4'),('n','<3f4'),('c','<u4'),('uv','<2f4')]))
    i0,ie=c['i']; idx=np.frombuffer(bytes(b[i0:ie]),'<u2').copy(); F=idx[:len(idx)//3*3].reshape(-1,3)
    ok=(F[:,0]!=F[:,1])&(F[:,1]!=F[:,2])&(F[:,0]!=F[:,2])
    q=np.round(V['p'].astype(np.float64)*2000).astype(np.int64)
    A,B,Cc=V['p'][F[:,0]],V['p'][F[:,1]],V['p'][F[:,2]]; nn=np.cross(B-A,Cc-A); cen=(A+B+Cc)/3
    out=((cen-C0)*nn).sum(1)
    d=collections.defaultdict(list)
    for i in np.nonzero(ok)[0]:
        k=tuple(sorted(map(tuple,q[F[i]]))); d[k].append(i)
    kill=set()
    for ids in d.values():
        if len(ids)<2: continue
        for a in ids:
            for bb in ids:
                if a<bb and np.dot(nn[a],nn[bb])<0 and a not in kill and bb not in kill:
                    if stock: kill.add(a if out[a]<out[bb] else bb)
                    else:   # capos da loja: so onde a superficie e quase horizontal (tira a copia virada para baixo)
                        za=nn[a,2]/(np.linalg.norm(nn[a])+1e-15)
                        if abs(za)>0.5: kill.add(a if za<0 else bb)
    # 2a passada: copias que ficaram deslocadas (ajustes dos farois moveram so a face de fora):
    # face virada para dentro a menos de 2 cm de uma face virada para fora tambem sai.
    ln=np.linalg.norm(nn,axis=1)+1e-15; o=out/ln/np.linalg.norm(cen-C0,axis=1)
    k2=0
    alive=ok.copy(); alive[list(kill)]=False
    outer=alive&(o>0.2); inner=alive&(o<-0.2)
    g=set(map(tuple,np.floor(cen[outer]/0.02).astype(int)))
    for i in (np.nonzero(inner)[0] if stock else []): kill.add(int(i)); k2+=1   # capo de fabrica: o verso nunca aparece de cima
    for i in kill: F[i]=F[i,0]
    idx[:len(F)*3]=F.ravel(); b[i0:ie]=idx.astype('<u2').tobytes(); tot+=len(kill)
    print('%-40s triangulos %6d  copias viradas para dentro removidas %6d (deslocadas %d)'%(n,ok.sum(),len(kill),k2))
open(gout,'wb').write(b); print('total',tot)
