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
- [ ] **17. Câmera interna.** *(Não resolvido: a câmera "capô" parece ficar dentro da entrada de ar do teto instalada; falta descobrir onde o jogo define essa posição. Testar sem a entrada de ar do teto.)* Na visualização pela câmera de dentro do veículo não aparece textura,
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
quando os itens abaixo estiverem aprovados. Instalado agora: GEOMETRY `022AD2FB…` (item 1, a testar).

- [x] **22. Marca e nome (item 8).** Aprovado no jogo em 26/09. O jogo mostrava "temp350" porque o Mod Loader
  procura `SECONDARY_LOGO_COBALTSS_1` (hash `623849E1`). Logo do 2018 com esse hash. Ver `CONTINUACAO-FUSION2012.md` seção 4.6.
- [x] **23. Tampa do porta-malas (item 7).** Aprovado no jogo em 26/09 (GEOMETRY `C159D615…`). A faixa clara/escura
  era a aba do friso cromado do 2018, inclinada e com frestas; ficou reta do vinco até a moldura da placa, sombreado
  uniforme, frestas fechadas por trás. O vinco de uma lanterna à outra permanece. Ver `versions/fusion2012-fwd/scripts/lidfix.py`
  e `versions/fusion2012-fwd/preview/tampa-item7.png`.
- [x] **24. Para-choque traseiro (item 6).** Pequena deformação no canto inferior, no meio. *(Aprovado no jogo em 26/09:
  GEOMETRY `A0F66D69…`. Normais do vinco inferior do centro trocadas pela da face traseira; ver
  `versions/fusion2012-fwd/scripts/fix6.py` e `preview/parachoque-traseiro-item6.png`.)*
- [ ] **25. Grade preta frontal inferior (item 1).** Não conecta os dois faróis de milha. Conferir com as fotos de referência.
  *(Feito em 26/09, instalado, aguardando teste: GEOMETRY `022AD2FB…`. Grade trapezoidal terminando antes dos faróis de
  milha, lataria pintada no vão; ver `versions/fusion2012-fwd/scripts/grille1.py` e `preview/grade-inferior-item1.png`.)*
- [ ] **26. Vazio abaixo dos faróis de milha (item 2).** Preencher esse espaço no para-choque.
- [ ] **27. Cor interna das lanternas (item 5).** A parte na tampa do porta-malas precisa da mesma cor e das mesmas
  camadas da parte externa (para-choque/carroceria).
- [ ] **28. Tamanho das lanternas traseiras (item 3).** Estão menores que o nicho; aumentar até encaixarem.
- [ ] **29. Lataria em volta dos faróis (item 4).** Faróis estão certos; há deformação no encaixe com o capô, o paralama
  e o para-choque.
