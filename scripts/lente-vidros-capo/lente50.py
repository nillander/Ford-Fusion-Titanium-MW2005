"""Lente do farol do Fusion 2018: aponta a UV de KIT00_RIGHT_HEADLIGHT_GLASS_A-D para uma celula
clara e quase transparente (RGB ~226, alfa 4/15 = 27 %, igual a lente do 2012) pintada numa area livre
do atlas MUSTANGGT_KIT00_HEADLIGHT_OFF (x 512-575, y 128-191). O pisca ambar (UV u > 0,332,
na celula laranja) nao e alterado. Edita os dois BIN no lugar (mesmo tamanho)."""
import sys,struct,shutil,numpy as np,mwgeo,tpk
gin,tin,gout,tout=sys.argv[1:5]
X0,Y0,S=512,128,64; U=(X0+S/2)/1024; V=(Y0+S/2)/1024
RGB=(226,228,232); A4=4
# textura
tb=bytearray(open(tin,'rb').read()); T=tpk.load2(tin); x=T[0x95de5b23]; assert x['fmt']==0x33545844 and x['w']==1024
c=((RGB[0]*31+127)//255<<11)|((RGB[1]*63+127)//255<<5)|((RGB[2]*31+127)//255)
blk=bytes([A4|(A4<<4)]*8)+struct.pack('<HHI',c,c,0)
for by in range(Y0//4,(Y0+S)//4):
    for bx in range(X0//4,(X0+S)//4):
        o=x['base']+(by*256+bx)*16; tb[o:o+16]=blk
open(tout,'wb').write(tb)
# geometria
gb=bytearray(open(gin,'rb').read()); P=mwgeo.load(gin); n=0
for p in P:
    nm=p.get('name','')
    if 'HEADLIGHT_GLASS_' in nm and nm.startswith('MUSTANGGT_KIT00_RIGHT'):
        for (o,cnt) in p['vbo']:
            k=0
            for i in range(cnt):
                u0,=struct.unpack_from('<f',gb,o+i*36+28)
                if u0>0.332: continue   # pisca ambar: celula laranja do atlas, fica como esta
                struct.pack_into('<2f',gb,o+i*36+28,U,V); k+=1
            n+=k; print(nm,cnt,'vertices,',k,'movidos,',cnt-k,'ambar mantidos')
open(gout,'wb').write(gb); print('uv',U,V,'total',n)
