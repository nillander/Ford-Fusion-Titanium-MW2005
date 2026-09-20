"""Build a MW-native RAWW TPK the game can load, including donor and F18 textures."""
import json
import shutil
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'work' / 'compiled-textures'
DST = ROOT / 'work' / 'game-tpk'
DST.mkdir(exist_ok=True)
textures = json.loads((ROOT / 'reference' / 'texture-independent-validation.json').read_text())['textures']
lines = ['[tpk]', 'identifier=', 'pipelinepath=', 'output=TEXTURES.BIN', '']
for texture in textures:
    name = texture['Name']
    source = SRC / f'{texture["TexHash"]:08X}.dds'
    if not source.exists():
        raise FileNotFoundError(source)
    target = DST / f'{name}.dds'
    data = bytearray(source.read_bytes())
    flags = struct.unpack_from('<I', data, 8)[0]
    struct.pack_into('<I', data, 8, (flags & ~8) | 0x80000)
    struct.pack_into('<I', data, 20, len(data) - 128)
    target.write_bytes(data)
    lines.extend(['[texture]', f'name={name}', f'file={name}.dds', ''])
(DST / 'textures.txt').write_text('\n'.join(lines), encoding='ascii')
mwtc = ROOT / 'tools' / 'mwtc' / 'mwtc.exe'
completed = subprocess.run([str(mwtc), 'textures.txt'], cwd=DST, check=True)
out = DST / 'TEXTURES.BIN'
release = ROOT / 'release' / 'MUSTANGGT' / 'TEXTURES.BIN'
shutil.copy2(out, release)
print('Wrote', out, 'bytes', out.stat().st_size)
