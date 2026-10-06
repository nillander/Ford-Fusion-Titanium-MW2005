# Ford Fusion Titanium 2012 FWD e Fusion Titanium 2018 AWD — Need for Speed Most Wanted (2005)

Dois mods para o Most Wanted de PC. Instalam juntos porque usam slots diferentes. O 2012 é a carroceria aprovada do Titanium 2018 com faróis, lanternas e faróis de milha do modelo 2012 (Ford Mondeo 2016 do GTA V).

| Carro | Substitui | Slot | Tração gravada na v2.4 |
| --- | --- | --- | --- |
| Ford Fusion Titanium 2012 FWD | Chevrolet Cobalt SS (carro inicial) | `COBALTSS` | Dianteira (`TORQUE_SPLIT` 1,0) |
| Ford Fusion Titanium 2018 AWD | Ford Mustang GT | `MUSTANGGT` | Traseira (`TORQUE_SPLIT` 0). O nome na garagem é AWD |

> **Release atual: v2.8 (06/10/2026).** Saíram de todas as peças os triângulos repetidos na mesma posição (o verso das chapas do GTA), que com Xbox 360 Stuff, pacotes de textura e ReShade deixavam manchas escuras: 42.314 triângulos a menos no 2018 e 48.459 no 2012. Ela inclui a v2.7: Os refletores traseiros do 2012 são vermelho sólido, as lanternas do 2018 preservam a lente sem reflexo excessivo e os retrovisores dos dois carros usam a lente inteira com textura local reflexiva, sem manchas pretas. A v2.7 também corrige os nomes no ModLoader. Ela inclui a v2.6: lente clara nos faróis do 2018, vidros em chapa única e capô sem cópias internas visíveis com Xbox 360 Stuff, pacotes de textura e ReShade. O estado do trabalho está em [docs/CONTINUACAO.md](docs/CONTINUACAO.md).

## No jogo

| Fusion Titanium 2012 FWD | Fusion Titanium 2018 AWD |
| --- | --- |
| ![Fusion 2012 no menu principal](capturas/2012/principal.png) | ![Fusion 2018 no menu principal](capturas/2018/principal-2.png) |
| ![Frente do 2012, com a cinta do kit](capturas/2012/Screenshot_175.png) | ![Lateral do 2018 na garagem](capturas/2018/Screenshot_170.png) |
| ![Traseira do 2012 e o logo FUSION](capturas/2012/Screenshot_172.png) | ![Traseira do 2018 com aerofólio](capturas/2018/Screenshot_168.png) |
| ![2012 na cidade](capturas/2012/Screenshot_178.png) | ![2018 em perseguição](capturas/2018/Screenshot_185.png) |

[Todas as capturas dos dois carros](capturas/README.md). São imagens feitas no jogo; algumas podem mostrar testes posteriores à v2.4. As anotações de diagnóstico (vermelho e amarelo) ficam em [docs/imagens-projeto/](docs/imagens-projeto/README.md).

## O que entra no jogo

O Mod Loader lê `ADDONS`. O instalador copia a mesma geometria e as mesmas texturas também para `CARS/<slot>`, que é o caminho que o jogo usa quando o addon não cobre o arquivo. Os dois caminhos precisam ser o mesmo arquivo.

### Fusion 2018 — slot `MUSTANGGT`

| Arquivo | Conteúdo |
| --- | --- |
| `CARS/MUSTANGGT/GEOMETRY.BIN` | 40,1 MB. Carroceria, capôs, kits, interior, vidros, luzes, rodas, freios, adesivos e pontos de montagem |
| `CARS/MUSTANGGT/TEXTURES.BIN` | 4,6 MB. Folhas do carro. Peças opacas em DXT1; lentes e vidro em DXT3 |
| `ADDONS/CARS_REPLACE/MUSTANGGT/ATTRIBUTES.MWPS` | Performance: motor, câmbio, chassi, massa, pneus e altura. O Mod Loader reaplica isto ao abrir o jogo |
| `ADDONS/CARS_REPLACE/MUSTANGGT/FE.MWPS` | Nome de fabricante Ford, preço 42.000 e nível 9 da Blacklist |
| `ADDONS/CARS_REPLACE/MUSTANGGT/CAR.INI` | `name=Ford Fusion Titanium AWD`, `internal=mustanggt`, `modloader=0.2` |
| `ADDONS/CARS_REPLACE/MUSTANGGT/SECONDARYLOGO.BIN` | Logo FUSION da tela de carros |
| `ADDONS/CARS_REPLACE/MUSTANGGT/VINYLS.BIN` e `PREVINYL.BIN` | Espaço de vinil do slot |
| `ADDONS/FRONTEND/MANUFACTURERS/27-FORD_HD.BIN` | Logo Ford em alta resolução. Vale para **todos** os carros Ford |

`GEOMETRY.BIN` e `TEXTURES.BIN` de `ADDONS/CARS_REPLACE/MUSTANGGT/` são cópias dos arquivos de `CARS/MUSTANGGT/`.

### Fusion 2012 — slot `COBALTSS`

| Arquivo | Conteúdo |
| --- | --- |
| `CARS/COBALTSS/GEOMETRY.BIN` | 47,6 MB. A malha do 2018 com as luzes 2012 enxertadas e os sólidos renomeados para `COBALTSS` |
| `CARS/COBALTSS/TEXTURES.BIN` | 4,1 MB. Atlas das luzes 2012 em `HEADLIGHT_OFF` (DXT1, opaco) e `BRAKELIGHT_OFF` (DXT3, lentes) |
| `ADDONS/CARS_REPLACE/COBALTSS/ATTRIBUTES.MWPS` | Chassi do 2018, motor do Cobalt SS com torque +20 % e tração dianteira |
| `ADDONS/CARS_REPLACE/COBALTSS/FE.MWPS` | Fabricante Ford no nó do Cobalt. Preço e Blacklist continuam os do carro inicial |
| `ADDONS/CARS_REPLACE/COBALTSS/CAR.INI` | `name=Ford Fusion 2012 FWD`, `internal=cobaltss`, `modloader=0.2` |
| `ADDONS/CARS_REPLACE/COBALTSS/SECONDARYLOGO.BIN` | Logo FUSION com o hash que o Mod Loader procura para este slot |
| `ADDONS/FRONTEND/MANUFACTURERS/27-FORD_HD.BIN` | O mesmo logo Ford HD do pacote 2018 |

