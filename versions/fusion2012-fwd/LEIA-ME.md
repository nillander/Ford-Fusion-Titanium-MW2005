# Fusion 2012 FWD — substitui o Chevrolet Cobalt SS (slot `COBALTSS`)

Base: V1prime-z10 (Fusion Titanium 2018, versão final aprovada). O 2012 e o 2018 são o mesmo carro; mudam
só **faróis, lanternas traseiras e faróis de milha**. Todo o resto (carroceria suavizada, vidros, rodas de 20 raios,
capôs e kits da loja, adesivos, antena, placa NEWZERA, emblemas, logo FUSION) é o da z10.

| Arquivo | SHA-256 |
| --- | --- |
| GEOMETRY.BIN (no zip, 26/09) | `2E4408AA0E079530D63E48C0A606D74B2DC76679DB25181C5C104D81291C8A5E` (TEXTURES `39505AD5…`) |
| GEOMETRY.BIN (instalada, item 27 aprovado) | `E3914698050B207AFA10DC0B4B03B47DDE4AD3135B0A1052DE2D319968A28E3E` |
| TEXTURES.BIN | `0DCF3F4984E2F07B68D5FC2C6F58111E01F86E6BC9B7029215B5C9A56C45920C` |
| ATTRIBUTES.MWPS | `744596F4A3E34A49BD83982C7D9C9294328004BAD40156B5F126A3C643C3A8D5` |

## O que mudou em relação à z10
- **Fonte das peças 2012:** `source/fusion-2016-dev` (Mondeo/Fusion 2016 do GTA V, `oracle_hi.yft`), lido com um
  parser RSC7/YFT próprio (`scripts/yftp.py`), sem Windows. Alinhamento global por ICP com a carroceria z10
  (erro mediano 1,2 cm) e ajuste fino por peça.
- **Faróis:** projetor, LEDs, refletor cromado e seta âmbar do 2012 nas peças `KIT00_LEFT/RIGHT_HEADLIGHT`;
  lente em `..._HEADLIGHT_GLASS`. Os faróis e o farol de milha do 2018 saíram (inclusive o interior deles em BASE e
  RIGHT_SIDE_MIRROR).
- **Lanternas:** lanterna 2012 (lente vermelha, ré e seta) em `KIT00_LEFT/RIGHT_BRAKELIGHT(_GLASS)`. **A faixa cromada
  da tampa do porta-malas, de uma lanterna à outra, foi removida**, com as aletas e a moldura das lanternas 2018.
  Aprovado no jogo em 26/09 (item 7): a aba inclinada onde o friso encaixava sombreava como uma faixa; ficou reta
  do vinco até a moldura da placa, com as frestas fechadas por trás (`scripts/lidfix.py`). O vinco permanece.
  **Para-choque traseiro (item 6, aprovado em 26/09):** o triângulo escuro no canto inferior do meio era a normal
  da face de baixo num vértice do vinco usado pela face traseira (já vinha da z10); `scripts/fix6.py` + `apply6.py`.
  Brake light central, refletores do para-choque e luzes do painel do 2018 foram mantidos.
- **Grade inferior (item 1, aprovado em 26/09):** trapézio como no 2013, terminando antes dos faróis de milha; o
  para-choque em volta do farol de milha e até o canto foi refeito com uma superfície lisa ajustada à lataria
  (`scripts/grille1.py`), o que também fechou o nicho baixo do 2018. Fotos de referência em `reference/fotos-2013/`.
- **Lanternas (item 27, aprovado em 26/09):** anel em lente vermelha e miolo em lente branca, iguais na tampa e na
  lateral; sem as aletas e a caixa da luz de ré do Mondeo; fundo vermelho/branco 6 mm atrás de cada lente
  (`scripts/tail27d.py`, sobre `tail27b.py`).
- **Faróis de milha (item 30):** sem a "perninha" (triângulo solto do Mondeo), sem o calo sob o aro, 0,8–2,0 cm mais
  à frente (`scripts/fog30.py`).
