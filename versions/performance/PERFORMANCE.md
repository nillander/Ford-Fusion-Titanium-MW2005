# Performance do Fusion (slot MUSTANGGT)

A carroceria do Fusion não guarda potência nem dirigibilidade. Isso fica no VLT de
`GLOBAL\ATTRIBUTES.BIN`. O Mod Loader reaplica `ADDONS\CARS_REPLACE\MUSTANGGT\ATTRIBUTES.MWPS`
toda vez que o jogo abre, então os dois arquivos precisam ser o mesmo conjunto.
`FE_ATTRIB.BIN` acompanha o par e, nestas três opções, é o mesmo arquivo.

A posição das rodas do Fusion fica como está. Altura, cambagem, largura de contato e a
reação da carroceria (mergulho, agachamento e rolagem) acompanham a dirigibilidade da opção.

O script `scripts/apply_m3gtr_performance.py` grava a opção `slr-m3gtr` no jogo e nesta pasta.
Ele não substitui `fusion-mustang` se os arquivos já existirem. A opção `m3gtr` fica guardada
aqui e não é regravada por uma nova execução.

## Opções

| Pasta | Potência | Dirigibilidade |
| --- | --- | --- |
| `fusion-mustang` | Ford Mustang GT original do slot. Torque de fábrica até 320, corte a 6250 rpm. A versão melhorada chega a 640 no mesmo corte. | A do Mustang GT |
| `m3gtr` | BMW M3 GTR do protagonista (`bmwm3gtr`). Torque até 283, corte a 8500 rpm. Os dois estágios usam a mesma curva, porque o M3 GTR não tem versão turbinada separada. | A do M3 GTR |
| `slr-m3gtr` | Mercedes-Benz SLR McLaren. Torque de fábrica até 523, corte a 7000 rpm. O estágio melhorado segue a `slr_top` (até 621, mesmo corte). | A do M3 GTR |

A opção instalada no jogo é `slr-m3gtr`.

## O que cada opção copia

`slr-m3gtr` junta as duas:

- da SLR, nos dois estágios: motor, câmbio e admissão (`slr` / `slr_top` para `mustanggt`, `mustanggt_top` e `mustanggt_base`);
- do M3 GTR, nos dois estágios: pneus, freios e chassi;
- do M3 GTR, no carro: massa, inércia (`TENSOR_SCALE`) e `HandlingRating`;
- do M3 GTR, no `ecar`: `RideHeight`, `CamberFront`, `CamberRear`, `TireSkidWidth`, `BodyDive`, `BodySquat` e `BodyRoll`.

`m3gtr` copia motor, câmbio, pneus, freios, chassi, massa, inércia, `HandlingRating` e os mesmos
campos de `ecar`. O M3 GTR não tem nó de admissão, então a admissão dessa opção continua a do Mustang.

`fusion-mustang` é o `ATTRIBUTES.BIN` do jogo antes da primeira troca, com o `ATTRIBUTES.MWPS`
que o Mod Loader usava. Não é a SLR. O script `scripts/copy_slr_stats_to_mustang.py` existe para
copiar a SLR inteira, mas essa cópia não está neste backup.

Fora das três opções ficam a posição das rodas (`TireOffsets`), o som e o modelo visual.

## Trocar a opção

Com o jogo fechado, copie da pasta escolhida:

- `ATTRIBUTES.MWPS` para `ADDONS\CARS_REPLACE\MUSTANGGT\`
- `ATTRIBUTES.BIN` e `FE_ATTRIB.BIN` para `GLOBAL\`

Diretório do jogo: `D:\Program Files (x86)\Electronic Arts\Need For Speed Most Wanted Black Edition`.
