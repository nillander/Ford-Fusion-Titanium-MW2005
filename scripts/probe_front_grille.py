"""Count installed BASE triangles in the Fusion front-grille cavity."""
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
geo = root / "release/MUSTANGGT/GEOMETRY.BIN"
out = root / "work/mustang-geometry.json"
exe = root / "tools/mwgc/InspectGeometry.exe"
if not out.exists() or out.stat().st_mtime < geo.stat().st_mtime:
    subprocess.check_call([str(exe), str(geo), str(out)])
data = json.loads(out.read_text())
base = next(part for part in data if part["name"] == "MUSTANGGT_BASE_A")
verts = base["mesh"]["Vertices"]
indices = base["mesh"]["Indices"]
front = 0
for index in range(0, len(indices), 3):
    triangle = [verts[indices[index + offset]]["Position"] for offset in range(3)]
    center_x = sum(point["x"] for point in triangle) / 3
    center_y = sum(point["y"] for point in triangle) / 3
    center_z = sum(point["z"] for point in triangle) / 3
    if center_x > 2.05 and abs(center_y) < 0.7 and center_z < 0.75:
        front += 1
print("BASE_A tris", base["mesh"]["TriangleCount"], "front_cavity", front)
print("shaders", [hex(shader) for shader in base["info"]["Shaders"]])
print("textures", [hex(texture) for texture in base["info"]["Textures"]])