- **Logotipo da tampa (item 31, também no 2018):** escrita e aro prata e fundo preto, como na frente (`scripts/logo31.py`).
- **Faróis de milha:** nicho trapezoidal preto + farol redondo com aro cromado na posição do 2012; o nicho baixo do
  2018 ficou fechado (preto, sem a peça de LED).
- **Encaixe na lataria:** a pele do 2018 é recortada exatamente no contorno das peças novas (triângulos subdivididos e
  cortados ao longo da borda, não removidos inteiros) e uma faixa de 2 cm da pele do 2012, grudada na superfície do
  2018 (+2 mm), cobre as emendas. Feito nas carrocerias KIT00/01/02, LODs A–E.
- **Texturas (lição 1 dos aprendizados):** peças internas das luzes usam `COBALTSS_KIT00_HEADLIGHT_OFF` em **DXT1**
  (opacas, gravam profundidade); só as lentes usam `COBALTSS_KIT00_BRAKELIGHT_OFF` em DXT3. Atlas: `preview/atlas-luzes.png`.
- **Pontos de luz:** HEADLIGHT no projetor 2012 (x 1,99 / y ±0,692 / z 0,567); BRAKELIGHT nas lanternas novas.
- **Slot:** todos os sólidos renomeados `MUSTANGGT_*` → `COBALTSS_*` e as texturas `COBALTSS_*` (hash pelo nome).
- **Limites:** maior peça 64.543 vértices (limite 65.535); nenhum grupo passa de 65.535 índices; leitura independente OK
  (175 peças, 1.130.161 triângulos).

## Performance (`ATTRIBUTES.MWPS`, nós `cobaltss` e `cobaltss_top`)
- Dirigibilidade do 2018 aprovado: chassi, pneus (aro 18"), freios, massa 1.600 kg, inércia, HandlingRating e
  posição/altura/cambagem das rodas (`ecar`).
- Motor e câmbio do Cobalt SS com **torque +20 %** (85–180 → 102–216; estágio top 182–595 → 218–714).
- **Tração dianteira:** `TORQUE_SPLIT` 1,0 nos dois estágios.
- `FE.MWPS`: fabricante Ford; preço e nível da Blacklist continuam os do Cobalt (carro inicial).

## Reconstruir
`scripts/run12.sh` (nuvem Linux com PowerShell 7 + os scripts C# do mwgc): gera as peças (`graft.py`, `build12.py`),
grava com `AddParts2.cs`, ajusta os pontos de luz (`SetMount.cs`), renomeia o slot (`Retarget2.cs`), e o TPK é
montado com o mwtc sem System.Drawing. Performance: `scripts/perf12.py`.

## Não testado no jogo
Tudo acima foi validado fora do jogo (leitura independente e renders). Pontos a conferir no jogo: se as peças
`KIT00_LEFT_*` (novas neste carro) aparecem; brilho das lanternas/faróis acesos; logo FUSION na tela de carros.

## 1º teste no jogo (26/09): falhou — corrigido, aguardando novo teste
"Temp 350" no lugar do logo e o jogo fechou ao selecionar o carro. Correções: TEXTURES.BIN refeita (o mwtc
estourava o campo de nome com `COBALTSS_KIT00_HEADLIGHT_OFF`/`_BRAKELIGHT_OFF`) e SECONDARYLOGO.BIN com hash próprio
`A3782D31` (`SECONDARY_LOGO_COBALTSS`). Detalhes e próximos passos em `CONTINUACAO-FUSION2012.md` (raiz do projeto).

## Testes seguintes (26/09)
- 2º–4º testes: o carro aparece e o jogo abre; o logo mostrava "temp350".
- **Logo corrigido e aprovado no jogo:** o Mod Loader procura `SECONDARY_LOGO_<internal>_1`; para o Cobalt, hash
  `623849E1`. `SECONDARYLOGO.BIN` = o do Fusion 2018 com esse hash (offsets 0xD4 e 0x108). Detalhes na seção 4.6 de
  `CONTINUACAO-FUSION2012.md`, que também lista as 7 correções de geometria pendentes (seção 4.7).
- `diag-z10-no-slot-cobalt/`: os .BIN ficam só locais (diagnóstico, não versionados).
