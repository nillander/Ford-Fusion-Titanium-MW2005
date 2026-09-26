# Continuação — Ford Fusion 2012 FWD (slot COBALTSS)

Documento de passagem para retomar o trabalho do Fusion 2012 FWD. Atualizado em 26/09/2026.
Leia antes: `APRENDIZADOS_FUSION_MW2005.md` (lições do 2018) e `versions/fusion2012-fwd/LEIA-ME.md` (o que foi feito).

## 1. Pedido do usuário
- Construir o **Ford Fusion 2012 FWD** reaproveitando todo o trabalho do 2018 (V1prime-z10, aprovado).
- 2012 e 2018 são o mesmo carro; mudam **só** faróis, lanternas traseiras e faróis de milha.
- Substituir o **Chevrolet Cobalt SS** (carro inicial). Fonte GTA V do 2012: `source/fusion-2016-dev`.
- Decisões do usuário durante o trabalho:
  - Farol de milha: **nicho trapezoidal do 2012 na posição do 2012**; o nicho baixo do 2018 fica fechado em preto.
  - Tampa do porta-malas **sem a faixa cromada** que liga uma lanterna à outra (removida).
  - Performance: **motor do Cobalt SS +20 % de torque + dirigibilidade do 2018 + tração dianteira (FWD)**.

## 2. Estado atual
| Item | Estado |
| --- | --- |
| Geometria 2012 (`GEOMETRY.BIN`) | Pronta, validada fora do jogo |
| Texturas (`TEXTURES.BIN`) | Refeita em 26/09 (bug do mwtc, ver seção 4) |
| Performance (`ATTRIBUTES.MWPS`, `FE.MWPS`) | Pronta |
| Instalação no jogo | Feita (CARS/COBALTSS e ADDONS/CARS_REPLACE/COBALTSS); backup do Cobalt em `_backup_COBALTSS_vanilla` |
| **Teste no jogo** | 4º teste: o carro abre. Item 8 (logo FUSION / nome) e item 7 (tampa) aprovados em 26/09. Item 6 (para-choque traseiro, GEOMETRY `A0F66D69…`) aprovado em 26/09. Próximo: item 1 |
| Git | Item 8 no commit inicial da branch. Item 7 (tampa, GEOMETRY `C159D615…`) no commit seguinte. O zip ainda tem `2D4AF358…` |

### Arquivos instalados agora (SHA-256)
| Arquivo | SHA-256 |
| --- | --- |
| GEOMETRY.BIN (CARS e ADDONS) | `A0F66D6903EDF7DC6A73836CDBED17BA4A86AF57BA1448396B2A6242F19A5F3A` (item 6, aprovado; antes do item 6 = `C159D615…` em `work/c2012-stage/item7/`; o zip ainda tem `2D4AF358…`) |
| TEXTURES.BIN (CARS e ADDONS) | `0DCF3F4984E2F07B68D5FC2C6F58111E01F86E6BC9B7029215B5C9A56C45920C` |
| ATTRIBUTES.MWPS | `744596F4A3E34A49BD83982C7D9C9294328004BAD40156B5F126A3C643C3A8D5` |
| FE.MWPS | `91B557D2B3368A09C695D104F289FD5D6C6C5AA21C03BACB43A22F5B4C7740E9` |
| CAR.INI | `A94EEB1DA890A0CECEEB3DE333AC2A6D33F2D3EF9E4D146203981DA7E5B2D867` |
| SECONDARYLOGO.BIN | `7FBFE6CAD5D86975448498C34E2DF0F3970AC4622E15C5BA1ABE67DB01D1700D` (logo do 2018, hash `623849E1` = `SECONDARY_LOGO_COBALTSS_1`) |
| Release `release/Fusion2012_FWD_MW2005.zip` | `8CE0EC32789042DC1115FEB2C4EF1D672517F267220E32167ADE57330C0745BA` |

Documentação e scripts: `versions/fusion2012-fwd/` (LEIA-ME, `scripts/`, `preview/`).
Diagnóstico pronto (não instalado): `versions/fusion2012-fwd/diag-z10-no-slot-cobalt/` (geometria 2018 no slot COBALTSS).

## 3. Próximo passo: item 1
Itens 8 (logo), 7 (tampa) e 6 (para-choque traseiro) aprovados no jogo em 26/09. Próximo: item 1 (TODO 25), grade
preta inferior que não deve ligar os dois faróis de milha. Um item por vez; avisar para testar. Lista completa em `TODO.md` (itens 24–29).

