"""Render the 2018 source lamp assemblies into a projection atlas in Blender.

No 2010 artwork or generated reference image is used. Geometry is taken from
the extracted GTA source. GTA materials are approximated for a static bake;
the final MW texture is completely opaque. Run with Blender --background.
"""
import bpy
import bmesh
import hashlib
import json
from pathlib import Path
import numpy as np
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'versions/v2-mustang-shelby/work/source-lamp-bake'
OUT.mkdir(parents=True, exist_ok=True)
source = json.loads((ROOT/'reference/source-structure.json').read_text())
alignment = json.loads((ROOT/'reference/alignment.json').read_text())
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 96
scene.cycles.use_denoising = True
scene.cycles.seed = 2018
scene.render.threads_mode = 'AUTO'
gpu = []
prefs = bpy.context.preferences.addons['cycles'].preferences
for backend in ('OPTIX', 'CUDA'):
    try:
        prefs.compute_device_type = backend
        prefs.get_devices()
        gpu = [d.name for d in prefs.devices if d.type == backend]
        if gpu:
            for d in prefs.devices:
                d.use = d.type == backend
            scene.cycles.device = 'GPU'
            break
    except Exception:
        continue
print('BAKE_GPU', gpu, flush=True)
scene.render.resolution_x = 1024
scene.render.resolution_y = 512
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.film_transparent = False
scene.view_settings.view_transform = 'AgX'
scene.world = bpy.data.worlds.new('Lamp studio')
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (.055, .065, .085, 1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .35

def mat(name, rgb, metal=0., rough=.3, emit=0., transparent=0.):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bs = m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*rgb, 1)
    bs.inputs['Metallic'].default_value = metal
    bs.inputs['Roughness'].default_value = rough
    bs.inputs['Emission Color'].default_value = (*rgb, 1)
    bs.inputs['Emission Strength'].default_value = emit
    if transparent:
        tr = m.node_tree.nodes.new('ShaderNodeBsdfTransparent')
        tr.inputs[0].default_value = (*rgb, 1)
        mix = m.node_tree.nodes.new('ShaderNodeMixShader')
        mix.inputs[0].default_value = transparent
        m.node_tree.links.new(bs.outputs[0], mix.inputs[1])
        m.node_tree.links.new(tr.outputs[0], mix.inputs[2])
        m.node_tree.links.new(mix.outputs[0], m.node_tree.nodes['Material Output'].inputs['Surface'])
    return m

materials = {
    'housing': mat('Source dark housing', (.015, .019, .025), .15, .26),
    'chrome': mat('Source chrome reflector', (.65, .69, .74), .9, .20),
    'white': mat('Source white light elements', (.7, .77, .85), .3, .19, .10),
    'red': mat('Source red lamp elements', (.36, .002, .003), .45, .24, .18),
    'redcover': mat('Source red lens', (.58, .045, .055), .05, .24, 0., .96),
    'clearcover': mat('Source clear rear insert', (.8, .83, .86), .05, .2, 0., .99),
    'amber': mat('Source amber indicator', (.65, .19, .006), .3, .24, .12),
}

def material_for(end, shader):
    if shader == 6: return materials['housing']
    if shader == 7: return materials['chrome']
    if shader == 14: return materials['redcover']
    if shader == 15: return materials['clearcover']
    if shader == 26: return materials['amber']
    return materials['white' if end == 'front' else 'red']

def aligned(p):
    return np.column_stack((p[:, 1]*alignment['longitudinal_scale']+alignment['forward_offset'],
                            -p[:, 0], p[:, 2]+alignment['vertical_offset']))

manifest = {'gpu': gpu, 'renderer': 'Cycles', 'samples': scene.cycles.samples,
            'source': 'source/fusion-2017-dev/fusion/dlc.rpf', 'regions': {}}
