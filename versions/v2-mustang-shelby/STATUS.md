# Fusion Titanium 2018 — V2 Mustang Shelby

**Retorno do usuário:** os desenhos de 2018 estão corretos, mas faróis e lanternas
somem em alguns ângulos. A validação visual permanece parcial. Investigar essa
falha e recuperar a grade frontal de referência sem reverter os avanços das luzes.

## Atualização vigente: textura da fonte de 2018

Faróis e lanternas agora usam um atlas renderizado das peças 3D da fonte,
mantendo o material opaco. A frente foi vista no jogo com os dois projetores.
A traseira exibe os novos detalhes, mas ainda apresenta interferências visuais.
O conjunto segue disponível para teste, sem aprovação do carro completo.

Veja [texturas de 2018](reference/TEXTURAS_LUZES_FONTE_2018.md).
GEOMETRY: `F349903F7565E4BAE9A70359D0F0587C7843A56E1A4C6BD67FA8981E39F6FCC9`.
TEXTURES: `563B585F4FBC3D0C85E22DA12E35037621040B4A0E505626BA478BD13B557CE9`.
`scripts/build_rear_lights_v2.ps1 -Install` reproduz essa versão; `-DonorAtlas`
recupera a aparência anterior. Os registros abaixo são históricos.

Estado em 20/09/2026, 21:33: V2 recompilado e instalado nas duas rotas do jogo.
Lanternas e faróis principais apareceram preenchidos nas vistas inspecionadas.
O veículo completo ainda não está aprovado; permanecem defeitos anteriores
na carroceria, grades e rodas, e falta testar a iluminação em corrida.

O registro atual, com aprendizado, validações e comando de reconstrução, está em
[APRENDIZADO_LANTERNAS_FAROIS.md](reference/APRENDIZADO_LANTERNAS_FAROIS.md).
O resultado frontal instalado tem SHA-256
`AC4DE300C521D15A596A28045987B81D37F5206DC7457C5C5444FDF0E93BC5E2`.
`scripts/build_rear_lights_v2.ps1 -Install` agora reproduz lanternas E faróis.

As seções abaixo conservam o histórico; os hashes e estados pendentes antigos
não representam a instalação atual.

O V2 preserva o slot `MUSTANGGT` e usará como base estrutural o pacote completo
`donor/ford_mustang_shelby/MODLOADER/ADDONS/CARS_REPLACE/MUSTANGGT`.
Nenhum arquivo do jogo foi alterado para iniciar esta versão.

## Marco concluído — 20/09/2026

- V1 preservado pela tag Git `fusion-v1-ajm3899` e por cópia local dos BINs.
- O GEOMETRY.BIN original do Shelby foi mantido intacto.
- `scripts/prepare_shelby_v2_donor.py` descomprime os 78 sólidos JDLZ do
  Shelby para uma cópia retail isolada em `work/shelby-retail.bin`.
- A cópia normalizada tem SHA-256
  `FB0CE1D5DC51F1A656C6B30B5F7EE36864E57667EB04C77C21F8172256DBF22F` e
  passou na leitura independente do NFS-ModTools: 78 peças e 87.829 triângulos.
- O catálogo confirmado contém BASE, pneus, freios, interior, vidros, faróis,
  lanternas, espelhos e aerofólio. A antiga atribuição das peças ausentes a
  uma limitação do AJM3899 foi retirada: o controle no jogo em 20/09 confirmou
  que o doador AJM original contém e exibe seus faróis, grades e rodas.

O pacote V2 foi instalado para teste em `CARS/MUSTANGGT` em 20/09/2026 após
leitura independente da geometria e das texturas. O estado anterior do jogo
foi copiado em `versions/v1-fusion-ajm3899/installed-game-backup/MUSTANGGT`.

## Protótipo de encaixe

O export atual do Fusion foi recompilado com o namespace `MUSTANGGT` e
mesclado à cópia retail do Shelby. A validação independente leu 85 peças e
247.765 triângulos em todos os LODs. Os slots do Shelby de pneus, freios e
aerofólio foram retidos; luzes, vidros, carroceria e interior foram trocados
pelo Fusion. O LOD A ficou em 142.994 triângulos, acima do alvo prático, e
por isso este protótipo não foi instalado nem empacotado.

## Pacote de teste instalado

O segundo exportador reduziu o LOD A para aproximadamente 63 mil triângulos e
mantém no Shelby os sólidos de pneus, freios, espelhos, faróis, lanternas e
aerofólio. O BIN instalado tem SHA-256
`96E3442D4BD8269B133DF68C360928570B69FA670B8EDEB989E6BEE81F533AA7`.
O TPK contém a placa `NEWZERA` e tem SHA-256
`F4C326F0075A9E2B59B1D8398469A93F9787574E70685FABA097BC3BC1825D6E`.

## Lanterna traseira — correção instalada para teste

Esta tentativa foi rejeitada pelo teste do usuário. A afirmação de que a
causa estava demonstrada como casca aberta não era sustentada pela validação
binária. O usuário continuou enxergando o interior pelas lanternas.

`scripts/OpaqueRearLights.cs` agora preserva todos os sólidos existentes e:

- mantém o material de lanterna com alpha de vértice 255;
- acrescenta um refletor fechado, de seis faces e 12 triângulos, atrás de cada
  lanterna traseira `*_BRAKELIGHT_A`;
- não altera grade, carroceria, rodas, nem os demais LODs.

