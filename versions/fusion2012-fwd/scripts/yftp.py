import sys,struct,numpy as np
sys.path.insert(0,'/home/claude/v3/versions/v1prime/variants/v1prime-v-gta-wheel/scripts')
import rsc, yft
def P(s,o):
    v=struct.unpack_from('<Q',s,o)[0]
    return (v&0x0FFFFFFF) if (v>>28)==5 else None
def cstr(s,o):
    e=s.index(b'\0',o); return s[o:e].decode('latin1')
def u16(s,o): return struct.unpack_from('<H',s,o)[0]
def u32(s,o): return struct.unpack_from('<I',s,o)[0]
def parse(path):
    s,g,ver,n,ss,gs=rsc.load(path)
    assert s[:4]==b'FRAG'
    d=P(s,0x30); assert s[d:d+4]==b'DRFR',s[d:d+4]
    out={}
    # shaders
    sg=P(s,d+0x10); assert s[sg:sg+4]==b'MATS'
    sp=P(s,sg+0x10); sc=u16(s,sg+0x18)
    shaders=[]
    for i in range(sc):
        so=P(s,sp+8*i); pp=P(s,so); nh=u32(s,so+8); pc=s[so+0x10]; fn=u32(s,so+0x18)
        tex={}
        for k in range(pc):
            dt=s[pp+16*k]; dp=P(s,pp+16*k+8)
            if dt==0 and dp is not None:
                npp=P(s,dp+0x28)
                tex[k]=cstr(s,npp) if npp else '?'
        # param hashes after params
        hp=pp+16*pc
        # compute data size of vector params
        off=hp
        tot=0
        for k in range(pc):
            dt=s[pp+16*k]; tot+=16*dt
        hashes=[u32(s,pp+16*pc+tot+4*k) for k in range(pc)]
        shaders.append(dict(name=nh,file=fn,tex=list(tex.values()),hashes=hashes))
    out['shaders']=shaders
    # skeleton
    sk=P(s,d+0x18); bones=[]
    if sk:
        bp=P(s,sk+0x20); bc=u16(s,sk+0x5E)
        for i in range(bc):
            b=bp+0x50*i
            q=struct.unpack_from('<4f',s,b); t=struct.unpack_from('<3f',s,b+0x10); par=struct.unpack_from('<h',s,b+0x32)[0]
            nm=cstr(s,P(s,b+0x38)); tag=u16(s,b+0x44)
            bones.append(dict(name=nm,rot=q,pos=t,parent=par,tag=tag))
    out['bones']=bones
    models=[]
    for lod,off in (('high',0x50),('med',0x58),('low',0x60),('vlow',0x68)):
        lp=P(s,d+off)
        if not lp: continue
        mp=P(s,lp); mc=u16(s,lp+8)
        for mi in range(mc):
            mo=P(s,mp+8*mi)
            gp=P(s,mo+8); gc=u16(s,mo+0x10); smap=P(s,mo+0x20); sb=u32(s,mo+0x28)
            geoms=[]
            for gi in range(gc):
                go=P(s,gp+8*gi); assert s[go:go+4]==b'MESH'
                vb=P(s,go+0x18); ib=P(s,go+0x38)
                v=yft.decode_vb(s,vb)
                ni=u32(s,ib+8); idx=np.frombuffer(s,'<u2',ni,P(s,ib+0x10)).copy()
                bip=P(s,go+0x68); bic=u16(s,go+0x72)
                bids=np.frombuffer(s,'<u2',bic,bip).copy() if bip and bic else np.zeros(0,np.uint16)
                geoms.append(dict(v=v,idx=idx,shader=u16(s,smap+2*gi),bone_ids=bids))
            models.append(dict(lod=lod,index=mi,skin=(sb>>8)&0xFF,bone=(sb>>24)&0xFF,sb=sb,geoms=geoms))
    out['models']=models
    return out
if __name__=='__main__':
    import pickle
    o=parse(sys.argv[1])
    print(len(o['shaders']),'shaders',len(o['bones']),'bones',len(o['models']),'models')
    for i,sh in enumerate(o['shaders']): print(i,'%08X %08X'%(sh['name'],sh['file']),sh['tex'])
    for i,b in enumerate(o['bones']): print(i,b['name'],b['parent'],np.round(b['pos'],3),np.round(b['rot'],3))
    for m in o['models']: print(m['lod'],m['index'],'skin',m['skin'],'bone',m['bone'],hex(m['sb']),len(m['geoms']),[ (g['shader'],len(g['idx'])//3) for g in m['geoms']])
    pickle.dump(o,open(sys.argv[2],'wb'))
