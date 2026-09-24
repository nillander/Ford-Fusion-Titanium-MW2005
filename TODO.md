# TODO — Fusion Titanium 2018 (base: checkpoint V1prime-d)

Ponto de partida seguro: `versions/checkpoint-v1prime-d` (GEOMETRY `C8A2D660…`, TEXTURES `BF9A0842…`).
Toda tarefa deve partir dele. Depois de pronta, testar **abrindo o jogo com o save ZHABES (que tem o
adesivo da Dinamarca)** antes de ser dada como concluída.

Regras aprendidas, para não quebrar nada (ver `APRENDIZADOS_FUSION_MW2005.md`):
peças opacas usam textura DXT1 com nome padrão; nenhum grupo pode passar de 65.535 índices; instalar
com o jogo fechado, nas duas rotas, conferindo o SHA-256.

- [ ] **1. Portas: deformação dos adesivos.** As UVs da pintura dão um salto entre a porta dianteira e a
  traseira. A tentativa V1prime-e, que refez as UVs da carroceria inteira, fez o jogo fechar na abertura.
  Nova abordagem: mudança mínima, só na ilha UV da porta traseira, alinhando-a à da dianteira. Testar
  com o save antes de instalar como versão.
- [ ] **2. Rodas originais do GTA.** Construir aro e pneu a partir de `source/fusion-2017-dev`
  e montar `KIT00_FRONT_TIRE_A–E`. O aro 18 é a roda padrão do Fusion e o tamanho mínimo:
  o jogo deve aceitar rodas de 18 até 22 polegadas.
- [ ] **3. Antena.** Remover a antena tipo para-raios do teto (em `BASE_A`, perto de x ≈ −1,06 m)
  e colocar uma antena tubarão na mesma posição.
- [ ] **4. Emblemas da tampa traseira.** Refazer `FUSION` (lado esquerdo) e `TITANIUM` (lado direito),
  que se deformaram e perderam o formato.
- [ ] **5. Suavidade da carroceria na traseira.** Corrigir os relevos e irregularidades perto do vidro
  traseiro (coluna C e tampa), sem alterar a UV da pintura.
- [ ] **6. Brake light.** A luz de freio está na tampa traseira. Mover para cima, no início do vidro
  traseiro.
- [ ] **7. Kits de carroceria na loja.** Instalar um dos 2 kits disponíveis faz a carroceria inteira
  sumir. Construir modelos para esses kits: pode ser uma réplica da carroceria padrão, diferente na
  peça instalada mas igual na forma, para a loja aceitar o kit sem apagar o carro.
