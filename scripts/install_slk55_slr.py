"""Install 2012 Mercedes-Benz SLK55 AMG into the SLR McLaren slot."""
from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"D:\Program Files (x86)\Electronic Arts\Need For Speed Most Wanted Black Edition")
DONOR = ROOT / "donor" / "2012 Mercedes-Benz SLK55 AMG" / "2012 Mercedes-Benz SLK55 AMG"
BACKUP = ROOT / "work" / "game-backup" / "vanilla-SLR"
RELEASE = ROOT / "release" / "SLR"
GAME_SLR = GAME / "CARS" / "SLR"
ADDONS = GAME / "ADDONS" / "CARS_REPLACE" / "SLR"
TOOLS = ROOT / "tools" / "mwgc"


def sha256(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def run(program: Path, arguments: list[str]) -> None:
    completed = subprocess.run([str(program), *arguments], cwd=ROOT, check=False)
    if completed.returncode != 0:
        raise SystemExit(f"falha {completed.returncode}: {program} {arguments}")


def main() -> None:
    BACKUP.mkdir(parents=True, exist_ok=True)
    RELEASE.mkdir(parents=True, exist_ok=True)
    for filename in ("GEOMETRY.BIN", "TEXTURES.BIN", "VINYLS.BIN", "PREVINYL.BIN"):
        source = GAME_SLR / filename
        if source.exists() and not (BACKUP / filename).exists():
            shutil.copy2(source, BACKUP / filename)
            print("backed up", filename)

    retargeted = ROOT / "work" / "slk55-slr-retargeted.bin"
    merged = ROOT / "work" / "slk55-slr-merged.bin"
    run(TOOLS / "RetargetSlot.exe", [str(DONOR / "SL65" / "GEOMETRY.BIN"), str(retargeted), "SL65", "SLR"])
    run(TOOLS / "MergeGeometry.exe", [str(BACKUP / "GEOMETRY.BIN"), str(retargeted), str(merged)])
    shutil.copy2(merged, RELEASE / "GEOMETRY.BIN")
    shutil.copy2(DONOR / "SL65" / "TEXTURES.BIN", RELEASE / "TEXTURES.BIN")
    for filename in ("VINYLS.BIN", "PREVINYL.BIN"):
        shutil.copy2(BACKUP / filename, RELEASE / filename)

    GAME_SLR.mkdir(parents=True, exist_ok=True)
    ADDONS.mkdir(parents=True, exist_ok=True)
    for filename in ("GEOMETRY.BIN", "TEXTURES.BIN", "VINYLS.BIN", "PREVINYL.BIN"):
        shutil.copy2(RELEASE / filename, GAME_SLR / filename)
        shutil.copy2(RELEASE / filename, ADDONS / filename)
        print("installed", filename, sha256(GAME_SLR / filename))

    (ADDONS / "CAR.INI").write_text(
        "[car]\nname=2012 Mercedes-Benz SLK55 AMG\nmanufacturer=MERCEDES\ninternal=slr\nmodloader=0.2\n",
        encoding="ascii",
    )
    shutil.copy2(DONOR / "SL65.nfsms", RELEASE / "SL65.nfsms")
    print("SLK55 no slot SLR")


if __name__ == "__main__":
    main()
