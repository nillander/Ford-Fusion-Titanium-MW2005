import struct, numpy as np
def al(o,a): return (o+a-1)//a*a
def load(path):
    b=open(path,'rb').read(); parts=[]; cur=None
    def walk(o,end):
        nonlocal cur
        while o+8<=end:
            t,l=struct.unpack_from('<Ii',b,o); s=o+8; e=s+l
            if t&0x80000000:
                if t==0x80134010:
                    cur=dict(groups=[],tex=[],sh=[],mat=[]); parts.append(cur)
                walk(s,e)
            else:
                if t==0x00134011:
                    h,=struct.unpack_from('<I',b,s+0x10); q=s+0xa0
                    nm=b[q:e].split(b'\0')[0].decode('latin1'); cur.update(name=nm,hash=h)
                elif t==0x00134012:
                    cur['tex']=[struct.unpack_from('<I',b,s+8*i)[0] for i in range(l//8)]
                elif t==0x00134013:
                    cur['sh']=[struct.unpack_from('<I',b,s+8*i)[0] for i in range(l//8)]
                elif t==0x00134900:
                    p=al(s,16); v=struct.unpack_from('<5i',b,p); cur['gc']=v[4]
                elif t==0x00134B01:
                    p=al(s,128); n=(e-p)//36
                    cur.setdefault('vbo',[]).append((p,n)); cur.setdefault('vbs',[]).append(np.frombuffer(b,dtype=np.dtype([('p','<3f4'),('n','<3f4'),('c','<u4'),('uv','<2f4')]),count=n,offset=p))
                elif t==0x00134B02:
                    p=al(s,16)
                    while p+104<=e:
                        bmin=struct.unpack_from('<3f',b,p); bmax=struct.unpack_from('<3f',b,p+12)
                        tx=b[p+24:p+29]; shi=b[p+29]
                        fl,vc,tcn,off=struct.unpack_from('<4i',b,p+56)
                        ln,=struct.unpack_from('<i',b,p+92)
                        cur['groups'].append(dict(tex=tuple(tx),sh=shi,flags=fl,vc=vc,tris=tcn,off=off,len=ln,bmin=bmin,bmax=bmax))
                        p+=104
                elif t==0x00134B03:
                    p=al(s,16); cur['idx']=np.frombuffer(b,dtype='<u2',count=(e-p)//2,offset=p)
                elif t==0x00134C02:
                    cur['mat'].append(b[s:e].split(b'\0')[0].decode('latin1'))
            o=e
    walk(0,len(b)); return parts
