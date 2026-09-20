"""Merge indexed MW TPKs without recompressing or altering donor texture payloads."""
import hashlib
import json
import struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def chunk(kind,data):return struct.pack('<II',kind,len(data))+data

def read_pack(path):
    data=path.read_bytes(); tables={}
    def walk(start,end):
        p=start
        while p+8<=end:
            kind,size=struct.unpack_from('<II',data,p)
            # The original donor stores indexed compressed blocks after its header.
            if kind not in (0,0xB3300000,0xB3310000,0xB3320000,0x33310001,0x33310002,0x33310003):break
            if p+8+size>end:raise ValueError('Truncated TPK chunk')
            if kind in (0xB3300000,0xB3310000):walk(p+8,p+8+size)
            else:tables[kind]=data[p+8:p+8+size]
            p+=8+size
    walk(0,len(data))
    entries={}
    for h,offset,packed,unpacked,flags,blank in struct.iter_unpack('<6I',tables[0x33310003]):
        payload=data[offset:offset+packed]
        if len(payload)!=packed or payload[:4] not in (b'JDLZ',b'RAWW'):raise ValueError('Unsupported texture payload')
        if h in entries:raise ValueError('Duplicate texture hash')
        entries[h]=(payload,unpacked,flags,blank)
    return tables[0x33310001],entries

def main():
    info,old=read_pack(ROOT/'donor/fusion-ajm3899/MUSTANGGT/TEXTURES.BIN')
    _,new=read_pack(ROOT/'work/mw-textures/new-textures.bin')
    if old.keys()&new.keys():raise ValueError('Texture hash collision')
    merged=old|new; hashes=sorted(merged)
    table_size=24*len(hashes)
    def header(table):
        return chunk(0,b'\0'*48)+chunk(0xB3310000,chunk(0x33310001,info)+
            chunk(0x33310002,b''.join(struct.pack('<II',h,0) for h in hashes))+chunk(0x33310003,table))
    head=header(b'\0'*table_size)
    pos=8+len(head); padding=(-pos-8)%128; pre=chunk(0,b'\0'*padding);pos+=len(pre)
    blocks=[];records=[]
    for h in hashes:
        payload,unpacked,flags,blank=merged[h]
        records.append(struct.pack('<6I',h,pos,len(payload),unpacked,flags,blank))
        blocks.append(payload); pos+=len(payload)
        pad=(-pos)%128;blocks.append(b'\0'*pad);pos+=pad
    result=chunk(0xB3300000,header(b''.join(records))+pre+b''.join(blocks))
    out=ROOT/'release/MUSTANGGT/TEXTURES.BIN';out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(result)
    _,check=read_pack(out)
    assert len(check)==len(merged)
    assert all(check[h]==entry for h,entry in merged.items())
    report={'donor_textures':len(old),'new_textures':len(new),'total':len(check),'bytes':len(result),
            'donor_payloads_unchanged':True,'sha256':hashlib.sha256(result).hexdigest()}
    (ROOT/'reference/texture-validation.json').write_text(json.dumps(report,indent=2))
    print(report)
if __name__=='__main__':main()
