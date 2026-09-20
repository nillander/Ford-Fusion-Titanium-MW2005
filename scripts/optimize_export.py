import bpy
import bmesh
import json
import math
import os
import struct
import numpy as np
from pathlib import Path
from collections import defaultdict
from mathutils.kdtree import KDTree

PROJECT=Path(__file__).resolve().parents[1]
# V2 writes every generated artifact under its own root but deliberately reads
# the immutable source scene and extracted GTA meshes from the project root.
ROOT=Path(os.environ.get('FUSION_OUTPUT_ROOT', str(PROJECT))).resolve()
INPUT_ROOT=PROJECT
for directory in ('work','reference','blender','preview'):
    (ROOT/directory).mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(INPUT_ROOT/'blender/source-aligned.blend'))
mapping=json.loads((INPUT_ROOT/'reference/materials.json').read_text())
grille_material_index=next(i for i,m in enumerate(mapping) if m['texture']=='MUSTANGGT_GRILLE')
# Official MW cars layer the regular glass shader with a separate tint shader.
# Keep this extra material local to the MWR export; its texture is global and
# intentionally absent from the car's TPK.
window_tint_index=len(mapping)
mapping.append({'shader':'0x3ed70c43','texture':'0x1b049702'})
replacement_materials={m['source']:i for i,m in enumerate(mapping) if m.get('source','').startswith('codex_')}
# Codex window export is keyed to the Mustang donor catalog: FRONT/REAR
# WINDOW only. The Ford GT catalog splits side glass into extra slots and
# would drop the official dual-layer tint construction.
donor=json.loads((ROOT/'work/donor-geometry.json').read_text())
names={x['name'].removeprefix('MUSTANGGT_') for x in donor}
names.update('KIT00_LEFT_SIDE_MIRROR_'+lod for lod in 'ABCDE')
groups=defaultdict(list)
alignment=json.loads((INPUT_ROOT/'reference/alignment.json').read_text())

def replacement_object(name,vertices,faces,material_key,bone):
    mesh=bpy.data.meshes.new(name+'_mesh')
    mesh.from_pydata(vertices,[],faces);mesh.update()
    uv=mesh.uv_layers.new(name='UVMap')
    for loop in mesh.loops:uv.data[loop.index].uv=(.5,.5)
    mat=bpy.data.materials.new(name+'_material')
    mat['source_shader']=replacement_materials[material_key]
    mesh.materials.append(mat)
    obj=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(obj)
    obj['source_shader']=replacement_materials[material_key]
    obj['dominant_bone']='codex_'+bone
    return obj

def box(name,center,size,material,bone):
    x,y,z=center;dx,dy,dz=(v/2 for v in size)
    v=[(x-dx,y-dy,z-dz),(x+dx,y-dy,z-dz),(x+dx,y+dy,z-dz),(x-dx,y+dy,z-dz),
       (x-dx,y-dy,z+dz),(x+dx,y-dy,z+dz),(x+dx,y+dy,z+dz),(x-dx,y+dy,z+dz)]
    f=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    return replacement_object(name,v,f,material,bone)

def prism_yz(name,x,depth,points,material,bone):
    points=list(points)
    area=sum(points[i][0]*points[(i+1)%len(points)][1]-points[(i+1)%len(points)][0]*points[i][1] for i in range(len(points)))
    if area<0:points.reverse()
    n=len(points);rear=x-depth/2;front=x+depth/2
    v=[(rear,y,z) for y,z in points]+[(front,y,z) for y,z in points]
    f=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
    for i in range(n):
        j=(i+1)%n;f.append((i,j,n+j,n+i))
    return replacement_object(name,v,f,material,bone)

def rod_xz(name,p0,p1,y,thickness,depth,material,bone):
    x0,z0=p0;x1,z1=p1;dx=x1-x0;dz=z1-z0;length=max(math.hypot(dx,dz),1e-6)
    nx=-dz/length*thickness/2;nz=dx/length*thickness/2;d=depth/2
    corners=[(x0-nx,z0-nz),(x1-nx,z1-nz),(x1+nx,z1+nz),(x0+nx,z0+nz)]
    v=[(x,y-d,z) for x,z in corners]+[(x,y+d,z) for x,z in corners]
    f=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    return replacement_object(name,v,f,material,bone)