O `VINYLS.BIN` do Cobalt permanece o do jogo. A pintura do 2012 usa a UV contínua já gravada na carroceria.

| Pacote v2.8 | SHA-256 do ZIP | `GEOMETRY.BIN` | `TEXTURES.BIN` |
| --- | --- | --- | --- |
| [Fusion2012_FWD_MW2005.zip](release/Fusion2012_FWD_MW2005.zip) | `FAF2EC7BBF3AF4CDF169CB9086163FDA8AE855D2C3C4916E162546DB4531987D` | `46EA905703DC3BADAA92236FCCA8DD0BE65BFBAA95DC65B9D807DC427F4115C3` | `380AEF7826723967DB0E3CD49284387A4469E75938D767EC437CEC9A8670A5B7` |
| [Fusion2018_AWD_MW2005.zip](release/Fusion2018_AWD_MW2005.zip) | `D786292C56092EEFAC98E4CAB19E1A7D16A1B15A4B9D367D5B6C76A1F9D51E71` | `C6506D3FA563EC05926315CCC994DE5DC3150DC281F460139BCEE2C16B706F01` | `8DF768ED4BCB4BF933FC4F686FDDF1B13FA203BCB21A656986132008A617F8EF` |

Os hashes de cada arquivo interno estão em [release/SHA256SUMS-conteudo.txt](release/SHA256SUMS-conteudo.txt). As notas da release estão em [release/NOTAS-v2.8.md](release/NOTAS-v2.8.md).

### Peças que o slot precisa ter

O kit de carroceria troca a lataria inteira. Um kit ausente deixa o carro sem carroceria na loja, na IA e nos carros prontos do jogo.

| Peça | Para que serve |
| --- | --- |
| `KIT00_BODY_A–E` | Carroceria de fábrica, do LOD alto ao mais baixo |
| `KIT01_BODY` a `KIT05_BODY` | A mesma lataria com uma cinta de reboque diferente em cada kit, na dianteira (lado direito) e na traseira (lado esquerdo): KIT01 preta 大吉大利, KIT02 vermelha 出入平安, KIT03 laranja 読めば尺八, KIT04 azul FBI, KIT05 zebrada (`kits48.py`, `tex48.py`). O Mustang do Razor e as cutscenes usam KIT04 ou KIT05; a cutscene `CS_CAR_14` usa o KIT04 do Cobalt |
| `STYLExx_HOOD` | 17 capôs da loja, no formato do capô do Fusion |
| `BASE` | Interior, vidros de apoio, motorista e pontos de luz, escapamento, aerofólio e entrada de ar do teto |
| `RIGHT_SIDE_MIRROR` | No catálogo do doador, este sólido guarda a grade, os frisos e o cromado. O nome não é o retrovisor |
| Faróis, lanternas e faróis de milha | No 2018 ficam nas peças `RIGHT_*` (os dois lados). No 2012 existem também as peças `LEFT_*` |
| `KIT00_FRONT/REAR_BRAKE` | Discos e pinças do Pontiac GTO, no lugar da textura de multimídia que o modelo trazia |
| `DECAL_*` | Adesivo de porta, números e faixas de para-brisa |

Cada sólido cabe em 65.535 vértices. Num sólido com vários materiais, o grupo que passa de 65.535 índices deixa de ser desenhado.

## Aprendizados

O relato completo, com as imagens de cada diagnóstico, está em [docs/APRENDIZADOS.md](docs/APRENDIZADOS.md). O que mais se repete:

1. **DXT1 para peça opaca.** O jogo trata textura DXT3 como translúcida e não grava profundidade. Grade, cromado, interior e emblema em DXT3 deixam o que é desenhado depois pintar por cima, mesmo estando atrás. MISC, LOGO e INTERIOR voltaram a DXT1. Lente e vidro continuam DXT3 e ficam por último na ordem de desenho.
2. **Limite de 65.535.** Vértices por sólido, e índices por grupo quando o sólido tem mais de um material. A grade sumia porque o grupo dela em `BASE_A` passava do índice; foi para o slot vazio `KIT00_RIGHT_SIDE_MIRROR_A`. No 2012 o `BODY_A` vive perto do limite de vértices: correção nova precisa apagar face escondida antes de criar vértice.
3. **Kit vazio apaga o carro.** A IA, o Razor, o menu da carreira e as cutscenes pedem KIT04 e KIT05. Sem essas carrocerias só sobram interior e rodas.
4. **Vinis usam a UV da pintura.** A UV herdada do GTA mapeia cada painel sozinho e o adesivo quebra entre as portas. O layout do jogo é contínuo: `u = 0,169·x + 0,5`, com `v` desenrolando a seção do carro (`versions/v1prime/scripts/vinyluv.py`).
5. **Mancha escura muitas vezes é normal, não buraco.** Um vértice do vinco com a normal da face de baixo escurece o triângulo da lataria. O render com normal de face esconde isso; o render com normal de vértice (`pgr.py`) mostra o que o jogo mostra.
6. **O jogo não desenha o verso da face.** Um render que pinta os dois lados esconde fresta. A conferência usa descarte de faces e fundo magenta (`rtc.py`).
7. **Nome de textura.** O mwtc grava o nome num campo de 24 bytes. Nome maior que 23 caracteres desloca o resto do TPK e fecha o jogo; o hash continua o do nome completo. UV exatamente em 0 ou 1 dá a volta para o quadrante vizinho do atlas e a lente sai preta: as UVs das luzes recuam 0,4 % da borda da célula.
8. **Logo da tela de carros.** O Mod Loader troca o nome procurado para `SECONDARY_LOGO_<internal>_1`. O hash dentro do `SECONDARYLOGO.BIN` (offsets 0xD4 e 0x108) tem de ser esse. Hash repetido de outro carro mostra "temp 350"; hash que já existe no `FrontB.lzc` mostra o logo original do slot.
9. **Duas pastas, jogo fechado.** Com o jogo aberto, `ADDONS/CARS_REPLACE` fica travada e só `CARS` atualiza. O Mod Loader lê `ADDONS`, então o teste mostra a versão antiga. Conferir o SHA-256 nos dois caminhos.
10. **Casca "gum" do GTA.** O shader gum do Mondeo é uma segunda carroceria preta colada na pintura. O que fica a menos de 4 mm da lataria entra no enxerto e precisa ser excluído.
11. **O que o jogo esconde, os mods mostram.** Com Xbox 360 Stuff, pacotes de textura e ReShade aparecem camadas que o jogo original não desenha: o verso das faces (a chapa de dentro dos vidros e a cópia virada para baixo do capô, que deixava o capô preto), a cor de uma lente que o shader original ignorava (lente do 2018 em área preta do atlas) e a UV dos vidros (o para-brisa usava um quarto da textura, espelhado no meio). Conferir com textura de teste e contar faces opostas coincidentes (`scripts/faces-duplicadas/scan2.py`). Na v2.8 todas as cópias saíram (`scripts/faces-duplicadas/`).