assemblies = {}
for end in ('front', 'rear'):
    objects, included, points = [], [], []
    for item in source['meshes']:
        shader = item['shader']
        if item['origin'] not in ('main', 'fusion_exh_2'):
            continue
        if shader not in ((2, 6, 7, 26) if end == 'front' else (4, 6, 7, 14, 15)):
            continue
        raw = np.load(ROOT/'work/source-meshes'/(item['key']+'.npz'))
        p = aligned(raw['vertices']['Position'])
        triangles = raw['indices'].reshape(-1, 3)
        centres = p[triangles].mean(axis=1)
        if end == 'front':
            mask = ((centres[:, 0] > 1.65) & (centres[:, 0] < 2.30) &
                    (centres[:, 1] > .44) & (centres[:, 1] < .88) &
                    (centres[:, 2] > .47) & (centres[:, 2] < .65))
        else:
            mask = ((centres[:, 0] < -1.7) & (centres[:, 1] > .34) &
                    (centres[:, 1] < .83) & (centres[:, 2] > .635) &
                    (centres[:, 2] < .796))
            # These source housings also contain unrelated trunk trim.
            if shader == 6 and item['origin'] == 'main' and item['key'] != 'main_m000_g044':
                continue
        triangles = triangles[mask]
        if not len(triangles):
            continue
        used, inverse = np.unique(triangles, return_inverse=True)
        mesh = bpy.data.meshes.new(end+'_'+item['key'])
        mesh.from_pydata(p[used].tolist(), [], inverse.reshape(-1, 3).tolist())
        mesh.update()
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=.00001)
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        bm.to_mesh(mesh)
        bm.free()
        mesh.polygons.foreach_set('use_smooth', [True]*len(mesh.polygons))
        mesh.materials.append(material_for(end, shader))
        obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(obj)
        obj.hide_render = True
        objects.append(obj)
        points.extend(p[used].tolist())
        included.append({'key': item['key'], 'source_shader': shader, 'triangles': len(triangles)})
    assemblies[end] = objects
    # Oblique projection captures the side wrap of each Fusion lamp. Mirror y
    # when applying this same atlas to the other side of the vehicle.
    outward = np.array((.8, .6, 0.) if end == 'front' else (-.8, .6, 0.))
    right = np.cross(-outward, (0., 0., 1.))
    p = np.array(points)
    horizontal = p@right
    umin, umax = float(horizontal.min()), float(horizontal.max())
    width = (umax-umin)*1.08
    ucentre = (umin+umax)/2
    zcentre = float((p[:, 2].min()+p[:, 2].max())/2)
    height = width/2
    target = right*ucentre + outward*float(np.mean(p@outward))
    target[2] = zcentre
    manifest['regions'][end] = {'right': right.tolist(), 'outward': outward.tolist(),
        'u_min': ucentre-width/2, 'z_min': zcentre-height/2, 'width': width, 'height': height,
        'atlas_rect': [0., 0. if end == 'front' else .5, 1., .5], 'sources': included}
    bpy.ops.object.camera_add(location=target+outward*4)
    camera = bpy.context.object
    camera.name = end+'_bake_camera'
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = width
    camera.rotation_euler = (Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
    lights = []
    for along, across, up, energy, size in ((1., -.5, .7, 80, .65), (1., .65, .1, 50, .5), (.1, -.1, .9, 35, .45)):
        location = target+outward*along+right*across+np.array((0, 0, up))
        bpy.ops.object.light_add(type='AREA', location=location)
        light = bpy.context.object
        light.data.energy = energy * (.4 if end == 'rear' else 1.)
        light.data.shape = 'RECTANGLE'
        light.data.size = size
        light.data.size_y = size*.25
        light.rotation_euler = (Vector(target)-light.location).to_track_quat('-Z','Y').to_euler()
        lights.append(light)
    for obj in objects: obj.hide_render = False
    scene.camera = camera
    scene.render.filepath = str(OUT/(end+'-source-bake.png'))
    bpy.ops.render.render(write_still=True)
    for obj in objects+lights: obj.hide_render = True

manifest['source_sha256'] = hashlib.sha256((ROOT/manifest['source']).read_bytes()).hexdigest()
(OUT/'projection.json').write_text(json.dumps(manifest, indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'source-lamp-bake.blend'))
print('SOURCE_LAMP_BAKE_READY', flush=True)
