# Fusion Titanium 2018 para MW2005

**Versão final: V1prime-z10** (aprovada no jogo em 25/09/2026).

**Fusion 2012 FWD (novo, 25/09/2026):** substitui o Chevrolet Cobalt SS (slot `COBALTSS`, carro inicial). Mesma
carroceria da V1prime-z10 com faróis, lanternas (sem a faixa cromada do porta-malas) e faróis de milha do 2012,
tração dianteira e motor do Cobalt +20 %. Release: [`release/Fusion2012_FWD_MW2005.zip`](release/); detalhes em
[versions/fusion2012-fwd/LEIA-ME.md](versions/fusion2012-fwd/LEIA-ME.md). Logo e tampa do porta-malas aprovados
no jogo em 26/09; as outras correções de lataria estão em [TODO.md](TODO.md). O zip ainda não inclui a tampa corrigida.

- Release única: [`release/Fusion2018_AWD_MW2005.zip`](release/) — instalação e créditos em [release/LEIA-ME.md](release/LEIA-ME.md).
- Lista do que foi feito e aprovado: [TODO.md](TODO.md).
- Aprendizados técnicos: [APRENDIZADOS_FUSION_MW2005.md](APRENDIZADOS_FUSION_MW2005.md) e os LEIA-ME de cada etapa em
  [versions/v1prime/variants/](versions/v1prime/variants/) e [versions/](versions/LEIA-ME.md).
- Galeria de imagens do projeto, etapa por etapa: [docs/imagens-projeto/](docs/imagens-projeto/README.md).
- Primeira release de teste (v0.1, histórica): [docs/historico/release-v0.1/](docs/historico/release-v0.1/LEIA-ME.md).

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

O arquivo `demanda.md` serviu como contexto técnico. A decisão de instalar ferramentas e deixar o teste no jogo para o final foi dada diretamente pelo usuário.
