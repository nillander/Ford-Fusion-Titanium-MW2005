# v2.10 — Fusion 2018 com pneus do SLR

Na v2.9 o Fusion 2018 tinha o motor do Mercedes-Benz SLR McLaren (pico de torque 523
no original e 621 no melhorado) em pneus de Mustang GT básico. Com a tração integral,
o carro perdia aderência com facilidade e ficava difícil de guiar, muito mais que o
Fusion 2012, que usa o mesmo chassi com menos da metade da potência.

Esta versão coloca no 2018 o bloco de pneus inteiro do SLR, nos dois níveis:

| | v2.9 original | v2.10 original | v2.9 melhorado | v2.10 melhorado |
|---|---|---|---|---|
| Aderência estática (diant. / tras.) | 1,75 / 1,85 | 2,10 / 2,10 | 2,025 / 2,10 | 2,20 / 2,20 |
| Aderência em derrapagem | 1,55 / 1,65 | 1,85 / 1,85 | 1,80 / 1,90 | 1,90 / 1,90 |
| Multiplicador de aderência | 1,00 / 1,00 | 1,15 / 1,14 | 1,10 / 1,10 | 1,20 / 1,20 |
| Controle de giro | inativo | 0,1 · 0,3 · 0,5 · 1,0 | inativo | 0,1 · 0,5 · 0,7 · 1,2 |
| Velocidade de giro | 0,40 | 0,45 | 0,38 | 0,47 |
| Direção | 1,00 | 1,04 | 1,00 | 1,15 |
| Medida | 255/40 R18 | 295/30 R19 | 255/40 R18 | 295/35 R19 |

Os diferenciais ficam em 0,7 / 0,7 / 0,7 (dianteiro, traseiro e central) nos dois
níveis, mais soltos que os 0,8 / 0,8 / 0,75 da v2.9. A tração continua integral
(`TORQUE_SPLIT` 0,5).

O controle de giro estava inativo desde as primeiras versões: o MWPS gravava os valores,
mas a lista ficava com zero itens e o jogo a ignorava. Agora a lista tem os quatro
valores do SLR.

No nível original a medida nova tem praticamente o mesmo diâmetro da antiga (660 mm
contra 661 mm), então a velocidade em cada marcha não muda. No melhorado o pneu 295/35 R19
é cerca de 4 % maior (689 mm), o que alonga um pouco as marchas, como no SLR. Só o `ATTRIBUTES.MWPS` do 2018 mudou. Geometria,
texturas, motor, câmbio, chassi, massa, preço e nomes continuam os da v2.9. O pacote do
Fusion 2012 FWD é exatamente o mesmo da v2.8.

Instalação: feche o MW e execute `instalar.bat` do ZIP do Fusion 2018. Para atualizar
uma instalação v2.9, basta substituir `ADDONS/CARS_REPLACE/MUSTANGGT/ATTRIBUTES.MWPS`
pelo arquivo da v2.10. O Mod Loader reaplica os valores ao abrir o jogo.

Validação: pneus do 2018 iguais byte a byte aos do SLR nos dois níveis, nenhum outro
byte do VLT alterado além dos pneus e diferenciais, e integridade e hashes do ZIP
conferidos. Dirigibilidade testada e aprovada no jogo.