A primeira aprovação visual do 2018, com a grade opaca de volta, foi a V1prime-d:

![V1prime-d aprovada no jogo](versions/v1prime/in-game/v1prime-d-approved.png)

## Performance

Potência e dirigibilidade ficam no VLT (`GLOBAL/ATTRIBUTES.BIN`), não na malha. O Mod Loader reaplica o `ATTRIBUTES.MWPS` do slot toda vez que o jogo abre. Trocar só o `GEOMETRY.BIN` não muda como o carro anda. As três opções testadas no 2018 (Mustang puro, M3 GTR e SLR com chassi de M3) estão em [versions/performance/PERFORMANCE.md](versions/performance/PERFORMANCE.md). A v2.1 gravou a mistura abaixo.

### Fusion 2018 (`MUSTANGGT`)

Motor e câmbio da Mercedes-Benz SLR McLaren; chassi, barras, molas, aderência e direção do Mustang GT, com massa de 1.600 kg. `STEERING` 1,0 e `YAW_SPEED` 0,40 / 0,38 nos dois estágios. `TORQUE_SPLIT` 0 nos dois estágios (tração traseira). Aro 18, perfil 40, seção 255 mm.

| | Estoque | Melhorado |
| --- | --- | --- |
| Pico da curva de torque | 523 | 621 |
| Corte (`RED_LINE`) | 7.000 rpm | 7.000 rpm |
| Marcha final | 3,06 | 3,50 |
| Barras dianteira / traseira | 250 / 250 | 300 / 325 |
| Molas dianteira / traseira | 500 / 500 | 600 / 700 |
| Aderência estática diant. / tras. | 1,75 / 1,85 | 2,025 / 2,1 |
| Peso dianteiro | 53 | 53,5 |

Rodas, medidas no `ecar` do próprio MWPS: dianteira em X = +1,425, traseira em X = −1,305 (entre-eixos 2,73 m), meia-bitola Y = 0,895, escala de diâmetro 0,345. Preço 42.000 e Blacklist 9 vêm do `FE.MWPS`. O detalhe campo a campo da dirigibilidade está em [versions/v1prime/variants/v1prime-z2-handling-logo/LEIA-ME.md](versions/v1prime/variants/v1prime-z2-handling-logo/LEIA-ME.md); o hash do `ATTRIBUTES.MWPS` da v2.1 é o dessa variante (`3BE53CF9…`).

### Fusion 2012 (`COBALTSS`)

`versions/fusion2012-fwd/scripts/perf12.py` copia o chassi, os pneus, os freios, a massa, a inércia e a altura do 2018 para os nós `cobaltss` / `cobaltss_top`, e mexe só no motor e na tração:

- torque do Cobalt SS × 1,2: 85–180 passa a 102–216; o estágio de cima, 182–595, passa a 218–714;
- `TORQUE_SPLIT` 1,0 nos dois estágios (tração dianteira; o Cobalt, o Golf GTI e o Punto do jogo já usam esse valor);
- fabricante Ford no `FE.MWPS`. Preço e Blacklist continuam os do Cobalt, para o carro seguir disponível no início da carreira.

O `GLOBAL/attributes.bin` do jogo não é substituído. Só o MWPS do Mod Loader altera o slot.

## Instalação

É necessário o **NFSMW Mod Loader** (o `CAR.INI` pede `modloader=0.2`). O executável vanilla não lê a pasta `ADDONS`.

1. Feche o jogo. Com ele aberto a pasta `ADDONS` fica travada, o `robocopy` falha, e um teste seguinte ainda mostra a versão anterior.
2. Faça backup de `CARS/<slot>` e `ADDONS/CARS_REPLACE/<slot>`. O `instalar.bat` não cria backup.
3. Extraia o ZIP. Ele abre numa pasta com o nome do arquivo, e `instalar.bat` fica ao lado de `CARS` e `ADDONS`. Execute o script **dentro dessa pasta**.
4. O script procura o Most Wanted no registro, em caminhos comuns e nas bibliotecas da Steam. Se não achar, varre os discos fixos por `speed.exe` com uma pasta `CARS` ao lado. Confirme o caminho antes de aceitar. A Black Edition serve.
5. Abra o jogo pelo Mod Loader. Para ter os dois Fusion, rode o instalador de cada ZIP.
6. Confira com `certutil -hashfile GEOMETRY.BIN SHA256` e compare com a tabela acima, nas duas pastas do slot.

O logo `27-FORD_HD.BIN` troca o emblema da Ford na seleção para todos os Ford, não só para estes dois. Para desinstalar, restaure o backup do passo 2 e apague esse arquivo se quiser o logo original de volta.

Se a cópia falhar no meio, feche o jogo, espere a trava soltar e rode de novo. Instalar só em `CARS` deixa o Mod Loader com a geometria antiga.

## História

O pedido inicial, em [docs/historico/demanda-inicial.md](docs/historico/demanda-inicial.md), era transplantar a geometria nova em cima de um carro que já funcionava no MW, em vez de ensinar o formato do zero. O doador de estrutura é o Fusion 2010 de Marcelo Castro (AJM3899), no slot `MUSTANGGT`. A carroceria nova vem dos drawables do Fusion no GTA V.

