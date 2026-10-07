# Atualização prioritária — v2.9 AWD (07/10/2026)

O usuário pediu corrigir o único defeito do 2018 (RWD indevido), instalar no jogo,
fazer commit e publicar tag/release/remoto. A v2.9 muda só quatro valores de
ATTRIBUTES.MWPS: TORQUE_SPLIT 0,5 e diferencial central 0,75, na base e melhorado.
Patch instalado em ADDONS/CARS_REPLACE/MUSTANGGT, hash
8C472EAF2E606560419E9C1B65DBFFD41483E84A5F9B0DB7B3CDD9BF22CB5831.
Backup local: work/zipbuild/v2.9-before/installed-ATTRIBUTES.MWPS.
Demais parâmetros, visual e preço MW (42.000) preservados; 2012 ZIP intacto.

Fonte atual: versions/performance/fusion-awd/ATTRIBUTES.MWPS.
Script: scripts/release_awd_v2_9.py; relatório docs/awd-v2.9-verification.json.
Validação de pacote/offsets concluída. Teste de dirigibilidade ainda pendente.
Remoto atual: git@github.com:nillander/Ford-Fusion-Titanium-MW2005.git.
Preservar releases/tags anteriores, conforme a publicação da v2.8.
Os estados e instruções de versões anteriores abaixo são históricos.

---

# Continuação — Ford Fusion Titanium 2012 FWD e Fusion Titanium 2018 AWD (NFS Most Wanted 2005)

Documento único para retomar o trabalho. Atualizado em 27/09/2026. Substitui os antigos `CONTINUACAO-CODEX.md`
(2018, V1prime) e `CONTINUACAO-FUSION2012.md`. Leia também `docs/APRENDIZADOS.md` (lições, com imagens),
`docs/TODO.md` (itens 1–52) e `versions/fusion2012-fwd/LEIA-ME.md`.

**Comece pela seção 3: a v2.8 foi publicada e todos os itens (1–53) estão fechados.** As seções 4 em diante registram a
construção e os testes antigos; números de versão e caminhos de nuvem nelas são históricos, não o estado instalado.

## 1. O projeto
- **Fusion 2018 AWD** no slot `MUSTANGGT` (Ford Mustang GT) e **Fusion Titanium 2012 FWD** no slot `COBALTSS` (Cobalt SS,
  carro inicial). O 2012 é o 2018 com faróis, lanternas e faróis de milha do modelo 2012 (Mondeo 2016 do GTA V,
  de Humster3D, portado por BritishGamer88).
- Branch `main`, tag única `v2.4`; remoto `git@github.com:nillander/nfsmw-ford-fusion-titanium.git`
  (SSH). O usuário quer **uma única tag e uma única release**, sempre da última versão. Não publicar o teste
  atual dos faróis sem pedido/aprovação. Commits, quando solicitados, como `Nillander Alarcão <nillander@live.com>`.
- Release **v2.4**: `release/Fusion2012_FWD_MW2005.zip` e `release/Fusion2018_AWD_MW2005.zip`.
  Cada ZIP abre na pasta com seu nome e inclui `instalar.bat`, `ADDONS`, `CARS`, `CREDITOS`, `LEIA-ME.md` e
  `SHA256SUMS.txt`. Notas em `release/NOTAS-v2.4.md` (cinco cintas nos kits; faróis e para-choque do 2012; chapa da grade).

## 2. Como trabalhar com o usuário
- Responder em **pt-BR**. **Um item por vez**; ao terminar, instalar no jogo e **parar para ele testar**.
- **Jogo aberto**: não instalar quando ele disser que está jogando; deixar o pacote em `work/c2012-stage/pacote-*/`.
- Instalar sempre nas duas pastas de cada carro (`CARS/<SLOT>` e `ADDONS/CARS_REPLACE/<SLOT>`) e conferir SHA-256.
- **Commit só quando ele pedir/aprovar**; zips só quando tudo estiver aprovado.
- Arquivos > 20 MB: dividir em partes de 15 MB na nuvem, gravar com `device_commit_files` e juntar com `cat` no PC.
- Git no PC: `git add` pode travar — usar `hash-object -w` / `update-index --cacheinfo` / `write-tree` /
  `commit-tree` / `update-ref`, com as linhas `Co-Authored-By`/`Claude-Session` no fim da mensagem.

## 3. Estado atual em 06/10/2026 — v2.8 publicada

Instalado no jogo = geometria da v2.8 nos dois carros (a da v2.7 ficou em `work/dup53/MUSTANGGT.BIN` e `COBALTSS.BIN`).
O `TEXTURES.BIN` do 2012 instalado (`477A7001…`) é de um teste posterior à v2.7 e não entrou na release.

| Carro | GEOMETRY.BIN | TEXTURES.BIN (release) | ZIP |
| --- | --- | --- | --- |
| 2012 (COBALTSS) | `46EA905703DC3BADAA92236FCCA8DD0BE65BFBAA95DC65B9D807DC427F4115C3` | `380AEF7826723967DB0E3CD49284387A4469E75938D767EC437CEC9A8670A5B7` | `FAF2EC7BBF3AF4CDF169CB9086163FDA8AE855D2C3C4916E162546DB4531987D` |
| 2018 (MUSTANGGT) | `C6506D3FA563EC05926315CCC994DE5DC3150DC281F460139BCEE2C16B706F01` | `8DF768ED4BCB4BF933FC4F686FDDF1B13FA203BCB21A656986132008A617F8EF` | `D786292C56092EEFAC98E4CAB19E1A7D16A1B15A4B9D367D5B6C76A1F9D51E71` |

- **v2.8 (item 53)**, sobre a v2.7: faces duplicadas na mesma posição removidas de todas as peças e LODs
  (`scripts/faces-duplicadas/`, ver o LEIA-ME da pasta). Aprovado pelo usuário no jogo com os mods.
