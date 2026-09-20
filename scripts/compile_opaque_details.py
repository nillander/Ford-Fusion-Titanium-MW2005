"""Build opaque 3D grille bars and solid light shells from fusion-2017-dev."""
import json
import struct
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
alignment = json.loads((ROOT / "reference/alignment.json").read_text())
src = json.loads((ROOT / "reference/source-structure.json").read_text())
sx = alignment["longitudinal_scale"]
tx = alignment["forward_offset"]
tz = alignment["vertical_offset"]


def transform(positions, normals):
    out_pos = np.column_stack((
        positions[:, 1] * sx + tx,
        -positions[:, 0],
        positions[:, 2] + tz,
    ))
    out_n = np.column_stack((normals[:, 1] / sx, -normals[:, 0], normals[:, 2]))
    out_n /= np.maximum(np.linalg.norm(out_n, axis=1)[:, None], 1e-8)
    return out_pos, out_n


def load_keys(keys, side=None):
    positions = []
    normals = []
    uvs = []
    faces = []
    for key in keys:
        raw = np.load(ROOT / "work/source-meshes" / f"{key}.npz")
        pos, norms = transform(
            raw["vertices"]["Position"].astype(np.float32),
            raw["vertices"]["Normal"].astype(np.float32),
        )
        tex = raw["vertices"]["TexCoord0"].astype(np.float32)
        tris = raw["indices"].reshape(-1, 3).astype(np.int32)
        if side == "right":
            centers = pos[tris].mean(axis=1)
            tris = tris[centers[:, 1] < 0]
        elif side == "left":
            centers = pos[tris].mean(axis=1)
            tris = tris[centers[:, 1] > 0]
        if len(tris) == 0:
            continue
        used = np.unique(tris.reshape(-1))
        remap = {int(old): index + len(positions) for index, old in enumerate(used)}
        positions.extend(pos[used])
        normals.extend(norms[used])
        uvs.extend(tex[used])
        faces.extend([[remap[int(a)], remap[int(b)], remap[int(c)]] for a, b, c in tris])
    if not faces:
        return None
    return (
        np.array(positions, dtype=np.float32),
        np.array(normals, dtype=np.float32),
        np.array(uvs, dtype=np.float32),
        np.array(faces, dtype=np.int32),
    )


def box(minimum, maximum):
    x0, y0, z0 = minimum
    x1, y1, z1 = maximum
    corners = np.array([
        [x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0],
        [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1],
    ], dtype=np.float32)
    faces = np.array([
        [0, 1, 2], [0, 2, 3], [4, 6, 5], [4, 7, 6],
        [0, 4, 5], [0, 5, 1], [3, 2, 6], [3, 6, 7],
        [0, 3, 7], [0, 7, 4], [1, 5, 6], [1, 6, 2],
    ], dtype=np.int32)
    normals = np.zeros_like(corners)
    for a, b, c in faces:
        normal = np.cross(corners[b] - corners[a], corners[c] - corners[a])
        normal /= max(float(np.linalg.norm(normal)), 1e-8)
        normals[a] += normal
        normals[b] += normal
        normals[c] += normal
    normals /= np.maximum(np.linalg.norm(normals, axis=1)[:, None], 1e-8)
    uvs = np.zeros((len(corners), 2), dtype=np.float32)
    uvs[:, 0] = (corners[:, 1] - y0) / max(y1 - y0, 1e-4)
    uvs[:, 1] = (corners[:, 2] - z0) / max(z1 - z0, 1e-4)
    return corners, normals, uvs, faces


def join_meshes(pieces):
    positions = []
    normals = []
    uvs = []
    faces = []
    for pos, norms, tex, tris in pieces:
        if tris is None or len(tris) == 0:
            continue
        offset = len(positions)
        positions.extend(pos)
        normals.extend(norms)
        uvs.extend(tex)
        faces.extend(tris + offset)
    return (
        np.array(positions, dtype=np.float32),
        np.array(normals, dtype=np.float32),
        np.array(uvs, dtype=np.float32),
        np.array(faces, dtype=np.int32),
    )


