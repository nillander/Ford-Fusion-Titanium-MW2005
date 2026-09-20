import hashlib
import json
import struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for directory in ('work','reference','blender','preview','release/FORDGT'):
    (ROOT/directory).mkdir(parents=True,exist_ok=True)
manifest={}
# Only the two declared conversion inputs are immutable. Other reference cars
# may be added under donor/ without invalidating this build's recorded inputs.
for directory in ('donor/fusion-ajm3899','source/fusion-2017-dev'):
    for path in sorted((ROOT/directory).rglob('*')):
        if path.is_file():
            with path.open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
            manifest[str(path.relative_to(ROOT))]={'bytes':path.stat().st_size,'sha256':digest}
previous=ROOT/'reference/input-manifest.json'
if previous.exists() and json.loads(previous.read_text())!=manifest:
    raise RuntimeError('Input files changed since the recorded manifest. Review the change before rebuilding.')
previous.write_text(json.dumps(manifest,indent=2),encoding='utf-8')
data=bytearray((ROOT/'donor/fusion-ajm3899/MUSTANGGT/GEOMETRY.BIN').read_bytes())
struct.pack_into('<I',data,4,len(data)-8)
(ROOT/'work/donor-nested.bin').write_bytes(data)
print('Inputs recorded:',len(manifest))
