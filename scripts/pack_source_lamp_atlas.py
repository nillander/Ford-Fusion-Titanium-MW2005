"""Pack Blender's source-geometry renders as an opaque MW DXT3 texture."""
import hashlib
import json
import struct
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'versions/v2-mustang-shelby/work/source-lamp-bake'
projection = json.loads((OUT/'projection.json').read_text())
atlas = Image.new('RGBA', (1024, 1024), (12, 15, 20, 255))
for end, y in (('front', 0), ('rear', 512)):
    with Image.open(OUT/(end+'-source-bake.png')) as image:
        assert image.size == (1024, 512)
        atlas.paste(image.convert('RGB').convert('RGBA'), (0, y))
atlas.save(OUT/'fusion2018-lamps-atlas.png')
dds = OUT/'4B7D95B6.dds'
atlas.save(dds, pixel_format='DXT3')
data = bytearray(dds.read_bytes())
flags = struct.unpack_from('<I', data, 8)[0]
struct.pack_into('<I', data, 8, (flags & ~8) | 0x80000)
struct.pack_into('<I', data, 20, len(data)-128)
dds.write_bytes(data)
with Image.open(dds) as check:
    assert check.convert('RGBA').getchannel('A').getextrema() == (255, 255)
report = {'origin': 'Blender renders of extracted Fusion 2018 source geometry',
          'uses_2010_artwork': False, 'uses_user_generated_reference': False,
          'texture_hash': '4B7D95B6', 'format': 'DXT3', 'size': [1024, 1024],
          'alpha_range': [255, 255], 'dds_sha256': hashlib.sha256(data).hexdigest(),
          'source_sha256': projection['source_sha256']}
(OUT/'atlas-report.json').write_text(json.dumps(report, indent=2))
print('SOURCE_ATLAS_READY', report['dds_sha256'])
