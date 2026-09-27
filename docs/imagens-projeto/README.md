# Imagens do projeto Fusion 2018 → NFS Most Wanted 2005

Todas as imagens que o Claude gerou ou analisou nas sessões de 23 a 25/09/2026, em ordem cronológica,
separadas pela etapa do trabalho. O nome de cada arquivo começa com `MMDD-HHMM` (horário UTC em que foi
criada ou recebida).

- `*-enviada-pelo-usuario-*.jpg`: capturas do jogo e fotos de referência que você mandou no chat
  (convertidas de PNG para JPEG qualidade 90 para o repositório ficar menor).
- Os outros arquivos são renders feitos fora do jogo pelos scripts do projeto (`render.py`, `diagrender.py`,
  `thru.py` etc.), usados para localizar peças, comparar antes/depois e conferir o resultado antes de instalar.
- Prévias que já estavam em cada variante (`versions/v1prime/variants/*/`) e as capturas aprovadas em
  `versions/v1prime/in-game/` continuam lá; aqui estão todas as imagens de trabalho.
- As etapas de 19 a 22/09 (v0, v1 AJM3899, v2 Shelby, v3) têm as prévias do Blender em `versions/*/preview`.

Cores usadas nos renders de diagnóstico: cada cor é uma peça ou grupo do GEOMETRY.BIN; nos renders
cinza "com faixas" o reflexo é listrado de propósito para exagerar qualquer erro de normal (ondulação).

## 01-diagnostico-do-modelo (23/09)
Mapa do modelo de referência AJM3899 (`ajm_*`) e das versões v2/v3 (`v2_*`, `v3*`): peças por cor, faces
invertidas (`*_cull`, `v3a_flipped`), lanternas e faróis (`*_lamps`), vidros, grupos da carroceria e um
triângulo espetado (`spike`).

## 02-lanternas-grade-e-normais (23/09)
Suas capturas mostrando lanternas/grade erradas. Zoom da grade e da textura (`front_zoom`, `grille_tex`),
cobertura de cada textura (`occ_*`), vidros, emblemas, e a correção das normais da v3 (`v3*_normals*`,
`v3b_final`).

## 03-v1prime-placas-grade-e-pecas (23/09)
Início da linha V1prime: simulação do visual no jogo (`sim_end`, `v1p_sim`), placas (`plate_*`, `prf_small`),
grade (`vp_grille_parts`, `grille_game_zoom`), peças coloridas A/B (`*_partcolor`, `partcmp`, `vp_AB`),
texturas da frente e traseira (`v1p*_front_tex`, `v1pb_*`). Suas capturas de cada tentativa.

## 04-adesivos-nas-portas (23–24/09, TODO item 8)
Adesivo da Dinamarca deformado nas portas: comparação das UVs (`vinyl_uv_*`), grade de teste na lateral
(`side_d*`, `uvlayout`, `orig`, `fix1`, `fix2`) e a bandeira corrigida (`cmp`). Resultado V1prime-g.

## 05-aerofolio-e-brake-light (24/09, itens 1 e 2)
Sua captura do aerofólio flutuando e os pontos de montagem SPOILER / CENTRE_BRAKELIGHT (`sp*`).

## 06-antena-tubarao (24/09, item 3)
Suas fotos da antena real (96 × 196 × 61 mm) e os renders da antena da cor do carro (`ant_A/B/C`, `fin2`,
`fin3`). Resultado V1prime-l.

## 07-emblemas-fusion-titanium (24/09, item 4)
Imagens de referência das letras cursivas, os contornos traçados (`fusion_mask`, `titanium_mask`,
`titanium_photo_mask`, `masks`, `tm`) e os emblemas 3D na tampa (`emb`, `emb2`, `emb3`, depois do ajuste
para caber no seu quadrado vermelho). Resultado V1prime-p.

## 08-entradas-de-ar-e-capo (24/09, itens 5 e 6)
Suas capturas das entradas de ar e do capô da loja deformado nas bordas vs. o original; render do capô e
das bordas (`hood`, `hoodedge`). Resultado V1prime-q e V1prime-s.

## 09-traseira-e-coluna-c (24–25/09, item 7)
Suavização da traseira (`rear_smooth`, `rear_cmp*`), sua captura das frestas na coluna C, frestas
(`crack_*`), tentativa de preenchimento (`fill_cmp`) e a camada de fundo pintada que resolveu
(`backing_cmp`). Resultado V1prime-u.

## 10-rodas-gta (25/09, item 10)
Roda de 20 raios lida do `fusion_hi.yft`: pneu, parede e peças (`tire`, `wall`, `wparts`), texturas do pneu
e do aro (`tex_*`, `texs`), sua foto da roda real e a comparação final (`wheel_cmp`). Resultado V1prime-y.

## 11-vidros-e-logotipo (25/09, itens 12 e 15)
Camadas de vidro antes/depois (`glass_layers`, `glass_new`, `glass_fr`); logotipo atual vs. novo, decodificado
do DXT3 (`logo_*`, `seek`), e o logo menor com espaço nas laterais (`*-z3`). Resultados V1prime-z e z3.

