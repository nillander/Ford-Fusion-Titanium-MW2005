"""Fusion 2012: build the new GEOMETRY.BIN part spec from z10 + Mondeo 2016 lamps (grafts_A.pkl)."""
import json
from graft import *
from partmesh import PartMesh, clip_tris
from atlas import cell_uv
import struct
G=pickle.load(open('/home/claude/c12/grafts_A.pkl','rb'))
TEX_A=0x95DE5B23   # <CAR>_KIT00_HEADLIGHT_OFF  -> opaque DXT1 atlas (lamp internals)
TEX_B=0x4B7D95B6   # <CAR>_KIT00_BRAKELIGHT_OFF -> DXT3 atlas (lenses)
SKIN=0x9A8AAD9E
SH_HEAD=0x9C645529; SH_BRAKE=0x05BC3A3C; SH_GLASS=0xA6348EE3
SHIFT={'head':0.002,'tail':0.002,'fog':0.0}
def dzw(k): return (-0.06,0.14) if k.startswith('fog') else (-0.06,0.08)
PARTS={p['name'][10:]:p for p in Z}
# ---------- Mondeo lamp meshes ----------
def lamp_uv(sh,uv,glass):
    out=np.empty_like(uv)
    for s in np.unique(sh):
        m=sh==s
        if s in (10,14): out[m]=np.c_[0.5+0.5*(0.004+0.992*np.clip(uv[m,0],0,1)),0.5*(0.004+0.992*np.clip(uv[m,1],0,1))]
        elif s==16: out[m]=np.c_[0.5*(0.004+0.992*np.clip(uv[m,0],0,1)),0.5+0.5*(0.004+0.992*np.clip(uv[m,1],0,1))]
        elif s==15: out[m]=cell_uv('clear')
        elif s==9: out[m]=cell_uv('chrome')
        else: out[m]=cell_uv('black')
    return out
def cluster(P,N,UV,I,cell):
    if cell<=0: return P,N,UV,I
    key=np.c_[np.floor(P/cell).astype(np.int64),np.round(UV*16).astype(np.int64)]
    _,cid,cnt=np.unique(key,axis=0,return_inverse=True,return_counts=True);cid=cid.ravel(); n=cid.max()+1
    Pc=np.zeros((n,3));Nc=np.zeros((n,3));Uc=np.zeros((n,2))
    np.add.at(Pc,cid,P);np.add.at(Nc,cid,N);np.add.at(Uc,cid,UV)
    Pc/=cnt[:,None];Uc/=cnt[:,None];Nc/=np.maximum(np.linalg.norm(Nc,axis=1,keepdims=True),1e-9)
    J=cid[I];ok=(J[:,0]!=J[:,1])&(J[:,1]!=J[:,2])&(J[:,0]!=J[:,2]);J=J[ok]
    J=np.unique(J,axis=0); used,inv=np.unique(J.ravel(),return_inverse=True)
    return Pc[used],Nc[used],Uc[used],inv.reshape(-1,3)
def mesh_from(g,mask,glass):
    """(P,N,UV,I) of Mondeo triangles `mask` placed by graft g, UVs mapped into the atlas"""
    F=MF[mask]; sh=MSH[mask]
    # per-vertex shader (vertices are not shared across GTA geometries)
    vsh=np.zeros(len(M),int); vsh[F.ravel()]=np.repeat(sh,3)
    ids,inv=np.unique(F.ravel(),return_inverse=True)
    P=g['P'][ids]; N=g['N'][ids]; UV=lamp_uv(vsh[ids],S['UV'][ids],glass)
    return P,N,UV,inv.reshape(-1,3)
def concat(ms):
    P=[];N=[];U=[];I=[];o=0
    for p,n,u,i in ms: P.append(p);N.append(n);U.append(u);I.append(i+o);o+=len(p)
    if not P: return np.zeros((0,3)),np.zeros((0,3)),np.zeros((0,2)),np.zeros((0,3),int)
    return np.concatenate(P),np.concatenate(N),np.concatenate(U),np.concatenate(I)
