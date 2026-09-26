"""Fusion 2012 FWD in the cobaltss slot: 2018 handling (from the approved mustanggt setup),
Cobalt SS engine +20% torque, front-wheel drive. Writes ATTRIBUTES.BIN + ATTRIBUTES.MWPS."""
import sys,re,struct,json
sys.path.insert(0,'/home/claude/v3/scripts')
from vlt_util import *
from copy_slr_stats_to_mustang import patch_vpak
ATTR='attr/ATTRIBUTES.BIN'
data=open(ATTR,'rb').read()
entry,raw,vlt=unpack_vpak(data)[0]
db=VltDatabase(raw,vlt)
H=hash_name
def coll(cls,name):
    r=db.find_collections(H(cls),H(name)); assert r,(cls,name); return r[0]
def req_span(cls,name):
    c=coll(cls,name); return c.required_offset, db.required_size(H(cls))
# ---- 1. apply the approved 2018 MWPS values to a working copy of the mustanggt nodes
mw=open('z10/ADDONS/CARS_REPLACE/MUSTANGGT/ATTRIBUTES.MWPS',encoding='utf-8').read().replace('\r','')
PL=re.compile(r'^patch\s+(\w+)\s+bin:(0x[0-9a-fA-F]+)\s+(\S+)')
W={'float':('<f',4),'int32':('<i',4),'int8':('<b',1),'int16':('<h',2)}
patches=[]
for line in mw.splitlines():
    m=PL.match(line.strip())
    if not m: continue
    kind,off,val=m.group(1),int(m.group(2),16),m.group(3)
    patches.append((kind,off,val))
src=bytearray(db.bin)
for kind,off,val in patches:
    fmt,n=W[kind]
    v=float(val) if kind=='float' else int(val.rstrip('Bb'),0)
    if kind!='float' and v>0x7FFFFFFF: v-=1<<32
    struct.pack_into(fmt,src,off,v)
# ---- 2. copy handling blocks mustanggt -> cobaltss (normal and _top)
out=db.bin   # bytearray, edited in place
changed=[]   # (offset,length)
def copy_block(cls,s,d):
    so,sz=req_span(cls,s); do,_=req_span(cls,d)
    out[do:do+sz]=src[so:so+sz]; changed.append((do,sz)); print('copied',cls,s,'->',d,sz,'bytes')
for cls in ('chassis','tires','brakes'):
    copy_block(cls,'mustanggt','cobaltss'); copy_block(cls,'mustanggt_top','cobaltss_top')
# ecar: the fields the 2018 MWPS sets (TireOffsets, ride, camber, body roll ...), same relative offsets
eso,esz=req_span('ecar','mustanggt'); edo,_=req_span('ecar','cobaltss')
for kind,off,val in patches:
    if eso<=off<eso+esz:
        n=W[kind][1]; out[edo+off-eso:edo+off-eso+n]=src[off:off+n]; changed.append((edo+off-eso,n))
# pvehicle: MASS, TENSOR_SCALE (required) + HandlingRating (optional)
pso,_=req_span('pvehicle','mustanggt'); pdo,_=req_span('pvehicle','cobaltss')
for fname in ('MASS','TENSOR_SCALE'):
    f=next(x for x in db.classes[H('pvehicle')].fields if x.name_hash==H(fname)); n=f.length*max(f.count,1)
    out[pdo+f.offset:pdo+f.offset+n]=src[pso+f.offset:pso+f.offset+n]; changed.append((pdo+f.offset,n))
def opt_off(name,field):
    c=coll('pvehicle',name)
    for o in c.optionals:
        if o.name_hash==H(field): return db.pointers[o.pointer]
hs,hd=opt_off('mustanggt','HandlingRating'),opt_off('cobaltss','HandlingRating')
if hs is not None and hd is not None: out[hd+8:hd+16]=src[hs+8:hs+16]; changed.append((hd+8,8)); print('HandlingRating copied')
# ---- 3. engine: Cobalt SS torque curve +20 %
tq=next(x for x in db.classes[H('engine')].fields if x.name_hash==H('TORQUE'))
for name in ('cobaltss','cobaltss_top'):
    o,_=req_span('engine',name); cap,cnt,esz=struct.unpack_from('<HHH',out,o+tq.offset); assert esz==4 and cnt<=tq.count
    d=o+tq.offset+8; vals=list(struct.unpack_from('<%df'%cnt,out,d))
    new=[v*1.2 for v in vals]; struct.pack_into('<%df'%cnt,out,d,*new); changed.append((d,4*cnt))
    print('TORQUE',name,[round(v) for v in vals],'->',[round(v) for v in new])
# ---- 4. front-wheel drive (TORQUE_SPLIT 1.0 = all torque to the front axle)
ts=next(x for x in db.classes[H('transmission')].fields if x.name_hash==H('TORQUE_SPLIT'))
for name in ('cobaltss','cobaltss_top'):
    o,_=req_span('transmission',name); struct.pack_into('<f',out,o+ts.offset,1.0); changed.append((o+ts.offset,4))
    print('TORQUE_SPLIT',name,struct.unpack_from('<f',out,o+ts.offset)[0])
# ---- 5. write MWPS (int32 words for every changed byte range; int8 for odd tails)
lines=['##'+'-'*60,'## Ford Fusion SE 2012 FWD','## Replacement for Chevrolet Cobalt SS','## Attributes.bin patch script','##'+'-'*60,'',
       'memfile GLOBAL\\GlobalMemoryFile.bin','vpak GLOBAL\\ATTRIBUTES.BIN db','',
       '## 2018 handling (chassis, tires, brakes, mass, inertia, ride), Cobalt SS engine +20% torque, TORQUE_SPLIT 1.0 (FWD)','']
seen=set()
for o,n in sorted(changed):
    k=o
    while k<o+n:
        if k in seen: k+=1; continue
        if k+4<=o+n and k%4==0:
            fv=struct.unpack_from('<f',out,k)[0]; iv=struct.unpack_from('<i',out,k)[0]
            import math
            if math.isfinite(fv) and (fv==0 or 1e-6<abs(fv)<1e7) and struct.unpack('<i',struct.pack('<f',float('%.9g'%fv)))[0]==iv:
                lines.append('patch\tfloat\tbin:0x%x\t%.9g'%(k,fv))
            else: lines.append('patch\tint32\tbin:0x%x\t%d'%(k,iv))
            seen.update(range(k,k+4)); k+=4
        else:
            lines.append('patch\tint8\tbin:0x%x\t%d'%(k,struct.unpack_from('<b',out,k)[0])); seen.add(k); k+=1
open('attr/ATTRIBUTES.MWPS','w',newline='\r\n').write('\n'.join(lines)+'\n')
print('mwps patches',sum(1 for l in lines if l.startswith('patch')))
open('attr/ATTRIBUTES.new.BIN','wb').write(data)
patch_vpak(__import__('pathlib').Path('attr/ATTRIBUTES.new.BIN'),db,entry.bin_offset)
