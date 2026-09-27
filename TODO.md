# TODO — Fusion Titanium 2018 (versão final: V1prime-z10)

Versão final: `release/Fusion2018_AWD_MW2005.zip` (V1prime-z10, GEOMETRY `BB90B702…`, TEXTURES `EEBB0B83…`, ATTRIBUTES.MWPS `3BE53CF9…`, SECONDARYLOGO.BIN `E4721014…`); ver `versions/checkpoint-v1prime-z10/LEIA-ME.md`.
Checkpoints anteriores (binários só no histórico do git, pelas tags): `checkpoint-v1prime-z8` (`FC6C27FA…`), `checkpoint-v1prime-z3` (`8D9BE4F9…`), `checkpoint-v1prime-z2` (`B12D0E90…`), `checkpoint-v1prime-y` (`A8DA8897…`), `checkpoint-v1prime-u` (`CD41C016…`), `checkpoint-v1prime-s` (`2F66D3D2…`), `checkpoint-v1prime-q` (`DD6212A8…`), `checkpoint-v1prime-p` (`B1375C52…`), `checkpoint-v1prime-l` (`695DC7F7…`), `checkpoint-v1prime-j` (`97803AD8…`), `checkpoint-v1prime-i` (`CD799ED4…`), `checkpoint-v1prime-g` (`EE2FFBAB…`), `checkpoint-v1prime-d` (`C8A2D660…`).
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
- [x] **4. Emblemas da tampa traseira.** Concluído em 25/09 (V1prime-p, GEOMETRY `B1375C52…`), aprovado
  no jogo. Letras do GTA removidas; FUSION (168 mm) e TITANIUM (181 mm) traçados das imagens oficiais,
  cromados, 2,5 mm em relevo. Ver `versions/v1prime/variants/v1prime-p-emblems-ford/LEIA-ME.md`.
- [x] **5. Entradas de ar no teto.** Concluído em 25/09 (V1prime-q, GEOMETRY `DD6212A8…`), aprovado no
  jogo. Criado o ponto de fixação `ROOF_SCOOP` (`90C81258`), que o doador não tinha, em x 0,300 / z 1,207 m,
  inclinado 6,5°. Ver `versions/v1prime/variants/v1prime-q-roof-scoop/LEIA-ME.md`.
- [x] **6. Capô da loja.** Concluído em 25/09 (V1prime-s, GEOMETRY `2F66D3D2…`), aprovado no jogo. Capô
  separado da carroceria em `KIT00_HOOD_A–D`; criados os 17 capôs da loja `STYLExx_HOOD_A–D` (capô do
  Fusion + detalhes dos capôs do GTO). Ver `versions/v1prime/variants/v1prime-s-hoods/LEIA-ME.md`.
- [x] **7. Suavidade da carroceria na traseira.** Concluído em 25/09 (V1prime-u, GEOMETRY `CD41C016…`),
  aprovado no jogo. Os riscos eram frestas na pele da coluna C mostrando o interior escuro: camada de
  fundo pintada 4 mm sob a pele + normais suavizadas. Ver `versions/v1prime/variants/v1prime-u-rear-backing/LEIA-ME.md`.
- [x] **8. Portas: deformação dos adesivos.** Concluído em 25/09 (V1prime-g, GEOMETRY `EE2FFBAB…`),
  aprovado no jogo com o adesivo da Dinamarca (`versions/v1prime/in-game/v1prime-g-vinyl-denmark-ok.png`).
  O mapa da pintura nas laterais foi endireitado com uma correção suave; o resto do carro ficou idêntico.
  Ver `versions/v1prime/variants/v1prime-g-door-uv/LEIA-ME.md`.
- [x] **9. Refino dos encaixes da carroceria.** *(Aprovado no jogo: V1prime-z8 — camada de fundo pintada, frente do motorista espelhada do passageiro, vão do capô fechado; ver `versions/v1prime/variants/v1prime-z8-fender-hoodgap/LEIA-ME.md`.)* Perto das junções aparecem manchas negras, um
  escurecimento da pintura. O para-lama dianteiro fica escuro na conexão com o para-choque, o farol
  e a porta. A hipótese é que triângulos e retângulos da geometria não se encontram e deixam fresta
  ou normal errada; conferir na carroceria inteira, começando por `Screenshot_146.png`, e polir só
  o encaixe, sem refazer a UV da pintura. Nos veículos do jogo é como se a lataria inteira fosse uma peça única, veja em `Screenshot_147.png`
