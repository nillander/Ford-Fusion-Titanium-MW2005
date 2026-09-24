# Fusion Titanium 2018 — V3 (base AJM3899 / Fusion 2010)

Iniciada em 23/09/2026 pelo Claude (Cowork), retomando o trabalho pausado pelo Codex.
V1 e V2 permanecem intactas. Slot: `MUSTANGGT`.

## Estado

- Instalada para teste em `CARS/MUSTANGGT` e `ADDONS/CARS_REPLACE/MUSTANGGT`.
- GEOMETRY: `ECBED63EAD7D996BBE246381AA796C169AD37F96A75A95605F2C4A10C99B7BBC`
- TEXTURES: `E68F7912131F0BE59EA413E32CCF2B6E842B74579F81B9C70DBFB1F6F8FF7816`
- Leitura independente (NFS-ModTools): 64 sólidos, 149.159 triângulos; TPK com 17 texturas.
- Backup da instalação anterior (V2 final `0DE11B06…`/`563B585F…`) em `work/game-backup-before-v3-*`.
- **Inspeção no jogo pendente.**

## Composição (catálogo AJM de 64 sólidos preservado, na ordem original)

| Slot AJM | Conteúdo V3 |
| --- | --- |
| `BASE_A–E` | BASE da V2 (Fusion 2018) + **mount points originais do AJM** (faróis, freio, ré, escape). A V2 não tinha nenhum marcador. Removido o triângulo "espeto" do cofre do motor. |
| `KIT00_BODY_A–E` | Só o grupo de pintura (CARSKIN) da carroceria V2 — inclui o único par de retrovisores, do Fusion 2018. Descartados os prismas sintéticos (santantônio, discos nas rodas, barras) que nunca apareceram no jogo. 1.601 triângulos com normal para dentro foram invertidos (manchas escuras do capô). |
| `KIT00_RIGHT_SIDE_MIRROR_A–E` | No AJM esse slot guarda grade, retrovisores 2010, frisos e chassi. Esvaziado e reaproveitado para a **grade 2018** (textura GRILLE), dupla-face. Na V2 a grade estava dentro de BODY e não era desenhada. |
| `KIT00_RIGHT_HEADLIGHT_A–C` / `RIGHT_BRAKELIGHT_A–C` | Luzes 2018 da V2 (atlas da fonte), lado esquerdo + direito no mesmo sólido, como o AJM organiza. Faces dupla-face mantidas. Índices: 40.104 / 42.240 no LOD A (< 65.535). |
| `*_GLASS`, `REAR_WINDOW_A`, `SPOILER`, `LEFT_SIDE_MIRROR_A` | Placeholders degenerados (peças 2010 removidas). |
| `FRONT_WINDOW_A–C`, `INTERIOR_A–C` | V2. |
| `DRIVER_A–C` | V1 (já alinhado ao banco 2018). |
| Pneus, freios, `KIT01/02_BODY` | AJM originais. Pneus/freios usavam a folha `2AF3D244` do AJM, que colide com o interior 2018; remapeados para `MUSTANGGT_AJM_INTERIOR` (`A2268EFB`). |

## Achados

- V1 falhou principalmente por **estouro de índices**: `KIT00_BODY_A` tinha 121.155 índices, `BASE_A` 78.084, `FRONT_WINDOW_A` 71.958 e `INTERIOR_A` 73.194 (limite 65.535).
- No AJM, a carroceria pintada fica em `BASE`; `RIGHT_SIDE_MIRROR` contém grade, retrovisores, frisos e chassi; `LEFT_SIDE_MIRROR_A` é parte do interior.
- Na V2, os slots `SIDE_MIRROR` do Shelby levavam retrovisores **e os abafadores** do Shelby.
- Limites de grupo, bounds e winding das luzes V2 estão corretos. Um rasterizador com backface culling (`scripts/render.py --cull`) mostra as luzes completas em 8 ângulos, então o recorte angular no jogo **não** vem de oclusão nem de culling. Suspeitas restantes: comportamento do shader BRAKELIGHT (`05BC3A3C`) no motor. `BuildV3.cs --dull-lamps` gera a variante com DULLPLASTIC para teste A/B; o teste antigo com DULLPLASTIC foi feito enquanto BASE estourava o índice e não é conclusivo.

## Toolchain (sem Windows)

Os terminais do Windows não aceitam digitação remota, então a V3 foi montada na nuvem em Linux:
PowerShell 7 (.NET 8) compila `tools/mwgc/RealGeometry.cs` e `tools/mwtc/*.cs` junto com os scripts (`scripts/mw.ps1`, `scripts/mwtc.ps1`);
o `Validator.dll` existente roda via `scripts/val.ps1`. A reconstrução do TPK V2 com essa cadeia ficou byte a byte idêntica ao original.

Reconstrução:

```
pwsh scripts/mw.ps1 scripts/BuildV3.cs <AJM GEOMETRY> <V2 GEOMETRY> <V1 GEOMETRY> v3-base.bin
pwsh scripts/mw.ps1 scripts/ApplyFlips.cs v3-base.bin reference/body-flips.txt GEOMETRY.BIN
pwsh scripts/mwtc.ps1 reference/textures.txt   # 16 DDS da V2 + A2268EFB.dds (AJM 2AF3D244)
```

Os caminhos dos `.ps1` apontam para o workspace da nuvem (`/home/claude/v3`) e precisam ser ajustados para rodar em outra máquina.