- Publicação: o GitHub não aceita push desta sessão; o commit e a tag são feitos no PC e o usuário roda
  `work/publicar-v2.8.bat` (push, tag e release nova, mantendo as anteriores).

## 3.b Estado da v2.6 (histórico)

Instalado no jogo = conteúdo dos ZIPs da v2.6 (pacote `work/pacote-27-09-capo62/`; a v2.5 que estava instalada ficou em
`work/pacote-27-09-vidros61/backup-antes/`). Jogo em `D:\Program Files (x86)\Electronic Arts\Need For Speed Most Wanted Black Edition`.

| Carro | GEOMETRY.BIN | TEXTURES.BIN | ZIP |
| --- | --- | --- | --- |
| 2012 (COBALTSS) | `2C8C625C2EF57F43F53E04093688D229AA008FBFAE5EB7FE106518FD12683AEE` | `380AEF7826723967DB0E3CD49284387A4469E75938D767EC437CEC9A8670A5B7` | `13F015B8036A945ADA169673340ADD0050CC63BEEE95A74681D60207C74E7CBB` |
| 2018 (MUSTANGGT) | `7D95E28E9A44307C90047CED1D1433BF607C61599505286572B636C14A0D5350` | `8DF768ED4BCB4BF933FC4F686FDDF1B13FA203BCB21A656986132008A617F8EF` | `6C76C445CE3B5590635DFC53701AD4F221CCED4DA8E834204040F83318A3110B` |

- **v2.6 (itens 50–52)**, sobre a v2.5, com os scripts de `scripts/lente-vidros-capo/` (leem e editam os BIN no lugar,
  em Python; ver o LEIA-ME da pasta): lente clara nos faróis do 2018 (`lente50.py`), uma chapa por vidro com UV 0–1
  sem espelho (`vidros51.py`, `aplica51.py`) e capô sem as cópias do verso (`capo52.py`). Aprovado pelo usuário no
  jogo com Xbox 360 Stuff e texturas.
- O usuário testa com mods (Xbox 360 Stuff, texturas, ReShade), que desenham o verso das faces e mostram UV e cor de
  lente que o jogo original ignora. Antes de concluir um item, procurar faces opostas coincidentes (`dupscan.py`).
- Pendências possíveis com mods: faces duplicadas no interior, na grade (`RIGHT_SIDE_MIRROR`), no pneu dianteiro e nas
  paredes das entradas de ar dos capôs da loja.

## 3.a Estado da v2.4 (histórico)

Instalado no jogo = conteúdo dos ZIPs da v2.4 (pacote `work/c2012-stage/pacote-27-09o-cintas5/`, montagem dos ZIPs
em `work/zipbuild/v2.4-pacotes/`):

| Carro | GEOMETRY.BIN | TEXTURES.BIN | ZIP |
| --- | --- | --- | --- |
| 2012 (COBALTSS) | `643E5E4A7DEFC67E82FF3FFDF381C2F5BC0E854EB7201369EC64E9C36F075583` | `26E9ADDEAA435A98AB5CE8D6CCEE9C695B49A03147C892B0DB8842412E954A6E` | `4E499260D8B8C326EF0B3E7B5AF9B8EA80A21C76FCEEC02CE5DC28DD8C3359F0` |
| 2018 (MUSTANGGT) | `4E950229DC116F8ACF3D79C1F2EDD5CFE93E68042D6FA6A1CC76EE09B9671C4E` | `F7C6C9F386CB1E8A347ACD704D235F59A6D45AA7FDF1AD5657279C9F0F69B648` | `B2C307C8479CF1B84E8A73B7B948C82EA1EC22A43ED294B01B2473E43EE32667` |

- **Cintas (item 48, v2.4)**: `kits48.py` monta KIT01–KIT05 a partir do `KIT00_BODY` (todos os LODs) com a cinta
  do kit na dianteira (y −0,33, z 0,148 → −0,03, só na parte preta) e na traseira (y +0,405, z 0,215 → 0,015);
  KIT03 recebe os decalques do KIT01. `tex48.py` grava as cinco texturas (64×256) no atlas das cintas: 2012
  `KIT00_HEADLIGHT_OFF` x 512–831 / y 768; 2018 `LOGO` x 768–1023 / y 0 e x 768 / y 256. Entrada: v2.3
  (2012 `12F99EE6…`, 2018 `EDDE6EE9…`).
- **Faróis do 2012 (candidato 57, `versions/fusion2012-fwd/scripts/hl59.py`)**: em vez de novos remendos, a pintura
  das carrocerias numa faixa de até 7,5 cm da lente é **projetada** numa superfície lisa. Parametrização radial a
  partir de um ponto dentro do carro (`hl58maps.py`: (s,t) = 0,7·(azimute, elevação), altura = raio; acompanha a
  quina frente→lado→capô, o que o plano da lente não fazia perto da grade). Superfície = lataria antiga filtrada
  (mediana 5×5 + gaussiana 1,5 cm, sem a lente), fora do capô (dilatação 1 célula) e da grade (5 células).
  Vértices a até 7 cm abaixo / 8 cm acima são movidos, com transição de 12 células (3,6 cm) na borda da faixa e
  normais do campo liso; mesma topologia, portanto sem costura nem vértices novos na carroceria. Pele de fundo
  1,5 mm abaixo em `BASE_A–E` tapa buracos. Parâmetros: `WIN_IN=0.07 WIN_OUT=0.08 CAP=0 RW=0 EXCL=5 EXH=1
  R=0.075 BLEND=12 SIG=0.015`. Entrada: `pacote-27-09k-farois56-grade/2012/GEOMETRY.BIN` (56 + chapa).
  Lições: recortar e costurar malha nova (hl57) deixava serrilhado; a superfície "continuação da lataria de fora"
  (extrapolação biharmônica) criava calombos onde a lataria real tem abas; subir a pele até a borda da lente criava
  um colar — o farol fica 1–3 cm saliente embaixo e a faixa escura da carcaça continua visível (item 46).
