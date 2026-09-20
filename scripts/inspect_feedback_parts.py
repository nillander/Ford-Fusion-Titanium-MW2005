import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
compiled = json.loads((root / "work/compiled-geometry.json").read_text())
print("=== compiled parts of interest ===")
keys = ("WHEEL", "TIRE", "BRAKE", "WINDOW", "BODY_A", "BASE_A", "INTERIOR_A")
for part in compiled:
    name = part["name"]
    if not any(key in name for key in keys):
        continue
    info = part["info"]
    mesh = part["mesh"]
    bound_min = info["BoundMin"]
    bound_max = info["BoundMax"]
    shaders = [hex(shader) for shader in info["Shaders"]]
    print(
        f"{name:50} tris={mesh['TriangleCount']:6} verts={len(mesh['Vertices']):6} "
        f"sh={shaders} x=({bound_min['x']:.2f},{bound_max['x']:.2f}) "
        f"z=({bound_min['z']:.2f},{bound_max['z']:.2f})"
    )

src = json.loads((root / "reference/source-structure.json").read_text())
want = {7, 8, 13, 16, 17, 19, 29, 30}
print("=== source meshes of interest ===")
for mesh in src["meshes"]:
    if mesh["shader"] not in want:
        continue
    minimum = mesh["min"]
    maximum = mesh["max"]
    print(
        f"{mesh['key']:28} origin={mesh['origin']:16} bone={mesh['dominant_bone']:16} "
        f"sh={mesh['shader']:2} tris={mesh['triangles']:5} "
        f"x=({minimum[0]:6.2f},{maximum[0]:6.2f}) y=({minimum[1]:6.2f},{maximum[1]:6.2f}) "
        f"z=({minimum[2]:6.2f},{maximum[2]:6.2f})"
    )
print("--- shaders ---")
for index, shader in enumerate(src["shaders"]):
    print(index, shader["preset"], shader["textures"].get("diffusesampler"))