def cylinder(name,center,length,radius,axis,material,bone,segments=16):
    x,y,z=center;v=[]
    for side in (-1,1):
        for i in range(segments):
            a=2*math.pi*i/segments;c=math.cos(a)*radius;s=math.sin(a)*radius
            if axis=='x':v.append((x+side*length/2,y+c,z+s))
            else:v.append((x+c,y+side*length/2,z+s))
    if axis=='x':v.extend(((x-length/2,y,z),(x+length/2,y,z)))
    else:v.extend(((x,y-length/2,z),(x,y+length/2,z)))
    f=[]
    for i in range(segments):
        j=(i+1)%segments;f.append((i,j,segments+j,segments+i))
        f.append((2*segments,i,j));f.append((2*segments+1,segments+j,segments+i))
    return replacement_object(name,v,f,material,bone)

# Upper grille: a solid backing plus physical bars and perimeter.  It sits a
# few millimetres outside the bumper to avoid depth fighting with old surfaces.
for i,(z,width) in enumerate(((.355,.86),(.39,.98),(.425,1.04),(.46,1.05),(.495,1.02),(.53,.92),(.565,.68))):
    box(f'CODEX_UPPER_GRILLE_BAR_{i}',(2.366,0,z),(.018,width,.01),'codex_dark','upper_grille')
    # MW's old renderer is much more reliable when the grille has a second
    # opaque layer behind the visible bars, equivalent to its dual-layer glass
    # construction.  The 6 mm offset prevents depth fighting.
    box(f'CODEX_UPPER_GRILLE_BACK_{i}',(2.360,0,z),(.012,width,.009),'codex_dark','upper_grille')

# Lower grille and fog lamps.
lower=[(-.58,.115),(-.52,.275),(.52,.275),(.58,.115),(.48,.085),(-.48,.085)]
prism_yz('CODEX_LOWER_GRILLE_BACK',2.37,.025,lower,'codex_dark','lower_grille')
prism_yz('CODEX_LOWER_GRILLE_REAR',2.364,.014,lower,'codex_dark','lower_grille')
for i,z in enumerate((.12,.16,.20,.24)):
    box(f'CODEX_LOWER_GRILLE_BAR_{i}',(2.374,0,z),(.018,1.02,.009),'codex_dark','lower_grille')
    box(f'CODEX_LOWER_GRILLE_BAR_BACK_{i}',(2.368,0,z),(.012,1.02,.008),'codex_dark','lower_grille')

# In-game verification showed the thin original bars only at the perimeter of
# the opening.  Build the grille as true 3D rectangular stock: a recessed
# opaque backing, broad horizontal slats, then vertical ribs.  Each visible
# element receives a second, recessed layer so the old renderer never exposes
# the hollow interior through a culled face.
upper_panel=[(-.57,.305),(-.535,.385),(-.44,.505),(-.27,.61),(.27,.61),(.44,.505),(.535,.385),(.57,.305)]
prism_yz('CODEX_GRILLE_SOLID_BACKING',2.332,.060,upper_panel,'codex_dark','upper_grille')
for i,(z,width) in enumerate(((.335,.68),(.375,.91),(.415,1.04),(.455,1.11),(.495,1.07),(.535,.95),(.575,.66))):
    box(f'CODEX_GRILLE_SLAT_{i}',(2.402,0,z),(.045,width,.030),'codex_metal','upper_grille')
    box(f'CODEX_GRILLE_SLAT_REAR_{i}',(2.352,0,z),(.030,width,.026),'codex_dark','upper_grille')
