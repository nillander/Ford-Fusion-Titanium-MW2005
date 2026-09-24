# Fusion Titanium 2018 — V1prime

Base: [vprime](../vprime/VPRIME.md).

## V1prime-e — UV de vinil contínuo entre as portas (24/09/2026)

GEOMETRY `14AC2AC7…66FE`, TEXTURES iguais à V1prime-d (`BF9A0842…47D8`).
A V1prime-d aprovada está preservada em `variants/v1prime-d-approved`.

**Defeito:** um adesivo (bandeira da Dinamarca) aplicado na lateral ficava desalinhado entre a porta
dianteira e a traseira (`in-game/v1prime-d-vinyl-denmark-defect.png`). No MW, os vinis usam as
**coordenadas UV do grupo de pintura (CARSKIN)**. Na vprime essas UVs vinham do GTA V, com cada painel
mapeado de um jeito, e havia salto entre as portas.

**Referência:** nos carros originais do jogo (Camaro), a pintura usa um layout único:
`u = 0,169·x + 0,5` ao longo do carro, e `v` "desenrolando" a seção transversal (lado +y em
v ≈ 0,05–0,39, teto ≈ 0,4–0,6, lado −y em v ≈ 0,5–0,93).

**Correção** (`scripts/vinyluv.py` + `scripts/ApplyUV.cs`, só nos `KIT00_BODY_A–E`):

- `u = 0,169·x + 0,5`;
- laterais: `v` pela altura (`S = ±(0,97 + 1,30 − z)`), assim as faixas ficam retas e contínuas
  entre as portas;
- teto, capô e porta-malas: `S = y`;
- as duas regiões são misturadas pela normal (`|n.y|`), e `v = 0,5 − 0,2·S`.

Posições, normais e todas as outras peças ficaram idênticas. Prévia do padrão de teste: `preview/vinyl-uv-v1prime-e.png`.

## V1prime-d — texturas opacas em DXT1 — APROVADA NO JOGO (24/09/2026)

O usuário aprovou: vidros, janelas, rodas, cromados, grade frontal, grade do escapamento e faróis.
Captura em `in-game/v1prime-d-approved.png`. Resumo completo em
[APRENDIZADOS_FUSION_MW2005.md](../../APRENDIZADOS_FUSION_MW2005.md).

GEOMETRY igual à V1prime-b (`C8A2D660…C5FB`); TEXTURES `BF9A0842…47D8`.

**O que o diagnóstico mostrou** (`in-game/v1prime-c-diag-front.png`):

- o anel e o logotipo vermelhos aparecem, mas as barras vermelhas do mesmo grupo não;
- o painel verde, que está **atrás** das barras e foi desenhado **depois** delas, cobre as barras;
- a cópia magenta em `BASE_A`, desenhada antes e 5 mm à frente, some por baixo do vermelho e do verde.

Ou seja: o que é desenhado depois cobre o que foi desenhado antes, mesmo estando atrás. Esses
materiais **não gravam profundidade**. A causa está no formato da textura: as texturas da vprime foram
todas regravadas como **DXT3 (com alfa)**, e o MW trata material com textura DXT3 como translúcido.
No AJM original, `MISC`, `LOGO`, `INTERIOR` e `KIT00_BRAKELIGHT` são **DXT1**. Isso explica a grade
(`MISC`) coberta pelo motor e pelo painel, desenhados depois, e provavelmente também os faróis e
lanternas "vistos através do carro" nas outras versões.

**Correção:** `MISC`, `LOGO` e `INTERIOR` regravadas em DXT1 (alfa descartado; eram 100 % opacas,
exceto 0,01 % dos texels), com `scripts/dxt.py`. As texturas das luzes (`KIT00_BRAKELIGHT`/`HEADLIGHT`,
cerca de 20 % de alfa) continuam DXT3 e ficam para o próximo passo, depois da confirmação da grade.

## V1prime-c-diag — teste de cores instalado (24/09/2026)

**Resultado da V1prime-b** (`in-game/v1prime-b-front.png`): as placas ficaram limpas, mas a grade
continua ausente mesmo com faces nos dois sentidos e em grupos no início do buffer. Com isso, orientação
de face e posição no buffer ficam descartadas.

**Diagnóstico instalado** (`variants/v1prime-c-diag`, `scripts/BuildDiag.cs`): usa cores sólidas nas
células livres da BADGING, no lugar das texturas normais. A imagem esperada está em
`preview/v1prime-c-diag-expected.png`.

- **vermelho**: barras e anel no início de `KIT00_RIGHT_SIDE_MIRROR_A`;
- **verde**: painel de fundo no mesmo sólido;
- **magenta**: cópia das barras 5 mm à frente, como primeiro grupo de `BASE_A`.

