# Fusion Titanium 2018 para MW2005

Projeto de transplante visual para o donor Fusion 2010 AJM3899, slot MUSTANGGT. O escopo inicial é um candidato de teste; a instalação do jogo e a validação em corrida ficaram para depois, conforme solicitado.

## Reconstruir

As ferramentas estão instaladas localmente em `tools/`, e as bibliotecas Python em `work/venv/`.

```powershell
Set-Location C:\Users\nillander\NoDocuments\fusion-mw2005
.\scripts\build.ps1
```

O script interrompe a execução quando alguma etapa retorna erro. Ele verifica os hashes das entradas antes de prosseguir e não escreve em `source/` ou `donor/`.

## Arquivos

- `release/Fusion2018_MW2005_test-v0.1.zip`: pacote para a futura instalação de teste.
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