| Quando | O que ficou |
| --- | --- |
| 19–23/09 | Tentativas v1 (catálogo AJM), v2 (Mustang Shelby) e v3 (reconstrução). A v2 duplicava retrovisor; a v3 escurecia o capô ao inverter faces sem recalcular normais. A base escolhida foi o backup **vprime** de 20/09 |
| 24/09 | **V1prime-a–d.** Grade devolvida ao ficar opaca em DXT1. Aprovada no jogo: vidros, rodas, cromados, grade, faróis |
| 24–25/09 | **V1prime-e–z10**, um item por vez: UV de vinil, aerofólio, brake light, antena tubarão, emblemas FUSION / TITANIUM, entrada de ar do teto, 17 capôs, camada de fundo na coluna C, roda de 20 raios em aro 18, kits, vidro de uma camada, dirigibilidade, logo, nitro nas saídas, suavidade e o lábio do para-choque |
| 26/09 | **Fusion 2012.** Luzes do `oracle_hi.yft` enxertadas na z10, slot `COBALTSS`. Logo, tampa, grade inferior, lanternas, faróis de milha, freios, kits com cinta, antena reta, KIT04/KIT05 |
| 27/09 | **v2.0**, os dois carros. Em seguida a **v2.1**, só as placas. A geometria da z10 do 2018 foi a origem do port para o Underground 2 |
| 27/09 | **v2.2**: chapa preta atrás da grade (2012 e 2018), cinta preta mais larga e, no 2012, a lataria em volta dos faróis refeita por projeção numa superfície lisa (candidato 57, `hl59.py`) |
| 27/09 | **v2.3**: no 2012, o para-choque sobe até a borda de baixo dos faróis e uma chapa na cor da pintura fecha a fresta por baixo (`hl59.py` com `LIFT`, `curtain.py`) |
| 27/09 | **v2.4**: cinco cintas diferentes nos kits KIT01–KIT05 (dianteira e traseira), KIT03 restaurado |
| 27/09 | **v2.5**: o texto da cinta laranja passou de 一路顺风 para 読めば尺八. A geometria continua a da v2.4 |
| 27/09 | **v2.6**: lente clara nos faróis do 2018, uma chapa por vidro com UV 0–1 sem espelho e capô sem as cópias do verso (`scripts/lente-vidros-capo/`) |
| 01/10 | **v2.7**: refletores traseiros do 2012 em vermelho sólido, lanternas do 2018 sem reflexo excessivo e lentes dos retrovisores inteiras |
| 06/10 | **v2.8**: faces duplicadas na mesma posição removidas de todas as peças e LODs dos dois carros (`scripts/faces-duplicadas/`) |

Checkpoints do 2018 e o commit de cada um estão em [versions/LEIA-ME.md](versions/LEIA-ME.md).

## Geometria e reconstrução

Os dois carros compartilham a lataria do Titanium 2018. O 2012 só troca faróis, lanternas e faróis de milha. A malha do 2018 foi montada primeiro, no slot `MUSTANGGT`.

### Fusion Titanium 2018

O doador de estrutura é o Fusion 2010 de AJM3899: 64 sólidos, marcadores, shaders e o catálogo que o Mustang GT já aceitava. A carroceria nova vem dos drawables do Fusion no GTA V (`main`, `fusion_exh_2`, `fusion_rfst`, `fusion_rollcage`). Azul é a lataria; vermelho, as rodas; amarelo e verde, as luzes.

| Catálogo do doador, Fusion 2010 | Carroceria nova, por peça |
| --- | --- |
| ![Peças do Fusion 2010 usado como estrutura](docs/imagens-projeto/01-diagnostico-do-modelo/0923-2105-ajm_parts.png) | ![Peças do Fusion 2018 lidas do GTA](docs/imagens-projeto/00-renders-iniciais/06-lateral-pecas-por-cor.png) |

| Frente do mesmo modelo | Traseira, cada peça numa cor | Capô aberto, rodas em vermelho |
| --- | --- | --- |
| ![Frente do modelo de origem, por peça](docs/imagens-projeto/00-renders-iniciais/08-perspectiva-frente-pecas-por-cor.png) | ![Traseira do GTA, por peça](docs/imagens-projeto/00-renders-iniciais/07-perspectiva-traseira-pecas-por-cor.png) | ![Lateral com o capô aberto](docs/imagens-projeto/00-renders-iniciais/05-lateral-capo-aberto.png) |

| Frente pintada | O que passava de 65.535 índices, em vermelho |
| --- | --- |
| ![Frente pintada do modelo de origem](docs/imagens-projeto/00-renders-iniciais/02-frente.png) | ![Trechos da vprime acima do limite de índices](versions/v1prime/preview/vprime-index-over-65535-red.png) |

**v2 e v3.** A v2, no catálogo Shelby, desenhava um segundo par de retrovisores. A v3a invertia faces sem recalcular as normais, e o capô ficava escuro. Um triângulo da reconstrução saía do teto. As luzes da v2 estavam num sólido que já passava de 65.535 índices: amarelo e ciano são faróis e lanternas.

| Capô escuro na v3a | Triângulo fora da carroceria |
| --- | --- |
| ![v3a com faces invertidas, frente e traseira](docs/imagens-projeto/01-diagnostico-do-modelo/0923-2118-v3a_flipped.png) | ![Triângulo espetado saindo do teto](docs/imagens-projeto/01-diagnostico-do-modelo/0923-2114-spike.png) |

![Faróis e lanternas da v2 em oito vistas](docs/imagens-projeto/01-diagnostico-do-modelo/0923-2110-v2_lamps.png)

**Grade ainda em DXT3.** A folha `MISC` não gravava profundidade. No jogo o miolo sumia e o interior aparecia no lugar das barras. A malha da grade é a colmeia; no atlas, o branco é a região que cada textura cobre.

| Na garagem | Malha da grade | Cobertura das texturas |
| --- | --- | --- |
| ![Grade vazia, com o interior à mostra](docs/imagens-projeto/02-lanternas-grade-e-normais/0923-2128-enviada-pelo-usuario-4389fc22.jpg) | ![Textura da colmeia](docs/imagens-projeto/02-lanternas-grade-e-normais/0923-2130-grille_tex.png) | ![Atlas com a cobertura em branco](docs/imagens-projeto/02-lanternas-grade-e-normais/0923-2132-occ.png) |

