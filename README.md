# Ford Fusion 2012 FWD e Fusion Titanium 2018 AWD para NFS Most Wanted 2005

**Versão final: v2.0** (27/09/2026), com os dois carros:

- **Fusion 2012 FWD**: substitui o Chevrolet Cobalt SS (slot `COBALTSS`, carro inicial).
  Detalhes em [versions/fusion2012-fwd/LEIA-ME.md](versions/fusion2012-fwd/LEIA-ME.md).
- **Fusion Titanium 2018 AWD**: substitui o Ford Mustang GT (slot `MUSTANGGT`).

Os dois zips estão em [`release/`](release/). Cada um abre numa pasta com o nome do arquivo e traz o
`instalar.bat`. Instalação e créditos em [release/LEIA-ME.md](release/LEIA-ME.md).

## Onde fica cada coisa
- [`docs/TODO.md`](docs/TODO.md): lista do que foi pedido, feito e aprovado no jogo.
- [`docs/CONTINUACAO.md`](docs/CONTINUACAO.md): estado atual e como retomar o trabalho.
- [`docs/APRENDIZADOS.md`](docs/APRENDIZADOS.md): lições técnicas do Most Wanted, com imagens.
- [`docs/PORTAR-PARA-NFSU2.md`](docs/PORTAR-PARA-NFSU2.md): como levar um carro já aprovado aqui para o Underground 2. O Fusion 2018 AWD foi o primeiro; o método está nesse arquivo.
- [`docs/imagens-projeto/`](docs/imagens-projeto/README.md): galeria de imagens, etapa por etapa.
- [`docs/historico/`](docs/historico/): pedido inicial (`demanda-inicial.md`) e a release de teste v0.1.
- [`versions/`](versions/LEIA-ME.md): histórico de cada versão. O 2012 fica em `versions/fusion2012-fwd/`; o 2018 em
  `versions/v1prime/` (variantes, capturas no jogo e checkpoints).
- `release/`: os zips de distribuição, o instalador e as notas da v2.0.
- `assets/`: logotipos. `source/` e `donor/`: modelos de origem (GTA V) e carros-base do MW. `tools/`: ferramentas.
- `scripts/`, `reference/`, `preview/`, `blender/` e `work/`: fluxo de montagem das versões v0.1–v3 (descrito abaixo).
  `work/` também guarda os pacotes intermediários do 2012 (`work/c2012-stage/`) e a montagem dos zips (`work/zipbuild/`).

O conteúdo abaixo descreve o fluxo das versões anteriores (v0.1–v3) e fica como histórico.

O projeto de transplante visual do Fusion Titanium 2018 para MW2005. O Fusion ocupa o slot MUSTANGGT e uma compilação `mwgc`+`MergeGeometry` no catálogo `donor/fordgt` ocupa o Ford GT. A SLR McLaren foi substituída pelo SLK55 AMG.

## Reconstruir

As ferramentas estão instaladas localmente em `tools/`, e as bibliotecas Python em `work/venv/`.

```powershell
Set-Location C:\Users\nillander\NoDocuments\fusion-mw2005
.\scripts\build.ps1
```

O script interrompe a execução quando alguma etapa retorna erro. Ele verifica os hashes das entradas antes de prosseguir e não escreve em `source/` ou `donor/`.

## Arquivos

- `versions/performance/`: as três performances do Fusion no slot MUSTANGGT. A instalada é `slr-m3gtr`.
- `scripts/apply_m3gtr_performance.py`: grava `slr-m3gtr` no jogo (potência da SLR, dirigibilidade do M3 GTR, curva aberta em alta).
- `scripts/copy_slr_stats_to_mustang.py`: copia a performance inteira da SLR para o mustanggt. Essa cópia não é nenhuma das três opções guardadas.
- `release/LEIA-ME.md`: instalação, limites e créditos da versão final.
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

O arquivo `docs/historico/demanda-inicial.md` serviu como contexto técnico. A decisão de instalar ferramentas e deixar o teste no jogo para o final foi dada diretamente pelo usuário.
