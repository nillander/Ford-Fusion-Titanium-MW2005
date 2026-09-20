"""Extract the NASCAR chrome bumper grille and place it on the Fusion 2018 opening."""
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
alignment = json.loads((ROOT / "reference/alignment.json").read_text())
nascar = json.loads((ROOT / "work/nascar-geometry.json").read_text())
body = next(part for part in nascar if part["name"] == "SUPRA_KIT00_BODY_A")
verts = body["mesh"]["Vertices"]
indices = body["mesh"]["Indices"]

positions = []
normals = []
faces = []
for index in range(0, len(indices), 3):
    triangle = [verts[indices[index + offset]] for offset in range(3)]
    points = [vertex["Position"] for vertex in triangle]
    center_x = sum(point["x"] for point in points) / 3
    center_y = sum(point["y"] for point in points) / 3
    center_z = sum(point["z"] for point in points) / 3
    # Front bumper opening: the chrome bar sits low on the fascia.
    if center_x < 2.04 or center_z > 0.26 or abs(center_y) > 0.84:
        continue
    face = []
    for vertex in triangle:
        face.append(len(positions))
        position = vertex["Position"]
        normal = vertex["Normal"]
        positions.append((position["x"], position["y"], position["z"]))
        normals.append((normal["x"], normal["y"], normal["z"]))
    faces.append(face)

positions = np.array(positions, dtype=np.float32)
normals = np.array(normals, dtype=np.float32)
faces = np.array(faces, dtype=np.int32)

# Source GTA chrome grille, after the same alignment used by build_scene.
sx = alignment["longitudinal_scale"]
tx = alignment["forward_offset"]
tz = alignment["vertical_offset"]
source_x = np.array([2.32, 2.45]) * sx + tx
source_z = np.array([-0.22, 0.07]) + tz
source_center = np.array([source_x.mean(), 0.0, source_z.mean()], dtype=np.float32)
nascar_center = positions.mean(axis=0)
# Keep the NASCAR width; only slide it into the Fusion bumper cavity.
offset = source_center - nascar_center
offset[1] = 0.0
positions = positions + offset

out = ROOT / "work/source-meshes"
out.mkdir(parents=True, exist_ok=True)
vertex_dtype = np.dtype([
    ("Position", "<f4", 3),
    ("Normal", "<f4", 3),
    ("TexCoord0", "<f4", 2),
])
vertices = np.zeros(len(positions), dtype=vertex_dtype)
vertices["Position"] = positions
vertices["Normal"] = normals
span_y = max(float(np.ptp(positions[:, 1])), 1e-4)
span_z = max(float(np.ptp(positions[:, 2])), 1e-4)
vertices["TexCoord0"][:, 0] = (positions[:, 1] - positions[:, 1].min()) / span_y
vertices["TexCoord0"][:, 1] = (positions[:, 2] - positions[:, 2].min()) / span_z
np.savez_compressed(out / "nascar_front_grille.npz", vertices=vertices, indices=faces.reshape(-1))
report = {
    "triangles": int(len(faces)),
    "vertices": int(len(positions)),
    "offset": offset.tolist(),
    "bounds": {
        "min": positions.min(axis=0).tolist(),
        "max": positions.max(axis=0).tolist(),
    },
}
(ROOT / "reference/nascar-grille.json").write_text(json.dumps(report, indent=2))
print("NASCAR_GRILLE", report["triangles"], report["bounds"])
