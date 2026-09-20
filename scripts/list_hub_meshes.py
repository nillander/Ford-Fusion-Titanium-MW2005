import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = json.loads((root / "reference/source-structure.json").read_text())
print("=== shaders ===")
for index, shader in enumerate(src["shaders"]):
    print(index, shader.get("preset"), shader.get("textures", {}).get("diffusesampler"))
print("=== hub/wheel/grade meshes ===")
for mesh in src["meshes"]:
    bone = mesh["dominant_bone"].lower()
    if any(token in bone for token in ("hub_", "wheelmesh", "wheel_l", "wheel_r", "grade", "grill")):
        if "steering" in bone:
            continue
        print(
            f"{mesh['key']:24} bone={mesh['dominant_bone']:16} "
            f"sh={mesh['shader']:2} tris={mesh['triangles']:5} origin={mesh['origin']}"
        )
