"""Export Fusion lenses for attachment to the Shelby-based car's BASE solids.

Run in Blender. This deliberately bypasses the whole-car classifier, which
routes red lenses to BRAKELIGHT_GLASS slots absent from the Shelby catalogue.
Pass --front after Blender's -- separator to export the eight HEADLIGHT solids.
"""
import bpy
import bmesh
import json
import struct
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FRONT = '--front' in sys.argv
END = 'front' if FRONT else 'rear'
OUT = ROOT / f'versions/v2-mustang-shelby/work/fusion-{END}-lenses'
OUT.mkdir(parents=True, exist_ok=True)
alignment = json.loads((ROOT / 'reference/alignment.json').read_text())
source = json.loads((ROOT / 'reference/source-structure.json').read_text())
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Keep the proven MW material/hash pair; the default DDS now contains a bake
# from the Fusion 2018 source. --donor-atlas selects the prior 2010 artwork.
MATERIAL = '0x05BC3A3C/0x4B7D95B6'
UVS = {2: (.80, .90), 14: (.70, .40), 15: (.80, .90), 26: (.32, .09)}
SHADERS = (2, 15, 26) if FRONT else (14, 15)
BACKING_SHADER = 15 if FRONT else 14
TARGETS = {2: 700, 14: 1300, 15: 600 if FRONT else 300, 26: 180}
PROJECTION = None
if '--donor-atlas' not in sys.argv:
    projection_path = ROOT/'versions/v2-mustang-shelby/work/source-lamp-bake/projection.json'
    PROJECTION = json.loads(projection_path.read_text())['regions'][END]

def triangle_record(mesh, tri, offset, shader):
    order = list(tri.vertices)[::-1]
    indices = [offset + int(n) for n in order]
    if PROJECTION:
        frame = PROJECTION
        x, y, w, h = frame['atlas_rect']
        uv = []
        for n in order:
            p = mesh.vertices[n].co
            position = (p.x, abs(p.y), p.z)
            across = (np.dot(position, frame['right'])-frame['u_min'])/frame['width']
            height = (p.z-frame['z_min'])/frame['height']
            uv.append((x+w*float(np.clip(across, .001, .999)),
                       y+h*(1-float(np.clip(height, .001, .999)))))
        return struct.pack('<i4h6f', 0, *indices, 0,
                           *(p[0] for p in uv), *(p[1] for p in uv))
    if FRONT and shader in (2, 15):
        # Project the complete silver reflector region from the native AJM
        # atlas onto both Fusion lamps. A single white texel loses all detail.
        uv = []
        for n in order:
            p = mesh.vertices[n].co
            across = np.clip((abs(p.y) - .46) / (.854 - .46), 0., 1.)
            height = np.clip((p.z - .486) / (.631 - .486), 0., 1.)
            uv.append((.54 - .50 * across, .975 - .235 * height))
        return struct.pack('<i4h6f', 0, *indices, 0,
                           *(p[0] for p in uv), *(p[1] for p in uv))
    u, v = UVS[shader]
    return struct.pack('<i4h6f', 0, *indices, 0, u, u, u, v, v, v)

materials = {}
for shader, colour in ((2, (.9, .9, .9, 1)), (14, (.52, .01, .015, 1)),
                       (15, (.7, .7, .7, 1)), (26, (.9, .4, .02, 1))):
    mat = bpy.data.materials.new('Fusion_lamp_' + str(shader))
    mat.diffuse_color = colour
    materials[shader] = mat

