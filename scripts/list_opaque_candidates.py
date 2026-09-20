import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = json.loads((root / "reference/source-structure.json").read_text())
print("=== shaders ===")
for index, shader in enumerate(src["shaders"]):
    print(index, shader.get("preset"), shader.get("textures", {}).get("diffusesampler"))

want_bones = ("grade", "grill", "headlight", "taillight", "indicator", "hub_", "wheel")
want_shaders = {2, 4, 7, 8, 13, 14, 15, 17, 18, 19, 26, 29, 30}
print("=== candidate meshes ===")
for mesh in src["meshes"]:
    bone = mesh["dominant_bone"].lower()
    key = mesh["key"].lower()
    hit_bone = any(token in bone or token in key for token in want_bones)
    hit_shader = mesh["shader"] in want_shaders
    if not (hit_bone or (hit_shader and mesh["origin"] != "fusion_exh_2")):
        continue
    if "steering" in bone:
        continue
    print(
        f"{mesh['key']:28} origin={mesh['origin']:16} bone={mesh['dominant_bone']:16} "
        f"sh={mesh['shader']:2} tris={mesh['triangles']:5} "
        f"x=({mesh['min'][0]:6.2f},{mesh['max'][0]:6.2f}) "
        f"y=({mesh['min'][1]:6.2f},{mesh['max'][1]:6.2f}) "
        f"z=({mesh['min'][2]:6.2f},{mesh['max'][2]:6.2f})"
    )