A primeira compilação está descrita em [versions/vprime/README.md](versions/vprime/README.md): extração do RPF, alinhamento no Blender (`scripts/build_scene.py`), `mwgc` para o `GEOMETRY.BIN`, transplante dos sólidos e marcadores de `donor/fusion-ajm3899`, TPK com `mwtc`. O BIN da v2.1 é a cadeia de patches seguinte, da vprime até a z10, um por variante em `versions/v1prime/variants/`.

**UV da pintura.** A UV do GTA mapeava cada porta sozinha. `vinyluv.py` + `ApplyUV.cs` gravaram `u = 0,169·x + 0,5` só nos `KIT00_BODY_A–E`.

![Grade de teste na UV da V1prime-e](versions/v1prime/preview/vinyl-uv-v1prime-e.png)

O quadriculado amarelo é o mesmo teste na malha inteira. Em cima, a UV do GTA, cada painel no seu mapa. Embaixo, as linhas seguem de uma porta à outra. No jogo a faixa quebrava nessa coluna.

| UV na carroceria | Faixa quebrada na garagem |
| --- | --- |
| ![UV do GTA em cima e a UV contínua embaixo](docs/imagens-projeto/04-adesivos-nas-portas/0923-2245-vinyl_uv_cmp.png) | ![Faixa interrompida entre as portas](docs/imagens-projeto/05-aerofolio-e-brake-light/0924-2234-enviada-pelo-usuario-08c54d2c.jpg) |

| Roda do doador e a roda lida do `fusion_hi.yft` | Normais da pele, antes e depois |
| --- | --- |
| ![Cinco raios do doador em cima, vinte raios do Fusion embaixo](versions/v1prime/variants/v1prime-v-gta-wheel/v1prime-v-roda.png) | ![Reflexo facetado na z0 e a pele suavizada na z6](versions/v1prime/variants/v1prime-z4-smooth-kits/suavidade-antes-depois.png) |

A roda de 20 raios entra no lugar da roda do Fusion 2010. O `fusion_hi.yft` chega partido em sólidos (calota, leque de raios, aro, pneu). O diâmetro acompanha aro 18 e perfil 40, que é o que a loja do MW oferece.

| Sólidos da roda do GTA | Doador de cinco raios e a roda de vinte, em várias vistas |
| --- | --- |
| ![Roda separada nos sólidos W1 a W8](docs/imagens-projeto/10-rodas-gta/0925-0021-wparts.png) | ![Cinco raios em cima, vinte raios no meio e embaixo](docs/imagens-projeto/10-rodas-gta/0925-0023-wheel_cmp.jpg) |

A suavidade veio de recalcular as normais na vizinhança, e de uma camada pintada 4 mm sob a pele, que tampa a fresta da coluna C e das junções. Na cobertura, verde é camada nova, azul é fundo que já existia, roxo e vermelho são o que ainda ficava aberto. O reflexo listrado exagera a normal: a z0 ainda mostra a faceta de cada triângulo; a z2 já acompanha o painel.

| Camada de fundo sob a pele | Lábio do para-choque, z9 em cima e z10 embaixo |
| --- | --- |
| ![Cobertura da camada pintada por baixo da lataria](versions/v1prime/variants/v1prime-z5-backing-details/camada-de-fundo-cobertura.png) | ![Para-choque inferior antes e depois da superfície única](versions/v1prime/variants/v1prime-z10-front-lip/parachoque-inferior-z9-z10.png) |

Os 17 capôs da loja são o capô do Fusion com o detalhe de cada `STYLE` do GTO, separados da carroceria em `KIT00_HOOD` e `STYLExx_HOOD`. Os emblemas FUSION e TITANIUM foram traçados das artes oficiais, em cromado, com 2,5 mm de relevo, no lugar das letras que vieram do GTA. Cada janela ficou com uma camada `WINDSHIELD` e a textura de vidro correspondente, para o insulfilme da loja pegar.

![Amostra dos capôs da loja sobre o capô do Fusion](versions/v1prime/variants/v1prime-s-hoods/v1prime-s-capos.png)

A malha do capô, isolada. Na borda do `STYLE07`, a fileira de cima é o capô padrão, a do meio é a V1prime-r (a borda entortava) e a de baixo é a V1prime-s, já alinhada ao padrão.

| Capô em malha de arame | Borda do STYLE07, antes e depois |
| --- | --- |
| ![Capô visto de cima e de lado](docs/imagens-projeto/08-entradas-de-ar-e-capo/0924-2345-hood.png) | ![Padrão, V1prime-r e V1prime-s na borda do capô](docs/imagens-projeto/08-entradas-de-ar-e-capo/0924-2354-hoodedge.png) |

Pontos de montagem gravados nessa malha, e herdados pelo 2012: aerofólio em x −2,150 / z 0,868, brake light central em x −1,170 / z 1,172, entrada de ar do teto em x 0,300 / z 1,207 (inclinação 6,5°), nitro no centro das saídas do para-choque. O doador não tinha o ponto `ROOF_SCOOP`.

O acervo inteiro, em ordem de trabalho, está em [docs/imagens-projeto/](docs/imagens-projeto/README.md). Cada pasta é uma etapa. O que segue é o diagnóstico de cada uma, com a captura que fecha o passo.

**Grade e normais.** O mapa de peças separa barras, anel e painel. O teste de cores sólidas mostra qual sólido o jogo desenha quando a profundidade não é gravada. O render listrado exagera a normal errada da v3, corrigida na v3b.

| Peças da grade | Cores sólidas nas barras | Normais da v3b |
| --- | --- | --- |
| ![Barras, anel e painel da grade em cores separadas](docs/imagens-projeto/03-v1prime-placas-grade-e-pecas/0923-2159-vp_grille_parts.png) | ![Barras pintadas de amarelo, vermelho e azul](docs/imagens-projeto/03-v1prime-placas-grade-e-pecas/0923-2216-partcmp.png) | ![Normais recalculadas na carroceria da v3b](docs/imagens-projeto/02-lanternas-grade-e-normais/0923-2135-v3b_normals.png) |

**Adesivo entre as portas.** A faixa de teste quebra na coluna B com a UV do GTA e segue reta depois da V1prime-g. Em cima, a UV antiga; embaixo, a contínua.

