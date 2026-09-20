import json
import math
from pathlib import Path

root = Path(__file__).resolve().parents[1]


def tire_stats(path, name):
    parts = json.loads(path.read_text())
    part = next(item for item in parts if item["name"] == name)
    verts = part["mesh"]["Vertices"]
    radii = []
    ys = []
    for vertex in verts:
        position = vertex["Position"]
        radii.append(math.hypot(position["x"], position["z"]))
        ys.append(position["y"])
    print(
        f"{path.name} {name} tris={part['mesh']['TriangleCount']} "
        f"radius=({min(radii):.3f},{max(radii):.3f}) "
        f"y=({min(ys):.3f},{max(ys):.3f}) "
        f"inner<0.12={sum(radius < 0.12 for radius in radii)} "
        f"inner<0.18={sum(radius < 0.18 for radius in radii)}"
    )


tire_stats(root / "work/donor-geometry.json", "MUSTANGGT_KIT00_FRONT_TIRE_A")
tire_stats(root / "work/nascar-geometry.json", "SUPRA_KIT00_FRONT_TIRE_A")
tire_stats(root / "work/compiled-geometry.json", "MUSTANGGT_KIT00_FRONT_TIRE_A")

donor = json.loads((root / "work/donor-geometry.json").read_text())
vanilla = json.loads((root / "work/vanilla-mustang-geometry.json").read_text())
print("\n=== donor BASE mount points ===")
base = next(item for item in donor if item["name"] == "MUSTANGGT_BASE_A")
print(base["info"].get("MountPoints"))
print("donor GeometryInfo keys sample skipped")
print("vanilla BASE mount", next(item for item in vanilla if item["name"] == "MUSTANGGT_BASE_A")["info"].get("MountPoints"))
