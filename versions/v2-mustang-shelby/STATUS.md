# Fusion Titanium 2018 — V2 Mustang Shelby

Estado: doador normalizado e validado; exportação do Fusion pendente.

O V2 preserva o slot `MUSTANGGT` e usará como base estrutural o pacote completo
`donor/ford_mustang_shelby/MODLOADER/ADDONS/CARS_REPLACE/MUSTANGGT`.
Nenhum arquivo do jogo foi alterado para iniciar esta versão.

## Marco concluído — 20/09/2026

- V1 preservado pela tag Git `fusion-v1-ajm3899` e por cópia local dos BINs.
- O GEOMETRY.BIN original do Shelby foi mantido intacto.
- `scripts/prepare_shelby_v2_donor.py` descomprime os 78 sólidos JDLZ do
  Shelby para uma cópia retail isolada em `work/shelby-retail.bin`.
- A cópia normalizada tem SHA-256
  `FB0CE1D5DC51F1A656C6B30B5F7EE36864E57667EB04C77C21F8172256DBF22F` e
  passou na leitura independente do NFS-ModTools: 78 peças e 87.829 triângulos.
- O catálogo confirmado contém BASE, pneus, freios, interior, vidros, faróis,
  lanternas, espelhos e aerofólio. Isso elimina a limitação estrutural do
  doador AJM3899 que contribuía para os componentes ausentes no V1.

Próximo passo: portar a geometria do Fusion para os slots desse catálogo,
preservando pneus, freios e os sólidos de iluminação/vidros do Shelby; depois
gerar uma pasta de lançamento V2 antes de tocar nos arquivos do jogo.

## Protótipo de encaixe

O export atual do Fusion foi recompilado com o namespace `MUSTANGGT` e
mesclado à cópia retail do Shelby. A validação independente leu 85 peças e
247.765 triângulos em todos os LODs. Os slots do Shelby de pneus, freios e
aerofólio foram retidos; luzes, vidros, carroceria e interior foram trocados
pelo Fusion. O LOD A ficou em 142.994 triângulos, acima do alvo prático, e
por isso este protótipo não foi instalado nem empacotado.
