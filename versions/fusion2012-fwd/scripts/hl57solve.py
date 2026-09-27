import numpy as np
from scipy.sparse import coo_matrix,vstack as svstack
from scipy.sparse.linalg import lsqr,spsolve
from scipy.ndimage import distance_transform_edt,binary_dilation,gaussian_filter,label
RES=0.003
def band_masks(d,R=0.055,Rin=0.0,excl_dil=2,excl_hood=None):
    lens=d['lens']
    dl=distance_transform_edt(~lens)*RES
    hood=~np.isnan(d['Dh'])&(np.nan_to_num(d['Dh'],nan=-9)>np.nan_to_num(d['Bh'],nan=-9)-0.002)
    oth=~np.isnan(d['Oh'])&(np.nan_to_num(d['Oh'],nan=-9)>np.nan_to_num(d['Bh'],nan=-9)-0.004)
    if excl_hood is None: excl=binary_dilation(hood|oth,iterations=excl_dil)
    else: excl=binary_dilation(oth,iterations=excl_dil)|(binary_dilation(hood,iterations=excl_hood) if excl_hood>0 else hood)
    band=(dl>Rin)&(dl<R)&~excl&~lens
    # keep only the connected piece touching the lens
    lab,n=label(band); touch=np.unique(lab[binary_dilation(lens,iterations=2)&band]); touch=touch[touch>0]
    band=np.isin(lab,touch)
    return band,dl,excl
def solve(d,band,edge_off=0.0015,w_edge=4.0):
    """biharmonic-like fill: minimise |Laplacian|^2 in the band, Dirichlet = old front skin outside the band,
    soft target at the lens rim = lens height - edge_off"""
    H=d['Bh'].copy(); nv,nu=H.shape
    known=~np.isnan(H)&~band
    idx=-np.ones(H.shape,int); ys,xs=np.nonzero(band); idx[ys,xs]=np.arange(len(ys)); n=len(ys)
    rows=[];cols=[];vals=[];rhs=[]; r=0
    def val(j,i):
        if 0<=j<nv and 0<=i<nu:
            if idx[j,i]>=0: return ('u',idx[j,i])
            if known[j,i]: return ('k',H[j,i])
        return None
    # laplacian equations on every band cell and on known cells adjacent to the band
    cand=binary_dilation(band,iterations=1)
    for j,i in zip(*np.nonzero(cand)):
        nb=[val(j+1,i),val(j-1,i),val(j,i+1),val(j,i-1)]; c=val(j,i)
        if c is None or any(x is None for x in nb): continue
        terms=[(c,-4.0)]+[(x,1.0) for x in nb]; b=0.0
        for (t,v),w in terms:
            if t=='u': rows.append(r);cols.append(v);vals.append(w)
            else: b-=w*v
        rhs.append(b); r+=1
    # rim target
    lensd=binary_dilation(d['lens'],iterations=1)
    Lh=d['Lh']; near=distance_transform_edt(np.isnan(Lh),return_indices=True)[1]
    Lfill=Lh[near[0],near[1]]
    rim=band&binary_dilation(lensd,iterations=1)
    for j,i in zip(*np.nonzero(rim)):
        rows.append(r);cols.append(idx[j,i]);vals.append(w_edge);rhs.append(w_edge*(Lfill[j,i]-edge_off)); r+=1
    # weak regulariser to old height where it exists (keeps the solve well posed in isolated pockets)
    for j,i in zip(ys,xs):
        if not np.isnan(H[j,i]): rows.append(r);cols.append(idx[j,i]);vals.append(0.02);rhs.append(0.02*H[j,i]); r+=1
    A=coo_matrix((vals,(rows,cols)),shape=(r,n)).tocsr(); b=np.array(rhs)
    x=spsolve((A.T@A).tocsc(),A.T@b)
    out=H.copy(); out[band]=x[idx[band]]
    return out

