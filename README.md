# Ford Fusion 2012 FWD e Fusion Titanium 2018 AWD — Need for Speed Most Wanted (2005)

Dois mods para o Most Wanted de PC. Instalam juntos porque usam slots diferentes. O 2012 é a carroceria aprovada do Titanium 2018 com faróis, lanternas e faróis de milha do modelo 2012 (Ford Mondeo 2016 do GTA V).

| Carro | Substitui | Slot | Tração gravada na v2.1 |
| --- | --- | --- | --- |
| Ford Fusion 2012 FWD | Chevrolet Cobalt SS (carro inicial) | `COBALTSS` | Dianteira (`TORQUE_SPLIT` 1,0) |
| Ford Fusion Titanium 2018 AWD | Ford Mustang GT | `MUSTANGGT` | Traseira (`TORQUE_SPLIT` 0). O nome na garagem é AWD |

> **Release atual: v2.1 (27/09/2026).** Ela corrige as placas dianteiras e traseiras dos dois carros: a moldura preta 3D separada foi removida, e a borda arredondada passou a fazer parte da placa. A faixa azul, a bandeira do Brasil e o texto `NEWZERA` foram mantidos. O ajuste dos faróis do 2012 e a chapa preta atrás da grade foram feitos depois desta release e **não estão nos ZIPs**. O estado do trabalho está em [docs/CONTINUACAO.md](docs/CONTINUACAO.md). O método que levou o 2018 ao Underground 2 está no repositório irmão `fusion-nfsu2`.

## No jogo

| Fusion 2012 FWD | Fusion Titanium 2018 AWD |
| --- | --- |
| ![Fusion 2012 no menu principal](capturas/2012/principal.png) | ![Fusion 2018 no menu principal](capturas/2018/principal-2.png) |
| ![Frente do 2012, com a cinta do kit](capturas/2012/Screenshot_175.png) | ![Lateral do 2018 na garagem](capturas/2018/Screenshot_170.png) |
| ![Traseira do 2012 e o logo FUSION](capturas/2012/Screenshot_172.png) | ![Traseira do 2018 com aerofólio](capturas/2018/Screenshot_168.png) |
| ![2012 na cidade](capturas/2012/Screenshot_178.png) | ![2018 em perseguição](capturas/2018/Screenshot_185.png) |

[Todas as capturas dos dois carros](capturas/README.md). São imagens feitas no jogo; algumas podem mostrar testes posteriores à v2.1. As anotações de diagnóstico (vermelho e amarelo) ficam em [docs/imagens-projeto/](docs/imagens-projeto/README.md).

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

| Pacote v2.1 | SHA-256 do ZIP | `GEOMETRY.BIN` | `TEXTURES.BIN` |
| --- | --- | --- | --- |
| [Fusion2012_FWD_MW2005.zip](release/Fusion2012_FWD_MW2005.zip) | `B47B3C372345C331DD847D022494B9B3AEEBD613B6CDC9975B64EA68A1BBE0DF` | `9021E30C13A6A7C9A6FE4305D4AB339E1EB3F529B556329634000A1B9A1B6895` | `C969CB9861DCA8F848C6A6E671F78816A72BAAA7A25B21206D07D11AA3723FFE` |
| [Fusion2018_AWD_MW2005.zip](release/Fusion2018_AWD_MW2005.zip) | `AC372B2D4B81F724977B08B3D1683CFE69ADC19D653599D21C3031CAC079A4A5` | `66B89F3051C6C933C5C52080CE3C1F983BC56CD97CA101ACF61E6CD4C699E48A` | `854CFB7754B9793D8D61367A4D6CD24C5D117106CD7D94D544657814EF7800E8` |

Os hashes de cada arquivo interno estão em [release/SHA256SUMS-conteudo.txt](release/SHA256SUMS-conteudo.txt). As notas da release estão em [release/NOTAS-v2.1.md](release/NOTAS-v2.1.md).

### Peças que o slot precisa ter

O kit de carroceria troca a lataria inteira. Um kit ausente deixa o carro sem carroceria na loja, na IA e nos carros prontos do jogo.

| Peça | Para que serve |
| --- | --- |
| `KIT00_BODY_A–E` | Carroceria de fábrica, do LOD alto ao mais baixo |
| `KIT01_BODY` e `KIT02_BODY` | Kits "Street" e "Race": a mesma lataria com uma cinta de reboque (preta com 大吉大利, vermelha com 出入平安) |
| `KIT04_BODY` e `KIT05_BODY` | Cópias com cinta. O Mustang do Razor e as cutscenes usam KIT04 ou KIT05; a cutscene `CS_CAR_14` usa o KIT04 do Cobalt |
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
| 24/09 | **V1prime-a–d.** Placa sem as letras 3D "CHAPINHA", grade devolvida ao ficar opaca em DXT1. Aprovada no jogo: vidros, rodas, cromados, grade, faróis |
| 24–25/09 | **V1prime-e–z10**, um item por vez: UV de vinil, aerofólio, brake light, antena tubarão, emblemas FUSION / TITANIUM, entrada de ar do teto, 17 capôs, camada de fundo na coluna C, roda de 20 raios em aro 18, kits, vidro de uma camada, dirigibilidade, logo, nitro nas saídas, suavidade e o lábio do para-choque |
| 26/09 | **Fusion 2012.** Luzes do `oracle_hi.yft` enxertadas na z10, slot `COBALTSS`. Logo, tampa, grade inferior, lanternas, faróis de milha, freios, kits com cinta, antena reta, KIT04/KIT05 |
| 27/09 | **v2.0**, os dois carros. Em seguida a **v2.1**, só as placas. A geometria da z10 do 2018 foi a origem do port para o Underground 2 |

