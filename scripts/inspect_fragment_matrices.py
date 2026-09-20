"""Inspect native YFT matrix data omitted by szio 1.3's high-level adapter."""
from pathlib import Path
import numpy as np
import pymateria.gta5.gen8 as pmg8

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "work/source-extracted/x64/vehicles.extracted/fusion_hi.yft"
fragment = pmg8.Fragment.import_rsc(path).result

print("fragment", type(fragment))
for name in ("shared_matrix_set", "drawable", "physics_lod_group"):
    value = getattr(fragment, name, None)
    print(name, type(value), value is None)

matrix_set = fragment.shared_matrix_set
if matrix_set is not None:
    print("matrix_set skinned", matrix_set.is_skinned, "count", len(matrix_set.matrices))
    for i, matrix in enumerate(matrix_set.matrices):
        try:
            arr = np.asarray(matrix)
        except Exception as exc:
            print(i, type(matrix), "convert error", repr(exc), dir(matrix))
            continue
        print(i, arr.shape, arr.tolist())

lod = fragment.physics_lod_group.high_lod
print("link attachments", len(lod.link_attachments))
skel = fragment.drawable.skeleton
print("skeleton fields", [n for n in dir(skel) if not n.startswith("_")])
native_bones = skel.get_bones()
print("native bones", len(native_bones), "fields", [n for n in dir(native_bones[0]) if not n.startswith("_")])
tag_to_bone = {b.id: (i, getattr(b, "name", "?"),
                      np.asarray(getattr(b, "default_translation", ())).tolist(),
                      np.asarray(getattr(b, "default_rotation", ())).tolist())
               for i, b in enumerate(native_bones)}
for i, group in enumerate(lod.groups):
    print("group", i, lod.group_names[i], "parent", group.parent_group_pointer_index)
for i, child in enumerate(lod.children):
    print("child", i, "tag", child.bone_id, "bone", tag_to_bone.get(child.bone_id),
          "group", child.owner_group_pointer_index)
for i, matrix in enumerate(lod.link_attachments):
    print("link", i, np.asarray(matrix).shape, np.asarray(matrix).tolist())