for i,y in enumerate((-.43,-.29,-.145,0,.145,.29,.43)):
    box(f'CODEX_GRILLE_RIB_{i}',(2.414,y,.455),(.046,.024,.255),'codex_metal','upper_grille')
    box(f'CODEX_GRILLE_RIB_REAR_{i}',(2.360,y,.455),(.030,.020,.245),'codex_dark','upper_grille')
# Five full 3D grille layers.  They are deliberately separated by 18 mm: the
# game can cull a face in one layer without revealing the hollow radiator.
for layer, x in enumerate((2.386, 2.368, 2.350, 2.332, 2.314)):
    layer_material = 'codex_metal' if layer in (0, 2) else 'codex_dark'
    prism_yz(f'CODEX_GRILLE_LAYER_BACK_{layer}',x-.012,.020,upper_panel,'codex_dark','upper_grille')
    for i,(z,width) in enumerate(((.335,.68),(.375,.91),(.415,1.04),(.455,1.11),(.495,1.07),(.535,.95),(.575,.66))):
        box(f'CODEX_GRILLE_LAYER_{layer}_SLAT_{i}',(x,0,z),(.024,width,.028),layer_material,'upper_grille')
    for i,y in enumerate((-.43,-.29,-.145,0,.145,.29,.43)):
        box(f'CODEX_GRILLE_LAYER_{layer}_RIB_{i}',(x+.004,y,.455),(.025,.022,.250),layer_material,'upper_grille')

# Window surrounds on both sides, including the central pillar.
window_outline=[(.91,.79),(.72,1.08),(-.55,1.19),(-1.46,1.04),(-1.72,.80),(.91,.79)]
for side in (-1,1):
    y=side*.782
    for i,(a,b) in enumerate(zip(window_outline,window_outline[1:])):
        rod_xz(f'CODEX_WINDOW_TRIM_{side}_{i}',a,b,y,.018,.018,'codex_dark','window_trim')
    rod_xz(f'CODEX_WINDOW_PILLAR_{side}',(-.18,.79),(-.18,1.165),y,.027,.02,'codex_dark','window_trim')

# Rear diffuser/grille and two fully modelled exhaust tips.
rear_panel=[(-.73,.09),(-.64,.23),(.64,.23),(.73,.09),(.57,.055),(-.57,.055)]
prism_yz('CODEX_REAR_EXHAUST_GRILLE',-2.385,.03,rear_panel,'codex_dark','exhaust_grille')
for side in (-1,1):
    cylinder(f'CODEX_EXHAUST_TIP_{side}',(-2.41,side*.61,.135),.13,.068,'x','codex_metal','exhaust',20)
    cylinder(f'CODEX_EXHAUST_INNER_{side}',(-2.481,side*.61,.135),.008,.047,'x','codex_dark','exhaust',20)

# Static axle-centred caps cover the transparent centre of all four wheels.
for axle,x in (('F',1.425),('R',-1.305)):
    for side in (-1,1):
        y=side*.895
        cylinder(f'CODEX_WHEEL_CAP_{axle}_{side}',(x,y,0),.028,.115,'y','codex_metal','wheel_center',24)
        cylinder(f'CODEX_WHEEL_HUB_{axle}_{side}',(x,y+side*.017,0),.009,.042,'y','codex_dark','wheel_center',20)

def tree_for(pos):
    tree=KDTree(len(pos))
    for i,p in enumerate(pos):tree.insert(p,i)
    tree.balance();return tree

targets={'KIT00_BODY':40000,'BASE':26000,'KIT00_INTERIOR':24000,
         'KIT00_LEFT_SIDE_MIRROR':6000,'KIT00_RIGHT_SIDE_MIRROR':6000,
         'KIT00_RIGHT_HEADLIGHT':2500,'KIT00_RIGHT_HEADLIGHT_GLASS':2000,
         'KIT00_RIGHT_BRAKELIGHT':2000,'KIT00_RIGHT_BRAKELIGHT_GLASS':1500,
         'KIT00_FRONT_WINDOW':12000,'KIT00_REAR_WINDOW':8000}