LAMPS={}
for sd in 'LR':
    gh,gf,gt=G['head'+sd],G['fog'+sd],G['tail'+sd]
    lens=np.isin(MSH,(15,16))
    fl=mesh_from(gf,gf['feature']&(MSH==15),True)
    q=fl[0][:,1:]; c0=(q.min(0)+q.max(0))/2; r=(q.max(0)-q.min(0)).max()/2
    uvf=np.c_[0.5+0.5*(0.927+0.058*(q[:,0]-c0[0])/r*(-1 if sd=='R' else 1)),0.5*(0.932-0.058*(q[:,1]-c0[1])/r)]
    fl=(fl[0],fl[1],uvf,fl[3])
    LAMPS['head_int'+sd]=concat([mesh_from(gh,gh['feature']&~lens,False),mesh_from(gf,gf['feature']&(MSH!=15),False),fl])
    LAMPS['head_gls'+sd]=concat([mesh_from(gh,gh['feature']&lens,True)])
    LAMPS['tail_int'+sd]=concat([mesh_from(gt,gt['feature']&~lens,False)])
    LAMPS['tail_gls'+sd]=concat([mesh_from(gt,gt['feature']&lens,True)])
for k,v in LAMPS.items(): print('lamp',k,'verts',len(v[0]),'tris',len(v[3]))
LODCELL={'A':0,'B':0.004,'C':0.009,'D':0.018,'E':0.03}
# ---------- body patch (paint) per graft ----------
def patch_mesh(g):
    F=MF[g['patch']]; ids,inv=np.unique(F.ravel(),return_inverse=True)
    return g['P'][ids],g['N'][ids],g['UV'][ids],inv.reshape(-1,3)
PATCH=concat([patch_mesh(g) for g in G.values() if g['patch'].any()])
print('body patch verts',len(PATCH[0]),'tris',len(PATCH[3]))
# ---------- part edits ----------
out=[]   # PartMesh objects to write
def edit_lamp_solid(L,base,tex,sh,side,key,keep2018):
    """KIT00_<side>_<base>_<L>: kept 2018 pieces (UV to Q0) + Mondeo mesh"""
    name='KIT00_%s_%s_%s'%(side,base,L)
    tmpl='MUSTANGGT_KIT00_RIGHT_%s_%s'%(base,L)
    src=PARTS.get('KIT00_RIGHT_%s_%s'%(base,L))
    pm=PartMesh(src); pm.name='MUSTANGGT_'+name
    T,rm=z_removed('KIT00_RIGHT_%s_%s'%(base,L))
    grp=pm.groups[0]
    if keep2018:
        keep=~rm; grp['F']=T['F'][keep]
        pm.UV=0.5*(0.004+0.992*np.clip(pm.UV,0,1))         # old atlas lives in the top-left quadrant now
    else: grp['F']=np.zeros((0,3),int)
    pm.tex=[tex]; pm.sh=[sh]; grp['ti']=0; grp['si']=0
    P,N,UV,I=LAMPS[key]
    P,N,UV,I=cluster(P,N,UV,I,LODCELL[L])
    o=pm.add_verts(P,N,UV,0xFFFFFFFF)
    grp['F']=np.r_[grp['F'],I+o]
    return pm,tmpl
def edit_base_like(n):
    p=PARTS[n]; pm=PartMesh(p); T,rm=z_removed(n)
    # soup order == group order: split mask per group
    k=0
    for gi,g in enumerate(pm.groups):
        cnt=len(g['F']); g['F']=g['F'][~rm[k:k+cnt]]; k+=cnt
    fg=[G['fogL'],G['fogR']]
    for g in pm.groups:
        for gg in fg:
            P2,N2,U2,C2,F2=clip_tris(pm.P,pm.N,pm.UV,pm.C,g['F'],lambda X,gg=gg:gg['fp'].sdf(X,*dzw('fog'),0.0))
            o=len(pm.P); pm.P=np.r_[pm.P,P2]; pm.N=np.r_[pm.N,N2]; pm.UV=np.r_[pm.UV,U2]; pm.C=np.r_[pm.C,C2]; g['F']=F2
    return pm