![Faixa de teste na lateral, antes e depois da UV](docs/imagens-projeto/04-adesivos-nas-portas/0924-2227-cmp.png)

**Aerofólio, brake light e antena.** O ponto `SPOILER` herdado do Mustang flutuava 8 cm acima da tampa. A antena tubarão (196 × 96 × 61 mm) entrou no grupo da pintura, no lugar da antena de para-raios.

| Pontos do aerofólio e do brake light | Antena tubarão no teto |
| --- | --- |
| ![Marcadores vermelhos na tampa e no vidro traseiro](docs/imagens-projeto/05-aerofolio-e-brake-light/0924-2238-sp3.png) | ![Antena em várias vistas, já no grupo da pintura](docs/imagens-projeto/06-antena-tubarao/0924-2303-fin3.png) |

**Emblemas.** As letras do GTA saíram. FUSION e TITANIUM foram traçados da arte oficial e extrudados 2,5 mm em cromado.

| Contorno usado no relevo | Letras na tampa |
| --- | --- |
| ![Máscaras de FUSION e TITANIUM](docs/imagens-projeto/07-emblemas-fusion-titanium/0924-2318-masks.png) | ![Emblemas 3D ao lado da placa NEWZERA](docs/imagens-projeto/07-emblemas-fusion-titanium/0924-2320-emb3.png) |

**Traseira e coluna C.** A tampa facetada foi suavizada antes de fechar o vão. No close, a esquerda é a pele em azul e a direita é a malha da mesma coluna. A camada pintada por baixo fecha o vão.

| Tampa, antes e depois | Coluna C, pele e o vão | Fresta fechada |
| --- | --- | --- |
| ![Tampa suavizada em cima e a facetada embaixo](docs/imagens-projeto/09-traseira-e-coluna-c/0924-2359-rear_cmp.png) | ![Coluna C em azul e a malha do vão](docs/imagens-projeto/09-traseira-e-coluna-c/0925-0008-cpillar.png) | ![Coluna C antes e depois da camada de fundo](docs/imagens-projeto/09-traseira-e-coluna-c/0925-0012-backing_cmp.png) |

![Traseira facetada à esquerda e a pele suavizada à direita](docs/imagens-projeto/comparacoes/traseira-antes-depois.png)

**Vidros e o logo da tampa.** Cada janela tinha duas camadas, e a cópia escondia o interior. Ficou uma camada `WINDSHIELD` por janela, com a textura de vidro daquela posição, para o insulfilme da loja pegar. O logo `FUSION` da z3 ficou menor, com margem nas laterais, para a palavra caber na tampa.

| As duas camadas, separadas | Cada janela com a textura da sua posição |
| --- | --- |
| ![Vidros duplicados, grupo 0 e grupo 1](docs/imagens-projeto/11-vidros-e-logotipo/0925-0038-glass_layers.png) | ![Para-brisa, laterais e vidro traseiro em cores diferentes](docs/imagens-projeto/11-vidros-e-logotipo/0925-0040-glass_new.png) |

![Logo FUSION da z3, com margem dos dois lados](docs/imagens-projeto/11-vidros-e-logotipo/0925-0105-logo-previa-z3.png)

**Nitro.** Os pontos `LEFT_EXHAUST` e `RIGHT_EXHAUST` (vermelho) estavam fora das saídas. Os novos (amarelo) ficam no centro de cada ponteira.

![Planta do para-choque com os pontos de nitro antigos e novos](docs/imagens-projeto/12-chama-do-nitro/0925-0107-nitro.png)

**Reflexo, bordas abertas e frestas.** A z0 ainda lê cada triângulo. A z2 acompanha o painel. As linhas vermelhas são as bordas da malha que ficaram abertas. No teste de profundidade o fundo vermelho marca abertura; na cobertura, verde é camada nova, azul é fundo que já existia, roxo e vermelho são o que ainda ficava aberto.

| Reflexo da z0 | Reflexo da z2 |
| --- | --- |
| ![Lateral facetada, antes da suavização](docs/imagens-projeto/13-suavidade-e-kits/0925-0119-z0.png) | ![A mesma lateral depois da suavização](docs/imagens-projeto/13-suavidade-e-kits/0925-0119-z2.png) |

| Bordas abertas da malha | Onde a camada de fundo cobre a pele |
| --- | --- |
| ![Contorno vermelho das arestas sem vizinho](docs/imagens-projeto/13-suavidade-e-kits/0925-0120-cracks.png) | ![Verde, azul, roxo e vermelho na traseira](docs/imagens-projeto/14-frestas-e-refino/0925-0148-cat.png) |

**Frestas e vão do capô.** Com a carroceria branca e o resto preto, o que aparece no fundo é buraco. No vão do capô, branco é lataria ou capô; a fenda preta é o que o jogo mostrava escuro. Azul, no close do vão, é a peça escura da base.

| Fundo vermelho nas aberturas da z5 | Carroceria branca, fundo azul onde não há pele | Vão entre capô e grade |
| --- | --- | --- |
| ![Pele da z5 sobre fundo vermelho](docs/imagens-projeto/14-frestas-e-refino/0925-0148-gap5.png) | ![Teste de fresta com a pele isolada](docs/imagens-projeto/14-frestas-e-refino/0925-0149-thru5.png) | ![Capô e carroceria em branco, o restante em preto](docs/imagens-projeto/16-ajustes-pos-teste-z6/0925-0908-hoodgap.png) |

| Porta, antes e depois | Peça escura no vão do capô |
| --- | --- |
| ![Fresta da porta em cima e a lateral fechada embaixo](docs/imagens-projeto/comparacoes/frestas-lateral-antes-depois.png) | ![Azul da base entre o capô e a grade](docs/imagens-projeto/17-para-lamas-e-vao-do-capo/0925-0939-hoodfront.png) |

**Adesivos da loja e kits.** As peças `DECAL_*` trazidas do GTO cobrem porta, números e as faixas do para-brisa e do vidro traseiro. Os kits da z6 ainda eram saias e lábios; na v2.1 viraram a carroceria de fábrica com a cinta de reboque.

