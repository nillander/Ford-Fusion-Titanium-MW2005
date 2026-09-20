import bpy
from pathlib import Path

root=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(root/'blender/source-aligned.blend'))
for o in bpy.data.objects:
    if o.type!='MESH' or 'source_shader' not in o or 'parachoquetras' not in str(o.get('dominant_bone', '')).lower():
        continue
    xs=[v.co.x for v in o.data.vertices]
    ys=[v.co.y for v in o.data.vertices]
    zs=[v.co.z for v in o.data.vertices]
    print('shader', o.get('source_shader'), o.name, o.get('source_key'), o.get('dominant_bone'), len(o.data.polygons),
          'bounds', round(min(xs),3),round(max(xs),3),round(min(ys),3),round(max(ys),3),round(min(zs),3),round(max(zs),3))