- [x] **10. Rodas originais do GTA.** Concluído em 25/09 (V1prime-y), aprovado no jogo. Roda de 20 raios
  lida do `fusion_hi.yft`, toda em metal usinado (tom médio, textura DXT1); aro 18" via `RIM_SIZE` 18 e
  `ASPECT_RATIO` 40 (mesmo diâmetro de pneu). O MW só tem rodas de loja de 17 a 20" e não oferece escolha
  de tamanho. Ver `versions/v1prime/variants/v1prime-v-gta-wheel/`, `-w-rim18/`, `-x-wheel-uniform/`, `-y-wheel-darker/`.
- [x] **11. Kits de carroceria na loja.** *(Aprovado no jogo: V1prime-z8, kits "Street" e "Race" encaixados nos para-choques.)* Instalar um dos 2 kits disponíveis na loja faz a carroceria inteira
  sumir. Construir modelos para esses kits: pode ser uma réplica da carroceria padrão, diferente na
  peça instalada mas igual na forma, para a loja aceitar o kit sem apagar o carro. Alguns carros de adversários gerados aleatóriamente acabam aplicando kits de carroceria e são exibidos de forma invisível quebrando a imersão do jogo
- [x] **12. Refazer os vidros.** *(Aprovado no jogo: V1prime-z, uma camada WINDSHIELD por janela; ver `versions/v1prime/variants/v1prime-z-glass-handling-logo/LEIA-ME.md`.)* Anteriormente, adicionamos multiplas camadas de vidro para tentar melhorar
  a visualização dos vidros do veículo, isso fez os insufilmes (películas do vidro) aparecerem mas por outro lado
  perdemos a visibilidade interna do veículo, acredito que esse problema poderia ter sido solucionado de outra forma
  deveria ser um problema de textura incorreta assim como tivemos nas lanternas e faróis.
- [x] **13. Dirigibilidade.** *(Aprovado no jogo: V1prime-z2, chassi, peso e aderência do Mustang GT; ver `versions/v1prime/variants/v1prime-z2-handling-logo/LEIA-ME.md`.)* Está muito sensível para fazer curvas, um leve toque no direcional faz o veículo girar. Procure um veículo compatível grande que tenha boa dirigibilidade
- [x] **14. Suavidade no veículo.** *(Aprovado no jogo: V1prime-z8, junto com o item 9.)* Vide item 8, existem ondulações no veículo, principalmente entre peças de encaixe, como entre o paralamas e portas, ou entre portas e parachoques, já foi ajustado anteriormente o encaixe de uma porta com a outra, mas ainda é necessário um refino completo no veículo para trazer uma suavidade por completo, de forma que comporte-se como os outros veículos, parecendo ser quase uma peça única
- [x] **15. Identidade visual.** *(Aprovado no jogo: V1prime-z3, logo menor com espaço nas laterais; ver `versions/v1prime/variants/v1prime-z3-logo-nitro/LEIA-ME.md`.)* Trocar o logotipo "FUSION" exibido nas telas do jogo (ex.: "Meus carros",
  canto superior direito) pelo logo de `assets/nao-usar/ford-fusion-seeklogo.png`.
- [x] **16. Chama do nitro.** *(Aprovado no jogo: V1prime-z3, pontos LEFT/RIGHT_EXHAUST no centro das saídas; ver `versions/v1prime/variants/v1prime-z3-logo-nitro/LEIA-ME.md`.)* O efeito de nitro/NOS exibe fogo saindo do escapamento, mas não está
  alinhado com a saída do escapamento do Fusion.
- [ ] **17. Câmera interna (Fusion 2018 e 2012).** *(Não resolvido: a câmera "capô" parece ficar dentro da entrada de ar do teto instalada; falta descobrir onde o jogo define essa posição. Testar sem a entrada de ar do teto.)* Na visualização pela câmera de dentro do veículo não aparece textura,
  só alguns itens pretos.
