# Ford Fusion 2012 FWD e Fusion Titanium 2018 AWD — Need for Speed Most Wanted (2005)

Dois mods para o Most Wanted de PC, instaláveis juntos porque usam slots diferentes:

| Carro | Substitui no jogo | Tração |
| --- | --- | --- |
| Ford Fusion 2012 FWD | Chevrolet Cobalt SS (`COBALTSS`) | Dianteira |
| Ford Fusion Titanium 2018 AWD | Ford Mustang GT (`MUSTANGGT`) | Integral |

> **Release atual: v2.1 (27/09/2026).** Ela corrige as placas dianteiras e traseiras dos dois carros: a
> moldura preta 3D separada foi removida, e a borda arredondada passou a fazer parte da placa. A faixa azul,
> a bandeira do Brasil e o texto da placa foram mantidos. O ajuste adicional do encaixe dos faróis do 2012
> ainda está em teste local e **não faz parte da v2.1**. Veja o [estado do trabalho](docs/CONTINUACAO.md).

## No jogo

| Fusion 2012 FWD | Fusion Titanium 2018 AWD |
| --- | --- |
| ![Fusion 2012 na tela principal](capturas/2012/principal.png) | ![Fusion 2018 na tela de carros](capturas/2018/principal-2.png) |
| ![Fusion 2012 visto por trás](capturas/2012/Screenshot_172.png) | ![Fusion 2018 visto por trás](capturas/2018/Screenshot_168.png) |

[Todas as capturas dos dois carros](capturas/README.md). São imagens feitas no jogo; algumas podem mostrar
testes locais posteriores à release e não substituem as notas de versão.

## O que os mods incluem

- Carroceria, interior, rodas, emblemas e iluminação próprios dos Fusion. O 2012 usa faróis, lanternas e
  faróis de milha do seu modelo; o 2018 mantém o conjunto visual Titanium.
- Kits de carroceria, capôs, aerofólio, entrada de ar do teto, adesivos e faixas para personalização.
- Nome e logotipo Fusion na seleção de carros, além de ajustes de performance e dirigibilidade por slot.
- Placas Mercosul `NEWZERA` com faixa azul e bandeira do Brasil.

Detalhes do 2012 estão em [versions/fusion2012-fwd/LEIA-ME.md](versions/fusion2012-fwd/LEIA-ME.md);
os arquivos incluídos, créditos e requisitos estão em [release/LEIA-ME.md](release/LEIA-ME.md).

## Instalação

É necessário o **NFSMW Mod Loader**. Feche o jogo e faça backup dos arquivos que serão substituídos antes de
instalar. Baixe o ZIP do carro desejado em [release/](release/) e extraia-o: ele abre numa pasta com o nome
do carro, contendo `instalar.bat`, `ADDONS`, `CARS`, `CREDITOS`, `LEIA-ME.md` e `SHA256SUMS.txt`.

Execute `instalar.bat` **de dentro dessa pasta**, confirme a instalação do Most Wanted encontrada pelo script
e abra o jogo pelo Mod Loader. Para usar os dois Fusion, execute o instalador de cada ZIP. O script copia
os arquivos para `CARS/<slot>` e `ADDONS/CARS_REPLACE/<slot>`; ele não cria backup automaticamente.
Confira os hashes dos arquivos internos em `SHA256SUMS.txt`.

| Pacote v2.1 | SHA-256 do ZIP |
| --- | --- |
| [Fusion2012_FWD_MW2005.zip](release/Fusion2012_FWD_MW2005.zip) | `B47B3C372345C331DD847D022494B9B3AEEBD613B6CDC9975B64EA68A1BBE0DF` |
| [Fusion2018_AWD_MW2005.zip](release/Fusion2018_AWD_MW2005.zip) | `AC372B2D4B81F724977B08B3D1683CFE69ADC19D653599D21C3031CAC079A4A5` |

As alterações da v2.1 estão em [release/NOTAS-v2.1.md](release/NOTAS-v2.1.md).

## Acompanhar e desenvolver

| Caminho | Conteúdo |
| --- | --- |
| [capturas/](capturas/README.md) | Galeria dos dois veículos no jogo |
| [docs/CONTINUACAO.md](docs/CONTINUACAO.md) | Estado instalado, testes pendentes e procedimento para retomar o trabalho |
| [docs/TODO.md](docs/TODO.md) | Itens concluídos e tarefas ainda abertas |
| [docs/APRENDIZADOS.md](docs/APRENDIZADOS.md) | Diagnósticos e lições técnicas com imagens |
| [docs/imagens-projeto/](docs/imagens-projeto/README.md) | Referências, defeitos anotados e prévias por etapa |
| [versions/](versions/LEIA-ME.md) | Histórico das versões e variantes |
| [docs/historico/](docs/historico/) | Pedido inicial e primeiras releases de teste |

`source/` e `donor/` guardam os modelos de origem e os carros-base; `scripts/`, `tools/`, `blender/` e
`work/` são usados na construção e validação. Os comandos de build antigos em `scripts/` não representam,
sozinhos, a v2.1 completa; para continuar o trabalho atual, comece pelo documento de continuação acima.