- **Chapa da grade** (`plate_grille.py` + `gmap.py`): grupo preto em `BASE_A–E`, x = 2,296 − 0,304·y², 12 mm atrás
  das barras.
- **Cinta preta** (`strap_wide.py`): KIT01/KIT05 30 % mais larga (6,5 cm).
- **Para-choque sob os faróis (item 46, v2.3)**: `hl59.py` com `LIFT=0.05 LOFF=0.0005 LENSIN=5 LSIG=0.006 BKIN=1`
  sobre `pacote-27-09k-farois56-grade` (mesmos demais parâmetros): abaixo da borda inferior da lente a superfície sobe
  até 0,5 mm dela (rampa de 4,5 cm, afinando nas pontas), e a superfície e a pele de fundo passam 5 células por baixo
  da borda da lente. `curtain.py`: piso inclinado na cor da pintura (pele de fundo de `BASE_A–E`) de 3 mm atrás da
  borda da lente até 7 cm para dentro e 6 cm para baixo, que fecha a visão do interior. Depois, `strap_wide.py`.
  Folga lente–lataria (`gapmeas.py`): de 20–50 mm para 1–9 mm.

## 3.0 Histórico do teste dos faróis antes da v2.2


Os itens 1–42 foram encerrados na v2.0. Depois, a v2.1 corrigiu as placas **dianteiras e traseiras dos dois
carros**: removeu a antiga moldura preta 3D texturizada, que flutuava atrás da placa; a borda preta com cantos
arredondados agora pertence à própria placa. **Preservar** a faixa azul Mercosul e a bandeira do Brasil. O texto
“Mercosul” na moldura descartada não era necessário. Depois de corrigir os ZIPs para conter a pasta-raiz de cada
carro e `instalar.bat`, a v2.1 foi publicada. Hashes dos ZIPs locais: 2012
`6D8631DE5E16E20892DB24457E730842F1BCCE2CF558B66E7F899740E4ECD2AD`; 2018
`AC372B2D4B81F724977B08B3D1683CFE69ADC19D653599D21C3031CAC079A4A5`.

**Trabalho ainda aberto:** encaixe dos faróis dianteiros do Fusion **2012** na lataria (capô, paralamas e
para-choque). As capturas do usuário estão preservadas em `docs/imagens-projeto/19-fusion2012-e-refino/usuario/`,
com nomes `teste-27-09-v21--*` e `teste-27-09-c55--*`. Vermelho e amarelo são anotações do usuário, não partes
da textura do carro. Distinção espacial essencial: a seção **laranja é a ponta externa/traseira**, junto ao
paralama; a **branca é a ponta interna/dianteira**, junto à grade. O usuário disse que o farol na ponta branca
já encaixa; ali há um **buraco triangular escuro** e saliências na **lataria**, não motivo para mover a luz inteira.
Também há um volume irregular acima da seção laranja. Em capturas anteriores, a seção laranja encaixava menos,
mas a última rodada marcou apenas os pontos restantes.

O **candidato 56 dos faróis**, ainda **não aprovado visualmente**, está instalado **com a chapa da grade** do
item 43, que foi aprovada separadamente no jogo. Estado verificado nas duas rotas de cada slot:

| Rota relativa ao jogo | Arquivo |
| --- | --- |
| `CARS/COBALTSS/GEOMETRY.BIN` e `ADDONS/CARS_REPLACE/COBALTSS/GEOMETRY.BIN` | SHA-256 `3872FCE73D04BE73AB2AF75FC72E332C1EDDE560C28080B5202D90F286340413` |
| `CARS/MUSTANGGT/GEOMETRY.BIN` e `ADDONS/CARS_REPLACE/MUSTANGGT/GEOMETRY.BIN` | SHA-256 `89700BC74AEAD99139AAE94DF44FF1F4B513AA3A0FCE0F4064B19ECD41ACCDCC` (chapa aprovada) |

Jogo em `D:\Program Files (x86)\Electronic Arts\Need For Speed Most Wanted Black Edition`;
repositório em `C:\Users\nillander\NoDocuments\fusion-mw2005`. Pacote instalado no 2012:
`work/c2012-stage/pacote-27-09k-farois56-grade/2012/GEOMETRY.BIN`. O 56 puro, **sem chapa**, permanece em
`work/c2012-stage/headlight56-full.BIN` (SHA-256
`41711104EE4C9BF76A1C71CE5F5F5AB9FBBD87F78D9D44D5CD8456EFD78BB73E`);
o candidato 55 anterior era `2ECEC047386FBF07E70F0B920EB9C024FD94C874E8051B0A7E010898C1254F30`.
As texturas não foram alteradas nesta rodada. A chapa da grade fica no `BASE_A–E`, enquanto os ajustes dos
faróis ficam no `BODY`/`HOOD`; por isso foram combinados sem deslocar as luzes. O BIN combinado tem 193 peças
e 1.437.081 triângulos. Não confundir a aprovação da chapa com a aprovação dos faróis.

**O que mudou no 56:** a partir do `headlight55-base-full.dump`, `work/hl54.py` com perfil `last-points`
ampliou a suavização topológica da pele pintada sobre a seção laranja e junto à ponta branca;
`work/hl49.py` suavizou as normais; `work/hl56_patch.py` criou uma cobertura pintada **só na região
interna e inferior** (`inner-lower` em `work/hl46.py`), evitando refazer a faixa larga que havia criado um calombo.
São 112 vértices adicionais no `KIT00_BODY_A`; o maior `BODY_A` está em 64.908 de 65.535 vértices.
O validador independente leu o BIN: **193 peças, 1.426.695 triângulos**.
Prévia `work/c2012-stage/headlight56-full-side.png`; mapa de lacunas `headlight56-gap.png`.
O render offline apresenta magenta por texturas incompletas e não reproduz os reflexos do jogo; julgar pelos
prints no jogo. O mapa de lacunas é uma aproximação no plano da lente, não prova de que todo pixel magenta é
um buraco visível.