def decimate(pos, norms, tex, tris, keep):
    if len(tris) <= keep:
        return pos, norms, tex, tris
    step = max(1, len(tris) // keep)
    subset = tris[::step][:keep]
    used = np.unique(subset.reshape(-1))
    remap = {int(old): index for index, old in enumerate(used)}
    return (
        pos[used],
        norms[used],
        tex[used],
        np.array([[remap[int(a)], remap[int(b)], remap[int(c)]] for a, b, c in subset], dtype=np.int32),
    )


def nascar_grille():
    raw = np.load(ROOT / "work/source-meshes/nascar_front_grille.npz")
    pos = raw["vertices"]["Position"].astype(np.float32)
    norms = raw["vertices"]["Normal"].astype(np.float32)
    tex = raw["vertices"]["TexCoord0"].astype(np.float32)
    faces = raw["indices"].reshape(-1, 3).astype(np.int32)
    return pos, norms, tex, faces


grade_keys = [
    item["key"] for item in src["meshes"]
    if item["origin"] == "fusion_rollcage"
    and item["dominant_bone"].lower() == "grade"
    and item["min"][1] > 2.2
]
head_keys = [
    "main_m000_g002",
    "main_m000_g003",
    "main_m000_g004",
    "main_m000_g005",
    "fusion_rollcage_m000_g007",
]
tail_keys = [
    "main_m000_g012",
    "main_m000_g100",
    "main_m000_g101",
    "fusion_rollcage_m000_g005",
]


def pack_part(name, material, pos, norms, tex, tris):
    vertex = np.column_stack((
        pos[:, 1], pos[:, 2], pos[:, 0],
        norms[:, 1], norms[:, 2], norms[:, 0],
    )).astype("<f4").tobytes()
    faces = b"".join(
        struct.pack(
            "<i4h6f", material, int(c), int(b), int(a), 0,
            float(tex[c][0]), float(tex[b][0]), float(tex[a][0]),
            float(1 - tex[c][1]), float(1 - tex[b][1]), float(1 - tex[a][1]),
        )
        for a, b, c in tris
    )
    return name, len(pos), len(tris), vertex, faces


def write_mwr(path, materials, export):
    def write_string(handle, text):
        payload = text.encode("ascii") + b"\0"
        handle.write(struct.pack("<i", len(payload)))
        handle.write(payload)

    with path.open("wb") as handle:
        handle.write(struct.pack("<3i", 0, len(materials), len(export)))
        for material in materials:
            write_string(handle, material)
        for name, vertex_count, face_count, _, _ in export:
            write_string(handle, name)
            handle.write(struct.pack("<2i16f", vertex_count, face_count, *np.eye(4).flatten()))
        for _, _, _, vertex, faces in export:
            handle.write(vertex)
            handle.write(faces)


def push_out(pos, norms, amount):
    return pos + norms * amount, norms


grille = nascar_grille()
head_right = load_keys(head_keys, side="right")
tail_right = load_keys(tail_keys, side="right")
head_both = load_keys(head_keys)
tail_both = load_keys(tail_keys)
if head_right is None or tail_right is None or head_both is None or tail_both is None:
    raise SystemError("missing light meshes")

# Sit details on the visible BODY shell (Shelby-style), not behind it on BASE.
# KIT00_BODY already has 27743 verts; stay under the signed 16-bit MW ceiling.
head_body = decimate(*head_both, 700)
tail_body = decimate(*tail_both, 600)
grille_body = decimate(*grille, 500)
grille_body = (grille_body[0] + np.array([0.025, 0.0, 0.0], dtype=np.float32), grille_body[1], grille_body[2], grille_body[3])
head_body = (head_body[0] + head_body[1] * 0.012, head_body[1], head_body[2], head_body[3])
tail_body = (tail_body[0] - np.array([0.012, 0.0, 0.0], dtype=np.float32), tail_body[1], tail_body[2], tail_body[3])
body_overlay = join_meshes([grille_body, head_body, tail_body])

export_grille = []
export_lights = []
export_body = []
for lod, ratio in (("A", 1.0), ("B", 0.5), ("C", 0.22), ("D", 0.09), ("E", 0.04)):
    keep = max(80, int(len(grille[3]) * ratio))
    part = decimate(*grille, keep)
    export_grille.append(pack_part(f"BASE_{lod}", 0, *part))
    keep_body = max(120, int(len(body_overlay[3]) * ratio))
    export_body.append(pack_part(f"KIT00_BODY_{lod}", 0, *decimate(*body_overlay, keep_body)))
    if lod in "ABC":
        keep_head = max(80, int(len(head_right[3]) * ratio))
        keep_tail = max(80, int(len(tail_right[3]) * ratio))
        head_part = decimate(*head_right, keep_head)
        tail_part = decimate(*tail_right, keep_tail)
        export_lights.append(pack_part(f"KIT00_RIGHT_HEADLIGHT_{lod}", 0, *head_part))
        export_lights.append(pack_part(f"KIT00_RIGHT_HEADLIGHT_GLASS_{lod}", 0, *head_part))
        export_lights.append(pack_part(f"KIT00_RIGHT_BRAKELIGHT_{lod}", 1, *tail_part))
        export_lights.append(pack_part(f"KIT00_RIGHT_BRAKELIGHT_GLASS_{lod}", 1, *tail_part))

write_mwr(ROOT / "work/opaque-grille.mwr", ["DULLPLASTIC/MUSTANGGT_MISC"], export_grille)
write_mwr(ROOT / "work/opaque-body.mwr", ["DULLPLASTIC/MUSTANGGT_MISC"], export_body)
write_mwr(
    ROOT / "work/opaque-lights.mwr",
    ["DULLPLASTIC/MUSTANGGT_KIT00_HEADLIG", "DULLPLASTIC/MUSTANGGT_KIT00_BRAKELI"],
    export_lights,
)
report = {
    "grade_keys": grade_keys,
    "head_keys": head_keys,
    "tail_keys": tail_keys,
    "grille_triangles": int(len(grille[3])),
    "head_triangles": int(len(head_right[3])),
    "tail_triangles": int(len(tail_right[3])),
    "body_overlay_triangles": int(len(body_overlay[3])),
    "body_overlay_bounds": {
        "min": body_overlay[0].min(axis=0).tolist(),
        "max": body_overlay[0].max(axis=0).tolist(),
    },
    "grille_bounds": {"min": grille[0].min(axis=0).tolist(), "max": grille[0].max(axis=0).tolist()},
}
(ROOT / "reference/opaque-details.json").write_text(json.dumps(report, indent=2))
print("OPAQUE_DETAILS", report)
