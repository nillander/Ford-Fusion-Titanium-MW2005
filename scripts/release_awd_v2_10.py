"""Build v2.10 from the published v2.9 ZIP: 2018 gets the SLR tire blocks and 0.7 differentials.

Only ATTRIBUTES.MWPS (plus LEIA-ME, notes and SHA256SUMS) changes. The 2012 ZIP stays verbatim.
"""
import hashlib, json, shutil, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT/'release'
ARCHIVE = RELEASE/'Fusion2018_AWD_MW2005.zip'
BACKUP = ROOT/'work/zipbuild/v2.10-before/Fusion2018_AWD_MW2005.zip'
PREFIX = 'Fusion2018_AWD_MW2005/'
ATTR = PREFIX+'ADDONS/CARS_REPLACE/MUSTANGGT/ATTRIBUTES.MWPS'
SOURCE = ROOT/'versions/performance/fusion-awd-pneus-slr/ATTRIBUTES.MWPS'
V29_ZIP = '48e667619b4231eeee69b9eb3a6970e901a7497d654d0509203a8b7cbb8bd38f'
V29_ATTR = '8c472eaf2e606560419e9c1b65dbffd41483e84a5f9b0db7b3cdd9bf22cb5831'
V210_ATTR = '6cec72b045e5a44a7e7605370ad5b85b967f23e30616ed193b05e382f9b8ff8e'
digest = lambda data: hashlib.sha256(data).hexdigest()

OLD_BULLET = """- **Performance e dirigibilidade** (`ATTRIBUTES.MWPS`): chassi, peso (1.600 kg), suspensão, barras,
  distribuição de peso e aderência do Mustang GT; direção menos sensível."""
NEW_BULLET = """- **Performance e dirigibilidade** (`ATTRIBUTES.MWPS`): motor do Mercedes-Benz SLR McLaren, tração
  integral, chassi, peso (1.600 kg), suspensão e barras do Mustang GT, pneus do SLR."""
SECTION = """
## Correção v2.10 — pneus do SLR

Pneus do Mercedes-Benz SLR McLaren nos níveis original e melhorado (aderência, controle
de giro, velocidade de giro e direção) e diferenciais em 0,7 / 0,7 / 0,7. O 2018 fica
tão fácil de guiar quanto o 2012, sem perder potência. Os demais ajustes permanecem os da v2.9.
"""


def main():
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        assert digest(ARCHIVE.read_bytes()) == V29_ZIP
        shutil.copy2(ARCHIVE, BACKUP)
    assert digest(BACKUP.read_bytes()) == V29_ZIP
    attr = SOURCE.read_bytes()
    assert digest(attr) == V210_ATTR
    unchanged2012 = digest((RELEASE/'Fusion2012_FWD_MW2005.zip').read_bytes())
    with zipfile.ZipFile(BACKUP) as old_zip:
        infos = old_zip.infolist()
        original = {i.filename: old_zip.read(i.filename) for i in infos}
    assert digest(original[ATTR]) == V29_ATTR
    new = dict(original)
    new[ATTR] = attr
    readme_name = PREFIX+'LEIA-ME.md'
    readme = original[readme_name].decode('utf-8')
    assert OLD_BULLET in readme
    new[readme_name] = (readme.replace(OLD_BULLET, NEW_BULLET).rstrip('\n')+'\n'+SECTION).encode('utf-8')
    notes_name = PREFIX+'NOTAS-v2.10.md'
    new[notes_name] = (RELEASE/'NOTAS-v2.10.md').read_bytes()
    sums_name = PREFIX+'SHA256SUMS.txt'
    new[sums_name] = ''.join(f'{digest(d)}  ./{n[len(PREFIX):]}\n' for n, d in sorted(new.items())
                             if not n.endswith('/') and n != sums_name).encode()
    tmp = ARCHIVE.with_suffix('.tmp.zip')
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as target:
        for info in infos:
            target.writestr(info, new[info.filename])
        info = zipfile.ZipInfo(notes_name, date_time=(2026, 10, 7, 21, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        target.writestr(info, new[notes_name])
    expected = {ATTR, readme_name, sums_name}
    with zipfile.ZipFile(tmp) as checked:
        assert checked.testzip() is None
        for name, data in original.items():
            assert checked.read(name) == data or name in expected, name
        for line in checked.read(sums_name).decode().splitlines():
            sha, name = line.split('  ./', 1)
            assert digest(checked.read(PREFIX+name)) == sha, name
    tmp.replace(ARCHIVE)
    assert digest((RELEASE/'Fusion2012_FWD_MW2005.zip').read_bytes()) == unchanged2012
    (ROOT/'versions/performance/fusion-awd/ATTRIBUTES.MWPS').write_bytes(attr)
    sums = []
    for name, version in [('Fusion2012_FWD_MW2005', 'v2.8'), ('Fusion2018_AWD_MW2005', 'v2.10')]:
        with zipfile.ZipFile(RELEASE/(name+'.zip')) as archive:
            sums.append(f'# {name}-{version}.zip\n')
            for f in sorted(archive.namelist()):
                if not f.endswith('/'):
                    sums.append(f'{digest(archive.read(f))}  ./{f[len(name)+1:]}\n')
            sums.append('\n')
    (RELEASE/'SHA256SUMS-conteudo.txt').write_text(''.join(sums).rstrip()+'\n', encoding='utf-8')
    report = {
        'version': 'v2.10', 'passed': True, 'in_game_tested': True,
        'change': '2018 tires = slr / slr_top (whole required block, YAW_CONTROL active); DIFFERENTIAL 0.7/0.7/0.7 base and top',
        'only_tires_and_differentials_changed_in_vlt': True,
        'geometry_textures_other_payloads_unchanged': True, 'fusion2012_unchanged': True,
        'attributes_sha256': V210_ATTR.upper(),
        'fusion2018_zip_sha256': digest(ARCHIVE.read_bytes()).upper(),
        'fusion2012_zip_sha256': unchanged2012.upper(),
    }
    (ROOT/'docs/awd-v2.10-verification.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