- [x] **18. Adesivos (vinis) que não aparecem.** *(Aprovado no jogo: V1prime-z8, peças DECAL_* trazidas do GTO; ver `versions/v1prime/variants/v1prime-z6-final-refine/LEIA-ME.md`.)* Os adesivos de porta, do para-brisa dianteiro, do para-brisa
  traseiro e os números de porta não são exibidos.
- [x] **19. Novos kits de carroceria.** *(Aprovado no jogo: V1prime-z8, kits "Street" e "Race".)* Gerar kits baseados em outros kits do jogo para ter mais uma opção
  de customização (hoje os kits 01 e 02 são cópias da carroceria padrão).
- [x] **20. Galeria de imagens do projeto (último item).** *(Feita em `docs/imagens-projeto/`, 18 etapas, 289 imagens.)* Salvar todas as imagens usadas no projeto e vistas
  pelo Claude num diretório organizado, com README explicando cada etapa (antes/depois da suavidade, renders 3D
  para mapear peças, antena tubarão etc.). *(Feito até a V1prime-z7 em `docs/imagens-projeto/`, 17 etapas, 265 imagens; completar se houver novos ajustes.)*

Pacote para outros jogadores: `release/Fusion2018_AWD_MW2005.zip` (versão final, única release).
- [x] **21. Parte de baixo do para-choque dianteiro.** *(Aprovado no jogo: V1prime-z10 — superfície única, sem o degrau do meio; ver `versions/v1prime/variants/v1prime-z10-front-lip/LEIA-ME.md`.)* Última peça com marcas pretas depois da V1prime-z8.

## Fusion 2012 FWD (slot COBALTSS)

Um item por vez, do mais simples ao mais difícil. Avisar para testar no jogo antes de seguir.
O zip `release/Fusion2012_FWD_MW2005.zip` ainda tem a geometria anterior (`2D4AF358…`) e só será refeito
quando os itens abaixo estiverem aprovados. Instalado e nos ZIPs de `release/` (26/09, tudo aprovado): 2012 `pacote-26-09e/` — GEOMETRY `2E4408AA…`/TEXTURES `39505AD5…`; 2018 `pacote-26-09d/` — GEOMETRY `B4D1BDDE…`/TEXTURES `13E45A9D…` — 2012 GEOMETRY `260F59AF…`/TEXTURES `39505AD5…`; 2018 GEOMETRY `B4D1BDDE…`/TEXTURES `13E45A9D…` (itens 36b e 39). Antes: `pacote-26-09c/` — 2012 GEOMETRY `BD51BA28…`/TEXTURES `39505AD5…`; 2018 GEOMETRY `2A26C393…`/TEXTURES `13E45A9D…` (o 2018 é o mesmo do `pacote-26-09b/`). Anterior aprovado: `pacote-26-09/`.

- [x] **22. Marca e nome (item 8).** Aprovado no jogo em 26/09. O jogo mostrava "temp350" porque o Mod Loader
  procura `SECONDARY_LOGO_COBALTSS_1` (hash `623849E1`). Logo do 2018 com esse hash. Ver `CONTINUACAO-FUSION2012.md` seção 4.6.
- [x] **23. Tampa do porta-malas (item 7).** Aprovado no jogo em 26/09 (GEOMETRY `C159D615…`). A faixa clara/escura
  era a aba do friso cromado do 2018, inclinada e com frestas; ficou reta do vinco até a moldura da placa, sombreado
  uniforme, frestas fechadas por trás. O vinco de uma lanterna à outra permanece. Ver `versions/fusion2012-fwd/scripts/lidfix.py`
  e `versions/fusion2012-fwd/preview/tampa-item7.png`.
- [x] **24. Para-choque traseiro (item 6).** Pequena deformação no canto inferior, no meio. *(Aprovado no jogo em 26/09:
  GEOMETRY `A0F66D69…`. Normais do vinco inferior do centro trocadas pela da face traseira; ver
  `versions/fusion2012-fwd/scripts/fix6.py` e `preview/parachoque-traseiro-item6.png`.)*
- [x] **25. Grade preta frontal inferior (item 1).** Não conecta os dois faróis de milha. Conferir com as fotos de referência.
  *(Aprovado no jogo em 26/09, com o encaixe do para-choque refinado: GEOMETRY `6B5A6327…`. Grade trapezoidal terminando antes dos faróis de
  milha, lataria pintada no vão; ver `versions/fusion2012-fwd/scripts/grille1.py` e `preview/grade-inferior-item1.png`.)*