def _lap_system(dom,known,H,eqmask=None):
    nv,nu=dom.shape; idx=-np.ones(dom.shape,int); ys,xs=np.nonzero(dom); idx[ys,xs]=np.arange(len(ys))
    rows=[];cols=[];vals=[];rhs=[];r=0
    cand=binary_dilation(dom,iterations=1) if eqmask is None else eqmask
    J,I=np.nonzero(cand)
    for j,i in zip(J,I):
        pts=[(j,i,-4.0),(j+1,i,1.0),(j-1,i,1.0),(j,i+1,1.0),(j,i-1,1.0)]
        ok=True;b=0.0;tr=[]
        for jj,ii,w in pts:
            if not(0<=jj<nv and 0<=ii<nu): ok=False;break
            if idx[jj,ii]>=0: tr.append((idx[jj,ii],w))
            elif known[jj,ii]: b-=w*H[jj,ii]
            else: ok=False;break
        if not ok or not tr:
            # incomplete stencil at a free boundary: weak first-order (membrane) equations
            if idx[j,i]>=0:
                for jj,ii,w in pts[1:]:
                    if 0<=jj<nv and 0<=ii<nu and (idx[jj,ii]>=0 or known[jj,ii]):
                        rows.append(r);cols.append(idx[j,i]);vals.append(0.5)
                        if idx[jj,ii]>=0: rows.append(r);cols.append(idx[jj,ii]);vals.append(-0.5);rhs.append(0.0)
                        else: rhs.append(0.5*H[jj,ii])
                        r+=1
            continue
        for c,w in tr: rows.append(r);cols.append(c);vals.append(w)
        rhs.append(b); r+=1
    return idx,rows,cols,vals,rhs,r
def extrap(d,band,with_lens=True):
    """smooth continuation of the outer skin under band(+lens) (min |Lap|^2, Dirichlet outside)"""
    H=d['Bh']; dom=(band|d['lens']) if with_lens else band; known=~np.isnan(H)&~dom&~(d['lens'] if not with_lens else False)
    idx,rows,cols,vals,rhs,r=_lap_system(dom,known,H)
    n=int(dom.sum())
    # tiny Tikhonov on the gradient keeps disconnected pockets defined
    A=coo_matrix((vals,(rows,cols)),shape=(r,n)).tocsr()
    from scipy.sparse import identity
    M=(A.T@A)+1e-8*identity(n); x=spsolve(M.tocsc(),A.T@np.array(rhs))
    out=np.full(H.shape,np.nan); out[dom]=x[idx[dom]]; return out
def harmonic_phi(band,rim):
    """phi=1 on rim cells, 0 on the other band boundary; Laplace inside"""
    dom=band&~rim; known=~dom
    H=np.where(rim,1.0,0.0)
    idx,rows,cols,vals,rhs,r=_lap_system(dom,known,H,eqmask=dom)
    A=coo_matrix((vals,(rows,cols)),shape=(r,int(dom.sum()))).tocsc(); x=spsolve(A,np.array(rhs))
    phi=np.where(rim,1.0,0.0); phi[dom]=x[idx[dom]]; return phi
def ramp(d,band,edge_off=0.0015,sig=0.012):
    Hx=extrap(d,band)
    lensd=binary_dilation(d['lens'],iterations=1)
    rim=band&binary_dilation(lensd,iterations=1)
    Lh=d['Lh']; near=distance_transform_edt(np.isnan(Lh),return_indices=True)[1]; Lf=Lh[near[0],near[1]]
    delta=np.where(rim,Lf-edge_off-Hx,np.nan)
    # spread the rim offset over the band (nearest rim cell) and smooth it along the contour
    ni=distance_transform_edt(~rim,return_indices=True)[1]
    dfield=delta[ni[0],ni[1]]
    wgt=gaussian_filter(rim.astype(float),sig/RES); dsm=gaussian_filter(np.where(rim,delta,0),sig/RES)/np.maximum(wgt,1e-9)
    dsm=np.where(wgt>1e-4,dsm,dfield)
    dfield=dsm[ni[0],ni[1]]
    phi=harmonic_phi(band,rim); s=phi*phi*(3-2*phi)
    H=Hx+dfield*s
    return np.where(band,H,np.nan),Hx,phi