O resultado foi lido independentemente pelo mwgc: 78 peças e 119.289
triângulos. Cada lanterna traseira de LOD A passou a ter três grupos, 593
vértices e 558 triângulos. O artefato instalado para o próximo teste é:

- `release/MUSTANGGT/GEOMETRY.BIN`
- jogo: `D:\Program Files (x86)\Electronic Arts\Need For Speed Most Wanted Black Edition\CARS\MUSTANGGT\GEOMETRY.BIN`
- SHA-256: `2F9D6A21BB3CC7425B08C758988217D3807D026A92A8DF8585704A6B67941925`

O BIN imediatamente anterior foi preservado em
`work/game-before-rear-reflector/GEOMETRY.BIN`. A textura instalada permanece
`8DF9EBDE632E0EAAE8A6907E7146291BD03CFC796C9B699C91B8581D12589954`.

## 20/09/2026 — lentes reais do Fusion e instalação dupla

Achados confirmados no código e nos arquivos:

- `optimize_export.py` classifica as lentes vermelhas (shader fonte 14) como
  `KIT00_RIGHT_BRAKELIGHT_GLASS`. O catálogo Shelby não possui esse sólido;
  o laço de exportação o descarta. O merge ainda retém as lanternas Shelby.
- As lentes do Fusion ficam em posições diferentes das do Shelby. Alterar
  somente o shader das peças Shelby não recoloca essas lentes descartadas.
- A instalação atual possui Mod Loader e o atalho `speed.exe -mod`.
  `ADDONS/CARS_REPLACE/MUSTANGGT` ainda continha geometria antiga de SHA
  `28CEF27A8C1E13651E95372D74C1552B58FF927EAA584EF0ABFE0BC6743E01BE`,
  enquanto as atualizações anteriores eram copiadas apenas para `CARS`.
  Não foi comprovado qual caminho o teste anterior carregou.

Correção atual:

- `scripts/export_fusion_rear_lights.py` exporta só as lentes traseiras do
  Fusion para os oito slots `KIT00_LEFT/RIGHT_BRAKELIGHT_A/B/C/D` existentes.
- Usa seleção por triângulo para excluir espelhos e indicadores contidos nos
  mesmos drawables GTA; preserva o formato com Decimate e Solidify de 3 mm.
- Material DULLPLASTIC usa a textura opaca existente `590566EC`, regiões
  vermelha e clara, com alpha confirmado em 255.
- `scripts/ReplaceRearLights.cs` substitui exatamente oito sólidos. As outras
  70 peças foram comparadas no JSON e permanecem idênticas. Isso também
  remove as caixas experimentais da tentativa anterior.
- `scripts/build_rear_lights_v2.ps1 -Install` reproduz exportação, compilação,
  validação e instalação; exige jogo fechado e cria backup. Atualiza geometria
  e texturas tanto em `CARS/MUSTANGGT` quanto em
  `ADDONS/CARS_REPLACE/MUSTANGGT` e compara seus hashes.

Validação: leitor independente NFS-ModTools, 78 sólidos, 128.789 triângulos
em todos os LODs. Prévia Blender do BIN mostra lentes preenchidas; isso não
substitui confirmação no motor do jogo. Teste anterior à sincronização das
duas pastas ainda mostrou ausência das lanternas. Novo teste pendente.

Hashes instalados nas DUAS pastas e na release:

- GEOMETRY: `76C1C1BBD1DA8001D6AA7C3412C1CE9042923B7ACCEB7CEB7521FD12D208296C`
- TEXTURES: `8DF9EBDE632E0EAAE8A6907E7146291BD03CFC796C9B699C91B8581D12589954`

Artefatos: `work/fusion-rear-lenses/`. Backup anterior à instalação dupla:
`work/fusion-rear-lenses/dual-install-backup-20260920-154255/`.
V1, source/ e donor/ preservados. Grade e faróis não foram alterados nesta etapa.

## 20/09/2026 — controle direto com o AJM3899 original

As tentativas anteriores NÃO estão aprovadas visualmente. O teste com lentes
anexadas a BASE mostrou variações de preto/transparência conforme o ângulo;
trocar somente a referência de textura e acrescentar fechamento convexo não
resolveu de modo consistente. Não concluir que falta de camadas seja a causa.

Controles executados no mesmo jogo:

- AJM3899 GEOMETRY.BIN e TEXTURES.BIN originais, copiados temporariamente nas
  duas rotas de instalação: frente, faróis, grades e rodas renderizados.
- `RoundTripGeometry.cs`: leitura e gravação do AJM sem alterar malhas.
  Também exibiu corretamente frente, faróis, grades e rodas. O serializador
  básico funciona para esse arquivo; isso não valida a classificação GTA.
- V2 e arquivos anteriores aos controles preservados em
  `work/fusion-rear-lenses/ajm-control-backup-20260920-211311/`.

Experimento atual (ainda requer inspeção): `native-donor-lights.bin` utiliza
o grupo opaco das lanternas AJM (shader 05BC3A3C, textura 4B7D95B6) ajustado
ao volume traseiro do Fusion 2018 e anexado a BASE A–D. A textura original
desse grupo foi copiada para um TPK de trabalho, preservando as outras 15.
O catálogo continua Shelby, 78 peças. Validação estrutural: 142.389 triângulos.
Não mudar V1/source/donor nem considerar o conjunto finalizado.

Comando atual de reconstrução das tentativas de lentes GTA:
`scripts/build_rear_lights_v2.ps1 -Install`. Ele NÃO reproduz o experimento
AJM acima; não executá-lo pensando que produzirá o último teste.