GEOMETRY `D1F81A65…8A71`, TEXTURES `33BB4195…9991`. Não é versão de uso, é só para o diagnóstico.

## V1prime-b — placas corrigidas (release atual)

GEOMETRY `C8A2D660B3A8031AA31FF9A61095F4A8A36366A520D162866B2F428E4311C5FB`,
TEXTURES `54869AC5…E198` (inalterado). Construída a partir da V1prime-a com `scripts/BuildV1PrimeB.cs`.
A V1prime-a está preservada em `variants/v1prime-a`.

### Resultado da V1prime-a no jogo (`in-game/v1prime-a-front.png`)

O miolo da grade não apareceu. Os painéis pretos laterais (LOGO) passaram a aparecer, mas as barras
horizontais continuam ausentes, e o centro mostra o fundo, visto através do carro.
**A regra dos 65.535 índices, sozinha, não explica a grade.**
Geometria, bounds, alpha da textura, cor de vértice e sentido das faces das barras foram conferidos
sem o jogo e estão corretos. Nenhuma outra peça fica na frente delas.

### Placa: resíduos de "CHAPINHA" removidos

A placa exportada tinha as letras **CHAPINHA em relevo 3D** (`preview/vprime-plate-chapinha-geometry.png`):
o grupo LICENSEPLATE continha a moldura, as letras (UV na área "BRASIL MERCOSUL" da BADGING) e uma
face com buracos no formato das letras. No jogo sobravam pedaços das letras e da pintura atravessando
a placa. Em todos os LODs e nas duas placas:

- as letras foram apagadas (147 triângulos no LOD A, 129 no B, 26 no C);
- a face furada foi trocada por uma face plana, com UV ajustado por mínimos quadrados, que mostra NEWZERA;
- moldura e parafusos foram mantidos, e a placa foi afastada 10 mm do para-choque.

### Grade: teste de faces nos dois sentidos

As barras (MISC) e o painel de fundo (LOGO) na área da grade foram tirados de `BASE_A` e da V1prime-a
e colocados como os **primeiros grupos** de `KIT00_RIGHT_SIDE_MIRROR_A`, **com faces nos dois sentidos**.
Texturas e shaders não mudaram. Com esse teste dá para separar:

- a grade aparece → o problema era orientação de face ou posição no buffer;
- a grade continua ausente → a causa é outra (material ou profundidade), e os próximos testes serão
  cor forçada ou shader diferente.

## V1prime-a — histórico

Mudança única em relação à vprime: a grade frontal.

- GEOMETRY `FF39ACACC7287B63EFC51E5493B1525449CDFE47E47FD427FBAEFA9CCBC949D7`
- TEXTURES `54869AC551D1633227170C5815C6E0B553231613AA059B94B3E84D26AA5DE198` (idêntico à vprime)
- Leitura independente: 64 sólidos. 62 idênticos à vprime; só `BASE_A` e `KIT00_RIGHT_SIDE_MIRROR_A` mudaram.

## Diagnóstico da grade na vprime

A grade exportada do GTA V está inteira no arquivo, dentro de `BASE_A`:

- grupo 2 (DULLPLASTIC, `MISC`): moldura cromada e parte das barras — **aparece**;
- grupo 4 (DULLPLASTIC, `LOGO`): miolo da grade e outras peças — **o miolo não aparece**.

`BASE_A` tem 78.144 índices. O grupo 4 começa em 38.646 e termina em 76.539, e os
triângulos do miolo ficam depois da posição 65.535. O grupo 5 (HEADLIGHTGLASS) começa em
76.539 e nunca foi desenhado. Ver `preview/vprime-index-over-65535-red.png` (vermelho = após 65.535)
e `preview/vprime-grille-groups.png`.

Os `KIT00_BODY_A` da vprime também passam do limite (119.901 índices), mas o porta-malas e as
portas aparecem no jogo. A regra que bate com todas as observações até agora é:
**num sólido com vários grupos, o que fica depois do índice 65.535 não é desenhado**. A mesma
causa explicou as luzes da V2 (`BASE_A` com 75.687 índices).

## Correção

`scripts/BuildV1Prime.cs`:

1. o grupo 4 de `BASE_A` foi movido inteiro para `KIT00_RIGHT_SIDE_MIRROR_A`, que na vprime estava
   vazio, com a mesma textura e o mesmo shader (37.893 índices);
2. `BASE_A` ficou com os grupos 0–3 (38.646 índices);
3. o grupo 5 (vidro dos faróis, que nunca apareceu) ficou fora de propósito. Se ele passasse a ser
   desenhado, mudaria a aparência dos faróis, que o usuário considera boa na vprime. Ele continua
   disponível no GEOMETRY da vprime.

LODs B–E não foram mexidos (todos abaixo de 65.535).