def edit_body(n):
    p=PARTS[n]; pm=PartMesh(p); L=n[-1]
    for g in pm.groups:
        if pm.tex[g['ti']]!=SKIN: continue
        hidden=None
        if n in ZVIS and len(pm.groups)==1:
            vis=ZVIS[n]; hidden=g['F'][~vis]; g['F']=g['F'][vis]
            Ch=pm.P[hidden].mean(1); ok=np.ones(len(hidden),bool)
            for gg in G.values():
                lo,hi=dzw(gg['k']); ok&=gg['fp'].sdf(Ch,lo,hi,SHIFT[kind(gg['k'])]-0.01)>0
            hidden=hidden[ok]
        for gg in G.values():
            lo,hi=dzw(gg['k'])
            P2,N2,U2,C2,F2=clip_tris(pm.P,pm.N,pm.UV,pm.C,g['F'],lambda X,gg=gg,lo=lo,hi=hi:gg['fp'].sdf(X,lo,hi,SHIFT[kind(gg['k'])]))
            pm.P=np.r_[pm.P,P2]; pm.N=np.r_[pm.N,N2]; pm.UV=np.r_[pm.UV,U2]; pm.C=np.r_[pm.C,C2]; g['F']=F2
        if hidden is not None: g['F']=np.r_[g['F'],hidden]
        P,N,UV,I=cluster(*PATCH,{'A':0.003,'B':0.004,'C':0.008,'D':0.015,'E':0.03}[L])
        o=pm.add_verts(P,N,UV,0xFFFFFFFF); g['F']=np.r_[g['F'],I+o]
        break
    return pm
if __name__=='__main__':
    recs=[]; report=[]
    for L in 'ABCD':
        for side in ('RIGHT','LEFT'):
            sd='R' if side=='RIGHT' else 'L'
            for base,tex,sh,key,keep in (('HEADLIGHT',TEX_A,SH_HEAD,'head_int','n'),('HEADLIGHT_GLASS',TEX_B,SH_GLASS,'head_gls','n'),
                                         ('BRAKELIGHT',TEX_A,SH_BRAKE,'tail_int','k'),('BRAKELIGHT_GLASS',TEX_B,SH_GLASS,'tail_gls','k')):
                pm,tmpl=edit_lamp_solid(L,base,tex,sh,side,key+sd,keep=='k' and side=='RIGHT')
                recs.append((pm,tmpl))
    for n in list(PARTS):
        if n.startswith('BASE_') or n=='KIT00_RIGHT_SIDE_MIRROR_A': recs.append((edit_base_like(n),None))
        elif any(n.startswith(b) for b in ('KIT00_BODY_','KIT01_BODY_','KIT02_BODY_')): recs.append((edit_body(n),None))
    with open('spec12.bin','wb') as f:
        for pm,tmpl in recs:
            b,nv=pm.record(tmpl); f.write(b)
            idx=sum(3*len(g['F']) for g in pm.groups)
            report.append((pm.name,nv,pm.ntris(),len([g for g in pm.groups if len(g['F'])])))
            print('%-44s verts %6d tris %6d groups %d%s'%(pm.name,nv,pm.ntris(),report[-1][3],'  !!VERTS' if nv>65535 else ''))
            if report[-1][3]>1:
                # multi-group solids: every group must end below index 65535
                off=0
                for g in pm.groups:
                    if not len(g['F']): continue
                    off+=3*len(g['F'])
                if off>65535: print('   !! multi-group index total',off)
    json.dump(report,open('spec12-report.json','w')) if False else None
