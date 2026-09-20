import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = json.loads((root / "reference/source-structure.json").read_text())
print("=== tire-shader meshes ===")
for mesh in src["meshes"]:
    if mesh["shader"] not in (12, 13, 17, 18, 19, 22, 23):
        continue
    print(
        f"{mesh['key']:24} bone={mesh['dominant_bone']:16} "
        f"sh={mesh['shader']:2} tris={mesh['triangles']:5} "
        f"x=({mesh['min'][0]:6.2f},{mesh['max'][0]:6.2f}) "
        f"y=({mesh['min'][1]:6.2f},{mesh['max'][1]:6.2f}) "
        f"z=({mesh['min'][2]:6.2f},{mesh['max'][2]:6.2f})"
    )
