# TODO — Fusion Titanium 2018 (base: checkpoint V1prime-l)

Ponto de partida seguro: `versions/checkpoint-v1prime-l` (GEOMETRY `695DC7F7…`, TEXTURES `BF9A0842…`).
Checkpoints anteriores: `checkpoint-v1prime-j` (`97803AD8…`), `checkpoint-v1prime-i` (`CD799ED4…`), `checkpoint-v1prime-g` (`EE2FFBAB…`), `checkpoint-v1prime-d` (`C8A2D660…`).
Toda tarefa deve partir dele. Depois de pronta, testar **abrindo o jogo com o save ZHABES (que tem o
adesivo da Dinamarca)** antes de ser dada como concluída.

Regras aprendidas, para não quebrar nada (ver `APRENDIZADOS_FUSION_MW2005.md`):
peças opacas usam textura DXT1 com nome padrão; nenhum grupo pode passar de 65.535 índices; instalar
com o jogo fechado, nas duas rotas, conferindo o SHA-256.

A ordem vai do menor deslocamento de uma peça já existente até a geometria que reexporta a
carroceria inteira e pode fechar o jogo.

- [x] **1. Altura do aerofólio.** Concluído em 25/09 (V1prime-i, GEOMETRY `CD799ED4…`), aprovado no jogo.
  O "aerofólio" é a asa da loja: o ponto de fixação `SPOILER` (herdado do Mustang) estava 8 cm acima
  da tampa e foi para x −2,150 / z 0,868 m. Ver `versions/v1prime/variants/v1prime-i-spoiler-mount/LEIA-ME.md`.
- [x] **2. Brake light.** Concluído em 25/09 (V1prime-j, GEOMETRY `97803AD8…`), aprovado no jogo.
  O ponto `CENTRE_BRAKELIGHT` (herdado do Mustang, na tampa) foi para x −1,170 / z 1,172 m, no topo do
  vidro traseiro. Ver `versions/v1prime/variants/v1prime-j-centre-brakelight/LEIA-ME.md`.
- [x] **3. Antena.** Concluído em 25/09 (V1prime-l, GEOMETRY `695DC7F7…`), aprovado no jogo. Antena
  para-raios removida; antena tubarão arredondada de 196 × 96 × 61 mm no grupo da pintura (cor do carro).
  Ver `versions/v1prime/variants/v1prime-l-sharkfin-body/LEIA-ME.md`.
- [ ] **4. Emblemas da tampa traseira.** Refazer `FUSION` (lado esquerdo) e `TITANIUM` (lado direito),
  que se deformaram e perderam o formato.
- [ ] **5. Entradas de ar no teto.** Ao escolher uma entrada de ar na loja, ela não aparece no teto.
  Corrigir para que as opções possam ser instaladas e fiquem visíveis.
- [ ] **6. Capô da loja.** Permitir trocar o capô pelos itens da loja, de forma que a peça escolhida
  substitua o capô padrão e apareça no carro.
- [ ] **7. Suavidade da carroceria na traseira.** Corrigir os relevos e irregularidades perto do vidro
  traseiro (coluna C e tampa), sem alterar a UV da pintura.
- [x] **8. Portas: deformação dos adesivos.** Concluído em 25/09 (V1prime-g, GEOMETRY `EE2FFBAB…`),
  aprovado no jogo com o adesivo da Dinamarca (`versions/v1prime/in-game/v1prime-g-vinyl-denmark-ok.png`).
  O mapa da pintura nas laterais foi endireitado com uma correção suave; o resto do carro ficou idêntico.
  Ver `versions/v1prime/variants/v1prime-g-door-uv/LEIA-ME.md`.
- [ ] **9. Refino dos encaixes da carroceria.** Perto das junções aparecem manchas negras, um
  escurecimento da pintura. O para-lama dianteiro fica escuro na conexão com o para-choque, o farol
  e a porta. A hipótese é que triângulos e retângulos da geometria não se encontram e deixam fresta
  ou normal errada; conferir na carroceria inteira, começando por `Screenshot_146.png`, e polir só
  o encaixe, sem refazer a UV da pintura.
- [ ] **10. Rodas originais do GTA.** Construir aro e pneu a partir de `source/fusion-2017-dev`
  e montar `KIT00_FRONT_TIRE_A–E`. O aro 18 é a roda padrão do Fusion e o tamanho mínimo:
  o jogo deve aceitar rodas de 18 até 22 polegadas.
- [ ] **11. Kits de carroceria na loja.** Instalar um dos 2 kits disponíveis faz a carroceria inteira
  sumir. Construir modelos para esses kits: pode ser uma réplica da carroceria padrão, diferente na
  peça instalada mas igual na forma, para a loja aceitar o kit sem apagar o carro.
- [ ] **12. Refazer os vidros.** Anteriormente, adicionamos multiplas camadas de vidro para tentar melhorar
  a visualização dos vidros do veículo, isso fez os insufilmes (películas do vidro) aparecerem mas por outro lado
  perdemos a visibilidade interna do veículo, acredito que esse problema poderia ter sido solucionado de outra forma
  deveria ser um problema de textura incorreta assim como tivemos nas lanternas e faróis.
- [ ] **13. Dirigibilidade.** Está muito sensível para fazer curvas, um leve toque no direcional faz o veículo girar. Procure um veículo compatível grande que tenha boa dirigibilidade
- [ ] **14. Suavidade no veículo.** Vide item 8, existem ondulações no veículo, principalmente entre peças de encaixe, como entre o paralamas e portas, ou entre portas e parachoques, já foi ajustado anteriormente o encaixe de uma porta com a outra, mas ainda é necessário um refino completo no veículo para trazer uma suavidade por completo, de forma que comporte-se como os outros veículos, parecendo ser quase uma peça única