Checkpoints do 2018 e o commit de cada um estão em [versions/LEIA-ME.md](versions/LEIA-ME.md).

## Geometria e reconstrução

O modelo de origem, lido do GTA e pintado por peça. Azul é a lataria; vermelho, as rodas; amarelo e verde, as luzes.

| Lateral | Frente |
| --- | --- |
| ![Peças do modelo de origem, vista lateral](docs/imagens-projeto/00-renders-iniciais/06-lateral-pecas-por-cor.png) | ![Peças do modelo de origem, vista frontal](docs/imagens-projeto/00-renders-iniciais/08-perspectiva-frente-pecas-por-cor.png) |

As luzes do 2012 saem do Mondeo (`source/fusion-2016-dev`, `oracle_hi.yft`) por um leitor RSC7 próprio (`versions/fusion2012-fwd/scripts/yftp.py`), sem o Windows. O alinhamento é afim, pelas rodas, e depois um ICP contra `KIT00_BODY_A` + o capô (erro mediano 1,2 cm), com um deslocamento local por lâmpada.

| Peça extraída e o furo na lataria | Encaixe colorido ao lado do modelo de origem |
| --- | --- |
| ![Seleção das luzes 2012](versions/fusion2012-fwd/preview/selecao-luzes-2016.png) | ![Comparação do enxerto com o GTA](versions/fusion2012-fwd/preview/comparacao-2018-x-2016-gta.png) |

A pele do 2018 é recortada no contorno da lente (subdivisão só onde a borda cruza o triângulo, corte linear). Uma aba de cerca de 2 cm da pintura do 2012, 2 mm para fora da pele do 2018, cobre a emenda. O atlas das luzes junta o que foi mantido do 2018, as folhas `fari` e `redglass` do Mondeo, e células de cor sólida para anel vermelho e miolo branco.

![Atlas das luzes do Fusion 2012](versions/fusion2012-fwd/preview/atlas-luzes.png)

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

A v2.1 está aprovada na garagem, na cidade e nas cenas que usam KIT04/KIT05.

- O encaixe final dos faróis do 2012 (lataria em volta da lente, item 44) está em teste local e fora do ZIP.
- Pela grade cromada ainda se vê o interior. Uma chapa preta atrás das barras foi aprovada no jogo depois da v2.1 e também está fora do ZIP.
- O 2018 se chama AWD na garagem e anda com tração traseira.
- O logo Ford HD vale para todos os Ford.
- Não há câmera interna neste jogo: a vista "de dentro" é a câmera do capô ou a do para-brisa.
- Alguns riscos finos na lateral traseira são costura da malha de origem.
- O modelo do Mondeo pede para não ser redistribuído sem permissão. O ZIP do 2012 é para uso pessoal.

## Onde continuar

| Caminho | Conteúdo |
| --- | --- |
| [docs/CONTINUACAO.md](docs/CONTINUACAO.md) | Estado instalado, hashes e como retomar o teste dos faróis |
| [docs/TODO.md](docs/TODO.md) | Itens 1–44, com o que foi aprovado no jogo |
| [docs/APRENDIZADOS.md](docs/APRENDIZADOS.md) | Diagnósticos, com imagem |
| [docs/imagens-projeto/](docs/imagens-projeto/README.md) | Renders e capturas anotadas, por etapa |
| [capturas/](capturas/README.md) | Galeria no jogo |
| [versions/](versions/LEIA-ME.md) | vprime, V1prime, performance e o 2012 |
| [release/LEIA-ME.md](release/LEIA-ME.md) | Texto que vai para quem só baixa o ZIP |

`source/` e `donor/` guardam os modelos de origem e o carro-base. `scripts/`, `tools/`, `blender/` e `work/` são a bancada de build. Os comandos antigos em `scripts/` não reconstroem a v2.1 sozinhos; para continuar, comece por [docs/CONTINUACAO.md](docs/CONTINUACAO.md).

## Créditos

Modelo 2018 no GTA V: AND1V79, com conversão e texturas disponibilizadas por Gabriel Lima. Faróis, lanternas e faróis de milha do 2012: Ford Mondeo Saloon de Humster3D, portado ao GTA V por BritishGamer88. Base no Most Wanted (Fusion 2010): Marcelo Castro (AJM3899), com peças de FOX, Porsche4ever e AJ Lethal. Conversão para o MW 2005: Nillander Alarcão, com Claude. Os textos de cada pacote estão em `CREDITOS/` dentro do ZIP.