if os.environ.get('FUSION_LOD_TARGETS'):
    targets.update(json.loads(os.environ['FUSION_LOD_TARGETS']))

def classify(o):
    si=int(o['source_shader']); mat=mapping[si]; bone=o['dominant_bone'].lower()
    center=sum(v.co.x for v in o.data.vertices)/len(o.data.vertices)
    if bone.startswith('codex_'):return 'KIT00_BODY'
    # The donor wheels already match the car slot and are kept unchanged.
    if 'hub_' in bone:return None
    if si==4:return 'KIT00_RIGHT_BRAKELIGHT'
    if si==28:return 'BASE'
    if si==16: return 'KIT00_FRONT_WINDOW' if center>-.3 else 'KIT00_REAR_WINDOW'
    # Match the working Shelby technique: keep one opaque backing shell, paint
    # the grille into its texture and attach it to the always-visible body.
    # The remaining source objects are overlapping chrome slats and badges;
    # stacking them caused the old engine to drop or z-fight the whole grille.
    if bone=='grade':
        return 'KIT00_BODY' if o.name.endswith(('_g017','_g018')) else None
    if mat['shader']=='CARSKIN':
        # Hood and trunk are permanent panels. Accessory slots would make them
        # disappear when the player installs mirrors or a spoiler.
        if 'bonnet' in bone or 'boot' in bone:return 'KIT00_BODY'
        if 'mirror' in bone: return 'KIT00_LEFT_SIDE_MIRROR' if 'dside' in bone else 'KIT00_RIGHT_SIDE_MIRROR'
        return 'KIT00_BODY'
    if si in (2,4,14,15,26):
        if center < -1.3:
            return 'KIT00_RIGHT_BRAKELIGHT_GLASS' if si in (14,15,26) else 'KIT00_RIGHT_BRAKELIGHT'
        if center > 1.3:
            return 'KIT00_RIGHT_HEADLIGHT_GLASS' if si in (15,26) else 'KIT00_RIGHT_HEADLIGHT'
    if mat['shader']=='INTERIOR' or si in (0,1,3,9,10,24,25): return 'KIT00_INTERIOR'
    return 'BASE'

for o in list(bpy.data.objects):
    if 'source_shader' in o:
        part=classify(o)
        if part is not None:
            if str(o.get('dominant_bone','')).lower()=='grade':
                grille=o.copy();grille.data=o.data.copy()
                for slot in grille.material_slots:
                    material=slot.material.copy();material['source_shader']=grille_material_index
                    slot.material=material
                grille['source_shader']=grille_material_index
                groups[part].append(grille)
            else:groups[part].append(o)

