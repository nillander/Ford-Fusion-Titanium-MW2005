# TODO — Fusion Titanium 2018 (versão final: V1prime-z10)

**Atualização de 27/09/2026:** o cabeçalho e os hashes a seguir são históricos. O estado da release v2.1 e
do teste atual do Fusion 2012 está em `docs/CONTINUACAO.md`, seção 3. A chapa do item 43 foi aprovada
visualmente; os faróis do item 44 ainda aguardam confirmação no jogo.

Versão final: `release/Fusion2018_AWD_MW2005.zip` (V1prime-z10, GEOMETRY `BB90B702…`, TEXTURES `EEBB0B83…`, ATTRIBUTES.MWPS `3BE53CF9…`, SECONDARYLOGO.BIN `E4721014…`); ver `versions/v1prime/checkpoints/checkpoint-v1prime-z10/LEIA-ME.md`.
Checkpoints anteriores (binários só no histórico do git; o commit de cada um está em `versions/LEIA-ME.md`): `checkpoint-v1prime-z8` (`FC6C27FA…`), `checkpoint-v1prime-z3` (`8D9BE4F9…`), `checkpoint-v1prime-z2` (`B12D0E90…`), `checkpoint-v1prime-y` (`A8DA8897…`), `checkpoint-v1prime-u` (`CD41C016…`), `checkpoint-v1prime-s` (`2F66D3D2…`), `checkpoint-v1prime-q` (`DD6212A8…`), `checkpoint-v1prime-p` (`B1375C52…`), `checkpoint-v1prime-l` (`695DC7F7…`), `checkpoint-v1prime-j` (`97803AD8…`), `checkpoint-v1prime-i` (`CD799ED4…`), `checkpoint-v1prime-g` (`EE2FFBAB…`), `checkpoint-v1prime-d` (`C8A2D660…`).
Toda tarefa deve partir dele. Depois de pronta, testar **abrindo o jogo com o save ZHABES (que tem o
adesivo da Dinamarca)** antes de ser dada como concluída.

Regras aprendidas, para não quebrar nada (ver `docs/APRENDIZADOS.md`):
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
  ou normal errada; conferir na carroceria inteira, começando por `versions/v1prime/in-game/2018-item9-manchas-nas-juncoes.png`, e polir só
  o encaixe, sem refazer a UV da pintura. Nos veículos do jogo é como se a lataria inteira fosse uma peça única, veja em `versions/v1prime/in-game/referencia-item9-carros-do-jogo-peca-unica.png`
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
- [x] **17. Câmera interna (Fusion 2018 e 2012).** *(Não resolvido: a câmera "capô" parece ficar dentro da entrada de ar do teto instalada; falta descobrir onde o jogo define essa posição. Testar sem a entrada de ar do teto.)* Na visualização pela câmera de dentro do veículo não aparece textura,
  só alguns itens pretos.
  *(27/09: encerrado sem alteração. Testando com a BMW original, o usuário viu que o MW não tem câmera interna: só a câmera sobre o capô e a do para-brisa, que nem mostra o capô. O teste do marcador ROOF_SCOOP foi desfeito; o jogo voltou para a GEOMETRY `2E4408AA…` (`pacote-26-09e`).)*
- [x] **18. Adesivos (vinis) que não aparecem.** *(Aprovado no jogo: V1prime-z8, peças DECAL_* trazidas do GTO; ver `versions/v1prime/variants/v1prime-z6-final-refine/LEIA-ME.md`.)* Os adesivos de porta, do para-brisa dianteiro, do para-brisa
  traseiro e os números de porta não são exibidos.
- [x] **19. Novos kits de carroceria.** *(Aprovado no jogo: V1prime-z8, kits "Street" e "Race".)* Gerar kits baseados em outros kits do jogo para ter mais uma opção
  de customização (hoje os kits 01 e 02 são cópias da carroceria padrão).
- [x] **20. Galeria de imagens do projeto (último item).** *(Feita em `docs/imagens-projeto/`, 18 etapas, 289 imagens.)* Salvar todas as imagens usadas no projeto e vistas
  pelo Claude num diretório organizado, com README explicando cada etapa (antes/depois da suavidade, renders 3D
  para mapear peças, antena tubarão etc.). *(Feito até a V1prime-z7 em `docs/imagens-projeto/`, 17 etapas, 265 imagens; completar se houver novos ajustes.)*