- [x] **26. Vazio abaixo dos faróis de milha (item 2).** Preencher esse espaço no para-choque. *(Resolvido junto com o item 1:
  a lataria refeita em volta do farol de milha fechou o nicho baixo do 2018.)*
- [x] **27. Cor interna das lanternas (item 5).** A parte na tampa do porta-malas precisa da mesma cor e das mesmas
  camadas da parte externa (para-choque/carroceria). *(Aprovado no jogo em 26/09, v4: GEOMETRY `E3914698…` (`scripts/tail27d.py`). v4 = v2 `8C3E936A…` +
  caixa da luz de ré removida + preto→vermelho + fundo atrás de cada lente, nas duas partes (vermelho atrás da vermelha,
  branco atrás da transparente, 6 mm para dentro): o interior não cobria toda a lente e o preto da carroceria aparecia
  pelas frestas; o miolo externo ficava vazado. Histórico:
  Pedido: anel externo em lente vermelha viva e miolo em lente branca uniforme, sem aletas, idênticos na tampa e na
  lateral. As faces do interior da tampa estavam viradas para dentro do carro (ficavam escuras no jogo): desviradas.
  Anel = vermelho sólido do atlas nas duas partes; miolo = branco sólido; aletas e barra cromada removidas. Ver
  `scripts/tail27b.py` (a v1, só UV, é `scripts/tail27.py`). v3 (`scripts/tail27c.py`): caixa da luz de ré do
  Mondeo no miolo da tampa trocada por um fundo branco com o formato da lente transparente; pontos pretos no anel →
  vermelho. Só a lente da tampa é copiada (|y| < 0,576): a primeira montagem pegou pedacinhos da ponta da lente
  externa que apareciam dentro do miolo externo.)*
- [x] **28. Tamanho das lanternas traseiras (item 3).** Estão menores que o nicho; aumentar até encaixarem.
  *(26/09: aprovado no jogo em 26/09 — pacote `work/c2012-stage/pacote-26-09/`: 4 % mais comprida, 3 % mais alta; `scripts/scale28.py`.)*
- [x] **29. Lataria em volta dos faróis (item 4).** *(Capturas de referência em
  `versions/fusion2012-fwd/reference/item4-lataria/`.)* Faróis estão certos; há deformação no encaixe com o capô, o paralama
  e o para-choque.
  *(26/09: aprovado no jogo em 26/09 — pacote `work/c2012-stage/pacote-26-09/`: faróis trazidos para fora até o nível da lataria (`hl29.py`), frestas das pontas fechadas (`hlfill.py`); sobra um triângulo escuro pequeno embaixo do meio do farol.)*
- [x] **30. Faróis de milha redondos e mais à frente.** O farol de milha do 2012 é totalmente circular: tirar a
  "perninha" (ponta da peça que avança sobre o para-choque). A peça está afundada no para-choque: trazer um pouco
  para a frente. *(Aprovado no jogo em 26/09: GEOMETRY `9ED9B105…`. A "perninha" era um triângulo
  solto do Mondeo 35 cm atrás; peça avançada +0,8 cm (ponta interna) a +2,0 cm (externa); base do aro cromado, que descia
  ~6 mm abaixo da moldura ("calo"), subida até a borda; ver `scripts/fog30.py`.)*
- [x] **31. Logotipo Ford da tampa do porta-malas em prata.** O oval da frente (para-choque) está certo nos dois
  Fusions (2018 e 2012); na tampa traseira a escrita "Ford" tem de ser prata, como na frente. *(Aprovado no jogo em 26/09,
  instalado nos dois: 2012 GEOMETRY `B8EF17BC…` (inclui o item 30), 2018 GEOMETRY `2F612825…`
  (z10 + só este ajuste; o zip do 2018 ainda tem `BB90B702…`). A escrita e o aro usavam o preto da borda da
  textura MISC; agora usam o prata da frente, e o fundo a área preta da frente. Ver `scripts/logo31.py`.)*
