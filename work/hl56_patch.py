"""Close only the small grille-side, below-lamp triangle on the 2012."""
import sys
import geo
from partmesh import PartMesh
from hlgap import masks
from hl46 import bridge,add_bridge


def main(src,out):
    parts={p['name']:p for p in geo.load(src)}
    regions={side:masks(parts,side) for side in ('LEFT','RIGHT')}
    records=[]
    for name in sorted(parts):
        if not ('_KIT' in name and '_BODY_' in name and name.rsplit('_',1)[-1] in 'ABCDE'):
            continue
        lod=name.rsplit('_',1)[-1]
        step={'A':5,'B':7,'C':10,'D':14,'E':14}[lod]
        geometries=[bridge(regions[s],step,s,'inner-lower') for s in ('LEFT','RIGHT')]
        geometries=[g for g in geometries if g is not None]
        if not geometries: continue
        pm=PartMesh(parts[name])
        added=add_bridge(pm,geometries)
        record,vertices=pm.record()
        if vertices>65535: raise ValueError((name,vertices))
        records.append(record)
        print(name,'added',added,'verts',vertices,flush=True)
    with open(out,'wb') as file:
        for record in records:file.write(record)


if __name__=='__main__':main(sys.argv[1],sys.argv[2])