Pacote para outros jogadores: `release/Fusion2018_AWD_MW2005.zip` (versão final, única release).
- [x] **21. Parte de baixo do para-choque dianteiro.** *(Aprovado no jogo: V1prime-z10 — superfície única, sem o degrau do meio; ver `versions/v1prime/variants/v1prime-z10-front-lip/LEIA-ME.md`.)* Última peça com marcas pretas depois da V1prime-z8.

## Fusion Titanium 2012 FWD (slot COBALTSS)

Um item por vez, do mais simples ao mais difícil. Avisar para testar no jogo antes de seguir.
O zip `release/Fusion2012_FWD_MW2005.zip` ainda tem a geometria anterior (`2D4AF358…`) e só será refeito
quando os itens abaixo estiverem aprovados. Instalado e nos ZIPs de `release/` (26/09, tudo aprovado): 2012 `pacote-26-09e/` — GEOMETRY `2E4408AA…`/TEXTURES `39505AD5…`; 2018 `pacote-26-09d/` — GEOMETRY `B4D1BDDE…`/TEXTURES `13E45A9D…` — 2012 GEOMETRY `260F59AF…`/TEXTURES `39505AD5…`; 2018 GEOMETRY `B4D1BDDE…`/TEXTURES `13E45A9D…` (itens 36b e 39). Antes: `pacote-26-09c/` — 2012 GEOMETRY `BD51BA28…`/TEXTURES `39505AD5…`; 2018 GEOMETRY `2A26C393…`/TEXTURES `13E45A9D…` (o 2018 é o mesmo do `pacote-26-09b/`). Anterior aprovado: `pacote-26-09/`.

- [x] **22. Marca e nome (item 8).** Aprovado no jogo em 26/09. O jogo mostrava "temp350" porque o Mod Loader
  procura `SECONDARY_LOGO_COBALTSS_1` (hash `623849E1`). Logo do 2018 com esse hash. Ver `docs/CONTINUACAO.md` anexo A.6.
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
- [x] **41. Refino de para-choques e paralamas dianteiros e traseiros (2012 e 2018).** Pedido de 27/09: tirar falhas,
  triângulos malfeitos, marcas escuras e aperfeiçoar o encaixe de faróis e lanternas; no 2012, faróis mais para a frente.
  *(27/09, instalado para teste — `work/c2012-stage/pacote-27-09/`: 2012 GEOMETRY `B45C6A20…`, 2018 `F5A4B50F…`; texturas
  iguais. (1) Normais da lataria: faces da pele visíveis de fora (id-buffer de 120 direções) na frente (x>1,3) e
  traseira (x<−1,5) com canto de normal muito diferente da forma (cos<0,7) recebem a normal geométrica (vizinhança
  <45°) — 3.739 cantos no 2012, 4.003 no 2018 (`scripts/nfix.py`, `nrm.py`, `vis.py`). (2) 2012: aba abaixo dos faróis
  com sombreado em dente de serra — normais dos vértices a até 6 cm abaixo da borda da lente = média das faces
  vizinhas viradas como o para-choque (`teeth.py`). (3) 2012: faróis 8 mm para a frente (+x) e aro da carcaça fora do
  contorno da lente aparado (`hltrim.py`). Prévias `versions/fusion2012-fwd/preview/refino-item41-2012.png` e
  `-2018.png` (esquerda antes, direita depois; `pgr.py`).)*