**Próximo passo:** receber o teste/prints do usuário para os faróis do candidato 56 combinado. Não afirmar que o encaixe está perfeito
sem essa verificação. Se persistir algum ponto, mexer apenas na região indicada, preparar novo BIN, validar,
verificar que `speed.exe` está fechado, fazer backup e instalar **nas duas rotas** com conferência SHA-256. Parar
para o usuário testar. **Não fazer commit, push, tag ou release da geometria pendente** até pedido/aprovação.
O repositório tem muitos arquivos modificados/não rastreados de trabalho anterior; não limpar nem incluir
indiscriminadamente. Em `docs/TODO.md`, os itens 1–42 são históricos/fechados; a chapa do 43 teve aprovação
visual, e os faróis do 44 ainda aguardam teste/aprovação.

### 3.1 Capturas para comparar e reprodução técnica

| Captura preservada em `docs/imagens-projeto/19-fusion2012-e-refino/usuario/` | Leitura |
| --- | --- |
| `teste-27-09-v21--farol-marcado-esquerdo.png` e `--farol-marcado-direito.png` | Deformações extensas iniciais em volta das duas luzes. |
| `teste-27-09-v21--encaixe-seta-laranja-1.png` e `--encaixe-seta-laranja-2.png` | Pior encaixe original junto à ponta externa laranja. |
| `teste-27-09-v21--calombo-ponta-branca.png` e `--saliencias-amarelas.png` | Calombo interno e saliências superiores/inferiores; não deslocar a ponta branca. |
| `teste-27-09-c55--buraco-triangular-interno.png` | Vão escuro na ponta branca junto à grade, após o candidato 55. |
| `teste-27-09-c55--saliencias-externa-interna.png` | Os últimos volumes irregulares marcados em amarelo. |

Arquivos de construção em `work/c2012-stage/`:

1. `headlight55-base-full.{BIN,dump}`: base já com cobertura da região **externa** e avanço local de 3 mm
   da ponta externa da luz (`work/hl46.py`), sem mover a ponta branca.
2. `headlight56-fair.spec` / `.BIN` / `.dump`: `work/hl54.py` no perfil `last-points`, aplicado a BODY de
   KIT00/01/02/04/05, LODs A–E.
3. `headlight56-norm.spec` / `.BIN` / `.dump`: `work/hl49.py`, normais de BODY e HOOD.
4. `headlight56-full.spec` / `.BIN` / `.dump`: `work/hl56_patch.py`, pequena cobertura interna inferior.
   `work/hl46.py` fornece `bridge(..., region='inner-lower')`; a máscara só considera a fração interna
   `<0,21` da largura da lente e a metade inferior do plano. Não alterar o modo `outer` ao refinar isso.

No Windows local, definir `PYTHONPATH` como
`work;versions\fusion2012-fwd\scripts;versions\v3-fusion-ajm3899\scripts` e usar
`work/venv/Scripts/python.exe`. Cada `.spec` é aplicado ao BIN da etapa anterior com:

```powershell
pwsh -NoProfile -File work/run_mw_local.ps1 -Source versions/fusion2012-fwd/scripts/AddParts2.cs <entrada.BIN> <patch.spec> <saida.BIN>
pwsh -NoProfile -File work/run_mw_local.ps1 -Source versions/v3-fusion-ajm3899/scripts/Dump.cs <saida.BIN> <saida.dump>
& 'C:\Program Files\dotnet\dotnet.exe' scripts/validator/bin/Release/net8.0/Validator.dll <saida.BIN> <validacao.json>
```

Não usar `dotnet` sem caminho: nesta máquina ele encontra primeiro o runtime x86 sem .NET 8. Revalidar sempre
o limite de 65.535 vértices por peça. `work/render_headlight.py` e `work/librast.so` produzem a prévia sob WSL;
`versions/fusion2012-fwd/scripts/hlgap.py` produz o mapa de lacunas. Os testes intermediários `hl47.py`,
`hl48.py`, `hl52.py` e `hl53.py` produziram sulcos escuros ou expuseram buracos ao empurrar/apagar a pele;
não tomá-los como base. A cobertura interna larga do 46 gerou calombo, motivo do recorte pequeno no 56.

## 4. Cadeia de geometria (nuvem, `/home/claude/c12/build`)
- **2012**: `36_12` → `hl37.py 1.10 1.10 0.010 sym` → `lid38.py` → `fin39.py` → `tail39.py` → `hl40.py 1.5 0.12`
  (= `40`, zip v2.0) → `nfix.py` (frente/traseira) → `teeth.py` → `hltrim.py 0.008` (= `41h`, pacote-27-09) →
  `nfix.py` com `XF=-99 XR=-99 PRUNE=prune12h.npy` → `hlvis.py` → `hlfill.py` (= `42f`, pacote-27-09b).
- **2018**: `36_18` → `fin39.py` (= `39_18`, zip v2.0) → `nfix.py` (= `41a18`) → `nfix.py` corpo todo → `lip42.py`
  (`SKIN=9A8AAD9E`) (= `42b18`).
- Scripts em `versions/fusion2012-fwd/scripts/` (copiar para `/home/claude/c12`). Visibilidade externa (`vis.py`) é
  gravada em `build/vis<TAG>.pkl` e depende da ordem das faces do dump de entrada: recalcular a cada novo dump.
- Pipeline de gravação: `python3 x.py in.dump spec.bin …` → `pwsh $S/mw.ps1 AddParts2.cs in.bin spec.bin out.bin` →
  `pwsh $S/mw.ps1 $S/Dump.cs out.bin out.dump` → `pwsh $S/val.ps1 out.bin v.json` (`S=/home/claude/v3/versions/v3-fusion-ajm3899/scripts`).
- **Limite de 65.535 vértices** por sólido: o `BODY_A` do 2012 está em ~64.400 (depois de apagar ~4.900 faces
  escondidas). Qualquer correção que crie vértices no 2012 precisa liberar espaço antes (`prune41.py`).