- [x] **32. Revisão da parte inferior do para-choque dianteiro.** A borda de baixo do para-choque (lábio sob a grade
  inferior e os faróis de milha, de um canto ao outro) ficou degradada: facetas, dentes e manchas escuras de
  sombreado ao longo de toda a largura. Captura: `versions/fusion2012-fwd/reference/item4-lataria/6-parachoque-inferior-degradado.png`.
  *(26/09: aprovado no jogo em 26/09 — pacote `work/c2012-stage/pacote-26-09/`: lábio refeito liso de |y| 0 a 0,70; `scripts/lip32.py`.)*
- [x] **33. Freios com a textura da multimídia (Fusion 2012 e 2018).** Com uma roda da loja (raios abertos) os discos e
  as pinças de freio aparecem com a textura da tela da multimídia. Causa: as peças `KIT00_FRONT_BRAKE_A–C` e
  `KIT00_REAR_BRAKE_A–C` usam a textura `<CARRO>_INTERIOR` (UV u 0,47–0,72 / v 0,27–0,52 e u 0,21–0,27 / v 0,57–0,73),
  que hoje é o atlas do interior do Fusion. Correção: usar a textura oficial de disco e pinça de outro carro do jogo.
  Captura: `versions/fusion2012-fwd/reference/item4-lataria/7-freio-textura-multimidia.png`.
  *(26/09: instalado para teste — pacote `work/c2012-stage/pacote-26-09b/`. Freios trocados pelos do Pontiac GTO do jogo, escala 1,15: disco com a textura global ROTOR1 (GLOBALB.BUN) e pinça com o recorte das pinças do GTO_MISC gravado numa área livre do <CARRO>_MISC; `scripts/brakes33.py`.)*
  *(Aprovado no jogo em 26/09, pacote `pacote-26-09d`.)*
- [x] **34. Fusion 2018: carro incompleto na seleção de carreira, nas cutscenes e com o Razor.** O Fusion 2018
  substitui o Mustang GT, que é o carro do Razor. Na tela "Menu da Carreira", nas cutscenes e quando o Razor pilota o
  carro numa corrida, a lataria e várias peças não aparecem: só se vê o interior, as rodas e a estrutura. No carro do
  jogador tudo aparece. Hipótese a conferir: nesses casos o jogo monta o carro com a configuração de fábrica do Razor
  (kit de carroceria, capô, aerofólio e outras peças da loja que o Mustang dele usa), e alguma dessas peças não existe
  no GEOMETRY.BIN do Fusion. **Pedido do usuário (26/09):** investigar se é um kit de carroceria exclusivo do Razor
  (preset do Mustang dele); se ficar provado que é, criar esse kit no Fusion 2018 do mesmo jeito do item 35
  (carroceria de fábrica + cinta de reboque). **Diagnóstico (26/09, confirmado):** os carros prontos do jogo
  (`GLOBAL/GLOBALB.BUN`, bloco 0x00030220, 82 registros de 0x290 bytes; modelo em +0x08, nome em +0x28, peças como
  bin-hash a partir de +0x60) usam kits que o Fusion não tem: `RAZORMUSTANG` e `OPM_MUSTANG_VERSION2` (cutscenes) =
  MUSTANGGT **KIT04** + capô STYLE04 (este existe); `BL8` = MUSTANGGT **KIT05**; no 2012, `CS_CAR_14` (cutscene) =
  COBALTSS **KIT04**. O Fusion só tem KIT00–02 → a lataria some. Correção: criar KIT04 e KIT05 (carroceria de fábrica +
  cinta) nos dois carros. Capturas: `versions/v1prime/in-game/2018-carreira-menu-partes-faltando.png` e
  `versions/v1prime/in-game/2018-razor-corrida-partes-faltando.png`.
  *(26/09: KIT04 e KIT05 criados (2012 e 2018), aprovados no jogo em 26/09 — pacote `work/c2012-stage/pacote-26-09/`.)*
