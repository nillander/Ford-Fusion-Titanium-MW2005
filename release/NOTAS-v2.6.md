# v2.6 — lente dos faróis, vidros e capô sem camadas escondidas

Esta atualização substitui os dois ZIPs da v2.5. O instalador, os slots, a performance e as cintas continuam os mesmos.
As correções aparecem sobretudo com mods que trocam os shaders e as texturas do jogo (Xbox 360 Stuff, pacotes de
texturas, ReShade). No jogo sem mods, o visual praticamente não muda.

- **Lente dos faróis do 2018:** a lente apontava para uma área preta e 80 % opaca da textura do farol. Agora usa
  vidro claro e quase transparente, como o do 2012. O pisca âmbar continua laranja.
- **Vidros (2012 e 2018):** cada janela tinha duas chapas (a de fora e a de dentro, a 5,5 mm) e a textura
  entrava espelhada no meio do para-brisa e do vidro traseiro. Agora é uma chapa por janela, com a textura da
  posição dela aplicada inteira, sem espelho.
- **Capô (2012 e 2018):** o capô de fábrica tinha cada triângulo repetido e virado para baixo. Com mods que
  desenham os dois lados, a cópia escura cobria a pintura e o capô ficava preto. As cópias saíram do capô de
  fábrica e das partes planas dos 17 capôs da loja.

Instalação: extraia o ZIP do carro desejado, feche o jogo e execute `instalar.bat`. Os arquivos `CARS` e
`ADDONS/CARS_REPLACE` do slot são atualizados juntos. Os SHA-256 dos arquivos internos estão em `SHA256SUMS.txt`
dentro de cada ZIP.