## 5. Ferramentas de conferência
- `pgr.py` (render em perspectiva com normais de vértice e brilho — mostra marcas escuras como no jogo),
  `persp.py` (perspectiva texturizada), `rtc.py` (ortográfico com corte de faces), `partview.py` (peças por cor),
  `gapview.py` (lente branca, carcaça laranja: frestas), `pick.py` (qual peça/face está num pixel), `slash.py`
  (riscos finos), `outl.py` (faces com normal fora da vizinhança), `hledge.py`/`tailtb.py`/`slice39.py` (medidas de
  encaixe por fatia), `darkfind.py`, `nrmstat*.py`.
- Imagens do usuário e prévias: `versions/fusion2012-fwd/reference/` e `preview/`; cópia organizada em
  `docs/imagens-projeto/19-fusion2012-e-refino/`.

## 6. Mapas úteis
- Pele: 2012 `0xB637F71F`, 2018 `0x9A8AAD9E`. Lente do farol 2012 `EE1FD517`, carcaça `C195B264`.
- `KIT00_RIGHT_SIDE_MIRROR_A` guarda a grade e peças pretas da frente (não é o retrovisor).
- 2018: só existem as peças `RIGHT_HEADLIGHT*`/`RIGHT_BRAKELIGHT*` (cobrem os dois lados).
- Pontos de montagem (BASE): luzes, escapamentos, `SPOILER` C93B73FD, `ROOF_SCOOP` 90C81258; não há ponto de câmera.

## 7. Como a geometria 2012 foi feita (resumo técnico)
1. **Leitura do YFT sem Windows** (`yftp.py`): RSC7 descomprimido (zlib raw), FRAG→DRFR (0x30), shaders (MATS 0x10),
   esqueleto (SKEL 0x20/0x5E), modelos high (0x50), geometrias MESH (VB 0x18, IB 0x38). Tipos de vértice no `yft.py` da
   pasta `v1prime-v-gta-wheel`. Vértices skinned já estão no espaço do objeto; osso por triângulo = maioria.
   Shaders do `oracle_hi.yft`: 0 pintura, 4 "gum" (casca preta duplicada da carroceria!), 9 cromado detail2, 10/14 `fari`
   (lâmpadas), 15 vidro claro (lentes E janelas), 16 `redglass` (lente vermelha). Texturas: `DEV Version/FordFusion/*.PNG`.
2. **Alinhamento** GTA→MW: `x = y·sx + tx`, `y = −x`, `z = z + 0,42`, com `sx` pelas rodas; depois ICP afim global
   contra `KIT00_BODY_A`+`HOOD_A` (mediana 1,2 cm) e translação local por lâmpada.
3. **Seleção das luzes** (`mondeo_lamps.py`): pegada 2D da lente (`footprint.py`) + ilhas conectadas por shader
   (`islands.py`) com ≥85 % da área dentro; faróis de milha por visibilidade + componente sem pintura (`fogsel.py`).
   Tirados: vidros da janela traseira (z ≥ 0,82), "gum" colado à lente (< 8 mm) e vidro claro duplicado sob a lente vermelha.
4. **Remoção do 2018** (`lamps2018.py`, `graft.py:z_extra_mask`): lâmpadas nas peças de luz (mantidos brake light central,
   refletores do para-choque, luzes do painel), interiores em BASE/RIGHT_SIDE_MIRROR, **faixa cromada** (BASE g2,
   x < −2,18, z 0,68–0,74), aletas/molduras das lanternas e o LED do farol de milha 2018.
5. **Enxerto** (`graft.py:compute_graft4`): lâmpada 2012 em translação rígida (farol de milha avançado 7,7 cm em x);
   aba de pintura 2012 de ~2 cm grudada na pele 2018 (+2 mm) e buracos do 2018 preenchidos com a pele 2012.
6. **Recorte da pele 2018** (`partmesh.py:clip_tris`): função distância com sinal da pegada, subdivisão adaptativa só
   onde a borda cruza e corte linear (marching triangles); vértices soldados na gravação. Aplicado a KIT00/01/02 BODY A–E
   e, no farol de milha, também a BASE/RIGHT_SIDE_MIRROR.
7. **Texturas**: `COBALTSS_KIT00_HEADLIGHT_OFF` DXT1 (interiores opacos) e `..._BRAKELIGHT_OFF` DXT3 (lentes).
   Atlas 1024: Q0 atlas 2018 (peças mantidas), Q1 `fari`, Q2 `redglass` (vermelho ×1,75), Q3 células sólidas.
   **UVs recuadas 0,4 % das bordas** (UV 0 ou 1 dava volta para outro quadrante → lente preta).
8. **Peças**: `KIT00_LEFT/RIGHT_{HEADLIGHT,HEADLIGHT_GLASS,BRAKELIGHT,BRAKELIGHT_GLASS}_A–D`, LODs por agrupamento de vértices.
   `AddParts2.cs` = AddParts que **preserva os mount points** ao substituir BASE.
9. **Pontos de luz** (`SetMount.cs`): HEADLIGHT 9DB90133/D09091C6 → (1,99, ∓0,692, 0,567); BRAKELIGHT 7A5B2F25/7ADF7EF8 →
   (−2,13, ±0,67, 0,72); BF700A79/31A66786 → (−2,245, ±0,49, 0,714).
10. **Slot** (`Retarget2.cs` + `build/texmap.txt`): sólidos `MUSTANGGT_*`→`COBALTSS_*` (bin-hash do nome) e hashes de
    textura MUSTANGGT_X→COBALTSS_X. Texturas com nome `_OFF`: `<CARRO>_KIT00_HEADLIGHT_OFF`/`_BRAKELIGHT_OFF`.