- [x] **35. Kits de carroceria = carro de fábrica + cinta de reboque (Fusion 2012 e 2018).** Em vez dos kits atuais
  (saias laterais maiores e uma faixa nos para-choques), os kits "Street" e "Race" passam a ser a carroceria de fábrica
  com uma cinta de reboque no para-choque dianteiro (ideia: uma cinta diferente em cada kit; o Race pode ter também a
  traseira). O kit não pode ficar vazio: no MW o kit troca a carroceria inteira (KIT01/KIT02_BODY_A–E), e sem lataria o
  carro some (antigo item 11). A cinta precisa de textura própria (senão sai na cor da pintura) e de um grupo próprio na
  peça; soma poucas centenas de vértices (KIT02_BODY_A do 2012 está em 63.887 de 65.535; voltar à carroceria de
  fábrica libera espaço). Referências em `reference/cintas-reboque/`: cinta preta com 大吉大利 em vermelho e cinta
  vermelha com 出入平安 em branco, suporte triangular preto; posição como na foto da cinta laranja (não usar a marca
  "R Racing" dela).
  *(26/09: aprovado no jogo em 26/09 — pacote `work/c2012-stage/pacote-26-09/`: KIT01 cinta preta, KIT02 vermelha, nos dois carros; `scripts/kits35.py`, `strap_tex.py`.)*
- [x] **36. Antena tubarão: traseira reta (Fusion 2012 e 2018).** Vista de trás, a base da antena é arredondada/cônica;
  deve terminar num corte reto, a 90° com o teto. A antena é a do item 3 (grupo da pintura em `KIT00_BODY`, criada na
  V1prime-l). Captura: `versions/fusion2012-fwd/reference/item4-lataria/8-antena-tubarao-traseira.png`.
  *(26/09: instalado para teste — pacote `work/c2012-stage/pacote-26-09b/`. Ponta cônica achatada num plano vertical (x −1,095), "V" de baixo fechado até o teto, antena recuada 1,7 cm; `scripts/fin36.py`.)*
  *(26/09, teste no jogo: a traseira ficou reta, mas aparece uma divisão em "V" no fundo da antena; tem de ser toda lisa. Imagem `versions/fusion2012-fwd/reference/teste-26-09c/antena-divisao.png`.)*
  *(26/09, instalado para teste — `pacote-26-09d`: a borda de baixo da face achatada é uma linha quebrada e o triângulo reto do fin36 deixava frestas finas entre os dois (era a divisão). A parte de baixo da face é preenchida por uma faixa de quadriláteros coluna a coluna (2 mm), do teto até 1,5 mm acima da borda real, no mesmo plano, com a mesma normal/UV/cor. 2012 e 2018, BODY A e B dos kits. `scripts/fin39.py`; prévia `versions/fusion2012-fwd/preview/antena-item36b.png`.)*
  *(Aprovado no jogo em 26/09, pacote `pacote-26-09d`.)*
- [x] **37. Faróis do 2012 ainda para dentro da lataria.** Mesmo depois do item 29 os faróis continuam afundados em
  relação à lataria em volta. Pode ser preciso aumentar um pouco o tamanho deles, como foi feito nas lanternas (item 28,
  `scripts/scale28.py`), além de trazê-los para fora. Ordem combinada em 26/09: 33, 36, 37, 17.
  *(26/09: instalado para teste — pacote `work/c2012-stage/pacote-26-09b/`. Farol aumentado 3 % para o lado da grade e 6 % para baixo; a ponta de fora e a borda de cima ficaram iguais porque, maiores, atravessavam o paralama/capô; `scripts/hl37.py`.)*
  *(26/09, 2ª versão — pacote `work/c2012-stage/pacote-26-09c/`: pedido "maiores e mais para fora". Farol inteiro (lente e interior, LODs A–D) aumentado 10 % por igual no plano da lente e levado 1 cm para fora ao longo da normal da lente; as peças da carcaça que sobram fora do contorno da lente aumentada (e atravessavam paralama/capô) são removidas. `scripts/hl37.py` com `1.10 1.10 0.010 sym`; prévia `versions/fusion2012-fwd/preview/farois-item37b.png` (em cima antes, embaixo depois).)*
  *(26/09, teste no jogo: faróis deslocados — ponta de trás (paralama) para fora e ponta da frente (grade) para dentro. 3ª versão, instalada para teste (`pacote-26-09e`): farol girado 1,5° em torno do eixo vertical da lente, pivô 12 cm do centro para o lado da grade: ponta de trás entra 11 mm, ponta da frente sai 5 mm. `scripts/hl40.py`, medida com `hlmeas.py`; prévia `versions/fusion2012-fwd/preview/farois-item37c.png` (em cima antes, embaixo depois).)*
  *(Aprovado no jogo em 26/09, pacote `pacote-26-09e`.)*
