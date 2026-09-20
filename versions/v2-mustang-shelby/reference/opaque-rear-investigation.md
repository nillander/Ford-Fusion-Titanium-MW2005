# Lanternas opacas — investigação e instalação

O BIN instalado usava lanternas Shelby com shaders 05BC3A3C e 721AFDDC,
mas o TPK continuava sendo o atlas Fusion. A referência D947F346 não estava
no TPK, e 5A00E244 apontava para o atlas Fusion em vez do acabamento Shelby.
Uma referência ausente também pode ser resolvida externamente pelo jogo;
isso não foi presumido como garantia de compatibilidade.

Comparação com work/vanilla-mustang-geometry.json: o Mustang original separa
corpo e vidro da lanterna em sólidos e materiais diferentes. O número de
grupos de materiais não prova um número igual de camadas físicas. Portanto,
as afirmações anteriores de três camadas oficiais não estavam demonstradas.

Correção de teste: somente as oito peças BRAKELIGHT receberam shader
0FEDEE40 (também usado na carcaça dos faróis vanilla), a textura Shelby
4B7D95B6 sob a referência D947F346 e seu acabamento original 5A00E244 sob
o hash exclusivo F18A0001. Texturas copiadas sem edição; alfa 255 confirmado
nos DDS extraídos do TPK final. Geometria, grade, vidros e demais materiais
comparados antes/depois e mantidos idênticos no leitor.

Validação independente: 78 peças, 119265 triângulos, 16 texturas.
Instalado em CARS/MUSTANGGT. Backup em work/game-before-opaque-rear nesta
versão. Ainda sem confirmação visual no jogo. O shader opaco pode alterar
a resposta visual ao frear; verificar isso no teste.

SHA256 GEOMETRY/TEXTURES e resultados de leitura estão nos arquivos da
pasta release e nos relatórios opaque-rear-geometry.json e
opaque-rear-textures.json. Scripts de correção: OpaqueRearLights.cs e
prepare_rear_lamp_tpk.py; a etapa é posterior ao merge/remap do build antigo.