def ramp2(d,band,edge_off=0.0015,sig=0.02):
    Hx=extrap(d,band)
    lensd=binary_dilation(d['lens'],iterations=1)
    rim=band&binary_dilation(lensd,iterations=1)
    Lh=d['Lh']; near=distance_transform_edt(np.isnan(Lh),return_indices=True)[1]; Lf=Lh[near[0],near[1]]
    delta=np.where(rim,Lf-edge_off-Hx,0)
    wgt=gaussian_filter(rim.astype(float),sig/RES); dsm=gaussian_filter(delta,sig/RES)/np.maximum(wgt,1e-9)
    dr=np.where(rim,dsm,0.0)
    dom=band&~rim; known=~dom
    idx,rows,cols,vals,rhs,r=_lap_system(dom,known,dr)
    from scipy.sparse import identity
    A=coo_matrix((vals,(rows,cols)),shape=(r,int(dom.sum()))).tocsr()
    x=spsolve(((A.T@A)+1e-8*identity(int(dom.sum()))).tocsc(),A.T@np.array(rhs))
    dl=dr.copy(); dl[dom]=x[idx[dom]]
    H=Hx+dl
    return np.where(band,H,np.nan),Hx,dl

def ramp3(d,band,edge_off=0.0015,sig=0.02,Rr=0.03):
    """Hx (smooth outer continuation) + biharmonic lift to the lens rim, confined to dist<Rr"""
    Hx=extrap(d,band)
    lensd=binary_dilation(d['lens'],iterations=1)
    rim=band&binary_dilation(lensd,iterations=1)
    Lh=d['Lh']; near=distance_transform_edt(np.isnan(Lh),return_indices=True)[1]; Lf=Lh[near[0],near[1]]
    delta=np.where(rim,Lf-edge_off-Hx,0)
    wgt=gaussian_filter(rim.astype(float),sig/RES); dsm=gaussian_filter(delta,sig/RES)/np.maximum(wgt,1e-9)
    dr=np.where(rim,dsm,0.0)
    dl=distance_transform_edt(~d['lens'])*RES
    dom=band&~rim&(dl<Rr); known=~dom
    idx,rows,cols,vals,rhs,r=_lap_system(dom,known,dr)
    from scipy.sparse import identity
    A=coo_matrix((vals,(rows,cols)),shape=(r,int(dom.sum()))).tocsr()
    x=spsolve(((A.T@A)+1e-8*identity(int(dom.sum()))).tocsc(),A.T@np.array(rhs))
    lift=dr.copy(); lift[dom]=x[idx[dom]]
    H=Hx+lift
    return np.where(band,H,np.nan),Hx,lift

def ramp4(d,band,edge_off=0.0015,sig=0.02,Rr=0.03,cap=0.008,Rw=0.005,with_lens=False):
    """Hx over the band only (natural boundary at the lens) + lift to the lens rim:
    up to `cap` spread biharmonically over Rr, the rest as a steep collar within Rw of the lens"""
    Hx=extrap(d,band,with_lens=with_lens)
    lensd=binary_dilation(d['lens'],iterations=1)
    rim=band&binary_dilation(lensd,iterations=1)
    Lh=d['Lh']; near=distance_transform_edt(np.isnan(Lh),return_indices=True)[1]; Lf=Lh[near[0],near[1]]
    delta=np.where(rim,Lf-edge_off-Hx,0)
    wgt=gaussian_filter(rim.astype(float),sig/RES); dsm=gaussian_filter(delta,sig/RES)/np.maximum(wgt,1e-9)
    dr=np.where(rim,np.clip(dsm,-cap,cap),0.0)
    if Rw<=0 and cap<=0: return np.where(band,Hx,np.nan),Hx,np.zeros_like(Hx)
    dl=distance_transform_edt(~d['lens'])*RES
    dom=band&~rim&(dl<Rr); known=~dom
    idx,rows,cols,vals,rhs,r=_lap_system(dom,known,dr)
    from scipy.sparse import identity
    A=coo_matrix((vals,(rows,cols)),shape=(r,int(dom.sum()))).tocsr()
    x=spsolve(((A.T@A)+1e-8*identity(int(dom.sum()))).tocsc(),A.T@np.array(rhs))
    lift=dr.copy(); lift[dom]=x[idx[dom]]
    # collar: remaining offset to the (unsmoothed) rim height, fading out over Rw
    ni=distance_transform_edt(~rim,return_indices=True)[1]
    rest=(Lf-edge_off-Hx-lift)[ni[0],ni[1]]
    rest=gaussian_filter(np.where(band,rest,0),1.0)
    t=np.clip(1-(dl-RES)/Rw,0,1); t=t*t*(3-2*t)
    H=Hx+lift+np.clip(rest,-0.05,0.05)*t
    return np.where(band,H,np.nan),Hx,lift
