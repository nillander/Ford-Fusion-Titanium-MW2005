import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = json.loads((root / "reference/source-structure.json").read_text())
print("=== source wheel / hub / grille / boot badge meshes ===")
tokens = ("wheel", "hub", "grade", "parachoque", "boot", "placa", "exhaust", "grill")
for mesh in src["meshes"]:
    bone = mesh["dominant_bone"].lower()
    if not any(token in bone or token in mesh["key"] for token in tokens) and mesh["shader"] not in (19, 29, 30):
        continue
    if mesh["shader"] == 5 and "boot" in bone:
        continue
    minimum = mesh["min"]
    maximum = mesh["max"]
    print(
        f"{mesh['key']:28} origin={mesh['origin']:16} bone={mesh['dominant_bone']:20} "
        f"sh={mesh['shader']:2} tris={mesh['triangles']:5} "
        f"y=({minimum[1]:6.2f},{maximum[1]:6.2f}) z=({minimum[2]:6.2f},{maximum[2]:6.2f}) "
        f"x=({minimum[0]:6.2f},{maximum[0]:6.2f})"
    )

alignment = json.loads((root / "reference/alignment.json").read_text())
print("\n=== alignment ===")
print(alignment)

nascar = json.loads((root / "work/nascar-geometry.json").read_text())
for name in ("SUPRA_KIT00_FRONT_TIRE_A", "SUPRA_KIT00_FRONT_BRAKE_A", "SUPRA_KIT00_BODY_A"):
    part = next(item for item in nascar if item["name"] == name)
    verts = part["mesh"]["Vertices"]
    xs = [vertex["Position"]["x"] for vertex in verts]
    ys = [vertex["Position"]["y"] for vertex in verts]
    zs = [vertex["Position"]["z"] for vertex in verts]
    print(
        f"{name} tris={part['mesh']['TriangleCount']} "
        f"x=({min(xs):.2f},{max(xs):.2f}) y=({min(ys):.2f},{max(ys):.2f}) z=({min(zs):.2f},{max(zs):.2f})"
    )

body = next(item for item in nascar if item["name"] == "SUPRA_KIT00_BODY_A")
verts = body["mesh"]["Vertices"]
indices = body["mesh"]["Indices"]
print("\n=== NASCAR front-lower triangles ===")
count = 0
min_x = min_y = min_z = 99
max_x = max_y = max_z = -99
for index in range(0, len(indices), 3):
    triangle = [verts[indices[index + offset]]["Position"] for offset in range(3)]
    center_x = sum(point["x"] for point in triangle) / 3
    center_y = sum(point["y"] for point in triangle) / 3
    center_z = sum(point["z"] for point in triangle) / 3
    if center_x >= 2.05 and center_z <= 0.28:
        count += 1
        min_x = min(min_x, *(point["x"] for point in triangle))
        max_x = max(max_x, *(point["x"] for point in triangle))
        min_y = min(min_y, *(point["y"] for point in triangle))
        max_y = max(max_y, *(point["y"] for point in triangle))
        min_z = min(min_z, *(point["z"] for point in triangle))
        max_z = max(max_z, *(point["z"] for point in triangle))
print(f"tris={count} x=({min_x:.2f},{max_x:.2f}) y=({min_y:.2f},{max_y:.2f}) z=({min_z:.2f},{max_z:.2f})")
