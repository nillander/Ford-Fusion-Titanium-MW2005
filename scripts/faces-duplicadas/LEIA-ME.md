# Faces duplicadas (item 53, v2.8)

Remove de todas as peças e LODs os triângulos repetidos na mesma posição (mesmos três vértices, tolerância de 0,5 mm),
tanto as cópias viradas ao contrário (o verso da chapa que veio do GTA) quanto as repetidas para o mesmo lado.

1. `scan2.py GEOMETRY.BIN` conta, por sólido, os pares opostos e iguais (`mwgeo.py` lê o BIN).
2. `decide.py SLOT` (lê `SLOT.BIN`) desenha cada sólido com pares, junto com as peças padrão do mesmo LOD, de 144
   direções de fora do carro (elevação 2° a 85°), com descarte de verso e z-buffer (`idr.c` compilado como
   `libidr.so`, `vis.py`). Grava quantos pixels cada triângulo mostra em `SLOT_vis.pkl`.
3. `kills.py SLOT` escolhe: em cada par oposto fica a face mais vista; se nenhuma aparece, a que aponta para fora do
   centro do carro; entre cópias iguais fica a última (a que o jogo desenhava por cima). Grava `SLOT_kills.json`.
4. `aplica53.py GEO_in GEO_out SLOT_kills.json` transforma os triângulos listados em degenerados, no lugar.

Resultado v2.8: 2018 −42.314 triângulos (117 sólidos), 2012 −48.459 (146 sólidos). Depois disso `scan2.py` não acha
nenhum par. Comparando o 2018 antes/depois com descarte de verso (como o jogo original desenha), 0,0006 % dos pixels
viraram fundo e 0,004 % mudaram de peça.