| Espaços de adesivo, cada um numa cor | Os três kits lado a lado |
| --- | --- |
| ![Porta, números e faixas de vidro mapeados na malha](docs/imagens-projeto/15-refino-final-camera-adesivos-kits/0925-0216-decals.png) | ![KIT00, Street e Race na mesma vista](docs/imagens-projeto/15-refino-final-camera-adesivos-kits/0925-0219-kits.jpg) |

**Para-lama do motorista.** Os dois lados da z6, com o reflexo listrado: o amassado estava no lado do motorista (`KIT00_DRIVER`, +Y). A z8 espelhou a pele boa do passageiro e fechou o vão do capô. A z6 também levou a subdivisão curva da pele.

| Os dois para-lamas da z6 | z7 à esquerda, z8 à direita |
| --- | --- |
| ![Para-lama do motorista e o do passageiro](docs/imagens-projeto/17-para-lamas-e-vao-do-capo/0925-0936-sides.jpg) | ![Para-lama do motorista, z7 à esquerda e z8 à direita](docs/imagens-projeto/comparacoes/para-lama-motorista-z7-z8.png) |

![Pele da z6 nos dois lados, depois da subdivisão](docs/imagens-projeto/15-refino-final-camera-adesivos-kits/0925-0210-r7.jpg)

**Kits encostados no para-choque e o emblema Ford.** Na z6 as saias ainda flutuavam. Na z7 o lábio, a saia e o difusor encostam na lataria. O emblema da grade ficou com letras e aro em cromado e o fundo preto.

| Kits soltos e kits encostados | Emblema Ford |
| --- | --- |
| ![Frente e traseira, antes em cima e depois embaixo](docs/imagens-projeto/16-ajustes-pos-teste-z6/0925-0910-kits2.png) | ![Letras e aro cromados no fundo preto](docs/imagens-projeto/comparacoes/emblema-ford.png) |

**Lábio inferior.** As marcas pretas debaixo do para-choque eram triângulos grandes dobrados, visíveis com a lataria branca e o resto preto. O perfil da malha original mostra a dobra; a luz de cima, como no jogo, desenha a ondulação na faixa clara. Os cortes em vários Y são o lábio antes da superfície única da z9.

| Lataria branca, o resto preto | Perfil dos triângulos dobrados |
| --- | --- |
| ![Para-choque inferior em várias vistas](docs/imagens-projeto/18-parachoque-inferior/0925-0958-lower.png) | ![Vista de frente e perfil do lábio original](docs/imagens-projeto/18-parachoque-inferior/0925-1000-lipgeo_orig.png) |

| Luz de cima, no lábio | Cortes do lábio antes da z9 |
| --- | --- |
| ![Faixa clara ondulada sob o para-choque](docs/imagens-projeto/18-parachoque-inferior/0925-0959-gl_cmp.png) | ![Seções de y = 0 a y = 0,83](docs/imagens-projeto/comparacoes/secoes-antes-z9.png) |

### Fusion 2012

As luzes do 2012 saem do Mondeo (`source/fusion-2016-dev`, `oracle_hi.yft`) por um leitor RSC7 próprio (`versions/fusion2012-fwd/scripts/yftp.py`), sem o Windows. O alinhamento é afim, pelas rodas, e depois um ICP contra `KIT00_BODY_A` + o capô (erro mediano 1,2 cm), com um deslocamento local por lâmpada.

| Peça extraída e o furo na lataria | Encaixe colorido ao lado do modelo de origem |
| --- | --- |
| ![Seleção das luzes 2012](versions/fusion2012-fwd/preview/selecao-luzes-2016.png) | ![Comparação do enxerto com o GTA](versions/fusion2012-fwd/preview/comparacao-2018-x-2016-gta.png) |

A pele do 2018 é recortada no contorno da lente (subdivisão só onde a borda cruza o triângulo, corte linear). Uma aba de cerca de 2 cm da pintura do 2012, 2 mm para fora da pele do 2018, cobre a emenda. O atlas das luzes junta o que foi mantido do 2018, as folhas `fari` e `redglass` do Mondeo, e células de cor sólida para anel vermelho e miolo branco.

![Atlas das luzes do Fusion 2012](versions/fusion2012-fwd/preview/atlas-luzes.png)

Cada item abaixo foi conferido num render com descarte de faces e fundo magenta, e depois no jogo. As prévias comparam o passo anterior (em cima, ou à esquerda) com o seguinte.

| Faróis girados 1,5° em torno da lente | Lanternas levadas até a borda da lataria |
| --- | --- |
| ![Farol do 2012 antes e depois do giro](versions/fusion2012-fwd/preview/farois-item37c.png) | ![Lanterna lateral antes e depois do cisalhamento](versions/fusion2012-fwd/preview/lanternas-item39b.png) |

| Grade inferior, terminando antes dos faróis de milha | Tampa reta no lugar da aba do friso cromado |
| --- | --- |
| ![Para-choque com a grade trapezoidal e o nicho do farol de milha](versions/fusion2012-fwd/preview/grade-inferior-item1.png) | ![Tampa do porta-malas antes e depois de alinhar a aba](versions/fusion2012-fwd/preview/tampa-item7.png) |

| Farol de milha redondo, sem a perninha | Discos e pinças do GTO no lugar da textura de multimídia |
| --- | --- |
| ![Farol de milha avançado e com o aro no plano da moldura](versions/fusion2012-fwd/preview/farol-milha-item30.png) | ![Freio dianteiro com disco e pinça próprios](versions/fusion2012-fwd/preview/freios-item33.png) |

| Cinta de reboque no para-choque dos kits | Antena com a traseira reta, sem o V da base |
| --- | --- |
| ![Cintas preta e vermelha na carroceria de fábrica](versions/fusion2012-fwd/preview/cinta-reboque-item35.png) | ![Base da antena fechada coluna a coluna](versions/fusion2012-fwd/preview/antena-item36b.png) |

| Normais da frente e da traseira do 2012 | O mesmo passe no 2018 |
| --- | --- |
| ![Reflexo do 2012 antes e depois de corrigir os cantos escuros](versions/fusion2012-fwd/preview/refino-item41-2012.png) | ![Reflexo do 2018 antes e depois das mesmas normais](versions/fusion2012-fwd/preview/refino-item41-2018.png) |

