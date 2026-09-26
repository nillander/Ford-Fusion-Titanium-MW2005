# Grava as normais do fix6 direto no GEOMETRY.BIN (só os 12 bytes da normal de cada vértice; tamanho igual).
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts');sys.path.insert(0,'/home/claude/c12')
import numpy as np,geo,fix6
src,dump,dst=sys.argv[1:4]
b=bytearray(open(src,'rb').read());P=geo.load(dump);pos=0;n=0
for p in P:
    vb=p['v'].tobytes()
    o=b.find(vb[:36*8],pos)
    assert o>=0 and bytes(b[o:o+len(vb)])==vb, p['name']
    pos=o+len(vb)
    if 'BODY' not in p['name']: continue
    for i,m in fix6.candidates(p).items():
        b[o+36*i+12:o+36*i+24]=np.asarray(m,'<f4').tobytes(); n+=1
open(dst,'wb').write(b); print('normais trocadas:',n)
