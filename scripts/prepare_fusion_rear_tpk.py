"""Keep V2 textures and use AJM's native opaque rear-lamp DDS."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1]
v2 = root / 'versions/v2-mustang-shelby'
source = v2 / 'work/opaque-rear-tpk'
work = v2 / 'work/fusion-rear-lenses'
out = work / 'tpk'
out.mkdir(parents=True, exist_ok=True)
subprocess.run([str(root / 'tools/dotnet/dotnet.exe'),
                str(root / 'scripts/validator/bin/Release/net8.0/Validator.dll'),
                str(root / 'donor/fusion-ajm3899/MUSTANGGT/TEXTURES.BIN'),
                str(work / 'ajm-tpk.json'), str(work / 'ajm-textures')], check=True)
catalog = json.loads((v2 / 'reference/opaque-rear-textures.json').read_text())['textures']
lines = ['[tpk]', 'name=MUSTANGGT', 'output=TEXTURES.BIN', '']
report = []
for texture in catalog:
    h = texture['TexHash']
    original = (work / 'ajm-textures' if h == 0x4B7D95B6 else source) / f'{h:08X}.dds'
    target = out / f'{h:08X}.dds'
    shutil.copy2(original, target)
    if h == 0x4B7D95B6:
        with Image.open(target) as im:
            assert im.convert('RGBA').getchannel('A').getextrema() == (255, 255)
    lines += ['[texture]', f'name={texture["Name"]}', f'hash={h:08X}', f'file={target.name}', '']
    report.append({'hash': f'{h:08X}', 'source': str(original.relative_to(root)),
                   'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
(out / 'textures.txt').write_text('\n'.join(lines), encoding='ascii')
subprocess.run([str(root / 'tools/mwtc/mwtc.exe'), 'textures.txt'], cwd=out, check=True)
(out / 'build-report.json').write_text(json.dumps(report, indent=2))
print('Native rear-light TPK ready:', len(catalog), 'textures')
