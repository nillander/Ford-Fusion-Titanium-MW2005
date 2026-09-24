# Fusion Titanium 2018 — V1prime

Base: [vprime](../vprime/VPRIME.md). Única mudança: a grade frontal. Estado: instalada para teste
em 24/09/2026, nas duas rotas (`CARS/MUSTANGGT` e `ADDONS/CARS_REPLACE/MUSTANGGT`).

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
