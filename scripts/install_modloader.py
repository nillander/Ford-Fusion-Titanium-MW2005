"""Install the classic NFSMW Mod Loader 1.3 next to speed.exe."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"D:\Program Files (x86)\Electronic Arts\Need For Speed Most Wanted Black Edition")
SOURCE = ROOT / "work" / "modloader" / "ml" / "MOD Loader manual install"
BACKUP = ROOT / "work" / "game-backup" / "pre-modloader"


def main() -> None:
    if not (SOURCE / "d3d9.dll").exists():
        raise SystemExit("pacote do Mod Loader ausente; baixe work/modloader primeiro")
    BACKUP.mkdir(parents=True, exist_ok=True)
    for filename in ("d3d9.dll", "modloader.ini"):
        existing = GAME / filename
        if existing.exists() and not (BACKUP / filename).exists():
            shutil.copy2(existing, BACKUP / filename)
            print("backed up", filename)
    shutil.copy2(SOURCE / "d3d9.dll", GAME / "d3d9.dll")
    ini = (SOURCE / "modloader.ini").read_text(encoding="ascii", errors="replace")
    ini = ini.replace("SkipFE=1", "SkipFE=0").replace("StartCar=sl65", "StartCar=mustanggt")
    (GAME / "modloader.ini").write_text(ini, encoding="ascii")
    (GAME / "Start NFS MW Mod Loader.bat").write_text("start speed.exe -mod\r\n", encoding="ascii")
    (GAME / "ADDONS" / "CARS_REPLACE").mkdir(parents=True, exist_ok=True)
    (GAME / "ADDONS" / "FRONTEND").mkdir(parents=True, exist_ok=True)
    print("Mod Loader em", GAME)
    print("Abra o jogo com 'Start NFS MW Mod Loader.bat' (speed.exe -mod)")


if __name__ == "__main__":
    main()