## 8. Performance (`perf12.py`)
- Aplica o `ATTRIBUTES.MWPS` aprovado do 2018 sobre os nós mustanggt e copia para cobaltss / cobaltss_top os blocos
  inteiros de chassis, tires, brakes; do ecar os campos do MWPS 2018; do pvehicle MASS, TENSOR_SCALE e HandlingRating.
- **Arrays VLT têm cabeçalho de 8 bytes** (capacidade u16, contagem u16, tamanho do elemento u16, pad). TORQUE começa em
  +8 (o `report_engine` antigo lia a partir de +0; os dois primeiros "valores" eram o cabeçalho). HandlingRating: dados em ponteiro+8.
- Torque ×1,2: 85–180 → 102–216 (top 182–595 → 218–714). `TORQUE_SPLIT` (transmission +112) = 1,0 = FWD
  (MW suporta: Cobalt, Golf GTI e Punto já são 1,0; Audi/Lamborghini 0,5).
- `FE.MWPS`: fabricante no nó frontend cobaltss (0xA3B8 + 0x40 = 0xA3F8) = 2 (Ford; Cobalt era 19). Preço 26000 e
  Blacklist 16 mantidos. O `GLOBAL/attributes.bin` do jogo **não** foi alterado (só o MWPS do Mod Loader).

## 9. Reconstruir na nuvem (container é efêmero)
1. Enviar para a nuvem (`device_stage_files`): `work/c2012-stage/scripts.tgz` (ferramentas antigas; refazer com
   `tar czf` de `tools/mwgc/*.cs tools/mwtc/*.cs versions/v3-fusion-ajm3899/scripts versions/v1prime/scripts
   versions/v1prime/variants/*/scripts scripts/*.cs scripts/*.py scripts/validator reference/*.json`),
   `release/Fusion2018_AWD_MW2005.zip` (z10), `source/fusion-2016-dev/Model/Ford Mondeo Saloon/oracle_hi.yft`,
   `DEV Version/FordFusion/{fari.PNG,redglass.png}`, `CARS/COBALTSS/{GEOMETRY,TEXTURES}.BIN` do backup vanilla,
   `GLOBAL/attributes.bin` e `GLOBAL/FE_ATTRIB.bin`.
2. `scripts/setup_cloud.sh` (PowerShell 7 do GitHub — apt e dot.net são bloqueados — e mwtc sem System.Drawing), depois
   aplicar `mwtc-Compiler.cs` (corte do nome em 23 caracteres) em `/home/claude/c12/mwtc/Compiler.cs` e `TpkCore.cs`.
3. Copiar `versions/fusion2012-fwd/scripts/*` para `/home/claude/c12` (os `.py` de `lib` e `gta` estão todos lá; os
   caminhos no código são `/home/claude/c12`, `/home/claude/c12/lib`, `/home/claude/c12/gta`, `/home/claude/v3`).
   Descompactar o zip da z10 em `/home/claude/c12/z10`; compilar `rast.c`: `gcc -O3 -shared -fPIC -o librast.so rast.c`.
4. Ordem: `yftp.py oracle_hi.yft oracle_hi.pkl` → soup (`gtamesh.soup` → `oracle_soup.pkl`) → `align.py` →
   `mondeo_islands.py` → `mondeo_lamps.py` → `fogsel.py` → `mvis.py` → `zvis.py` → Dump da z10 (`z10.dump`) e
   validator nas texturas (`z10tex/`) → `run12.sh` → TPK (`build/tpk/textures.txt` + `mwtc.ps1`) → `Retarget2.cs` →
   `perf12.py`.

## 10. Lições da construção do 2012
- Nome de textura > 23 caracteres no mwtc original **corrompe o TPK** (e provavelmente fechou o jogo).
- O hash dentro do `SECONDARYLOGO.BIN` (offsets 0xD4 e 0x108) tem de ser `bStringHash("SECONDARY_LOGO_<INTERNAL>_1")` — regra do Mod Loader (seção 4.6).
- A malha "gum" do GTA é uma segunda casca preta de toda a carroceria: excluir o que estiver a < 4 mm da pintura.
- Recortar a pele com triângulos grandes deixa dentes; subdividir só onde a borda cruza e cortar linearmente.
- UV exatamente em 0/1 dá volta para o outro lado do atlas; recuar as UVs dentro de cada quadrante.

## Anexo A — O que deu errado no 1º teste e o que foi corrigido
### A.1 Travamento ao selecionar (causa provável, corrigida)
O `mwtc` original grava o nome da textura num campo fixo de 24 bytes com `PadRight`, **sem cortar** nomes maiores.
`COBALTSS_KIT00_HEADLIGHT_OFF` (28) e `COBALTSS_KIT00_BRAKELIGHT_OFF` (29) estouraram o campo e deslocaram o resto da
estrutura da textura (hash, formato, tamanho…). O validador ainda lia, mas o jogo recebia lixo nas duas texturas de
luzes. Correção: `WriteString` corta o nome em 23 caracteres (+ NUL), como fazia a porta usada na z10
(`versions/fusion2012-fwd/scripts/mwtc-Compiler.cs`). Conferido: fora nome/hash/offset, a estrutura agora é igual à
do TPK da z10. **Regra: nomes de textura com mais de 23 caracteres são truncados; o hash usa o nome completo.**

### A.2 "Temp 350" no nome/logo (corrigido, a confirmar)
"Temp 350" é o que o jogo mostra quando não acha a textura do logo (já visto na V1prime-z). O `SECONDARYLOGO.BIN`
tinha sido copiado do Mustang com o hash `DEA6DBC0`, **igual ao do Mustang instalado** → dois logos com o mesmo hash.
Agora o do Cobalt usa `A3782D31` = bin-hash de `SECONDARY_LOGO_COBALTSS`, que é o nome que o jogo procura
(tabela de `FRONTEND/FrontB.lzc`: `SECONDARY_LOGO_<CARRO>`; string `SECONDARY_LOGO_%s` no `speed.exe`).
Os hashes `DEA6DBC0` (Mustang) e `6F4044F1` (Supra/NASCAR) não correspondem a `SECONDARY_LOGO_<carro>`; se o logo
continuar "Temp 350", o Mod Loader (`d3d9.dll`, usa `CARNAME_%s_%s`) deve remapear de outro jeito — investigar
testando um hash único qualquer ou o original do Cobalt.

