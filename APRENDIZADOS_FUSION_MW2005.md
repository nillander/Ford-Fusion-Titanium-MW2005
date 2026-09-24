# Aprendizados — Fusion Titanium 2018 no NFS Most Wanted 2005

Documento consolidado em 24/09/2026, depois da aprovação da **V1prime-d** no jogo ("vidros, janelas,
rodas, cromados, grade frontal, grade do escapamento, faróis, tudo").

| Item | Valor |
| --- | --- |
| Versão aprovada | `versions/v1prime/release/MUSTANGGT` |
| GEOMETRY.BIN | `C8A2D660B3A8031AA31FF9A61095F4A8A36366A520D162866B2F428E4311C5FB` |
| TEXTURES.BIN | `BF9A08426FB00AD40784558E99A179715B8FE916E58CF3A46F97673566B847D8` |
| Slot | `MUSTANGGT`, instalado em `CARS/MUSTANGGT` e em `ADDONS/CARS_REPLACE/MUSTANGGT` |
| Base | vprime (backup `fusion-mw2005.7z` de 20/09 03:10): catálogo AJM3899 com 64 sólidos e carroceria 2018 montada a partir dos drawables do GTA V |

---

## 1. O problema principal: texturas DXT3 tornavam as peças "translúcidas"

### Sintomas (todos com a mesma causa)

- grade frontal: aparecia só a borda; o miolo mostrava o motor ou o fundo;
- faróis e lanternas visíveis **através** do carro em alguns ângulos, e vice-versa;
- peças "sumindo" conforme o ângulo, sem padrão geométrico aparente.

### Causa

O MW 2005 decide como desenhar cada material pelo **formato da textura** no `TEXTURES.BIN`:

- **DXT1** (sem canal alfa): material **opaco**. O motor grava a profundidade de cada pixel
  (*z-buffer*). Uma peça que está atrás e é desenhada depois é descartada naquele pixel.
- **DXT3** (com canal alfa): material **translúcido**. O motor desenha com mistura de cores e
  **não grava profundidade**. Qualquer peça desenhada depois, mesmo estando atrás, pinta por cima.

Numa etapa anterior, as folhas `MISC`, `LOGO` e `INTERIOR` foram regravadas em **DXT3**, embora sejam
100 % opacas. No doador AJM original essas três são **DXT1**. Com isso, a grade (textura `MISC`) virou
"translúcida". O motor, o painel de fundo e o interior, desenhados depois, pintavam por cima dela.
Só sobrava visível o que não tinha nada desenhado depois atrás: a borda, o anel e o logotipo.

### A correção

Regravar `MISC`, `LOGO` e `INTERIOR` em **DXT1**, sem mexer na geometria e sem trocar shader.
Foi o que resolveu grade, cromados, grade do escapamento e a sensação de ver peças através do carro.

### Como o diagnóstico foi fechado (V1prime-c)

A grade foi pintada com cores sólidas em células livres da folha BADGING:

| Cor | Onde estava | Posição | Resultado no jogo |
| --- | --- | --- | --- |
| vermelho | barras e anel, em `RIGHT_SIDE_MIRROR_A` | na frente | só o anel apareceu |
| verde | painel de fundo, no mesmo sólido, desenhado depois | atrás das barras | cobriu as barras |
| magenta | cópia das barras em `BASE_A`, desenhada antes | 5 mm à frente | sumiu por baixo das outras |

O que foi desenhado por último sempre venceu, independentemente de estar na frente ou atrás. Isso só
acontece quando a profundidade não é gravada. A comparação com o TPK do AJM (DXT1) confirmou a causa.

### Sobre a ideia de "z-index"

A intuição estava certa em essência. O efeito é o mesmo de elementos com `z-index` fora de ordem, mas o
mecanismo é outro: não existe um número de camada por peça. Normalmente a GPU decide quem fica na frente
**pixel a pixel**, pela distância gravada no z-buffer. Quando o material é tratado como translúcido,
a distância não é gravada, e passa a valer a **ordem de desenho** (como no "algoritmo do pintor", ou num
HTML sem `z-index` em que o último elemento fica por cima). Por isso a solução não foi reordenar peças,
e sim fazer o motor voltar a tratá-las como opacas.

---

## 2. Limite de 65.535 índices por sólido

- Num sólido com vários grupos de material, a parte de um grupo que passa do índice **65.535** não é
  desenhada. Nas luzes da V2, `BASE_A` chegou a 75.687 índices e as lanternas sumiam.
- Na vprime, `BASE_A` tinha 78.144 índices; o grupo 4 (LOGO) começava em 38.646 e passava do limite.
- **Correção (V1prime-a):** mover o grupo 4 inteiro para o slot vazio `KIT00_RIGHT_SIDE_MIRROR_A`.
- Ferramenta: `versions/v1prime/scripts/beyond.py` pinta de vermelho o que passa do limite.
- Sozinho, isso **não** resolveu a grade. Só resolveu junto com o DXT1 da seção 1.
- Sólidos de grupo único acima do limite (`KIT00_BODY_A`, 119.901 índices) aparecem inteiros.

## 3. Placa: letras "CHAPINHA" em relevo

- A placa exportada do GTA tinha as letras **CHAPINHA em 3D**. A face da placa tinha buracos no formato
  das letras. No jogo sobravam pedaços das letras e da pintura atravessando a placa.
- **Correção (V1prime-b):**
  - apagar as letras (147 triângulos no LOD A, 129 no B e 26 no C);
  - trocar a face furada por uma face plana, com UV ajustado por mínimos quadrados para mostrar NEWZERA;
  - manter moldura e parafusos;
  - afastar a placa 10 mm do para-choque, nas duas placas e em todos os LODs.

## 4. Outros aprendizados do caminho (V2/V3)

- **Retrovisores duplicados (V2):** o catálogo Shelby trazia um par de retrovisores próprio, além do par
  incorporado à carroceria 2018. Voltar ao catálogo AJM resolve.
- **Organização do AJM:** a carroceria pintada fica em `BASE`. `RIGHT_SIDE_MIRROR` guarda grade,
  retrovisores 2010, frisos e chassi. `LEFT_SIDE_MIRROR_A` faz parte do interior. Os slots não
  correspondem ao nome.
- **Nomes de textura (V3):** a conclusão "nome fora do padrão não é desenhado" provavelmente era o
  mesmo efeito DXT3 da seção 1. Não usar mais como regra sem novo teste.
- **Normais invertidas:** inverter faces sem recalcular as normais escurece a pintura (capô da V3a).
- **Instalação:** há duas rotas (`CARS` e `ADDONS/CARS_REPLACE` do Mod Loader). Com o jogo aberto, a
  pasta ADDONS fica travada e a cópia falha com "Permission denied". Feche o jogo, espere alguns
  segundos e confira o SHA-256 nas duas rotas.
- **Vprime:** é a melhor base. As tentativas V2 (Shelby) e V3 (reconstrução) pioraram a carroceria.

## 5. Checklist para novas peças e versões

1. **Textura:** peça opaca usa **DXT1**. DXT3 só para vidro ou onde o alfa é realmente usado.
   Conferir com `scripts/validator` (campo `Format`: `31545844` = DXT1, `33545844` = DXT3).
2. **Índices:** nenhum grupo de sólido com vários grupos pode ultrapassar 65.535 índices
   (`beyond.py`). Se passar, dividir em outro slot.
3. **Geometria importada do GTA:** procurar texto em relevo, peças sobrepostas e superfícies
   atravessando outras (placa, emblemas).
4. **Teste de cores:** quando uma peça não aparece, pintá-la com cores sólidas em células livres de
   uma folha opaca (`BuildDiag.cs`) e ver o que o jogo desenha.
5. **Instalação:** jogo fechado, duas rotas, conferir SHA-256, reabrir o jogo.

## 6. Ferramentas usadas (sem Windows)

| Tarefa | Como |
| --- | --- |
| Compilar e ler GEOMETRY | PowerShell 7 (.NET 8) compilando `tools/mwgc/RealGeometry.cs` com os scripts C#: `scripts/mw.ps1` |
| Montar TPK | fontes do `mwtc` sem System.Drawing: `scripts/mwtc.ps1` (reconstrução do TPK V2 byte a byte idêntica) |
| Validar | `Validator.dll` existente: `scripts/val.ps1` |
| Visualizar | rasterizador Python com backface culling (`render.py`, `partcolor.py`, `simgame.py`) |
| Codificar texturas | DXT1/DXT3 em numpy: `scripts/dxt.py` |

Os scripts estão em `versions/v3-fusion-ajm3899/scripts` e `versions/v1prime/scripts`.

## 7. Vinis desalinhados entre painéis (V1prime-e)

- Vinis e adesivos do MW usam as **UVs do grupo de pintura (CARSKIN)**. UVs herdadas do GTA V mapeiam
  cada painel separadamente, e o adesivo "quebra" entre a porta dianteira e a traseira.
- Os carros originais usam um layout único: `u = 0,169·x + 0,5`, com `v` desenrolando a seção do carro
  (laterais pela altura, teto pela largura).
- `versions/v1prime/scripts/vinyluv.py` gera esse layout para `KIT00_BODY_A–E`, e `ApplyUV.cs` grava as
  UVs sem mexer em mais nada.

## 8. Performance fica no VLT, não na carroceria

Potência e dirigibilidade do Fusion estão em `GLOBAL\ATTRIBUTES.BIN` e no
`ATTRIBUTES.MWPS` do Mod Loader. Trocar `GEOMETRY.BIN` não muda como o carro anda.
O detalhe das três opções e o que cada uma copia está em
[versions/performance/PERFORMANCE.md](versions/performance/PERFORMANCE.md).

A opção instalada é `slr-m3gtr`: motor, câmbio e admissão da Mercedes-Benz SLR McLaren;
pneus, freios, chassi, massa e a reação da suspensão do BMW M3 GTR. O acerto puro do M3
nesse carro empurrava o bico em alta, então a direção, a rotação e a barra traseira foram
abertas. A posição das rodas do Fusion permanece a do carro.

## 9. Próximos passos sugeridos

- `KIT00_BRAKELIGHT` e `KIT00_HEADLIGHT` continuam DXT3 (cerca de 20 % de alfa). O teste atual aprovou
  os faróis; manter assim enquanto não houver defeito.
- O vidro dos faróis (grupo 5 antigo de `BASE_A`) foi deixado fora na V1prime; pode ser reavaliado.
