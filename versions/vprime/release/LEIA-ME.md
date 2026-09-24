# Fusion Titanium 2018 — MW2005 — candidato de teste v0.1

Pacote gerado e verificado fora do jogo. Ainda NÃO foi testado no MW2005.
Substitui a geometria do donor Fusion 2010 de AJM3899, mantendo o slot MUSTANGGT.
O modelo fornecido é identificado como Titanium 2018 no leia-me original.

## Instalação, quando o jogo estiver disponível

1. Prepare uma cópia do NFS Most Wanted 2005 com o Mod Loader compatível com o donor (CAR.INI informa modloader=0.2).
2. Confirme que o donor original funciona nessa cópia. Este é o controle para separar falhas da instalação de falhas da conversão.
3. Faça backup da pasta ADDONS/CARS_REPLACE/MUSTANGGT existente.
4. Copie a pasta ADDONS contida no ZIP para a raiz dessa cópia do jogo, usando o mesmo método do donor.
5. Teste primeiro o Mustang GT/Fusion com kit original, sem personalizações adicionais.

Os arquivos MWPS e CAR.INI permanecem byte a byte iguais ao donor; não aplique os patches manualmente a uma instalação desconhecida.
O nome Fusion 2010 e elementos de interface do donor podem continuar aparecendo. O slot/performance continuam sendo os do donor.
Este pacote não instala o jogo nem o Mod Loader e não é um addon independente.

## Conteúdo e verificações

- GEOMETRY.BIN novo: 64 peças; preserva os 64 nomes originais e acrescenta quatro níveis de distância para a peça auxiliar do capô.
- 116,674 triângulos somando as peças A do arquivo; 207,956 somando todos os LODs. A soma inclui peças opcionais, não é a contagem exata de um frame do jogo.
- TEXTURES.BIN: 40 texturas, incluindo as 9 do donor com payloads preservados e 31 novas.
- Rodas e freios do donor preservados. Motorista ajustado 0,15 m para trás e 0,20 m para baixo para caber no interior novo.
- Marcadores do donor preservados, incluindo matrizes. Posição exata das luzes ainda depende de inspeção no jogo.
- Leitura independente com NFS-ModTools; índices, nomes, limites, referências novas de textura e decodificação das 40 imagens verificados.
- Os arquivos de entrada em donor/ e source/ não foram modificados.

## Limites desta primeira versão

As prévias são renders do BIN reimportado no Blender, não capturas do jogo. Os shaders GTA foram aproximados para shaders MW conhecidos.
Existem simplificações de malha, reflexos/sombreamento ainda sujeitos a refinamento e substituições neutras para texturas globais GTA ausentes.
As rodas são as do Fusion 2010; rodas Titanium, danos, funcionamento das luzes, transparência, personalizações e transições de LOD ainda precisam de teste no motor do jogo.
Uma referência global de textura herdada do donor permanece externa: 1B049702, 7B220DDF.
Os pontos de roda usam as configurações existentes do donor; a carroceria foi ajustada longitudinalmente para elas.

## Roteiro de teste

Abra a garagem, entre numa corrida, examine frente/traseira/laterais e gire a câmera.
Confira rodas esterçando, distância ao chão, faróis, lanternas ao frear, vidros e motorista.
Afaste a câmera para observar os LODs. Só depois experimente pintura, vinis ou peças opcionais.
Em caso de falha, restaure a pasta do donor que foi guardada no backup.

## Créditos

Donor: Marcelo Castro (AJM3899); Turn 10 Studios; Riva; FOX; Porsche4ever; AJ Lethal.
Fonte GTA: modelo AND1V79; disponibilização Gabriel Lima; motor CH4P4X; demais atribuições no leia-me original incluído em credits/.
Ferramentas: Blender, Sollumz I/O/PyMateria, mwgc/mwtc de Arushan, NFSTools/NFS-ModTools, MWisBest/OpenNFSTools.
Os créditos originais foram preservados nos dois arquivos em credits/.
