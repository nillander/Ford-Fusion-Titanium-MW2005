# Lente, vidros e capô (itens 50–52, v2.6)

Scripts em Python (numpy) que leem e editam o `GEOMETRY.BIN` e o `TEXTURES.BIN` do MW **no lugar**, sem recompilar:
o número de vértices e de índices de cada sólido não muda. Triângulo removido vira degenerado (três índices iguais).

| Script | Uso |
| --- | --- |
| `mwgeo.py` | Leitor do `GEOMETRY.BIN` (sólidos, grupos, vértices de 36 bytes, índices, offsets dos buffers) |
| `tpk.py` | Leitor do `TEXTURES.BIN` (blocos `RAWW`) e decodificador DXT1/DXT3 |
| `hashes.py` | Hash de nome do jogo (`h = h*33 + c`, começa em `0xFFFFFFFF`) |
| `lente50.py` | Item 50. `python lente50.py GEO_in TEX_in GEO_out TEX_out`. Pinta uma célula clara (RGB ~226, alfa 27 %) em x 512–575 / y 128–191 do atlas `MUSTANGGT_KIT00_HEADLIGHT_OFF` e aponta a UV das lentes `KIT00_RIGHT_HEADLIGHT_GLASS_A–D` para ela; o pisca âmbar (u > 0,332) fica como está |
| `win.py`, `comp.py` | Classificação das faces dos vidros (fora/dentro/borda) e componentes conexas |
| `vidros51.py` | Item 51. A partir de `vidros2018.npz` (P, UV, F e textura por triângulo de `FRONT_WINDOW_A` e `REAR_WINDOW_A`), mantém só a chapa de fora, descarta peças cobertas por outras, separa as seis janelas e gera UV 0–1 plana por janela, sem espelho (topo da imagem na borda de cima, imagem direita vista de fora). Grava `layout51.npz`. Precisa de scipy |
| `aplica51.py` | Item 51. `python aplica51.py GEO_in GEO_out SLOT`. Grava `layout51.npz` em `FRONT_WINDOW_A–D` e `REAR_WINDOW_A–D` (os LODs e os dois carros têm a mesma malha de vidro) |
| `capo52.py` | Item 52. `python capo52.py GEO_in GEO_out SLOT`. No `KIT00_HOOD_A–D` apaga toda face virada para dentro (cópias do verso do capô); nos `STYLExx_HOOD` só a cópia virada para baixo em superfície quase horizontal |
| `dupscan.py` | Lista, por sólido, pares de triângulos coincidentes com faces opostas (o que aparece preto com mods que desenham os dois lados) |

Ordem da v2.6: v2.5 → `lente50.py` (só 2018) → `aplica51.py` → `capo52.py`.
