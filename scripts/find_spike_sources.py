import bpy
from pathlib import Path

root=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(root/'blender/source-aligned.blend'))
targets={
    'front_a':(.633884966,1.17401016,.68120414),
    'front_b':(.6234016,1.17401016,-.7023255),
    'front_tip':(1.17165768,1.92619145,.456104815),
    'rear_tip':(1.381003,-1.25311542,0.0),
}
for label,target in targets.items():
    matches=[]
    for o in bpy.data.objects:
        if o.type!='MESH' or 'source_shader' not in o:continue
        best=min((sum((v.co[j]-target[j])**2 for j in range(3)),i) for i,v in enumerate(o.data.vertices))
        matches.append((best[0],o.name,o.get('source_key'),o.get('source_shader'),o.get('dominant_bone'),len(o.data.polygons),best[1]))
    print(label,sorted(matches)[:8])
