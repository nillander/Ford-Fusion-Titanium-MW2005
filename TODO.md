# TODO — Fusion Titanium 2018 (base: checkpoint V1prime-d)

Ponto de partida seguro: `versions/checkpoint-v1prime-d` (GEOMETRY `C8A2D660…`, TEXTURES `BF9A0842…`).
Toda tarefa deve partir dele. Depois de pronta, testar **abrindo o jogo com o save ZHABES (que tem o
adesivo da Dinamarca)** antes de ser dada como concluída.

Regras aprendidas, para não quebrar nada (ver `APRENDIZADOS_FUSION_MW2005.md`):
peças opacas usam textura DXT1 com nome padrão; nenhum grupo pode passar de 65.535 índices; instalar
com o jogo fechado, nas duas rotas, conferindo o SHA-256.

A ordem vai do menor deslocamento de uma peça já existente até a geometria que reexporta a
carroceria inteira e pode fechar o jogo.

- [ ] **1. Altura do aerofólio.** O aerofólio está um pouco alto demais. Abaixar só um pouco, sem
  mudar o formato.
- [ ] **2. Brake light.** A luz de freio está na tampa traseira. Mover para cima, no início (topo) do vidro
  traseiro.
- [ ] **3. Antena.** Remover a antena tipo para-raios do teto (em `BASE_A`, perto de x ≈ −1,06 m)
  e colocar uma antena tubarão na mesma posição.
- [ ] **4. Emblemas da tampa traseira.** Refazer `FUSION` (lado esquerdo) e `TITANIUM` (lado direito),
  que se deformaram e perderam o formato.
- [ ] **5. Entradas de ar no teto.** Ao escolher uma entrada de ar na loja, ela não aparece no teto.
  Corrigir para que as opções possam ser instaladas e fiquem visíveis.
- [ ] **6. Capô da loja.** Permitir trocar o capô pelos itens da loja, de forma que a peça escolhida
  substitua o capô padrão e apareça no carro.
- [ ] **7. Suavidade da carroceria na traseira.** Corrigir os relevos e irregularidades perto do vidro
  traseiro (coluna C e tampa), sem alterar a UV da pintura.
- [ ] **8. Portas: deformação dos adesivos.** As UVs da pintura dão um salto entre a porta dianteira e a
  traseira. A tentativa V1prime-e, que refez as UVs da carroceria inteira, fez o jogo fechar na abertura.
  Nova abordagem: mudança mínima, só na ilha UV da porta traseira, alinhando-a à da dianteira. Testar
  com o save antes de instalar como versão.
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
