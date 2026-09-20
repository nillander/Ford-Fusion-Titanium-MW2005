"""Extract unencrypted RPF7 archives; layout reference: dexyfex/CodeWalker RpfFile.cs."""
import hashlib
import json
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
records = []

def extract(data, destination, depth=0):
    if depth > 16:
        raise ValueError('Archive nesting limit')
    magic, count, names_size, encryption = struct.unpack_from('<4I', data)
    if magic != 0x52504637 or encryption not in (0, 0x4E45504F):
        raise ValueError(f'Unsupported or encrypted RPF: {encryption:08x}')
    end = 16 + count * 16
    names = data[end:end + names_size]
    if len(names) != names_size:
        raise ValueError('Truncated table')
    entries = [data[16+i*16:32+i*16] for i in range(count)]
    visited = set()

    def visit(index, parent):
        if index in visited or not 0 <= index < count:
            raise ValueError('Invalid directory tree')
        visited.add(index)
        e = entries[index]
        a, b, c, d = struct.unpack('<4I', e)
        directory = b == 0x7FFFFF00
        no = a if directory else a & 0xFFFF
        terminator = names.find(b'\0', no)
        if terminator < no:
            raise ValueError('Invalid name')
        name = names[no:terminator].decode('utf-8')
        if index == 0:
            target = parent
        else:
            if not name or name in ('.', '..') or any(x in name for x in '/\\:'):
                raise ValueError('Unsafe archive name')
            target = parent / name
        if directory:
            for child in range(c, c+d):
                visit(child, target)
            return
        resource = bool(b & 0x80000000)
        size = int.from_bytes(e[2:5], 'little')
        offset = (int.from_bytes(e[5:8], 'little') & 0x7FFFFF) * 512
        if resource and size == 0xFFFFFF:
            h = data[offset:offset+16]
            size = h[7] | h[14] << 8 | h[5] << 16 | h[2] << 24
        packed = data[offset:offset+(size or c)]
        if len(packed) != (size or c):
            raise ValueError('Truncated file')
        if not resource and d:
            raise ValueError('Encrypted binary entry')
        payload = zlib.decompress(packed, -15) if size and not resource else packed
        if not resource and len(payload) != c:
            raise ValueError('Uncompressed size mismatch')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        records.append({'path': str(target.relative_to(ROOT)), 'bytes': len(payload),
                        'sha256': hashlib.sha256(payload).hexdigest(), 'resource': resource})
        print(target.relative_to(ROOT), len(payload))
        if target.suffix.lower() == '.rpf':
            extract(payload, target.with_suffix('.extracted'), depth+1)

    visit(0, destination)

if __name__ == '__main__':
    extract((ROOT/'source/fusion-2017-dev/fusion/dlc.rpf').read_bytes(), ROOT/'work/source-extracted')
    (ROOT/'reference/rpf-inventory.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