### A.4 Logo do Cobalt no 2º teste (corrigido, a confirmar)
Com o hash `A3782D31` (`SECONDARY_LOGO_COBALTSS`) o jogo mostrou o logo **original do Cobalt**: a textura do jogo com
esse hash (FrontB.lzc) ganha da nossa. Conclusão: o Mod Loader usa o hash que estiver dentro do `SECONDARYLOGO.BIN`
como logo do carro, e esse hash tem de ser **único** — nem igual ao de outro carro do Mod Loader (1º teste: `DEA6DBC0`
igual ao do Mustang → "Temp 350"), nem igual a uma textura do jogo. Os logos do Mustang (`DEA6DBC0`) e do Supra
(`6F4044F1`) seguem essa regra. Agora: `A1CE36B0` = bin-hash de `SECONDARY_LOGO_FUSION2012FWD`, ausente de
FrontB.lzc, FRONTA.BUN, GLOBALB.BUN e dos outros SECONDARYLOGO.

### A.5 Jogo fechando ao abrir (3º teste) e o logo pelo FRONTEND
- Com `SECONDARYLOGO.BIN` de hash `A1CE36B0` o jogo passou a fechar antes do menu (sem dump novo em
  `%LOCALAPPDATA%\CrashDumps`; os `SPEED2.EXE*.dmp` de lá são do NFS Underground 2, não do MW). Revertido para a versão
  do 2º teste (`A3782D31`), com a qual o jogo abria. Cópia da versão que quebrou: `work/c2012-stage/logo/SECONDARYLOGO_A1CE36B0_quebrou.BIN`.
- Como o jogo acha o logo (disassembly): `speed.exe` 0x591292 monta `SECONDARY_LOGO_%s` e procura pelo bStringHash
  (maiúsculas) → para o Cobalt, `A3782D31`. O Mod Loader (`d3d9.dll` 0x10002b44) só carrega o `SECONDARYLOGO.BIN` como
  pacote extra; não remapeia nada. Se o hash já existe no jogo, vale a textura do jogo.
- Esta instalação usa um FRONTEND HD: `FRONTEND/FRONTA.BUN` tem `SECONDARY_LOGO_COBALTSS` em 1024×256 DXT3 (é o que aparece)
  e `FrontB.lzc` em 256×64. **Solução aplicada:** troquei só os pixels desses dois logos pelo FUSION (mesmo tamanho e
  formato, cabeçalhos intactos). FRONTA.BUN: offset 0x3A4F700 (dados 0x15280 + MemoryOffset 0x3A3A480), 262.144 bytes;
  FrontB.lzc: 16.384 bytes (mesmos pixels do logo FUSION 256×64 do 2018). Backups em `_backup_FRONTEND_pre-fusion2012/`.
  Prévia: `versions/fusion2012-fwd/preview/logo-fusion-hd.png`. Isso não vai no zip (FRONTA.BUN é o FRONTEND HD do usuário).
- Se o jogo **continuar fechando ao abrir** com o logo revertido, a causa não é o logo: testar a versão vanilla do
  Cobalt (mover `ADDONS/CARS_REPLACE/COBALTSS` para fora e restaurar `CARS/COBALTSS` de `_backup_COBALTSS_vanilla`), depois
  o diagnóstico da seção 5.

### A.6 Regra definitiva do logo (resolvida por disassembly do d3d9.dll)
O Mod Loader intercepta `speed.exe` 0x591292 (`SECONDARY_LOGO_%s`): se o carro tem `SECONDARYLOGO.BIN` e o
`internal=` do CAR.INI bate com o nome do carro, troca o nome por `%s_1` → o jogo procura **`SECONDARY_LOGO_<internal>_1`**
(bStringHash em maiúsculas). Mustang: `SECONDARY_LOGO_MUSTANGGT_1` = `DEA6DBC0`; Supra: `6F4044F1`; **Cobalt: `623849E1`**.
Qualquer outro hash → "temp350" (imagem-padrão). O hash aparece 2× no BIN (0xD4 e 0x108).
Aplicado: `SECONDARYLOGO.BIN` do 2018 (MUSTANGGT) com o hash trocado para `623849E1` nos dois lugares.
O patch no FRONTEND (4.5) foi **desfeito** (FRONTA.BUN e FrontB.lzc restaurados do backup; não é necessário).
Nome em texto: o Mod Loader responde à string `CARNAME_<manufacturer>_<internal>` com o `name=` do CAR.INI.

## Anexo A.7 Lista de correções pedidas após o 4º teste (um item por vez, avisar para testar)
Carro abriu e apareceu. Pendências (ordem: mais simples primeiro):
8. Nome/logo "temp350" → **feito (4.6), aprovado no jogo**.
7. Tampa do porta-malas: remendo da faixa cromada ruim → **feito, aprovado no jogo em 26/09** (GEOMETRY `C159D615…`;
   anterior guardada em `work/c2012-stage/pre-item7/GEOMETRY.BIN` = `2D4AF358…`). Causa: o 2018 tem, sob o vinco
   (z≈0,776), uma aba inclinada para fora/baixo até z≈0,73 onde ficava o friso, com normais para baixo e uma
   fresta aberta no vinco (buraco já existente na z10) e na base da aba. `scripts/lidfix.py` (chamado em
   `build12.py:edit_body`, todas as carrocerias/LODs): puxa a aba para o plano do 2012 (reto do vinco para baixo,
   inclinação 0,07 como no Mondeo), normais do plano, normais das fileiras de cima da tampa inferior sem a
   influência da prateleira, e duas faixas de pintura 3–4 mm atrás do plano cobrindo as frestas.
   Build rápido sem refazer enxertos: `scripts/run12b.sh` e depois `Retarget2.cs` (MUSTANGGT→COBALTSS).
