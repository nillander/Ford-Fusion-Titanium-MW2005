import geo,numpy as np,struct,sys
# Vinyl-friendly UVs for the CARSKIN (paint) group, in the layout used by vanilla MW cars:
# u = 0.169*x + 0.5 (along the car); v = 0.5 - 0.2*S, S = signed arc length from the roof
# centre line (+y side negative v), approximated as y plus the drop below the local roof line.
def compute(p):
    V=p['v']['p'].astype(float); N=p['v']['n'].astype(float); x,y,z=V[:,0],V[:,1],V[:,2]
    ay=np.abs(y); sg=np.where(y>=0,1.0,-1.0)
    # side panels: straight projection (v from height) so stripes stay horizontal across doors;
    # upper surfaces: v from y (across the roof/hood/boot). Blend by how sideways the normal is.
    S_side=sg*(0.97+(1.30-z))
    S_top=y
    w=np.clip((np.abs(N[:,1])-0.35)/0.35,0,1)
    S=w*S_side+(1-w)*S_top
    u=0.169*x+0.5; v=0.5-0.2*S
    return np.c_[u,v].astype(np.float32)

if __name__=='__main__':
    P=geo.load(sys.argv[1]); out=open(sys.argv[2],'wb'); n=0
    for p in P:
        nm=p['name']
        if '_KIT00_BODY_' not in nm: continue
        uv=compute(p)
        b=nm.encode(); out.write(struct.pack('<i',len(b))+b+struct.pack('<i',len(uv))+uv.tobytes()); n+=1
        print(nm,'uv range',uv.min(0).round(3),uv.max(0).round(3))
    out.close(); print('parts',n)
