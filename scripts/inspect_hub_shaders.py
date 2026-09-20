import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = json.loads((root / "reference/source-structure.json").read_text())
print("=== shaders 18,22,23 and hub-like ===")
for mesh in src["meshes"]:
    if mesh["shader"] not in (12, 13, 17, 18, 22, 23) and "hub" not in mesh["dominant_bone"].lower():
        continue
    minimum = mesh["min"]
    maximum = mesh["max"]
    print(
        f"{mesh['key']:28} origin={mesh['origin']:16} bone={mesh['dominant_bone']:20} "
        f"sh={mesh['shader']:2} tris={mesh['triangles']:5} "
        f"x=({minimum[0]:6.2f},{maximum[0]:6.2f}) y=({minimum[1]:6.2f},{maximum[1]:6.2f}) "
        f"z=({minimum[2]:6.2f},{maximum[2]:6.2f})"
    )

nascar = json.loads((root / "work/nascar-geometry.json").read_text())
tire = next(item for item in nascar if item["name"] == "SUPRA_KIT00_FRONT_TIRE_A")
print("\nNASCAR tire shaders", [hex(shader) for shader in tire["info"]["Shaders"]])
print("NASCAR tire textures", [hex(texture) for texture in tire["info"]["Textures"]])
print("NASCAR tire groups", tire["mesh"]["Groups"])
