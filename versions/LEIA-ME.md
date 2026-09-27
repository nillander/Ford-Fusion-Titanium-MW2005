# Histórico de versões

A versão final é a **v2.0**, com o Fusion Titanium 2012 FWD e o Fusion Titanium 2018 AWD (zips em `release/`).

Nesta pasta ficam o histórico e os aprendizados de cada etapa: LEIA-ME, STATUS, prévias, validações e scripts.

| Pasta | O que é |
| --- | --- |
| `fusion2012-fwd/` | Fusion Titanium 2012 FWD (slot COBALTSS): scripts, prévias e referências |
| `v1prime/` | Fusion 2018 (slot MUSTANGGT), linha final: variantes a–z10, capturas no jogo (`in-game/`) e checkpoints (`checkpoints/`) |
| `performance/` | As três performances testadas para o 2018 |
| `vprime/` | Base de onde saiu a v1prime (backup de 20/09) |
| `v1-fusion-ajm3899/`, `v2-mustang-shelby/`, `v3-fusion-ajm3899/` | Tentativas anteriores |

Os binários do jogo das versões antigas (GEOMETRY/TEXTURES/SECONDARYLOGO `.BIN`, `.dds`, `.blend`, ZIPs)
foram retirados em 25/09/2026. Os que estavam versionados continuam no histórico da `main`;
`git checkout <commit> -- <caminho>` recupera o arquivo. Commit de cada checkpoint do 2018:

| Checkpoint | Commit |
| --- | --- |
| `checkpoint-v1prime-d` | `cd73849a` |
| `checkpoint-v1prime-g` | `86d895ec` |
| `checkpoint-v1prime-i` | `d3255124` |
| `checkpoint-v1prime-j` | `b1036cc8` |
| `checkpoint-v1prime-l` | `4ea09b68` |
| `checkpoint-v1prime-p` | `cc4a954b` |
| `checkpoint-v1prime-q` | `52bd534a` |
| `checkpoint-v1prime-s` | `f6565a66` |
| `checkpoint-v1prime-u` | `d36de78d` |
| `checkpoint-v1prime-y` | `e035c832` |
| `checkpoint-v1prime-z2` | `0d758edf` |
| `checkpoint-v1prime-z3` | `798e57d4` |
| `checkpoint-v1prime-z8` | `65e31736` |
| `checkpoint-v1prime-z10` | `4d5a9736` |

Os caminhos antigos das pastas de checkpoint eram `versions/checkpoint-v1prime-*`; nesses commits os
arquivos ainda estão nesse caminho.
