"""Install the Fusion visual compiled against donor/fordgt into CARS/FORDGT."""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"D:\Program Files (x86)\Electronic Arts\Need For Speed Most Wanted Black Edition")
RELEASE = ROOT / "release" / "FORDGT"
FUSION = ROOT / "work" / "game-backup" / "pre-fordgt-slot-MUSTANGGT"
VANILLA_BACKUP = ROOT / "work" / "game-backup" / "vanilla-FORDGT"
DONOR = ROOT / "donor" / "fordgt" / "ADDONS" / "CARS_REPLACE" / "FORDGT"
GAME_FORDGT = GAME / "CARS" / "FORDGT"
ADDONS = GAME / "ADDONS" / "CARS_REPLACE" / "FORDGT"


def sha256(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def main() -> None:
    if not (RELEASE / "GEOMETRY.BIN").exists():
        raise SystemExit("release/FORDGT/GEOMETRY.BIN ausente")

    VANILLA_BACKUP.mkdir(parents=True, exist_ok=True)
    for filename in ("GEOMETRY.BIN", "TEXTURES.BIN", "VINYLS.BIN", "PREVINYL.BIN"):
        source = GAME_FORDGT / filename
        target = VANILLA_BACKUP / filename
        if source.exists() and not target.exists():
            shutil.copy2(source, target)
            print("backed up vanilla", filename)

    for filename in ("TEXTURES.BIN", "VINYLS.BIN", "PREVINYL.BIN"):
        shutil.copy2(FUSION / filename, RELEASE / filename)

    shutil.copy2(DONOR / "CAR.INI", RELEASE / "CAR.INI")
    shutil.copy2(DONOR / "ATTRIBUTES.MWPS", RELEASE / "ATTRIBUTES.MWPS")
    shutil.copy2(DONOR / "FE.MWPS", RELEASE / "FE.MWPS")
    if (DONOR / "SECONDARYLOGO.BIN").exists():
        shutil.copy2(DONOR / "SECONDARYLOGO.BIN", RELEASE / "SECONDARYLOGO.BIN")

    GAME_FORDGT.mkdir(parents=True, exist_ok=True)
    ADDONS.mkdir(parents=True, exist_ok=True)
    for filename in ("GEOMETRY.BIN", "TEXTURES.BIN", "VINYLS.BIN", "PREVINYL.BIN"):
        shutil.copy2(RELEASE / filename, GAME_FORDGT / filename)
        shutil.copy2(RELEASE / filename, ADDONS / filename)
        print("installed", filename, GAME_FORDGT.joinpath(filename).stat().st_size, sha256(GAME_FORDGT / filename))
    for filename in ("CAR.INI", "ATTRIBUTES.MWPS", "FE.MWPS", "SECONDARYLOGO.BIN"):
        if (RELEASE / filename).exists():
            shutil.copy2(RELEASE / filename, ADDONS / filename)


if __name__ == "__main__":
    main()
