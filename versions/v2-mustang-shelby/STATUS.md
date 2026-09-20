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

O pacote V2 foi instalado para teste em `CARS/MUSTANGGT` em 20/09/2026 após
leitura independente da geometria e das texturas. O estado anterior do jogo
foi copiado em `versions/v1-fusion-ajm3899/installed-game-backup/MUSTANGGT`.

## Protótipo de encaixe

O export atual do Fusion foi recompilado com o namespace `MUSTANGGT` e
mesclado à cópia retail do Shelby. A validação independente leu 85 peças e
247.765 triângulos em todos os LODs. Os slots do Shelby de pneus, freios e
aerofólio foram retidos; luzes, vidros, carroceria e interior foram trocados
pelo Fusion. O LOD A ficou em 142.994 triângulos, acima do alvo prático, e
por isso este protótipo não foi instalado nem empacotado.

## Pacote de teste instalado

O segundo exportador reduziu o LOD A para aproximadamente 63 mil triângulos e
mantém no Shelby os sólidos de pneus, freios, espelhos, faróis, lanternas e
aerofólio. O BIN instalado tem SHA-256
`96E3442D4BD8269B133DF68C360928570B69FA670B8EDEB989E6BEE81F533AA7`.
O TPK contém a placa `NEWZERA` e tem SHA-256
`F4C326F0075A9E2B59B1D8398469A93F9787574E70685FABA097BC3BC1825D6E`.

## Lanterna traseira — correção instalada para teste

O teste visual mostrou que as lanternas traseiras Shelby eram cascas finas e
abertas: era possível enxergar o interior através delas. A troca anterior de
shader e textura opaca foi corretamente exportada e instalada, mas não alterou
o resultado no motor; portanto transparência de textura não era a causa única.

`scripts/OpaqueRearLights.cs` agora preserva todos os sólidos existentes e:

- mantém o material de lanterna com alpha de vértice 255;
- acrescenta um refletor fechado, de seis faces e 12 triângulos, atrás de cada
  lanterna traseira `*_BRAKELIGHT_A`;
- não altera grade, carroceria, rodas, nem os demais LODs.

O resultado foi lido independentemente pelo mwgc: 78 peças e 119.289
triângulos. Cada lanterna traseira de LOD A passou a ter três grupos, 593
vértices e 558 triângulos. O artefato instalado para o próximo teste é:

- `release/MUSTANGGT/GEOMETRY.BIN`
- jogo: `D:\Program Files (x86)\Electronic Arts\Need For Speed Most Wanted Black Edition\CARS\MUSTANGGT\GEOMETRY.BIN`
- SHA-256: `2F9D6A21BB3CC7425B08C758988217D3807D026A92A8DF8585704A6B67941925`

O BIN imediatamente anterior foi preservado em
`work/game-before-rear-reflector/GEOMETRY.BIN`. A textura instalada permanece
`8DF9EBDE632E0EAAE8A6907E7146291BD03CFC796C9B699C91B8581D12589954`.
