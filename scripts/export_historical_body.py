"""Export only KIT00_BODY A-E from the 20/09 12:48 Blender checkpoint."""
import bpy
import json
import struct
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / 'versions/v2-mustang-shelby'
CHECKPOINT = V2 / 'blender/fusion-export-intermediate.blend1'
OUT = V2 / 'work/historical-body-1248'
OUT.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(CHECKPOINT))
mapping = json.loads((ROOT / 'reference/materials.json').read_text())

def write_string(handle, value):
    data = value.encode('ascii') + b'\0'
    handle.write(struct.pack('<i', len(data)))
    handle.write(data)

records = []
report = []
for lod in 'ABCDE':
    name = 'KIT00_BODY_' + lod
    matches = [o for o in bpy.data.objects if o.type == 'MESH' and o.name == name]
    if len(matches) != 1:
        raise RuntimeError(f'Expected one {name}, found {len(matches)}')
    obj = matches[0]
    mesh = obj.data
    mesh.calc_loop_triangles()
    uv_layer = mesh.uv_layers.active.data
    vertices = np.array([(*v.co, *v.normal) for v in mesh.vertices], dtype=np.float32)
    vertex_bytes = vertices[:, [1, 2, 0, 4, 5, 3]].astype('<f4').tobytes()
    faces = []
    used_materials = set()
    for tri in mesh.loop_triangles:
        order = list(tri.vertices)[::-1]
        loops = list(tri.loops)[::-1]
        material = mesh.materials[tri.material_index]
        source_shader = int(material['source_shader'])
        used_materials.add(source_shader)
        tex = [uv_layer[index].uv for index in loops]
        faces.append(struct.pack('<i4h6f', source_shader, *order, 0,
                                 *(float(t.x) for t in tex),
                                 *(float(1.0 - t.y) for t in tex)))
    records.append((name, len(mesh.vertices), len(faces), vertex_bytes, b''.join(faces)))
    report.append({'part': name, 'vertices': len(mesh.vertices),
                   'triangles': len(faces), 'materials': sorted(used_materials)})

with (OUT / 'historical-body.mwr').open('wb') as handle:
    handle.write(struct.pack('<3i', 0, len(mapping), len(records)))
    for material in mapping:
        write_string(handle, material['shader'] + '/' + material['texture'])
    for name, vertex_count, triangle_count, _, _ in records:
        write_string(handle, name)
        handle.write(struct.pack('<2i16f', vertex_count, triangle_count,
                                 *np.eye(4).flatten()))
    for _, _, _, vertices, faces in records:
        handle.write(vertices)
        handle.write(faces)
(OUT / 'export-report.json').write_text(json.dumps(report, indent=2))
print('HISTORICAL_BODY_READY', report)
