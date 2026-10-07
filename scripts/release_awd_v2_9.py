"""Build v2.9 from the approved v2.8 ZIP, changing only the 2018 AWD settings.

No game files are written. Preserve all BIN payloads and the 2012 ZIP verbatim.
"""
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT/'release'
ARCHIVE = RELEASE/'Fusion2018_AWD_MW2005.zip'
BACKUP = ROOT/'work/zipbuild/v2.9-before/Fusion2018_AWD_MW2005.zip'
PREFIX = 'Fusion2018_AWD_MW2005/'
ATTR = PREFIX+'ADDONS/CARS_REPLACE/MUSTANGGT/ATTRIBUTES.MWPS'
CHANGES = {'0x1e718': '0.5', '0x1f690': '0.5', '0x1e6e4': '0.75', '0x1f65c': '0.75'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        assert digest(ARCHIVE.read_bytes()) == 'd786292c56092eefac98e4cab19e1a7d16a1b15a4b9d367d5b6c76a1f9d51e71'
        shutil.copy2(ARCHIVE, BACKUP)
    assert digest(BACKUP.read_bytes()) == 'd786292c56092eefac98e4cab19e1a7d16a1b15a4b9d367d5b6c76a1f9d51e71'
    unchanged2012 = digest((RELEASE/'Fusion2012_FWD_MW2005.zip').read_bytes())
    with zipfile.ZipFile(BACKUP) as old_zip:
        infos = old_zip.infolist()
        original = {info.filename: old_zip.read(info.filename) for info in infos}
    assert digest(original[ATTR]) == '3be53cf93b914ddebf65efc1cc22fb1594c74be74b8482e288954280c9b40617'
    new = dict(original)
    text = original[ATTR].decode('utf-8')
    for offset, value in CHANGES.items():
        pattern = rf'(?m)^(patch\s+float\s+bin:{offset}\s+)0(?=\r?$)'
        text, count = re.subn(pattern, lambda match: match[1]+value, text)
        assert count == 1, offset
    new[ATTR] = text.encode('utf-8')
    # Exactly four values differ; comments and every other patch are unchanged.
    altered = [(a,b) for a,b in zip(original[ATTR].decode().splitlines(),text.splitlines()) if a!=b]
    assert len(altered) == 4
    source = ROOT/'versions/performance/fusion-awd/ATTRIBUTES.MWPS'
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_bytes(new[ATTR])
    readme_name = PREFIX+'LEIA-ME.md'
    readme = original[readme_name].decode('utf-8')
    readme = readme.replace('Release v2.8 de 06/10/2026.', 'Release v2.9 de 07/10/2026.')
    readme += '\n## Correção v2.9 — AWD\n\nTração integral nos níveis original e melhorado: TORQUE_SPLIT 0,5 e\ndiferencial central ativo (0,75). Os demais ajustes permanecem os da v2.8.\n'
    new[readme_name] = readme.encode('utf-8')
    notes_name = PREFIX+'NOTAS-v2.9.md'
    new[notes_name] = (RELEASE/'NOTAS-v2.9.md').read_bytes()
    sums_name = PREFIX+'SHA256SUMS.txt'
    new[sums_name] = ''.join(f'{digest(data)}  ./{name[len(PREFIX):]}\n'
                           for name,data in sorted(new.items())
                           if not name.endswith('/') and name!=sums_name).encode()
    temporary = ARCHIVE.with_suffix('.tmp.zip')
    with zipfile.ZipFile(temporary,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as target:
        for info in infos:
            target.writestr(info,new[info.filename])
        info = zipfile.ZipInfo(notes_name, date_time=(2026,10,7,12,0,0))
        info.compress_type = zipfile.ZIP_DEFLATED
        target.writestr(info,new[notes_name])
    with zipfile.ZipFile(temporary) as checked:
        assert checked.testzip() is None
        expected_changes = {ATTR,readme_name,sums_name}
        for name,data in original.items():
            assert checked.read(name)==data or name in expected_changes, name
        for line in checked.read(sums_name).decode().splitlines():
            sha,name = line.split('  ./',1)
            assert digest(checked.read(PREFIX+name))==sha, name
    temporary.replace(ARCHIVE)
    assert digest((RELEASE/'Fusion2012_FWD_MW2005.zip').read_bytes())==unchanged2012
    global_sums = []
    for name,version in [('Fusion2012_FWD_MW2005','v2.8'),('Fusion2018_AWD_MW2005','v2.9')]:
        with zipfile.ZipFile(RELEASE/(name+'.zip')) as archive:
            global_sums.append(f'# {name}-{version}.zip\n')
            for file in sorted(archive.namelist()):
                if not file.endswith('/'):
                    global_sums.append(f'{digest(archive.read(file))}  ./{file[len(name)+1:]}\n')
            global_sums.append('\n')
    (RELEASE/'SHA256SUMS-conteudo.txt').write_text(''.join(global_sums).rstrip()+'\n',encoding='utf-8')
    report = {
        'version':'v2.9', 'passed':True, 'in_game_tested':False,
        'patch_changes':CHANGES, 'only_four_patch_values_changed':True,
        'geometry_textures_other_payloads_unchanged':True, 'fusion2012_unchanged':True,
        'attributes_sha256':digest(new[ATTR]).upper(),
        'fusion2018_zip_sha256':digest(ARCHIVE.read_bytes()).upper(),
        'fusion2012_zip_sha256':unchanged2012.upper(),
    }
    (ROOT/'docs/awd-v2.9-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
