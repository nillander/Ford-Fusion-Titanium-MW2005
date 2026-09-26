"""Item 33 (Fusion 2012 e 2018): freios com textura oficial.
As peças KIT00_FRONT/REAR_BRAKE_A–C do Fusion usavam o atlas do interior (<CARRO>_INTERIOR), que mostra a tela da
multimídia através das rodas da loja. Agora são as peças de freio do Pontiac GTO do jogo (disco + pinça), com as
texturas oficiais: disco = ROTOR1 (0x7811C146, textura global em GLOBAL/GLOBALB.BUN) e pinça = recorte das pinças do
GTO_MISC (u 0,23–0,98, v 0,35–0,51 no GTO), copiado 2× para a área livre (0,0–0,75; 0,50–0,656) do <CARRO>_MISC
(DXT1, gravado direto no TEXTURES.BIN). Escala 1,15× no plano do disco (disco de 31 → 36 cm, como o do Fusion),
deslocamento −12 mm no eixo da roda."""
import sys;sys.path.insert(0,'/home/claude/v3/versions/v3-fusion-ajm3899/scripts');sys.path.insert(0,'/home/claude/c12')
import numpy as np,geo
from partmesh import PartMesh
from PIL import Image
from strap_tex import dxt1_encode
GX0,GY0,GW,GH=120,178,384,80; S=1.15; DY=-0.012
MISC={'COBALTSS':0xE67A7FA5,'MUSTANGGT':0x5A00E244}
def uvmap(uv): return np.c_[(uv[:,0]*512-GX0)*2/1024,(uv[:,1]*512-GY0)*2/1024+0.5]
def parts(gto_dump,pre,out):
    Z={p['name']:p for p in geo.load(gto_dump)}; recs=[]
    for k in ('FRONT_BRAKE','REAR_BRAKE'):
        for L in 'ABC':
            pm=PartMesh(Z['GTO_KIT00_%s_%s'%(k,L)]); pm.name='%s_KIT00_%s_%s'%(pre,k,L)
            v=np.unique(np.concatenate([g['F'] for g in pm.groups]))
            pm.P[v,0]*=S; pm.P[v,2]*=S; pm.P[v,1]+=DY
            mi=pm.tex.index(0x130BA4F4); pm.tex[mi]=MISC[pre]
            for g in pm.groups:
                if g['ti']==mi:
                    vv=np.unique(g['F']); pm.UV[vv]=uvmap(pm.UV[vv])
            recs.append(pm)
    with open(out,'wb') as f:
        for pm in recs: b,nv=pm.record(); f.write(b); print(pm.name,nv)
def texpatch(texbin,ddsfile,gto_misc_dds,out):
    b=bytearray(open(texbin,'rb').read()); d=open(ddsfile,'rb').read(); off=b.find(d[128:]); assert off>0 and b.count(d[128:])==1
    assert int.from_bytes(d[84:88],'little')==0x31545844
    g=Image.open(gto_misc_dds).convert('RGB').crop((GX0,GY0,GX0+GW,GY0+GH)).resize((GW*2,GH*2),Image.LANCZOS)
    enc=dxt1_encode(g); bw=g.size[0]//4; rowbytes=(1024//4)*8; x0,y0=0,512
    for r in range(g.size[1]//4):
        src=enc[r*bw*8:(r+1)*bw*8]; dst=off+((y0//4)+r)*rowbytes+(x0//4)*8; b[dst:dst+len(src)]=src
    open(out,'wb').write(b); g.save('build/caliper_region.png')
if __name__=='__main__':
    if sys.argv[1]=='parts': parts(*sys.argv[2:5])
    else: texpatch(*sys.argv[2:6])
