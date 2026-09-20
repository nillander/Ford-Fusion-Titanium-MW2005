"""Keep the Fusion textures and add opaque, unmodified Shelby rear lamp DDSs."""
import json
import shutil
import subprocess
from pathlib import Path
from PIL import Image

root=Path(__file__).resolve().parents[1]
v2=root/'versions/v2-mustang-shelby'
out=v2/'work/opaque-rear-tpk'
out.mkdir(parents=True,exist_ok=True)
catalog=json.loads((v2/'reference/texture-v2-validation.json').read_text())['textures']
entries=[(t['Name'],t['TexHash'],v2/'work/compiled-textures'/f"{t['TexHash']:08X}.dds") for t in catalog]
entries.extend([
    ('SHELBY_REAR_HOUSING',0xF18A0001,v2/'work/shelby-textures/5A00E244.dds'),
    ('SHELBY_REAR_LAMP',0xD947F346,v2/'work/shelby-textures/4B7D95B6.dds'),
])
lines=['[tpk]','name=MUSTANGGT','output=TEXTURES.BIN','']
seen=set()
for name,h,path in entries:
    assert h not in seen, hex(h)
    seen.add(h)
    if name.startswith('SHELBY_REAR'):
        with Image.open(path) as im:
            assert im.convert('RGBA').getchannel('A').getextrema()==(255,255)
    target=out/f'{h:08X}.dds'
    shutil.copy2(path,target)
    lines+=['[texture]',f'name={name}',f'hash={h:08X}',f'file={target.name}','']
(out/'textures.txt').write_text('\n'.join(lines),encoding='ascii')
subprocess.run([str(root/'tools/mwtc/mwtc.exe'),'textures.txt'],cwd=out,check=True)
print('Built rear-lamp TPK:',len(entries),'textures')