Se o jogo voltar a fechar ou a mostrar "temp350", o histórico abaixo ainda vale:
- **Ainda fecha:** instalar o diagnóstico (seção 5) para separar geometria x slot/texturas/MWPS.
- **Ainda "Temp 350" mas não fecha:** o logo — ver seção 4.6 (a regra que ficou aprovada).

## 4. O que deu errado no 1º teste e o que foi corrigido
### 4.1 Travamento ao selecionar (causa provável, corrigida)
O `mwtc` original grava o nome da textura num campo fixo de 24 bytes com `PadRight`, **sem cortar** nomes maiores.
`COBALTSS_KIT00_HEADLIGHT_OFF` (28) e `COBALTSS_KIT00_BRAKELIGHT_OFF` (29) estouraram o campo e deslocaram o resto da
estrutura da textura (hash, formato, tamanho…). O validador ainda lia, mas o jogo recebia lixo nas duas texturas de
luzes. Correção: `WriteString` corta o nome em 23 caracteres (+ NUL), como fazia a porta usada na z10
(`versions/fusion2012-fwd/scripts/mwtc-Compiler.cs`). Conferido: fora nome/hash/offset, a estrutura agora é igual à
do TPK da z10. **Regra: nomes de textura com mais de 23 caracteres são truncados; o hash usa o nome completo.**

### 4.2 "Temp 350" no nome/logo (corrigido, a confirmar)
"Temp 350" é o que o jogo mostra quando não acha a textura do logo (já visto na V1prime-z). O `SECONDARYLOGO.BIN`
tinha sido copiado do Mustang com o hash `DEA6DBC0`, **igual ao do Mustang instalado** → dois logos com o mesmo hash.
Agora o do Cobalt usa `A3782D31` = bin-hash de `SECONDARY_LOGO_COBALTSS`, que é o nome que o jogo procura
(tabela de `FRONTEND/FrontB.lzc`: `SECONDARY_LOGO_<CARRO>`; string `SECONDARY_LOGO_%s` no `speed.exe`).
Os hashes `DEA6DBC0` (Mustang) e `6F4044F1` (Supra/NASCAR) não correspondem a `SECONDARY_LOGO_<carro>`; se o logo
continuar "Temp 350", o Mod Loader (`d3d9.dll`, usa `CARNAME_%s_%s`) deve remapear de outro jeito — investigar
testando um hash único qualquer ou o original do Cobalt.

### 4.4 Logo do Cobalt no 2º teste (corrigido, a confirmar)
Com o hash `A3782D31` (`SECONDARY_LOGO_COBALTSS`) o jogo mostrou o logo **original do Cobalt**: a textura do jogo com
esse hash (FrontB.lzc) ganha da nossa. Conclusão: o Mod Loader usa o hash que estiver dentro do `SECONDARYLOGO.BIN`
como logo do carro, e esse hash tem de ser **único** — nem igual ao de outro carro do Mod Loader (1º teste: `DEA6DBC0`
igual ao do Mustang → "Temp 350"), nem igual a uma textura do jogo. Os logos do Mustang (`DEA6DBC0`) e do Supra
(`6F4044F1`) seguem essa regra. Agora: `A1CE36B0` = bin-hash de `SECONDARY_LOGO_FUSION2012FWD`, ausente de
FrontB.lzc, FRONTA.BUN, GLOBALB.BUN e dos outros SECONDARYLOGO.

### 4.5 Jogo fechando ao abrir (3º teste) e o logo pelo FRONTEND
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

### 4.6 Regra definitiva do logo (resolvida por disassembly do d3d9.dll)
O Mod Loader intercepta `speed.exe` 0x591292 (`SECONDARY_LOGO_%s`): se o carro tem `SECONDARYLOGO.BIN` e o
`internal=` do CAR.INI bate com o nome do carro, troca o nome por `%s_1` → o jogo procura **`SECONDARY_LOGO_<internal>_1`**
(bStringHash em maiúsculas). Mustang: `SECONDARY_LOGO_MUSTANGGT_1` = `DEA6DBC0`; Supra: `6F4044F1`; **Cobalt: `623849E1`**.
Qualquer outro hash → "temp350" (imagem-padrão). O hash aparece 2× no BIN (0xD4 e 0x108).
Aplicado: `SECONDARYLOGO.BIN` do 2018 (MUSTANGGT) com o hash trocado para `623849E1` nos dois lugares.
O patch no FRONTEND (4.5) foi **desfeito** (FRONTA.BUN e FrontB.lzc restaurados do backup; não é necessário).
Nome em texto: o Mod Loader responde à string `CARNAME_<manufacturer>_<internal>` com o `name=` do CAR.INI.

