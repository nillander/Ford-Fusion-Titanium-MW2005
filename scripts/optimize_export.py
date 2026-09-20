import bpy
import bmesh
import json
import struct
import numpy as np
from pathlib import Path
from collections import defaultdict
from mathutils.kdtree import KDTree

ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'blender/source-aligned.blend'))
mapping=json.loads((ROOT/'reference/materials.json').read_text())
# Official MW cars layer the regular glass shader with a separate tint shader.
# Keep this extra material local to the MWR export; its texture is global and
# intentionally absent from the car's TPK.
window_tint_index=len(mapping)
mapping.append({'shader':'0x3ed70c43','texture':'0x1b049702'})
# Codex window export is keyed to the Mustang donor catalog: FRONT/REAR
# WINDOW only. The Ford GT catalog splits side glass into extra slots and
# would drop the official dual-layer tint construction.
donor=json.loads((ROOT/'work/donor-geometry.json').read_text())
names={x['name'].removeprefix('MUSTANGGT_') for x in donor}
names.update('KIT00_LEFT_SIDE_MIRROR_'+lod for lod in 'ABCDE')
groups=defaultdict(list)
alignment=json.loads((ROOT/'reference/alignment.json').read_text())

def tree_for(pos):
    tree=KDTree(len(pos))
    for i,p in enumerate(pos):tree.insert(p,i)
    tree.balance();return tree

targets={'KIT00_BODY':40000,'BASE':26000,'KIT00_INTERIOR':18000,
         'KIT00_LEFT_SIDE_MIRROR':6000,'KIT00_RIGHT_SIDE_MIRROR':6000,
         'KIT00_RIGHT_HEADLIGHT':2500,'KIT00_RIGHT_HEADLIGHT_GLASS':2000,
         'KIT00_RIGHT_BRAKELIGHT':2000,'KIT00_RIGHT_BRAKELIGHT_GLASS':1500,
         'KIT00_FRONT_WINDOW':12000,'KIT00_REAR_WINDOW':8000}

def classify(o):
    si=int(o['source_shader']); mat=mapping[si]; bone=o['dominant_bone'].lower()
    center=sum(v.co.x for v in o.data.vertices)/len(o.data.vertices)
    # The donor wheels already match the car slot and are kept unchanged.
    if 'hub_' in bone:return None
    if si==4:return 'KIT00_RIGHT_BRAKELIGHT'
    if si==28:return 'BASE'
    if si==16: return 'KIT00_FRONT_WINDOW' if center>-.3 else 'KIT00_REAR_WINDOW'
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
        if part is not None:groups[part].append(o)

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
        # Hinged painted panels show collapse holes much sooner than broad body
        # panels, so reserve enough topology for their compound curved shells.
        if part=='KIT00_BODY' and 'boot' in bone:return 3.0
        return detail_weight if int(o['source_shader']) in detail_shaders else 1.0
    def preserve_panel(o):
        if part!='KIT00_BODY':return False
        bone=o['dominant_bone'].lower()
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
        original=np.load(ROOT/'work/source-meshes'/f'{source_obj["source_key"]}.npz')['vertices']['Normal']
        original=np.column_stack((original[:,1]/alignment['longitudinal_scale'],-original[:,0],original[:,2]))
        original/=np.maximum(np.linalg.norm(original,axis=1)[:,None],1e-8)
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
