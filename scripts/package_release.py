import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
release=ROOT/'release'
report=json.loads((ROOT/'reference/release-validation.json').read_text())
assert report['passed'] and not report['in_game_tested']
fordgt=release/'FORDGT'
fordgt.mkdir(exist_ok=True)
shutil.copy2(ROOT/'work/fordgt-vanilla/VINYLS.BIN',fordgt/'VINYLS.BIN')
shutil.copy2(ROOT/'work/fordgt-vanilla/PREVINYL.BIN',fordgt/'PREVINYL.BIN')
mustang=release/'MUSTANGGT'
mustang.mkdir(exist_ok=True)
vanilla=ROOT/'work/vanilla-mustang-extract/Need For Speed Most Wanted Black Edition/CARS/MUSTANGGT'
for filename in ('GEOMETRY.BIN','TEXTURES.BIN','VINYLS.BIN','PREVINYL.BIN'):
    shutil.copy2(vanilla/filename,mustang/filename)
(release/'credits').mkdir(exist_ok=True)
shutil.copy2(ROOT/'donor/fusion-ajm3899/readme.txt',release/'credits/donor-readme.txt')
shutil.copy2(ROOT/'source/fusion-2017-dev/leai-me.txt',release/'credits/source-readme.txt')
readme=f'''# Fusion Titanium 2018 — MW2005 — candidato de teste v0.1

Pacote gerado e verificado fora do jogo. Ainda NÃO foi testado no MW2005 neste slot.
Substitui o Ford GT (slot FORDGT) pelo visual atual do Fusion Titanium.
Restaura o Ford Mustang GT original no slot MUSTANGGT.

## Instalação

1. Faça backup de `CARS/FORDGT` e `CARS/MUSTANGGT`.
2. Copie `CARS/FORDGT` deste pacote por cima da pasta do Ford GT.
3. Copie `CARS/MUSTANGGT` deste pacote por cima da pasta do Mustang GT.
4. Teste o Ford GT no seletor: visual Fusion, performance do Ford GT.
5. Confirme que o Mustang GT voltou ao modelo original.

O handling, classes e nome de menu do Ford GT permanecem os do jogo.
As texturas do Fusion continuam com os hashes já conhecidos do TPK.

## Conteúdo e verificações

- GEOMETRY.BIN do Fusion no slot FORDGT: {report['parts']} peças; preserva os {report['original_slots_preserved']} nomes originais do Ford GT.
- {report['triangles_lod_a']:,} triângulos somando as peças A do arquivo; {report['triangles_all_lods']:,} somando todos os LODs.
- TEXTURES.BIN: atlas do Fusion Titanium, incluindo `MUSTANGGT_RIM`.
- Rodas e marcadores visuais vêm do modelo Fusion atual, não das malhas do Ford GT.
- Os arquivos de entrada em donor/ e source/ não foram modificados.

## Limites desta versão

Peças exclusivas do Ford GT (capôs da loja, dano, faróis esquerdos separados) ficam como placeholders vazios para não reaparecer o GT original.
Os faróis e lanternas do Fusion já cobrem os dois lados na malha RIGHT.
Ainda depende de inspeção no motor do jogo.

## Roteiro de teste

Abra a garagem no Ford GT, entre numa corrida e compare com o Mustang restaurado.
Confira rodas, altura, faróis, lanternas e LODs.

## Créditos

Donor visual: Marcelo Castro (AJM3899); Turn 10 Studios; Riva; FOX; Porsche4ever; AJ Lethal.
Fonte GTA: modelo AND1V79; disponibilização Gabriel Lima; motor CH4P4X.
Slot de performance: Ford GT original do MW2005.
Ferramentas: Blender, Sollumz I/O/PyMateria, mwgc/mwtc de Arushan, NFSTools/NFS-ModTools, MWisBest/OpenNFSTools.
'''
(release/'LEIA-ME.md').write_text(readme,encoding='utf-8')
for filename in ('release-validation.json','geometry-validation.json','texture-independent-validation.json','materials.json','alignment.json','lod-report.json'):
    (release/'validation').mkdir(exist_ok=True)
    shutil.copy2(ROOT/'reference'/filename,release/'validation'/filename)
for name in ('perspective','rear','side','front'):
    (release/'preview').mkdir(exist_ok=True)
    shutil.copy2(ROOT/'preview'/f'compiled-{name}.png',release/'preview'/f'{name}.png')
manifest={}
for slot in ('FORDGT','MUSTANGGT'):
    for path in sorted((release/slot).glob('*')):
        with path.open('rb') as file:
            digest=hashlib.file_digest(file,'sha256').hexdigest()
        manifest[f'{slot}/{path.name}']={'bytes':path.stat().st_size,'sha256':digest}
(release/'SHA256.json').write_text(json.dumps(manifest,indent=2))
archive=release/'Fusion2018_MW2005_test-v0.1.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive_file:
    for path in sorted(release.rglob('*')):
        if not path.is_file() or path.suffix=='.zip':continue
        relative=path.relative_to(release)
        target=Path('CARS')/relative if relative.parts[0] in ('FORDGT','MUSTANGGT') else relative
        archive_file.write(path,target.as_posix())
with zipfile.ZipFile(archive) as archive_file:
    assert archive_file.testzip() is None
print('Package:',archive,'bytes:',archive.stat().st_size)
