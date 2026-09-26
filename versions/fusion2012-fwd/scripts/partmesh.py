import numpy as np, struct
class PartMesh:
    """editable MW solid: shared vertex arrays + list of groups (each with its own triangle array)"""
    def __init__(self,p):
        v=p['v']; self.name=p['name']; self.tex=list(p['tex']); self.sh=list(p['shaders'])
        self.P=v['p'].astype(np.float64).copy(); self.N=v['n'].astype(np.float64).copy(); self.UV=v['uv'].astype(np.float64).copy(); self.C=v['c'].astype(np.int64).copy()&0xFFFFFFFF
        self.groups=[]
        for g in p['groups']:
            seg=p['idx'][g['offset']:g['offset']+g['length']].astype(np.int64)
            self.groups.append(dict(ti=g['tex'][0],si=g['shader'],flags=g['flags'],unk1=g['unk1'],F=seg[:len(seg)//3*3].reshape(-1,3)))
    def add_verts(self,P,N,UV,C):
        o=len(self.P); self.P=np.r_[self.P,P]; self.N=np.r_[self.N,N]; self.UV=np.r_[self.UV,UV]; self.C=np.r_[self.C,np.broadcast_to(C,(len(P),)) if np.ndim(C)==0 else C]; return o
    def tex_index(self,h):
        if h not in self.tex: self.tex.append(h)
        return self.tex.index(h)
    def sh_index(self,h):
        if h not in self.sh: self.sh.append(h)
        return self.sh.index(h)
    def ntris(self): return sum(len(g['F']) for g in self.groups)
    def record(self,tmpl=None):
        o=bytearray()
        def s(x): b=x.encode();return struct.pack('<i',len(b))+b
        groups=[g for g in self.groups if len(g['F'])]
        o+=s(self.name)+s(tmpl or self.name)+struct.pack('<i',len(self.tex))+struct.pack('<%dI'%len(self.tex),*self.tex)+struct.pack('<i',len(self.sh))+struct.pack('<%dI'%len(self.sh),*self.sh)+struct.pack('<i',len(groups))
        nv=0
        for g in groups:
            ids,inv=np.unique(g['F'].ravel(),return_inverse=True)
            V=np.c_[self.P[ids],self.N[ids],self.UV[ids]].astype(np.float32)
            key=np.c_[np.round(V[:,:3]/1e-5),np.round(V[:,3:6]*1e3),np.round(V[:,6:8]*1e5),self.C[ids]].astype(np.int64)
            _,first,winv=np.unique(key,axis=0,return_index=True,return_inverse=True)
            inv=winv.ravel()[inv]; ids=ids[first]; V=V[first]
            Fl=inv.reshape(-1,3); okf=(Fl[:,0]!=Fl[:,1])&(Fl[:,1]!=Fl[:,2])&(Fl[:,0]!=Fl[:,2]); inv=Fl[okf].ravel()
            o+=struct.pack('<iiiii',g['ti'],g['si'],g['flags'],g['unk1'],len(V))
            rec=np.zeros(len(V),dtype=[('v','<8f4'),('d','<u4')]);rec['v']=V;rec['d']=self.C[ids].astype(np.uint32)
            o+=rec.tobytes()+struct.pack('<i',inv.size)+inv.astype(np.int32).ravel().tobytes(); nv+=len(V)
        return bytes(o),nv
def clip_tris(P,N,UV,C,F,phi_fn,maxedge=0.008,maxdepth=4):
    """keep the part of triangles F where phi>0. Returns new vertex arrays + triangles (indices into
    the extended arrays: original verts first). Triangles fully phi>0 kept as is; fully <0 dropped."""
    ph=phi_fn(P)
    pf=ph[F]
    keep_all=(pf>0).all(1); drop=(pf<=0).all(1); mid=~keep_all&~drop
    outF=[F[keep_all]]; newP=[];newN=[];newUV=[];newC=[]; base=len(P)
    for t in np.nonzero(mid)[0]:
        A=P[F[t]]; e=max(np.linalg.norm(A[0]-A[1]),np.linalg.norm(A[1]-A[2]),np.linalg.norm(A[2]-A[0]))
        n=int(np.clip(np.ceil(e/maxedge),1,2**maxdepth))
        # barycentric grid subdivision n x n
        bs=[];tris=[]
        idx={}
        for i in range(n+1):
            for j in range(n+1-i):
                idx[(i,j)]=len(bs); bs.append((1-(i+j)/n,i/n,j/n))
        for i in range(n):
            for j in range(n-i):
                tris.append((idx[(i,j)],idx[(i+1,j)],idx[(i,j+1)]))
                if i+j<n-1: tris.append((idx[(i+1,j)],idx[(i+1,j+1)],idx[(i,j+1)]))
        bs=np.array(bs); Q=bs@A; phq=phi_fn(Q)
        # marching triangles
        vb=list(bs)  # barycentrics of output verts
        out=[]
        def edge(a,b):
            ta=phq[a]/(phq[a]-phq[b]); vb.append(bs[a]*(1-ta)+bs[b]*ta); return len(vb)-1
        for (a,b,c) in tris:
            s=[phq[a]>0,phq[b]>0,phq[c]>0]; k=sum(s)
            if k==3: out.append((a,b,c))
            elif k==0: continue
            else:
                vs=[a,b,c]
                # rotate so that pattern is canonical
                for r in range(3):
                    if k==1 and s[r]: i0=r;break
                    if k==2 and not s[r]: i0=r;break
                a0,b0,c0=vs[i0],vs[(i0+1)%3],vs[(i0+2)%3]
                if k==1:
                    p1=edge(a0,b0);p2=edge(a0,c0); out.append((a0,p1,p2))
                else:
                    p1=edge(a0,b0);p2=edge(a0,c0); out.append((p1,b0,c0)); out.append((p1,c0,p2))
        if not out: continue
        vb=np.array(vb); o=base+sum(len(x) for x in newP)
        newP.append(vb@A); nn=vb@N[F[t]]; newN.append(nn/np.linalg.norm(nn,axis=1,keepdims=True)); newUV.append(vb@UV[F[t]]); newC.append(np.full(len(vb),C[F[t][0]]))
        outF.append(np.array(out)+o)
    if newP:
        return np.concatenate(newP),np.concatenate(newN),np.concatenate(newUV),np.concatenate(newC),np.concatenate(outF)
    return np.zeros((0,3)),np.zeros((0,3)),np.zeros((0,2)),np.zeros(0,np.int64),np.concatenate(outF)
def clip_tris(P,N,UV,C,F,phi_fn,maxedge=0.025,maxdepth=6):
    """adaptive version: recursively 4-split only triangles that straddle phi=0, then clip linearly"""
    ph=phi_fn(P); pf=ph[F]
    keep_all=(pf>0).all(1); drop=(pf<=0).all(1)
    # also refine triangles whose vertices are all outside but that the zero set may cross (big tris)
    T3=P[F]; samp=np.stack([T3.mean(1),(T3[:,0]+T3[:,1])/2,(T3[:,1]+T3[:,2])/2,(T3[:,2]+T3[:,0])/2],1)
    ps=phi_fn(samp.reshape(-1,3)).reshape(-1,4)
    suspicious=(keep_all&(ps.min(1)<=0))|(drop&(ps.max(1)>0))
    mid=~keep_all&~drop|suspicious
    outF=[F[keep_all&~suspicious]]; newP=[];newN=[];newUV=[];newC=[]; base=len(P)
    for t in np.nonzero(mid)[0]:
        A=P[F[t]]
        vb=[np.eye(3)[0],np.eye(3)[1],np.eye(3)[2]]; cache={}
        tris=[]
        def vid(b):
            k=tuple(np.round(b*2**maxdepth).astype(int))
            if k not in cache: cache[k]=len(vb); vb.append(b)
            return cache[k]
        for i in range(3): cache[tuple(np.round(vb[i]*2**maxdepth).astype(int))]=i
        stack=[(0,1,2,0)]
        leaves=[]
        while stack:
            a,b,c,d=stack.pop()
            B3=np.array([vb[a],vb[b],vb[c]]); Q=B3@A
            e=max(np.linalg.norm(Q[0]-Q[1]),np.linalg.norm(Q[1]-Q[2]),np.linalg.norm(Q[2]-Q[0]))
            q=phi_fn(np.r_[Q,Q.mean(0,keepdims=True),(Q[0:1]+Q[1:2])/2,(Q[1:2]+Q[2:3])/2,(Q[2:3]+Q[0:1])/2])
            if d<maxdepth and e>maxedge and (q.min()<=0) and (q.max()>0):
                ab=vid((vb[a]+vb[b])/2); bc=vid((vb[b]+vb[c])/2); ca=vid((vb[c]+vb[a])/2)
                stack+= [(a,ab,ca,d+1),(ab,b,bc,d+1),(ca,bc,c,d+1),(ab,bc,ca,d+1)]
            else: leaves.append((a,b,c))
        vbA=np.array(vb); phq=phi_fn(vbA@A)
        out=[]
        def edge(a,b):
            ta=phq[a]/(phq[a]-phq[b]); vb.append(vbA[a]*(1-ta)+vbA[b]*ta); return len(vb)-1
        for (a,b,c) in leaves:
            s=[phq[a]>0,phq[b]>0,phq[c]>0]; k=sum(s)
            if k==3: out.append((a,b,c))
            elif k==0: continue
            else:
                vs=[a,b,c]
                for r in range(3):
                    if (k==1 and s[r]) or (k==2 and not s[r]): i0=r;break
                a0,b0,c0=vs[i0],vs[(i0+1)%3],vs[(i0+2)%3]
                p1=edge(a0,b0);p2=edge(a0,c0)
                if k==1: out.append((a0,p1,p2))
                else: out.append((p1,b0,c0)); out.append((p1,c0,p2))
        if not out: continue
        vbx=np.array(vb); o=base+sum(len(x) for x in newP)
        newP.append(vbx@A); nn=vbx@N[F[t]]; newN.append(nn/np.linalg.norm(nn,axis=1,keepdims=True)); newUV.append(vbx@UV[F[t]]); newC.append(np.full(len(vbx),C[F[t][0]]))
        outF.append(np.array(out)+o)
    if newP:
        return np.concatenate(newP),np.concatenate(newN),np.concatenate(newUV),np.concatenate(newC),np.concatenate(outF)
    return np.zeros((0,3)),np.zeros((0,3)),np.zeros((0,2)),np.zeros(0,np.int64),np.concatenate(outF)