collection=bpy.data.collections.new('MW_EXPORT'); bpy.context.scene.collection.children.link(collection)
report=[]; export=[]
for part,objects in groups.items():
    source_tris=sum(len(o.data.polygons) for o in objects)
    # Give small textured details twice the density of ordinary surfaces while
    # keeping the whole part inside its final budget.  The old code exempted
    # every detail mesh from reduction, then tried to collapse the joined
    # result.  BASE consequently fed hundreds of thousands of triangles to a
    # single-threaded Decimate pass and could take more than 50 minutes.
    detail_shaders={0,1,19,20,21,24,25,29,30}
    detail_weight=2.0
    def object_weight(o):
        bone=o['dominant_bone'].lower()
        if bone.startswith('codex_'):return 12.0
        if part=='KIT00_BODY' and bone=='grade':return 1.5
        # Hinged painted panels show collapse holes much sooner than broad body
        # panels, so reserve enough topology for their compound curved shells.
        if part=='KIT00_BODY' and 'boot' in bone:return 3.0
        return detail_weight if int(o['source_shader']) in detail_shaders else 1.0
    def preserve_panel(o):
        if os.environ.get('FUSION_DISABLE_PANEL_PRESERVE') == '1':
            return False
        if part!='KIT00_BODY':return False
        bone=o['dominant_bone'].lower()
        if bone.startswith('codex_'):return True
        if 'bonnet' in bone:return True
        # One boot-bound geometry is actually the long upper body/cowl shell.
        # Its thin overlapping surface tears around the windshield if collapsed.
        if 'boot' in bone:
            xs=[v.co.x for v in o.data.vertices]
            return max(xs)-min(xs)>4.0
        return False
    forced_full=[o for o in objects if preserve_panel(o)]
    forced_tris=sum(len(o.data.polygons) for o in forced_full)
    weighted_tris=sum(
        len(o.data.polygons)*object_weight(o)
        for o in objects if o not in forced_full
    )
    base_ratio=min(1.0,max(0,targets[part]-forced_tris)/max(1,weighted_tris))
    # Decimate each source section to retain material boundaries and tiny badges.
    reduced=[];normal_positions=[];normal_values=[]
    for source_obj in objects:
        o=source_obj.copy(); o.data=source_obj.data.copy(); collection.objects.link(o)
        if source_obj not in forced_full:
            bm=bmesh.new();bm.from_mesh(o.data)
            bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001)
            bm.to_mesh(o.data);bm.free();o.data.update()
            bpy.context.view_layer.objects.active=o; o.select_set(True)
            local_ratio=min(1.0,base_ratio*object_weight(source_obj))
            # Keep at least one small triangle cluster for badges and lamp details.
            local_ratio=max(local_ratio,min(1.0,4/max(1,len(o.data.polygons))))
            mod=o.modifiers.new('MW reduction','DECIMATE'); mod.ratio=local_ratio
            mod.use_collapse_triangulate=True
            bpy.ops.object.modifier_apply(modifier=mod.name)
        # Record original shading for export after topology reduction.
        if 'source_key' in source_obj:
            original=np.load(INPUT_ROOT/'work/source-meshes'/f'{source_obj["source_key"]}.npz')['vertices']['Normal']
            original=np.column_stack((original[:,1]/alignment['longitudinal_scale'],-original[:,0],original[:,2]))
            original/=np.maximum(np.linalg.norm(original,axis=1)[:,None],1e-8)
        else:
            original=np.array([v.normal[:] for v in source_obj.data.vertices],dtype=np.float32)
        normal_positions.extend(v.co[:] for v in source_obj.data.vertices)
        normal_values.extend(original.tolist())
        reduced.append(o); o.select_set(False)
    bpy.ops.object.select_all(action='DESELECT')
    for o in reduced:o.select_set(True)
    bpy.context.view_layer.objects.active=reduced[0]; bpy.ops.object.join()
    base=bpy.context.object; base.name=part+'_A'
    base['mw_part']=part
    base_tree=tree_for(normal_positions);base_normals=normal_values
    for lod,factor in [('A',1),('B',.5),('C',.22),('D',.09),('E',.04)]:
        if part+'_'+lod not in names: continue
        if lod=='A': o=base
        else:
            o=base.copy(); o.data=base.data.copy(); collection.objects.link(o); o.name=part+'_'+lod
            bpy.context.view_layer.objects.active=o
            mod=o.modifiers.new('Distance LOD','DECIMATE'); mod.ratio=factor; mod.use_collapse_triangulate=True
            bpy.ops.object.modifier_apply(modifier=mod.name); o.hide_render=True; o.hide_viewport=True
        # MWR has signed 16-bit source indices. Keep comfortably below this ceiling.
        attempts=0
        while len(o.data.vertices)>=30000 and attempts<8:
            attempts+=1
            bpy.context.view_layer.objects.active=o
            mod=o.modifiers.new('Index budget','DECIMATE'); mod.ratio=min(.65,25000/len(o.data.vertices)); mod.use_collapse_triangulate=True
            bpy.ops.object.modifier_apply(modifier=mod.name)
            bm=bmesh.new();bm.from_mesh(o.data)
            bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
            bm.to_mesh(o.data);bm.free();o.data.update()
        mesh=o.data; mesh.calc_loop_triangles()
        if len(mesh.vertices)>=32768: raise RuntimeError(f'{o.name}: too many source vertices')
        pos=np.array([v.co for v in mesh.vertices],dtype=np.float32)
        scratch=bpy.data.meshes.new('normal_recalculation')
        scratch.from_pydata(pos.tolist(),[],[tuple(p.vertices) for p in mesh.polygons]);scratch.update()
        normals=np.array([v.normal for v in scratch.vertices],dtype=np.float32)
        bpy.data.meshes.remove(scratch)
        # Preserve source smoothing while rejecting coincident opposite-facing inner panels.
        for vi,p in enumerate(pos):
            candidates=base_tree.find_n(p,8)
            distance=candidates[0][2]
            eligible=[c for c in candidates if c[2]<=distance+.0001]
            best=max(eligible,key=lambda c:float(np.dot(base_normals[c[1]],normals[vi])))
            if np.dot(base_normals[best[1]],normals[vi])>.3:normals[vi]=base_normals[best[1]]
        face_records=[]
        tint_faces=[]
        is_window=part in ('KIT00_FRONT_WINDOW','KIT00_REAR_WINDOW')
        uv=mesh.uv_layers.active.data
        for tri in mesh.loop_triangles:
            # mwgc reverses input winding; reverse here so output retains Blender winding.
            vi=list(tri.vertices)[::-1]; li=list(tri.loops)[::-1]
            tex=[uv[k].uv for k in li]
            si=int(mesh.materials[tri.material_index]['source_shader'])
            rect=mapping[si].get('uv_rect')
            if rect:
                rx,ry,rw,rh=rect
                transformed=[]
                for t in tex:
                    source_u=t.x%1.0; source_v=(1-t.y)%1.0
                    transformed.append((rx+source_u*rw,ry+source_v*rh))
                out_u=[t[0] for t in transformed];out_v=[t[1] for t in transformed]
            else:
                out_u=[t.x for t in tex];out_v=[1-t.y for t in tex]
            face_records.append(struct.pack('<i4h6f',si,*vi,0,*out_u,*out_v))
            if is_window:
                tint_vi=[index+len(pos) for index in vi]
                tint_faces.append(struct.pack('<i4h6f',window_tint_index,*tint_vi,0,*out_u,*out_v))
        if is_window:
            # Match the two-layer construction used by official cars while
            # avoiding coplanar z-fighting between clear glass and tint.
            tint_pos=pos-normals*.001
            export_pos=np.vstack((pos,tint_pos))
            export_normals=np.vstack((normals,normals))
            face_records.extend(tint_faces)
        else:
            export_pos=pos
            export_normals=normals
        vertex_records=np.column_stack((export_pos[:,1],export_pos[:,2],export_pos[:,0],
                                        export_normals[:,1],export_normals[:,2],export_normals[:,0])).astype('<f4').tobytes()
        export.append((o.name,len(export_pos),len(face_records),vertex_records,b''.join(face_records)))
        report.append({'part':o.name,'vertices':len(pos),'triangles':len(face_records),'source_triangles':source_tris})
        print(o.name,len(pos),len(face_records),flush=True)
    for o in objects: o.hide_render=True; o.hide_viewport=True

def string(f,s):
    b=s.encode('ascii')+b'\0';f.write(struct.pack('<i',len(b)));f.write(b)
with (ROOT/'work/fusion.mwr').open('wb') as f:
    f.write(struct.pack('<3i',0,len(mapping),len(export)))
    for m in mapping: string(f,m['shader']+'/'+m['texture'])
    for name,nv,nf,_,_ in export:
        string(f,name);f.write(struct.pack('<2i16f',nv,nf,*np.eye(4).flatten()))
    for _,_,_,v,faces in export:f.write(v);f.write(faces)
(ROOT/'reference/lod-report.json').write_text(json.dumps(report,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'blender/fusion-export-intermediate.blend'))
scene=bpy.context.scene;scene.render.filepath=str(ROOT/'preview/optimized-perspective.png')
bpy.ops.render.render(write_still=True)
print('MWR_READY',len(export))