- [x] **42. Riscos escuros, lábio dianteiro e encaixe do farol do 2012 (teste de 27/09).** Imagens em
  `versions/fusion2012-fwd/reference/teste-27-09/`: riscos no paralama junto à coluna e acima da lanterna (2012 e
  2018), lábio de baixo do para-choque dianteiro ondulado (2018), farol do 2012 com frestas, buracos pretos e lascas.
  *(27/09, instalado para teste — `work/c2012-stage/pacote-27-09b/`: 2012 GEOMETRY `0D618738…`, 2018 `EFA07989…`.
  (1) Correção de normais estendida à lataria inteira (antes só frente/traseira): 2.930 cantos no 2012, 2.481 no 2018;
  no 2012, para caber no limite de 65.535 vértices, apagadas 4.940 faces escondidas da frente/traseira (`nfix.py`,
  `prune41.py`). (2) 2018: lábio de baixo do para-choque refeito como superfície lisa, como no item 32 do 2012
  (`lip42.py`). (3) 2012: lascas da carcaça do farol que apareciam por fora (fora do contorno da lente e visíveis de
  fora) apagadas (`hlvis.py`); buraco na ponta do farol junto à grade (via-se o interior preto do carro) e frestas em
  volta fechados com pele pintada (`hlfill.py`, máscara da lente sem furos). Prévias `preview/refino-item42-*.png` e
  `farois-item42.png`. Pendente: alguns riscos finos na lateral traseira são costuras da malha original.)*
  *(27/09: o usuário deu o trabalho por finalizado; itens 41 e 42 encerrados e incluídos na release v2.0 — pacote `pacote-27-09b`.)*

- [x] **43. Chapa preta atrás da grade superior (2012 e 2018).** Pela grade cromada via-se o interior do carro (bancos
  de couro claro, `<CARRO>_INTERIOR`). *(27/09, instalado para teste — `work/c2012-stage/pacote-27-09j-grade-chapa/`:
  2012 GEOMETRY `5D110F4D…` (sobre `headlight55-full` `2ECEC047…`), 2018 `89700BC7…` (sobre `pacote-27-09e` `66B89F30…`);
  texturas iguais. Grupo novo em `BASE_A–E` (vale para todos os kits), textura `<CARRO>_LOGO` em área preta sólida
  (UV 0,1; 0,45): superfície x = 2,296 − 0,304·y², 12 mm atrás da face de trás das barras, contorno = abertura da
  lataria + 2,5 cm escondidos atrás da lataria (fora dos faróis). `versions/fusion2012-fwd/scripts/plate_grille.py`
  (+ `gmap.py`); prévias `versions/fusion2012-fwd/preview/grade-chapa-2012.png` e `-2018.png`.)*

- [x] **44. Encaixe final dos faróis dianteiros do Fusion 2012 após a v2.1.** Corrigir as saliências da lataria
  acima da ponta externa laranja e junto à ponta interna branca, além do buraco triangular escuro entre esta
  ponta e a grade. Não deslocar o farol inteiro: a ponta branca já encaixa. Candidato 56 instalado para teste
  nas duas rotas `COBALTSS` em 27/09; ainda aguarda avaliação no jogo pelo usuário. Geometria
  `41711104EE4C9BF76A1C71CE5F5F5AB9FBBD87F78D9D44D5CD8456EFD78BB73E`;
  `work/c2012-stage/pacote-27-09j-ultimos-pontos-farois/`. Capturas preservadas em
  `docs/imagens-projeto/19-fusion2012-e-refino/usuario/`; procedimento e contexto em
  `docs/CONTINUACAO.md`, seção 3. Este candidato não inclui a chapa do item 43. Não fazer release
  nem marcar concluído sem aprovação visual.
  *(27/09: chapa da grade aprovada no jogo pelo usuário (testada sobre o 55). Como a instalação dela tinha sobrescrito o
  candidato 56 dos faróis, foi montado e instalado o 56 + chapa: `work/c2012-stage/pacote-27-09k-farois56-grade/`,
  2012 GEOMETRY `3872FCE7…` (193 peças, 1.437.081 triângulos; o 56 só altera BODY e a chapa só altera BASE_A–E).
  Backup do que estava instalado (55 + chapa, `5D110F4D…`) em `backup/`. Faróis do 56 aguardando teste no jogo.)*
  - [x] **44 (cont.). Candidato 57 — nova abordagem.** Teste de 27/09 do candidato 56 (junto com a chapa
  da grade): ainda havia calombos na ponta interna (junto à grade), sob o farol e acima da seção laranja.
  *(27/09, instalado para teste — `work/c2012-stage/pacote-27-09l-farois57-cinta/`: 2012 GEOMETRY `FC59A72A…` (sobre
  `3872FCE7…`, que está em `backup/2012/`). Em vez de remendos sobrepostos: parametrização radial a partir de um ponto
  dentro do carro (`hl58maps.py`, acompanha a quina frente→lado→capô); superfície alvo = lataria antiga filtrada
  (mediana 5×5 + gaussiana de 1,5 cm, sem a lente) numa faixa de até 7,5 cm da lente, fora do capô e da grade
  (`hl57solve.py`); os vértices da pintura das carrocerias (todos os kits, LODs A–E) perto da superfície são projetados
  nela (mesma topologia, sem costura, transição de 3,6 cm) com normais do campo liso; pele de fundo 1,5 mm abaixo em
  `BASE_A–E` tapa os buracos (`hl59.py` com `WIN_IN=0.07 WIN_OUT=0.08 CAP=0 RW=0 EXCL=5 EXH=1 R=0.075 BLEND=12 SIG=0.015`).
  Farol e capô não foram movidos. 193 peças, 1.437.336 triângulos. Prévia `versions/fusion2012-fwd/preview/farois-item57.png`
  (esquerda antes, direita depois).)*