- [x] **38. Tampa do porta-malas entre as lanternas deformada (2012).** Depois do conserto das lanternas o espaço
  entre uma lanterna e a outra ficou deformado. Diagnóstico: a lataria da tampa não foi alterada nos itens 27/28, mas as
  lanternas aumentadas (item 28) avançaram 1,5 cm para o centro, e as paredes do rebaixo da lataria passaram a
  atravessar a lente vermelha perto das pontas internas (manchas verdes/da cor do carro dentro da lanterna).
  *(26/09: instalado para teste — pacote `work/c2012-stage/pacote-26-09c/`. Triângulos da lataria que ficam na frente da
  lente, a menos de 2 cm dela, removidos (a lente cobre a área); faixa da tampa entre as lanternas suavizada em x
  (Taubin, vinco e bordas fixos) com normais recalculadas; KIT00/01/02/04/05 BODY A–E. `scripts/lid38.py`; prévia
  `versions/fusion2012-fwd/preview/tampa-item38.png` (em cima antes, embaixo depois).)*
  *(Aprovado no jogo em 26/09, pacote `pacote-26-09d`.)*
- [x] **39. Lanternas do 2012 ainda para dentro da carroceria (vista de trás/lado).** No teste de 26/09 (pacote
  `pacote-26-09c`) a ponta de fora da lanterna, na lateral/para-lama traseiro, continua afundada: a lataria forma uma aba
  em volta e a lanterna fica recuada. Imagens `versions/fusion2012-fwd/reference/teste-26-09c/lanterna-lateral-1.png` e
  `lanterna-lateral-2.png`.
  *(26/09, instalado para teste — `pacote-26-09d`: medido por fatias em x, a lente ficava 1,3–3 cm para dentro da borda da lataria (bordas de cima e de baixo do buraco) na parte lateral (x −2,15 a −1,80). Lanterna inteira (lente e interior, LODs A–D) deslocada para fora em y, fatia a fatia, até 1 mm da borda, suavizado em x e com rampa na quina de trás (x −2,20 a −2,14; a parte de trás não se move). Folga final 0–3 mm. `scripts/tail39.py` + `slice39.py`; prévia `versions/fusion2012-fwd/preview/lanternas-item39.png` (em cima antes, embaixo depois).)*
  *(26/09, teste no jogo: ainda para dentro — aba da lataria acima da ponta de fora. Medido por fatias: a borda de BAIXO da lente já estava no nível da lataria, mas a de CIMA ficava 3–4,5 cm para dentro (a lente "olhava" para cima). 2ª versão, instalada para teste (`pacote-26-09e`): cisalhamento em y pela altura (0 na borda de baixo, gap − 3 mm na de cima), x −2,21 → −1,70 com rampa na quina; folga final da borda de cima 1–4 mm. `scripts/tail40.py` + `tailtb.py`; prévia `versions/fusion2012-fwd/preview/lanternas-item39b.png` (render em perspectiva, `persp.py`; em cima antes, embaixo depois).)*
  *(Aprovado no jogo em 26/09, pacote `pacote-26-09e`.)*
- [x] **40. Para-brisa com "duas faixas faltando" (2012; conferir no 2018).** Visto de frente, o para-brisa mostra duas
  faixas verticais mais claras (imagem `versions/fusion2012-fwd/reference/teste-26-09e/para-brisa-faixas.png`).
  Análise de 26/09: a malha do para-brisa (`KIT00_FRONT_WINDOW_A`, grupo 7B220DDF) não tem buracos nem normais
  trocadas vista de fora; as faixas coincidem com os dois bancos da frente (couro claro, `KIT00_INTERIOR_A`, 6BCF3825)
  vistos através do vidro escuro — prévia `versions/fusion2012-fwd/preview/para-brisa-bancos.png`. Aguardando decisão:
  escurecer os bancos/interior ou o vidro.
  *(27/09: usuário deu tudo como certo e pediu a release; item encerrado sem alteração na geometria.)*
