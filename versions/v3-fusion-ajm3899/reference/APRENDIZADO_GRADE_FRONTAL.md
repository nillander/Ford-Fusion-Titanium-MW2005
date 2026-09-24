# Aprendizado: grade frontal do Fusion 2018 no MW2005

Atualizado em 24/09/2026 (Claude/Cowork). Vale para V2 e V3. A correção da V3b ainda
**não foi confirmada no jogo**; o diagnóstico abaixo é a hipótese mais bem sustentada até agora.

## Sintoma

Da V2 até a V3a, a abertura da grade aparece vazia no jogo: dá para ver o cofre do motor,
as rodas e o interior através dela. O Codex tentou "recuperar" a grade restaurando o BODY
de 20/09 às 12:48. A malha voltou para o arquivo, mas continuou sem aparecer.

## O que existe no arquivo

No `KIT00_BODY_A` da V2 há três grupos:

| Grupo | Shader | Textura | Conteúdo |
| --- | --- | --- | --- |
| 0 | CARSKIN `D6D6080A` | SKIN1 `9A8AAD9E` | pintura (aparece) |
| 1 | DULLPLASTIC `0FEDEE40` | `MUSTANGGT_GRILLE` `D0612097` | colmeia real da grade, 347 triângulos, x 2,21–2,34 |
| 2 | DULLPLASTIC `0FEDEE40` | `MUSTANGGT_OPAQUE_PARTS` `590566EC` | peças 3D do Codex: barras da grade, molduras das janelas, difusor, ponteiras, discos nas rodas |

Os grupos 1 e 2 **nunca foram desenhados no jogo**. Na V3a a colmeia foi para um sólido
próprio (`KIT00_RIGHT_SIDE_MIRROR_A–E`, com faces dupla-face) e **continuou invisível**.
Portanto, a causa não é o slot BODY.

## Causas descartadas (verificadas offline)

- Posições, normais e UVs válidos: sem NaN, normais unitárias, UV da colmeia em 0–0,81.
- Bounds do grupo e da peça iguais aos da geometria real.
- Culling: o rasterizador com backface culling (`scripts/render.py --cull`) mostra a
  grade de frente.
- Índices: todos os sólidos ficaram abaixo de 65.535.
- Alpha: `D0612097` e `590566EC` têm alpha 255 em todos os texels.

## Causa mais provável: nome de textura fora do padrão

Tudo o que usava textura com nome próprio sumia, e tudo o que usava nome padrão aparecia:

| Textura | Nome | No jogo |
| --- | --- | --- |
| `D0612097` | `MUSTANGGT_GRILLE` | grade sumiu (V2 e V3a) |
| `590566EC` | `MUSTANGGT_OPAQUE_PARTS` | peças do Codex sumiram (V2) |
| `A2268EFB` | `MUSTANGGT_AJM_INTERIOR` | aros das rodas sumiram (V3a) |
| `4B7D95B6` | `MUSTANGGT_KIT00_BRAKELIGHT` | faróis e lanternas aparecem |
| `339D0D44` / `5A00E244` / `5A006DE9` / `2AF3D244` | BADGING / MISC / LOGO / INTERIOR | peças da BASE aparecem |

O TPK original do Camaro só contém nomes da lista fixa (`MISC`, `TIRE`, `TIRE_N`,
`BADGING`, `BADGING_N`, `INTERIOR`, `KIT00_BRAKELIGHT_ON/OFF`, `KIT00_BRAKELIGHT_GLASS_ON/OFF`,
`KIT00_HEADLIGHT_ON`, `KIT00_HEADLIGHT_GLASS_ON`). Isso é compatível com o motor procurar as
texturas do carro por nome (`<CARRO>_<SUFIXO>`) e ignorar hashes que estejam fora da lista,
mesmo que estejam dentro do `TEXTURES.BIN`.

**Regra prática:** cada grupo precisa referenciar uma textura com nome padrão ou uma
textura global do jogo. Uma arte nova entra em uma área livre de uma folha padrão; não se
cria uma textura nova com outro nome.

## Correção aplicada na V3b

1. A folha `BADGING` (`339D0D44`, DXT3 1024²) tinha o quadrante inferior direito livre
   (preto e sem UV usando essa área). Ali entraram a colmeia (u,v 0,50–0,75) e quatro
   blocos de cor lisa (u 0,75–1,0 / v 0,50–0,75): cromado acetinado, metal escuro, preto e cinza.
   Atlas: `preview/v3b-badging-atlas.png`; DDS: `reference/339D0D44-badging-with-grille.dds`.
2. UV da colmeia remapeado com `u' = 0,5 + 0,25·u/0,72` e `v' = 0,5 + 0,25·(v+0,05)/0,87`.
   A área foi preenchida com a repetição original da textura nesse intervalo, para o padrão
   não mudar de escala.
3. Grade, difusor e ponteiras ficam em `KIT00_RIGHT_SIDE_MIRROR_A–E`, com DULLPLASTIC e
   faces dupla-face. No AJM esse slot já concentrava a grade, os frisos e o chassi.
4. Peças do Codex que foram descartadas porque ficariam visíveis e erradas assim que passassem
   a ser desenhadas:
   - molduras das janelas, que flutuam acima do teto;
   - barras sobre a colmeia, a mais de 2 cm à frente do para-choque;
   - discos presos à carroceria nas rodas, que não giram.
5. A codificação DXT3 é feita por `scripts/dxt.py`. Uma decodificação e recodificação da
   folha deu erro médio de 0,02/255. O `mwtc` só grava o mip 0, como nas versões anteriores.

## O que não repetir

- Restaurar ou mover a malha da grade sem trocar a textura: isso não muda nada no jogo.
- Dar nome novo a uma textura para "separar" uma peça (grade, peças opacas, aros).
- Colocar peças 3D sintéticas presas à carroceria nas rodas.

## Como verificar

- No jogo, na garagem: a colmeia preta deve preencher a abertura inteira, sem mostrar o motor.
- Offline: `pwsh scripts/mw.ps1 scripts/Dump.cs GEOMETRY.BIN out.dump` e depois conferir
  se todos os hashes referenciados estão no TPK e têm nome padrão, ou se são globais conhecidos
  (`1B049702`, `7811C146`, `7B220DDF`, `9A8AAD9F`).

## Pendências

- Confirmar no jogo. Se a colmeia continuar invisível, a hipótese do nome cai. O próximo
  teste seria usar CHROME ou ENGINE, que o AJM usa na grade dele.
- Friso cromado real das janelas: a V2 não tem essa peça em condição de uso.

## Atualização 24/09 — grade real do GTA V na vprime (limite de 65.535 índices)

Na vprime a grade exportada do GTA V fica em `BASE_A`. A moldura está no grupo 2 (`MISC`), e o
miolo está no grupo 4 (`LOGO`). As duas texturas têm nome padrão, então o nome não é a causa aqui.
`BASE_A` tem 78.144 índices, e os triângulos do miolo ficam depois da posição 65.535. No jogo
aparecem só as bordas. É a mesma causa das luzes da V2.

Regra que explica todas as observações até agora: **em sólido com mais de um grupo, a parte
posterior ao índice 65.535 não é desenhada**. `KIT00_BODY_A` com um único grupo de 119.901
índices aparece inteiro no jogo. A V1prime move o grupo 4 para `KIT00_RIGHT_SIDE_MIRROR_A`.
Ver `versions/v1prime/STATUS.md`.

Antes de mexer em material ou textura, rode `versions/v1prime/scripts/beyond.py`. Ele pinta de
vermelho o que passa do limite.
