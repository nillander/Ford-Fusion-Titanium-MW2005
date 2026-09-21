# Fusion Titanium 2018 para MW2005

Estado atual de V2 (Mustang Shelby, slot MUSTANGGT):
[STATUS](versions/v2-mustang-shelby/STATUS.md) e
[aprendizado sobre lanternas e faróis](versions/v2-mustang-shelby/reference/APRENDIZADO_LANTERNAS_FAROIS.md).
Para reproduzir a correção de iluminação instalada, use
`scripts/build_rear_lights_v2.ps1 -Install` com o jogo fechado.
O fluxo `build.ps1` descrito abaixo pertence à compilação anterior.

O projeto de transplante visual do Fusion Titanium 2018 para MW2005. O Fusion ocupa o slot MUSTANGGT e uma compilação `mwgc`+`MergeGeometry` no catálogo `donor/fordgt` ocupa o Ford GT. A SLR McLaren foi substituída pelo SLK55 AMG.

## Reconstruir

As ferramentas estão instaladas localmente em `tools/`, e as bibliotecas Python em `work/venv/`.

```powershell
Set-Location C:\Users\nillander\NoDocuments\fusion-mw2005
.\scripts\build.ps1
```

O script interrompe a execução quando alguma etapa retorna erro. Ele verifica os hashes das entradas antes de prosseguir e não escreve em `source/` ou `donor/`.

## Arquivos

- `release/FORDGT/`: visual Fusion no slot do Ford GT, mais o exemplo FordGT-EC.
- `scripts/copy_slr_stats_to_mustang.py`: copia a performance da SLR para o mustanggt.
- `release/LEIA-ME.md`: instalação, limites e créditos.
- `blender/source-aligned.blend`: modelo completo importado e alinhado.
- `blender/fusion-mw.blend`: cena do resultado reimportado, com materiais de prévia.
- `preview/compiled-*.png`: quatro vistas geradas a partir do BIN compilado.
- `reference/release-validation.json`: verificações finais e indicação explícita de que não houve teste no jogo.
- `reference/toolchain.json`: versões e commits utilizados.
- `scripts/build.ps1`: fluxo reproduzível da extração ao pacote.

## Cadeia efetivamente utilizada

RPF7 aberto → extração Python → Sollumz I/O + PyMateria → Blender 4.5.14 → MWR → mwgc → transplante dos slots e marcadores → TPK com mwtc → leitura independente com NFS-ModTools → render do resultado e ZIP.

O repositório indicado no documento para BNV disponibilizava apenas o README quando foi consultado. Foram usados os compiladores originais de geometria e textura de Arushan. A leitura direta dos YFT com Sollumz I/O dispensou a instalação do CodeWalker neste fluxo; seu código RPF foi consultado como referência do formato.

Fontes das ferramentas: [Blender](https://www.blender.org/), [Sollumz I/O](https://github.com/Sollumz/szio), [mwgc](https://github.com/NFSTools/mwgc), [mwtc](https://github.com/NFSTools/mwtc), [NFS-ModTools](https://github.com/NFSTools/NFS-ModTools), [OpenNFSTools](https://github.com/MWisBest/OpenNFSTools).

O arquivo `demanda.md` serviu como contexto técnico. A decisão de instalar ferramentas e deixar o teste no jogo para o final foi dada diretamente pelo usuário.