- [x] **45. Cinta de reboque preta mais larga (2012 e 2018).** A preta parecia mais estreita que a vermelha (geometria e
  textura eram iguais, 5 cm; o fundo escuro se confunde com a grade preta). *(27/09, instalado para teste no mesmo pacote:
  cinta preta dos kits KIT01/KIT05 30 % mais larga (6,5 cm), vermelha igual; `strap_wide.py`; 2018 GEOMETRY `EDDE6EE9…`
  (sobre `89700BC7…`, em `backup/2018/`). Prévia `preview/cinta-preta-larga.png`.)*
  *(27/09: itens 43, 44 (candidato 57) e 45 aprovados no jogo ("está quase perfeito") e publicados na **v2.2**: 2012
  GEOMETRY `FC59A72A…`, 2018 `EDDE6EE9…`, texturas iguais às da v2.1. Capturas do teste em
  `docs/imagens-projeto/19-fusion2012-e-refino/usuario/teste-27-09-c57--*.png`.)*
- [x] **46. Para-choque encaixando na parte de baixo do farol (2012).** Pedido de 27/09 após a v2.2: a borda de cima do
  para-choque deve encostar na parte de baixo do farol (hoje aparece a faixa escura da carcaça entre os dois, sob o
  farol e junto à ponta interna). Capturas `teste-27-09-c57--parachoque-sob-farol-marcado.png` e
  `teste-27-09-c57--parachoque-ponta-interna-marcado.png` (marcações em amarelo do usuário).
  *(27/09, instalado para teste — `work/c2012-stage/pacote-27-09m-parachoque-farol/`: 2012 GEOMETRY `12F99EE6…`
  (sobre a v2.2 `FC59A72A…`, em `backup/`). `hl59.py` com `LIFT=0.05 LOFF=0.0005 LENSIN=5 LSIG=0.006 BKIN=1`: a
  lataria abaixo da borda de baixo da lente sobe até 0,5 mm dela (rampa de até 4,5 cm, afinando nas pontas) e a
  superfície passa por baixo da borda da lente; pele de fundo chega até a lente. Fresta medida por fatias
  (`gapmeas.py`): de 20–50 mm para 1–9 mm. `curtain.py`: piso inclinado na cor da pintura sob cada farol
  (em `BASE_A–E`) que fecha a visão para dentro do carro por baixo do farol. Cinta preta larga mantida.
  193 peças, 1.441.090 triângulos. Prévia `preview/parachoque-farol-item46.png`.)*
  *(27/09: aprovado no jogo ("ficou perfeito") e publicado na **v2.3**: 2012 GEOMETRY `12F99EE6…`; 2018 igual à v2.2.)*