As capturas anotadas pelo jogo (farol, lanterna, lábio, antena) e o restante das prévias estão em [docs/imagens-projeto/19-fusion2012-e-refino/](docs/imagens-projeto/19-fusion2012-e-refino/). O relato de cada item está em [docs/APRENDIZADOS.md](docs/APRENDIZADOS.md).

A prévia offline, antes de instalar. O render não reproduz o reflexo do jogo; serve para ver peça faltando, face virada e fresta.

| Prévia do 2012 | LODs e o kit 01 |
| --- | --- |
| ![Prévia offline do Fusion 2012](versions/fusion2012-fwd/preview/fusion2012-previa.png) | ![LODs da carroceria e o kit com cinta](versions/fusion2012-fwd/preview/lods-e-kit01.png) |

Ordem usada na nuvem para refazer o 2012, detalhada na seção 9 de [docs/CONTINUACAO.md](docs/CONTINUACAO.md):

```
yftp.py oracle_hi.yft oracle_hi.pkl
# sopa de triângulos, align.py, mondeo_lamps.py, fogsel.py
# Dump da geometria z10 e validador das texturas
run12.sh          # graft.py + build12.py + AddParts2.cs + SetMount.cs
Retarget2.cs      # hashes MUSTANGGT -> COBALTSS
perf12.py         # ATTRIBUTES.MWPS
```

`AddParts2.cs` regrava peças e preserva os pontos de montagem. Sem mudança, a ida e volta é idêntica byte a byte, então um ajuste de normal ou de UV pode ser um patch pequeno em cima do BIN já aprovado. O validador (`scripts/validator`) confere estrutura, formato de textura (`31545844` = DXT1, `33545844` = DXT3) e o limite de índices. No Windows local o Python é `work/venv/Scripts/python.exe`, com `PYTHONPATH` em `work`, `versions/fusion2012-fwd/scripts` e `versions/v3-fusion-ajm3899/scripts`.

## Limites conhecidos

A v2.8 está publicada e foi aprovada no jogo com Xbox 360 Stuff e texturas, sem faces duplicadas. A v2.6 corrigiu faróis, vidros e capô. Nela a lente do 2018, os vidros e o capô foram corrigidos sobre a v2.5 (cinta laranja 読めば尺八). A v2.4 foi aprovada na garagem, na cidade e nas cenas que usam KIT04/KIT05, com os faróis do 2012 encaixados na lataria e no para-choque e a chapa preta atrás da grade.

- O 2018 se chama AWD na garagem e anda com tração traseira.
- O logo Ford HD vale para todos os Ford.
- Não há câmera interna neste jogo: a vista "de dentro" é a câmera do capô ou a do para-brisa.
- Alguns riscos finos na lateral traseira são costura da malha de origem.
- Cerca de 800 pares no 2018 e 1.500 no 2012 eram chapas finas vistas dos dois lados (partes do interior, da grade e do pneu). Ficou uma face só: com mods ela aparece dos dois lados; no jogo sem mods, só de um.

## Onde continuar

| Caminho | Conteúdo |
| --- | --- |
| [docs/CONTINUACAO.md](docs/CONTINUACAO.md) | Estado instalado, hashes e como retomar o teste dos faróis |
| [docs/TODO.md](docs/TODO.md) | Itens 1–53, com o que foi aprovado no jogo |
| [docs/APRENDIZADOS.md](docs/APRENDIZADOS.md) | Diagnósticos, com imagem |
| [docs/imagens-projeto/](docs/imagens-projeto/README.md) | Renders e capturas anotadas, por etapa |
| [capturas/](capturas/README.md) | Galeria no jogo |
| [versions/](versions/LEIA-ME.md) | vprime, V1prime, performance e o 2012 |
| [release/LEIA-ME.md](release/LEIA-ME.md) | Texto que vai para quem só baixa o ZIP |

`source/` e `donor/` guardam os modelos de origem e o carro-base. `scripts/`, `tools/`, `blender/` e `work/` são a bancada de build. Os comandos antigos em `scripts/` não reconstroem a v2.1 sozinhos; para continuar, comece por [docs/CONTINUACAO.md](docs/CONTINUACAO.md).

## Créditos

Modelo 2018 no GTA V: AND1V79, com conversão e texturas disponibilizadas por Gabriel Lima. Faróis, lanternas e faróis de milha do 2012: Ford Mondeo Saloon de Humster3D, portado ao GTA V por BritishGamer88. Base no Most Wanted (Fusion 2010): Marcelo Castro (AJM3899), com peças de FOX, Porsche4ever e AJ Lethal. Conversão para o MW 2005: Nillander Alarcão. A parte de cada agente oficial está em [Contribuidores](#contribuidores). Os textos de cada pacote estão em `CREDITOS/` dentro do ZIP.

## Contribuidores

A conversão é de Nillander Alarcão. Três agentes oficiais entraram em etapas diferentes. No git, o Claude Code assina `Claude Opus 5.5 <noreply@anthropic.com>` e o Cursor assina `Cursor <cursoragent@cursor.com>`. O ChatGPT entrou como agente Codex (`Codex <noreply@openai.com>`); os commits dessa etapa estão no histórico sem trailer de coautor.

| Agente | O que ficou neste repositório |
| --- | --- |
| **Claude Code** | A partir da V3, um defeito por vez, medido na malha: grade opaca em DXT1, limite de 65.535 índices, kits que a IA e o Razor pedem, UV de vinil contínua, Fusion 2012 no slot `COBALTSS`, releases v2.0 e v2.1. O encaixe dos faróis do 2012 na lataria continua em teste local, fora dos ZIPs. |
| **ChatGPT** | O começo: transplantar a carroceria nova para um carro doador que já abre no jogo. O plano está em [docs/historico/demanda-inicial.md](docs/historico/demanda-inicial.md); a release v0.1 seguiu esse fluxo. |
| **Cursor** | Em 20/09, slot, grade 3D e cromado das tentativas v1 e v2. Em 24/09, a UV reta das portas na V1prime. Em 27/09, a documentação reunida numa estrutura só. O port aprovado no Underground 2 está no repositório [Ford-Fusion-Titanium-NFSU2](https://github.com/nillander/Ford-Fusion-Titanium-NFSU2). |
