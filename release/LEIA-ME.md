# Ford Fusion Titanium 2018 AWD — Need for Speed: Most Wanted (2005)

Substitui o **Ford Mustang GT** (slot `MUSTANGGT`). Release v2.1 de 27/09/2026.

## O que vem no pacote
- **Visual**: carroceria do Fusion Titanium 2018 com faróis, lanternas, grade, vidros com película, antena
  tubarão, emblemas FUSION / TITANIUM na tampa e Ford prata na frente, rodas originais de 20 raios (aro 18"),
  carroceria suavizada, discos e pinças de freio com textura própria, antena com a traseira reta, chama do
  nitro saindo das saídas do escapamento. O carro aparece completo também no Menu da Carreira, nas cutscenes e
  com o Razor.
- **Personalização**: 17 capôs da loja ajustados ao Fusion, entrada de ar do teto, aerofólio, dois kits de
  carroceria ("Street" e "Race": a carroceria de fábrica com uma cinta de reboque no para-choque), adesivos
  de porta, números de porta e faixas do para-brisa e do vidro traseiro.
- **Performance e dirigibilidade** (`ATTRIBUTES.MWPS`): chassi, peso (1.600 kg), suspensão, barras,
  distribuição de peso e aderência do Mustang GT; direção menos sensível.
- **Telas do jogo**: nome "Ford Fusion Titanium AWD", logotipo FUSION (`SECONDARYLOGO.BIN`) e logotipo
  Ford em alta resolução (`ADDONS/FRONTEND/MANUFACTURERS/27-FORD_HD.BIN`; troca o logo da Ford para
  todos os carros Ford).

## Requisitos
- NFS Most Wanted 2005 (PC) com o **NFSMW Mod Loader** (o `CAR.INI` pede `modloader=0.2`), que lê a
  pasta `ADDONS`.

## Instalação
1. Extraia o ZIP. Ele abre numa pasta com o mesmo nome do arquivo.
2. Feche o jogo e execute `instalar.bat` nessa pasta. O script copia `ADDONS` e `CARS` para o jogo.
3. Abra o jogo pelo Mod Loader. O Fusion 2018 aparece no lugar do Mustang GT. O Fusion 2012, no lugar do Cobalt SS.

Para desinstalar, restaure o backup do passo 1. Confira os arquivos com `SHA256SUMS.txt`
(ex.: `certutil -hashfile GEOMETRY.BIN SHA256` no Windows).

## Créditos
Modelo GTA V: AND1V79; conversão e texturas para o GTA V pelo autor do pacote original, disponibilizado
por Gabriel Lima (ver `CREDITOS/source-readme.txt`). Base MW (Fusion 2010): Marcelo Castro (AJM3899), com
peças de FOX, Porsche4ever e AJ Lethal (ver `CREDITOS/donor-readme.txt`). Conversão para o MW 2005: Nillander Alarcão, com Claude.

---
Arquivos para distribuir (v2.1, 27/09/2026):

| ZIP | Carro | SHA-256 |
|---|---|---|
| `Fusion2012_FWD_MW2005.zip` | Ford Fusion 2012 FWD (slot COBALTSS) | `B47B3C372345C331DD847D022494B9B3AEEBD613B6CDC9975B64EA68A1BBE0DF` |
| `Fusion2018_AWD_MW2005.zip` | Ford Fusion Titanium 2018 AWD (slot MUSTANGGT) | `AC372B2D4B81F724977B08B3D1683CFE69ADC19D653599D21C3031CAC079A4A5` |

`SHA256SUMS-conteudo.txt` lista os arquivos de dentro dos dois ZIPs. O LEIA-ME de cada carro está dentro do seu ZIP.