## 4.7 Lista de correções pedidas após o 4º teste (um item por vez, avisar para testar)
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
1. Grade preta inferior não deve ligar os dois faróis de milha (ver fotos de referência 2013).
2. Vazio abaixo dos faróis de milha no para-choque → preencher.
5. Parte interna das lanternas (tampa) com cor/camadas diferentes da parte externa.
3. Lanternas traseiras menores que o nicho → aumentar até encaixar.
4. Deformações da lataria em volta dos faróis (capô, paralama, para-choque).

### 4.3 Outras hipóteses se ainda fechar
1. **Tamanho da geometria**: 38,3 MB contra 32,5 MB da z10 (+5,8 MB: luzes 2012 com ~17 mil triângulos por farol no
   LOD A, recortes nas carrocerias A–C dos 3 kits). Pode passar do limite de memória do carro. Reduzir: decimar as luzes
   (`LODCELL` em `build12.py`, ex.: A 0,0015, B 0,005, C 0,012, D 0,025) e aumentar `maxedge` do recorte.
2. **Peças `KIT00_LEFT_*` novas** (HEADLIGHT, HEADLIGHT_GLASS, BRAKELIGHT, BRAKELIGHT_GLASS, LODs A–D). O catálogo do
   2018 só tinha RIGHT. Alternativa: juntar lado esquerdo e direito nas peças RIGHT (atenção: grupo único, ≤ 65.535 vértices).
3. Maior peça com 64.543 vértices (KIT02_BODY_A), no limite; a z10 tinha no máximo 57.995.
4. `ATTRIBUTES.MWPS`: gerado por `perf12.py` (offsets dos nós cobaltss calculados pelo VLT). Para testar, remover o
   arquivo da pasta ADDONS temporariamente.

## 5. Teste de diagnóstico (se precisar)
Copiar `versions/fusion2012-fwd/diag-z10-no-slot-cobalt/GEOMETRY.BIN` e `TEXTURES.BIN` para `CARS/COBALTSS` e
`ADDONS/CARS_REPLACE/COBALTSS` (jogo fechado). É a z10 aprovada só renomeada para COBALTSS.
Abriu → problema na geometria 2012 (seção 4.3 itens 1–3). Fechou → slot, texturas ou MWPS.
Para voltar à versão 2012: reinstalar a partir de `release/Fusion2012_FWD_MW2005.zip`.

## 6. Como a geometria 2012 foi feita (resumo técnico)
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

## 7. Performance (`perf12.py`)
- Aplica o `ATTRIBUTES.MWPS` aprovado do 2018 sobre os nós mustanggt e copia para cobaltss / cobaltss_top os blocos
  inteiros de chassis, tires, brakes; do ecar os campos do MWPS 2018; do pvehicle MASS, TENSOR_SCALE e HandlingRating.
- **Arrays VLT têm cabeçalho de 8 bytes** (capacidade u16, contagem u16, tamanho do elemento u16, pad). TORQUE começa em
  +8 (o `report_engine` antigo lia a partir de +0; os dois primeiros "valores" eram o cabeçalho). HandlingRating: dados em ponteiro+8.
- Torque ×1,2: 85–180 → 102–216 (top 182–595 → 218–714). `TORQUE_SPLIT` (transmission +112) = 1,0 = FWD
  (MW suporta: Cobalt, Golf GTI e Punto já são 1,0; Audi/Lamborghini 0,5).
- `FE.MWPS`: fabricante no nó frontend cobaltss (0xA3B8 + 0x40 = 0xA3F8) = 2 (Ford; Cobalt era 19). Preço 26000 e
  Blacklist 16 mantidos. O `GLOBAL/attributes.bin` do jogo **não** foi alterado (só o MWPS do Mod Loader).

## 8. Reconstruir na nuvem (container é efêmero)
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

## 9. Lições novas desta etapa
- Nome de textura > 23 caracteres no mwtc original **corrompe o TPK** (e provavelmente fechou o jogo).
- O hash dentro do `SECONDARYLOGO.BIN` (offsets 0xD4 e 0x108) tem de ser `bStringHash("SECONDARY_LOGO_<INTERNAL>_1")` — regra do Mod Loader (seção 4.6).
- A malha "gum" do GTA é uma segunda casca preta de toda a carroceria: excluir o que estiver a < 4 mm da pintura.
- Recortar a pele com triângulos grandes deixa dentes; subdividir só onde a borda cruza e cortar linearmente.
- UV exatamente em 0/1 dá volta para o outro lado do atlas; recuar as UVs dentro de cada quadrante.
- Créditos: o Mondeo (Humster3D / BritishGamer88) pede "não redistribuir sem permissão"; o zip é para uso pessoal.