records = []
report = []
for side, sign in (('LEFT', 1), ('RIGHT', -1)):
    pieces = []
    backing_points = {'main': [], 'fusion_exh_2': []}
    for shader in SHADERS:
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
            if FRONT:
                mask = ((centre[:, 0] > 1.65) & (centre[:, 2] > .4)
                        & (centre[:, 2] < .8) & (centre[:, 1] * sign > 0))
            else:
                mask = ((centre[:, 0] < -1.7) & (centre[:, 2] > .53)
                        & (centre[:, 2] < .84) & (centre[:, 1] * sign > 0))
            t = t[mask]
            if not len(t):
                continue
            used, inverse = np.unique(t, return_inverse=True)
            faces.extend((inverse.reshape(-1, 3) + len(positions)).tolist())
            positions.extend(p[used].tolist())
            if shader == BACKING_SHADER:
                backing_points[item['origin']].extend(p[used].tolist())
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

    # The GTA red geometry outlines each lamp and leaves areas for separate
    # reflector meshes. Close the inner and outer lamp volumes independently,
    # following their real contours, instead of adding rectangular boxes.
    backings = []
    for origin, points in backing_points.items():
        if not points:
            continue
        bm = bmesh.new()
        for point in np.unique(np.round(points, 5), axis=0):
            bm.verts.new((point[0] + (-.004 if FRONT else .004), point[1], point[2]))
        hull = bmesh.ops.convex_hull(bm, input=list(bm.verts), use_existing_faces=False)
        unused = [v for v in bm.verts if not v.link_faces]
        bmesh.ops.delete(bm, geom=unused, context='VERTS')
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        mesh = bpy.data.meshes.new(side + '_' + origin + '_closed_backing')
        bm.to_mesh(mesh)
        bm.free()
        backing_obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(backing_obj)
        bpy.context.view_layer.objects.active = backing_obj
        mod = backing_obj.modifiers.new('Compact closed backing', 'DECIMATE')
        mod.ratio = min(1., 160 / max(1, len(mesh.polygons)))
        bpy.ops.object.modifier_apply(modifier=mod.name)
        mesh = backing_obj.data
        mesh.calc_loop_triangles()
        backings.append(mesh)

    for lod, factor in (('A', 1), ('B', .5), ('C', .25), ('D', .1)):
        vertices, normals, triangles = [], [], []
        for original, shader, keys in pieces:
            obj = original.copy()
            obj.data = original.data.copy()
            bpy.context.collection.objects.link(obj)
            bpy.context.view_layer.objects.active = obj
            target = TARGETS[shader] * factor
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
            for tri in mesh.loop_triangles:
                # mwgc reverses the input order. Keep the source surface
                # winding and let Solidify supply its inward facing surface.
                triangles.append(triangle_record(mesh, tri, offset, shader))
            if lod == 'A':
                obj.name = 'FUSION_' + side + '_' + str(shader) + '_A'
                report.append({'side': side, 'shader_source': shader, 'sources': keys,
                               'vertices': len(mesh.vertices), 'triangles': len(mesh.loop_triangles)})
            else:
                bpy.data.objects.remove(obj, do_unlink=True)
        for mesh in backings:
            offset = len(vertices)
            vertices.extend(tuple(v.co) for v in mesh.vertices)
            normals.extend(tuple(v.normal) for v in mesh.vertices)
            for tri in mesh.loop_triangles:
                triangles.append(triangle_record(mesh, tri, offset, BACKING_SHADER))
        if len(vertices) >= 30000:
            raise RuntimeError(END + ' light exceeds MWR index budget')
        p, n = np.array(vertices), np.array(normals)
        packed = np.column_stack((p[:, 1], p[:, 2], p[:, 0], n[:, 1], n[:, 2], n[:, 0])).astype('<f4').tobytes()
        slot = 'HEADLIGHT' if FRONT else 'BRAKELIGHT'
        name = f'KIT00_{side}_{slot}_{lod}'
        records.append((name, len(vertices), len(triangles), packed, b''.join(triangles)))
        print(name, len(vertices), len(triangles), flush=True)
    for obj, _, _ in pieces:
        bpy.data.objects.remove(obj, do_unlink=True)

def write_string(handle, text):
    data = text.encode('ascii') + b'\0'
    handle.write(struct.pack('<i', len(data)))
    handle.write(data)

with (OUT / f'fusion-{END}-lenses.mwr').open('wb') as handle:
    handle.write(struct.pack('<3i', 0, 1, len(records)))
    write_string(handle, MATERIAL)
    for name, nv, nt, _, _ in records:
        write_string(handle, name)
        handle.write(struct.pack('<2i16f', nv, nt, *np.eye(4).flatten()))
    for _, _, _, vertices, faces in records:
        handle.write(vertices)
        handle.write(faces)
(OUT / 'export-report.json').write_text(json.dumps(report, indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / f'fusion-{END}-lenses.blend'))
print(f'FUSION_{END.upper()}_LENSES_READY')
