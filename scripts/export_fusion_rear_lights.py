"""Export the Fusion's actual rear lenses into Shelby's existing light slots.

Run in Blender. This deliberately bypasses the whole-car classifier, which
routes red lenses to BRAKELIGHT_GLASS slots absent from the Shelby catalogue.
Only the eight BRAKELIGHT solids are emitted; all other installed parts survive.
"""
import bpy
import bmesh
import json
import struct
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'versions/v2-mustang-shelby/work/fusion-rear-lenses'
OUT.mkdir(parents=True, exist_ok=True)
alignment = json.loads((ROOT / 'reference/alignment.json').read_text())
source = json.loads((ROOT / 'reference/source-structure.json').read_text())
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Fully opaque atlas already present in the installed TPK. Red and silver
# occupy separate quadrants; no transparent GTA lens texture is reused.
MATERIAL = 'DULLPLASTIC/0x590566EC'
UVS = {14: (.75, .75), 15: (.25, .75)}
materials = {}
for shader, colour in ((14, (.52, .01, .015, 1)), (15, (.7, .7, .7, 1))):
    mat = bpy.data.materials.new('Fusion_red' if shader == 14 else 'Fusion_reverse')
    mat.diffuse_color = colour
    materials[shader] = mat

records = []
report = []
for side, sign in (('LEFT', 1), ('RIGHT', -1)):
    pieces = []
    for shader in (14, 15):
        positions, faces, keys = [], [], []
        for item in source['meshes']:
            if item['origin'] not in ('main', 'fusion_exh_2') or item['shader'] != shader:
                continue
            raw = np.load(ROOT / 'work/source-meshes' / (item['key'] + '.npz'))
            p = raw['vertices']['Position']
            p = np.column_stack((p[:, 1] * alignment['longitudinal_scale'] + alignment['forward_offset'],
                                 -p[:, 0], p[:, 2] + alignment['vertical_offset']))
            t = raw['indices'].reshape(-1, 3)
            centre = p[t].mean(axis=1)
            # Some GTA drawables combine lenses with mirrors and indicators.
            # Select rear lamp faces, not a whole mixed drawable by its centre.
            mask = ((centre[:, 0] < -1.7) & (centre[:, 2] > .53)
                    & (centre[:, 2] < .84) & (centre[:, 1] * sign > 0))
            t = t[mask]
            if not len(t):
                continue
            used, inverse = np.unique(t, return_inverse=True)
            faces.extend((inverse.reshape(-1, 3) + len(positions)).tolist())
            positions.extend(p[used].tolist())
            keys.append(item['key'])
        if not faces:
            raise RuntimeError('Missing Fusion lens: ' + side + '/' + str(shader))
        mesh = bpy.data.meshes.new(side + '_' + str(shader))
        mesh.from_pydata(positions, [], faces)
        mesh.materials.append(materials[shader])
        mesh.update()
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=.00001)
        # Adjacent source sections repeat some exactly coincident triangles.
        seen, duplicates = set(), []
        bm.verts.index_update()
        for face in bm.faces:
            key = tuple(sorted(v.index for v in face.verts))
            if key in seen:
                duplicates.append(face)
            else:
                seen.add(key)
        bmesh.ops.delete(bm, geom=duplicates, context='FACES_ONLY')
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        bm.to_mesh(mesh)
        bm.free()
        obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(obj)
        pieces.append((obj, shader, keys))

    for lod, factor in (('A', 1), ('B', .5), ('C', .25), ('D', .1)):
        vertices, normals, triangles = [], [], []
        for original, shader, keys in pieces:
            obj = original.copy()
            obj.data = original.data.copy()
            bpy.context.collection.objects.link(obj)
            bpy.context.view_layer.objects.active = obj
            target = (1300 if shader == 14 else 300) * factor
            mod = obj.modifiers.new('Preserve lens silhouette', 'DECIMATE')
            mod.ratio = min(1., target / max(1, len(obj.data.polygons)))
            mod.use_collapse_triangulate = True
            bpy.ops.object.modifier_apply(modifier=mod.name)
            # A physical inner surface and closed rim make the lens visible
            # from either side. This follows the Fusion silhouette, not a box.
            mod = obj.modifiers.new('Opaque lens thickness', 'SOLIDIFY')
            mod.thickness = .003
            mod.offset = -1
            mod.use_rim = True
            bpy.ops.object.modifier_apply(modifier=mod.name)
            mesh = obj.data
            mesh.calc_loop_triangles()
            offset = len(vertices)
            vertices.extend(tuple(v.co) for v in mesh.vertices)
            normals.extend(tuple(v.normal) for v in mesh.vertices)
            u, v = UVS[shader]
            for tri in mesh.loop_triangles:
                # mwgc reverses the input order. Keep the source surface
                # winding and let Solidify supply its inward facing surface.
                i = [offset + int(n) for n in tri.vertices][::-1]
                triangles.append(struct.pack('<i4h6f', 0, *i, 0, u, u, u, v, v, v))
            if lod == 'A':
                obj.name = 'FUSION_' + side + '_' + str(shader) + '_A'
                report.append({'side': side, 'shader_source': shader, 'sources': keys,
                               'vertices': len(mesh.vertices), 'triangles': len(mesh.loop_triangles)})
            else:
                bpy.data.objects.remove(obj, do_unlink=True)
        if len(vertices) >= 30000:
            raise RuntimeError('Rear light exceeds MWR index budget')
        p, n = np.array(vertices), np.array(normals)
        packed = np.column_stack((p[:, 1], p[:, 2], p[:, 0], n[:, 1], n[:, 2], n[:, 0])).astype('<f4').tobytes()
        name = f'KIT00_{side}_BRAKELIGHT_{lod}'
        records.append((name, len(vertices), len(triangles), packed, b''.join(triangles)))
        print(name, len(vertices), len(triangles), flush=True)
    for obj, _, _ in pieces:
        bpy.data.objects.remove(obj, do_unlink=True)

def write_string(handle, text):
    data = text.encode('ascii') + b'\0'
    handle.write(struct.pack('<i', len(data)))
    handle.write(data)

with (OUT / 'fusion-rear-lenses.mwr').open('wb') as handle:
    handle.write(struct.pack('<3i', 0, 1, len(records)))
    write_string(handle, MATERIAL)
    for name, nv, nt, _, _ in records:
        write_string(handle, name)
        handle.write(struct.pack('<2i16f', nv, nt, *np.eye(4).flatten()))
    for _, _, _, vertices, faces in records:
        handle.write(vertices)
        handle.write(faces)
(OUT / 'export-report.json').write_text(json.dumps(report, indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / 'fusion-rear-lenses.blend'))
print('FUSION_REAR_LENSES_READY')