6. Deformação no para-choque traseiro, canto inferior no meio → **feito, aprovado no jogo em 26/09** (GEOMETRY
   `A0F66D69…`, em `work/c2012-stage/item6/`; anterior = `item7/` `C159D615…`). Causa (já existia na z10): no vinco
   inferior do para-choque (z≈0,258, x≈−2,36), o vértice do centro (y=0, lado −y) tinha a normal da face de baixo
   (−0,29; 0; −0,96) e é usado por um triângulo de 16 cm² da face traseira → triângulo escuro parecendo amassado.
   `scripts/fix6.py`: nas carrocerias (todos os kits/LODs), região x<−2,28, |y|<0,35, z 0,22–0,36, vértices usados
   por faces traseiras (nx<−0,85) cuja normal difere >40° da média dessas faces recebem essa média. 45 normais
   (15 por kit: A, B, C). `scripts/apply6.py` grava só os 12 bytes de cada normal no BIN (tamanho igual; leitura
   independente OK, 175 peças). Patch em `work/c2012-stage/item6/item6-patch.json` (offsets sobre `C159D615…`).
   Não está em `build12.py`: num rebuild, rodar `apply6.py <bin> <dump> <saída>` depois do `Retarget2.cs`.
   Prévia: `versions/fusion2012-fwd/preview/parachoque-traseiro-item6.png`.
1. Grade preta inferior não deve ligar os dois faróis de milha (ver fotos de referência 2013) → **feito, aprovado
   no jogo em 26/09** (GEOMETRY `022AD2FB…`, em `work/c2012-stage/item1/`; anterior = `item6/` `A0F66D69…`).
   `scripts/grille1.py` (roda sobre o dump da geometria instalada e grava com `AddParts2.cs`; ida e volta do
   AddParts2 sem mudanças é byte a byte idêntica): a grade termina em |y| = 0,40 (z 0,08) → 0,46 (z 0,19), ponta
   inclinada como no 2013; triângulos pretos além disso recortados (`clip_tris`) em RIGHT_SIDE_MIRROR_A e BASE_B–E.
   O vão até o canto é fechado com pele pintada no grupo da pintura das carrocerias KIT00/01/02, LODs A–E:
   superfície ajustada (polinômio em y,z; resíduo mediano 1 mm) à lataria em volta da abertura, 3 mm para dentro,
   furo no contorno do farol de milha (moldura preta ~5 mm), parede de 4 cm na ponta da grade. Isso também fechou o
   nicho baixo antigo do 2018 sob o farol de milha (ver item 2). Vértices: KIT02_BODY_A 65.397 (limite 65.535).
   Prévia: `versions/fusion2012-fwd/preview/grade-inferior-item1.png`.
   **Teste de 26/09:** conceito aprovado (grade e farol de milha), mas o encaixe do para-choque ficou deformado:
   degrau na borda sob o farol de milha, quina externa do nicho com lascas/frestas, lábio inferior facetado.
   **Refino (GEOMETRY `6B5A6327…`, em `work/c2012-stage/item1b/`), aprovado no jogo em 26/09.** Só lataria; faróis intactos.
   - Causa do degrau: a superfície ajustada usava amostras em z 0,0805, logo acima da prateleira horizontal do
     lábio (z 0,08), e acertava a parte de trás (~10 cm atrás da borda). Agora amostra a borda do lábio em z 0,074.
   - Todo o contorno do nicho (y > 0,5, até z 0,30) é refeito com a superfície ajustada: a pele antiga ali (aba do
     enxerto 2012, paredes do nicho baixo do 2018, restos de recorte) é apagada (~3.100 triângulos no LOD A).
   - Furo = silhueta do farol de milha vista de frente, suavizada, 3 mm para fora; malha com pontos a cada 5 mm no
     contorno + grade interna, Delaunay com teste de dentro/fora em polígonos (pacote `triangle` indisponível).
   - Paredes de 3 cm no contorno do nicho e de 4 cm na ponta da grade.
   - Lábio inferior (z < 0,095): normais recalculadas pela média das faces vizinhas do mesmo lado (sombreado liso).
   - Vértices: KIT02_BODY_A 63.887. Prévia: `versions/fusion2012-fwd/preview/parachoque-farol-milha-item1b.png`.
2. Vazio abaixo dos faróis de milha no para-choque → preencher.
5. Parte interna das lanternas (tampa) com cor/camadas diferentes da parte externa.
3. Lanternas traseiras menores que o nicho → aumentar até encaixar.
4. Deformações da lataria em volta dos faróis (capô, paralama, para-choque).

### A.3 Outras hipóteses se ainda fechar
1. **Tamanho da geometria**: 38,3 MB contra 32,5 MB da z10 (+5,8 MB: luzes 2012 com ~17 mil triângulos por farol no
   LOD A, recortes nas carrocerias A–C dos 3 kits). Pode passar do limite de memória do carro. Reduzir: decimar as luzes
   (`LODCELL` em `build12.py`, ex.: A 0,0015, B 0,005, C 0,012, D 0,025) e aumentar `maxedge` do recorte.
2. **Peças `KIT00_LEFT_*` novas** (HEADLIGHT, HEADLIGHT_GLASS, BRAKELIGHT, BRAKELIGHT_GLASS, LODs A–D). O catálogo do
   2018 só tinha RIGHT. Alternativa: juntar lado esquerdo e direito nas peças RIGHT (atenção: grupo único, ≤ 65.535 vértices).
3. Maior peça com 64.543 vértices (KIT02_BODY_A), no limite; a z10 tinha no máximo 57.995.
4. `ATTRIBUTES.MWPS`: gerado por `perf12.py` (offsets dos nós cobaltss calculados pelo VLT). Para testar, remover o
   arquivo da pasta ADDONS temporariamente.