## 12-chama-do-nitro (25/09, item 16)
Vista traseira baixa com os pontos LEFT/RIGHT_EXHAUST antigos (vermelho) e novos (amarelo) no centro das
saídas do para-choque (`rear_low`, `tipL`, `nitro`). Resultado V1prime-z3.

## 13-suavidade-e-kits (25/09, itens 9, 14 e 11)
`Screenshot_146/147` (Fusion vs. SLR no jogo), mapa do erro das normais (`dev`), peças (`parts`, `zp`),
reflexo em faixas antes (`nrm`, `z0`) e depois da suavização com raio 5 e 9 cm (`nrm1`, `nrm2`, `z2`,
`zrear`), bordas abertas da malha (`cracks`). Resultado V1prime-z4.

## 14-frestas-e-refino (25/09, refino dos itens 9 e 14)
Suas capturas marcadas em vermelho. Detector de frestas por profundidade (`gap*`: preto = fresta),
cobertura da camada de fundo (`cat`: verde novo, azul já existente, roxo/vermelho sem fundo),
carroceria branca com o resto preto para ver o que aparece pelas frestas (`thru4` = z4, `thru5` = z5,
`t4_*`/`t5_*`, `crop_*`, `cmp_*`), e o reflexo em faixas final (`nrm5`). Resultado V1prime-z5.

## 15-refino-final-camera-adesivos-kits (25/09, itens 9, 14, 17, 18 e 19)
Suas capturas marcadas (para-lama junto ao farol, lateral traseira, lábios dos para-choques). Reflexo em faixas
antes/depois da subdivisão curva da pele e da suavização leve das posições (`r5` = z5, `r6` só subdivisão,
`r7` = subdivisão + suavização; comparações `r56_*`, `r57_*`), zoom do para-lama e capô (`f_g5b`, `f_g7`,
`f57`, `hood7`). Peças de adesivo novas coloridas por espaço de adesivo (`decals`: porta, números, lateral
traseira, faixas do para-brisa e do vidro traseiro). Os três kits lado a lado (`kits`: KIT00 de fábrica,
KIT01 "Street" com lábio, saias e lábio traseiro, KIT02 "Race" com splitter, saias maiores e difusor com aletas).
Resultado V1prime-z6.

## 16-ajustes-pos-teste-z6 (25/09)
Suas 7 capturas do teste da z6 (kits flutuando, para-choque inferior, para-lamas, frestas do capô, emblema Ford,
visão de dentro). Texturas conferidas para achar o texel preto e o cromado (`tex_*`, `texs2`, `misc_cur`),
emblema Ford com letras e aro prata e fundo preto (`badge`), para-lamas dos dois lados antes/depois do
espelhamento (`fp*`, `fm*`, `fpm*`, `f4`), carroceria e capô separados para achar os recortes (`hc*`, `sep`),
lábio inferior do para-choque antes/depois (`lip*`), piso pintado sob o contorno do capô (`hoodgap`: branco =
carroceria/capô, preto = demais peças) e os kits encaixados nos para-choques (`kits2`). Resultado V1prime-z7.

## 17-para-lamas-e-vao-do-capo (25/09)
Suas capturas do teste da z7. Lado do motorista (+y, onde fica o `KIT00_DRIVER`) comparado com o passageiro
(`sides`: mostra que o lado ruim era o do motorista), tentativas no para-lama (`k1cmp`, `pk1`, `p8`),
peças escuras no vão entre capô e para-choque (`hoodfront`: azul = peça escura da base) e o vão fechado
(`hf`), tentativas no lábio inferior do para-choque que foram descartadas (`lip*`), e simulações de câmera
em perspectiva usadas para procurar a posição da câmera "capô" (`cams`). Resultado V1prime-z8.

## 18-parachoque-inferior (25/09)
Investigação das marcas pretas na parte de baixo do para-choque dianteiro: vistas de frente/baixo com carroceria
branca e demais peças pretas ou coloridas (`lower`), a malha original em perfil e de frente mostrando os
triângulos grandes dobrados (`lipgeo_*`), render com luz vinda de cima como no jogo antes/depois (`gl_*`,
`g3_*`, `g4_*`, `c3`, `c4`, `gl_cmp*`) e reflexo em faixas (`sl_*`, `sb_*`, `s3_*`, `slcmp`). Resultado V1prime-z9.

## 19-fusion2012-e-refino (26–27/09, Fusion 2012 e refino dos dois carros)
`usuario/`: capturas enviadas pelo usuário — fotos do Fusion 2013 de referência (`fotos-2013--*`), lataria e freios
(`item4-lataria--*`), cintas de reboque de referência (`cintas-reboque--*`), testes de 26/09 (lanternas laterais,
divisão da antena, faixas do para-brisa) e de 27/09 (riscos no paralama e na lateral traseira, lábio do 2018, farol do
2012). `previas/`: renders antes/depois de cada item do 2012 e do refino (itens 1, 6, 7, 27–42).
Resultados: release v2.0 e pacotes `pacote-27-09`/`27-09b`.