- [x] **47. Cintas de reboque sem repetição entre os kits (2012 e 2018).** Pedido de 27/09: KIT00 fábrica sem cinta;
  KIT01/KIT02 dianteira preta/vermelha; KIT03/KIT04 traseira preta/vermelha, do lado esquerdo, por dentro do
  escapamento, presa na faixa preta; KIT05 dianteira e traseira laranja com texto preto. Sem kits novos: só os seis
  que o jogo já tem para o slot (o KIT03 existia no Cobalt e no Mustang originais e faltava no Fusion).
  *(27/09, instalado para teste — `work/c2012-stage/pacote-27-09n-kits-cintas/`: 2012 GEOMETRY `A065ACDD…` /
  TEXTURES `A62F9A5D…`, 2018 GEOMETRY `B52C25E6…` / TEXTURES `DC88390E…`; anteriores em `backup/`.
  `kits46.py` (traseira: y +0,42, z 0,215 → 0,015, 1 cm atrás do para-choque; KIT03 com os decalques do KIT01) e
  `tex46.py` (cinta laranja 一路顺风 em área livre do atlas). Prévia `preview/kits-cintas-item47.png`.)*
  *(Substituído pelo item 48.)*
- [x] **48. Cinco cintas diferentes, uma por kit (2012 e 2018).** Pedido de 27/09: KIT01–KIT05 com cintas distintas, cada
  uma na dianteira (lado direito) e na traseira (lado esquerdo): preta/vermelho, vermelha/branco, laranja/preto, azul
  com F B I amarelo e zebrada preta e amarela; dianteira baixada para ficar só na parte preta do para-choque; traseira
  1,5 cm mais longe do escapamento. *(`kits48.py`, `tex48.py`; pacote `work/c2012-stage/pacote-27-09o-cintas5/`:
  2012 GEOMETRY `643E5E4A…` / TEXTURES `26E9ADDE…`, 2018 GEOMETRY `4E950229…` / TEXTURES `F7C6C9F3…`. Publicado na
  **v2.4**. Prévias `preview/kits-cintas-item48.png` e `cintas-item48.png`.)*
- [x] **49. Texto da cinta laranja: 読めば尺八 (yomeba shakuhachi).** *(27/09, instalado: só `TEXTURES.BIN` dos dois
  carros — 2012 `380AEF78…`, 2018 `38F231C8…`; pacote `work/c2012-stage/pacote-27-09p-cinta-laranja/`, anterior em
  `backup/`. `tex48.py` (5 caracteres, fonte 40 px) e `strap_tex.py` (tamanho e espaçamento configuráveis). Prévia
  `preview/cintas-item49.png`. A geometria é a da v2.4. Publicado na **v2.5**.)*
- [x] **50. Lente dos faróis do 2018 preta com listras (prévia e jogo com mods).** A UV de
  `KIT00_RIGHT_HEADLIGHT_GLASS_A–D` apontava para uma área preta do atlas `KIT00_HEADLIGHT_OFF`, com alfa em colunas
  (três 100 %, uma 20 %). O jogo original não mostra a cor dessa lente; o Xbox 360 Stuff e texturas novas mostram.
  *(`scripts/lente-vidros-capo/lente50.py`: célula clara com alfa 27 % em x 512–575 / y 128–191 e UV da lente nela;
  pisca âmbar mantido. Imagens em `docs/imagens-projeto/20-lente-vidros-capo/`. Aprovado no jogo e publicado na **v2.6**.)*
- [x] **51. Para-brisa em duas camadas e textura espelhada (2012 e 2018).** Cada vidro tinha a chapa de fora e a de
  dentro (5,5 mm) e o para-brisa usava um quarto da textura, espelhado no meio; o vidro traseiro também, dividido
  entre dois sólidos. *(`vidros51.py` + `aplica51.py`: uma chapa por janela, textura da posição, UV 0–1 plana sem
  espelho, em `FRONT_WINDOW_A–D` e `REAR_WINDOW_A–D`. Aprovado no jogo e publicado na **v2.6**.)*
- [x] **52. Capô preto com mods (2012 e 2018).** O `KIT00_HOOD` tinha cada triângulo repetido com a face para baixo
  na mesma posição; com os dois lados desenhados, a cópia escura cobria a pintura. *(`capo52.py`: sai toda face do
  `KIT00_HOOD_A–D` virada para dentro; nos `STYLExx_HOOD` só a cópia de baixo nas partes planas. Aprovado no jogo e
  publicado na **v2.6**: 2012 GEOMETRY `2C8C625C…`, 2018 GEOMETRY `7D95E28E…` / TEXTURES `8DF768ED…`.)*
