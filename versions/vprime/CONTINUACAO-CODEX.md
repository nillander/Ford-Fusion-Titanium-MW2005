# Estado do transplante Fusion 2018 para NFS MW 2005

Atualizado em 2026-09-20 após corrigir o material dos aros originais.

## Estado instalado no jogo

Diretório: `D:\Program Files (x86)\Electronic Arts\Need For Speed Most Wanted Black Edition\CARS\MUSTANGGT`

- `GEOMETRY.BIN`: SHA-256 `74E39AF4A8C64025C7FD6963FE6E649D6E75F67FCFE04FF26C2606FBF8912F86`
- `TEXTURES.BIN`: SHA-256 `54869AC551D1633227170C5815C6E0B553231613AA059B94B3E84D26AA5DE198`
- Os hashes instalados são idênticos aos de `release/MUSTANGGT`.
- `VINYLS.BIN` e `PREVINYL.BIN` não foram alterados.
- Backup imediatamente anterior: `work/game-backup/before-gray-rim-test-MUSTANGGT`.

O candidato está pronto para teste. `reference/release-validation.json` continua com `in_game_tested: false` até a confirmação no motor.

## Descoberta principal

O veículo completo da fonte GTA é composto por quatro drawables complementares: `main`, `fusion_exh_2`, `fusion_rfst` e `fusion_rollcage`. A composição recuperou teto, vidros, faróis, lanternas, grades, para-choques, laterais e traseira. `source/` e `donor/` permanecem inalterados.

## Correções implementadas

- `scripts/build_scene.py`: usa os quatro drawables, eleva a carroceria em 0,15 m e usa a RTX 3080 Ti via OptiX.
- `scripts/optimize_export.py`: mantém capô e porta-malas em `KIT00_BODY`, motor em `BASE`, preserva rodas/freios do donor, reduz por objeto com pesos e conserva integralmente as cascas finas do capô.
- A redução global que levava mais de 50 minutos foi eliminada do fluxo normal.
- `scripts/remove_mwr_spikes.py`: remove faces anômalas antes do `mwgc`; eliminou o triângulo que atravessava capô e para-brisa em todos os LODs.
- `scripts/finalize_build.ps1`: recompila, remapeia, valida e empacota a partir do MWR existente.
- `scripts/render_compiled.py`: usa somente a GPU selecionada e aceita `MW_QUICK_RENDER=1`.
- Sollumz oficial e dependências `szio`, `pymateria` e `numpy` foram instalados para validar a fonte.

## Recursos

- RTX 3080 Ti configurada com OptiX; CPU desativada nos renders Cycles.
- Blender com prioridade alta e acesso aos 24 processadores lógicos.
- Decimate é monothread internamente; o orçamento por objeto evita a passagem global lenta.

## Validação offline

- Aprovada: 64 peças e nove texturas retail/RAWW.
- Aproximadamente 207.951 triângulos em todos os LODs e 116.667 nos LODs A.
- `KIT00_BODY_A`: 27.743 vértices e 39.967 triângulos.
- `BASE_A`: aproximadamente 28 mil vértices e 26.048 triângulos após o filtro.
- Rodas, freios, markers, slots e layout retail com sólidos irmãos preservados.
- Inputs originais inalterados.
- `preview/compiled-perspective.png` mostra o carro montado, sem o triângulo espúrio.

A placa ainda aparece como `CHAPINHA` na prévia offline. A troca para `NEWZERA` permanece pendente após o teste estrutural.

## Teste atual

### Ajuste isolado: aros cinza

Os vidros oficiais em duas camadas foram aprovados no jogo e permanecem inalterados. O cinza opaco também permanece nas antigas superfícies cromadas. A malha das rodas era idêntica à do donor, mas o aro usava o shader `0xC83DAC78` e o hash `0x2AF3D244`, agora ocupado pelo atlas interno do Fusion. O candidato atual remapeia apenas o aro para `DULLPLASTIC` e para a nova textura cinza `MUSTANGGT_RIM` (`0x0A7C3B20`); pneu, freios e encaixe não mudaram.

O teste deve avaliar somente se as rodas padrão aparecem com os aros cinza/prata, sem depender de instalar uma roda da loja. Os vidros devem continuar iguais ao teste aprovado.

## Próximo item registrado

- Investigar e remover o spike/polígonos irregulares que saem da frente do capô, após os itens visuais pendentes.

Verificar no seletor e no jogo:

1. frente, traseira e laterais completas;
2. vidros, faróis, lanternas e ambas as grades;
3. altura da carroceria e encaixe das quatro rodas;
4. porta-malas permanecendo ao instalar um aerofólio;
5. ausência de triângulos esticados ou peças piscando;
6. estabilidade ao alternar entre os LODs.

Depois da confirmação, corrigir a placa para `NEWZERA`, marcar `in_game_tested: true` e gerar o pacote final.

## Comandos

```powershell
Set-Location C:\Users\nillander\NoDocuments\fusion-mw2005
.\scripts\build.ps1
```

```powershell
.\scripts\finalize_build.ps1
```
