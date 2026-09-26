from graft import *
from partmesh import clip_tris
import sys
G=pickle.load(open('grafts_A.pkl','rb'))
SHIFT={'head':0.002,'tail':0.002,'fog':0.0}
def dz_win(k): return (-0.06,0.14) if k.startswith('fog') else (-0.06,0.08)
def clip_soup(T,keep,gs):
    P,N,UV,Cc=T['P'],T['N'],T['UV'],np.zeros(len(T['P']),np.int64)
    F=T['F'][keep]; tex=T['tex'][keep]
    for g in gs:
        lo,hi=dz_win(g['k'])
        phi=lambda X,g=g,lo=lo,hi=hi: g['fp'].sdf(X,lo,hi,SHIFT[kind(g['k'])])
        P2,N2,U2,C2,F2=clip_tris(P,N,UV,Cc,F,phi)
        # tex per output tri: map through nearest source (all body tris same tex group anyway)
        P=np.r_[P,P2];N=np.r_[N,N2];UV=np.r_[UV,U2];Cc=np.r_[Cc,C2];F=F2
        tex=np.full(len(F),tex[0] if len(tex) else 0)
    return P,N,UV,F,tex
if __name__=='__main__':
    Ps=[];Fs=[];Cs=[];UVs=[];TIDs=[];off=0
    for p in Z:
        n=p['name'][10:]
        if not n.endswith('_A') or any(k in n for k in ['KIT01','KIT02','STYLE','DECAL','TIRE','BRAKE_A','DRIVER']): continue
        T,m=z_removed(n)
        keep=~m
        if 'BODY' in n:
            P,N,UV,F,tex=clip_soup(T,keep,list(G.values()))
        elif n.startswith('BASE') or 'SIDE_MIRROR' in n:
            P=T['P'];F=T['F'][keep];tex=T['tex'][keep]
            fg=[g for g in G.values() if g['k'].startswith('fog')]
            # group-wise clip (keep textures): clip each texture separately
            outF=[];outT=[];PP=P;NN=T['N'];UU=T['UV'];CC=np.zeros(len(P),np.int64)
            for th in np.unique(tex):
                FF=F[tex==th]
                for g in fg:
                    P2,N2,U2,C2,FF=clip_tris(PP,NN,UU,CC,FF,lambda X,g=g:g['fp'].sdf(X,-0.06,0.14,0.0))
                    PP=np.r_[PP,P2];NN=np.r_[NN,N2];UU=np.r_[UU,U2];CC=np.r_[CC,C2]
                outF.append(FF);outT.append(np.full(len(FF),th))
            P=PP;UV=UU;F=np.concatenate(outF);tex=np.concatenate(outT)
        else:
            P=T['P'];F=T['F'][keep];tex=T['tex'][keep];UV=T['UV']
        Ps.append(P); Fs.append(F+off); off+=len(P)
        c=np.where((tex==0x9A8AAD9E)[:,None],[0.78,0.78,0.8],[0.3,0.3,0.33]); Cs.append(c)
        UVs.append(UV if len(UV)==len(P) else np.zeros((len(P),2))); TIDs.append(np.full(len(F),-1))
    col,tid=mcol(S)
    for k,g in G.items():
        m=g['feature']|g['patch']
        c=col[m].copy(); c[MSH[m]==0]=[0.78,0.78,0.8] if 'src' not in sys.argv else [0.55,0.75,1.0]
        Ps.append(g['P']); Fs.append(MF[m]+off); off+=len(g['P']); Cs.append(c); UVs.append(S['UV']); TIDs.append(tid[m])
    P=np.concatenate(Ps);F=np.concatenate(Fs);C=np.concatenate(Cs).astype(np.float32);UV=np.concatenate(UVs);TID=np.concatenate(TIDs)
    pickle.dump(dict(P=P,F=F,C=C,UV=UV,TID=TID),open('comp_A.pkl','wb'))
    views=[(0,5,(2.2,0,0.35),420),(30,8,(2.0,0.62,0.45),900),(330,8,(2.0,-0.62,0.45),900),(20,3,(2.1,0.7,0.25),1300),(180,8,(-2.2,0,0.6),420),(200,10,(-2.05,0.6,0.7),900),(160,10,(-2.05,-0.6,0.7),900),(180,40,(-2.05,0,0.7),500),(120,10,(-1.9,-0.6,0.7),700),(250,25,(-1.9,0.6,0.7),700)]
    ims=[Image.fromarray(rast.render(P,F,C,uv=UV,texid=TID,textures=[FARI,RED],az=a,el=e,W=700,H=420,center=c,scale=s)[0]) for a,e,c,s in views]
    o=Image.new('RGB',(1400,420*((len(ims)+1)//2)))
    for i,m in enumerate(ims): o.paste(m,((i%2)*700,(i//2)*420))
    o.save(sys.argv[1])
