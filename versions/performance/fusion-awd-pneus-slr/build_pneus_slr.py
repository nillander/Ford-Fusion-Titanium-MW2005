"""v2.10: copia o bloco `tires` do SLR (slr -> mustanggt, slr_top -> mustanggt_top) e poe
DIFFERENTIAL 0,7/0,7/0,7 nos dois niveis do Fusion 2018, a partir do MWPS da v2.9.

Uso: python build_pneus_slr.py <GLOBAL/attributes.bin do MW> <MWPS v2.9> <MWPS saida>
"""
import re, struct, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]/'scripts'))
from vlt_util import VltDatabase, hash_name, unpack_vpak

H = hash_name
PL = re.compile(r'^(patch\s+)(\w+)(\s+bin:)(0x[0-9a-fA-F]+)(\s+)(\S+)\s*$')
FMT = {'float': '<f', 'int32': '<i', 'int16': '<h', 'int8': '<b'}


def short(f):
    if f == int(f):
        return str(int(f))
    for p in range(1, 10):
        s = '%.*g' % (p, f)
        if struct.pack('<f', float(s)) == struct.pack('<f', f):
            return s
    return '%.9g' % f


def main(attributes, source, target):
    _, raw, vlt = unpack_vpak(Path(attributes).read_bytes())[0]
    db = VltDatabase(raw, vlt)
    text = Path(source).read_text(encoding='utf-8')
    buf = bytearray(db.bin)
    for line in text.split('\n'):
        m = PL.match(line)
        if m:
            k, v = m.group(2), m.group(6)
            val = float(v) if k == 'float' else int(v.removesuffix('B'), 0)
            if k != 'float' and val > 0x7FFFFFFF:
                val -= 1 << 32
            struct.pack_into(FMT[k], buf, int(m.group(4), 16), val)

    def span(cls, name):
        c = next(x for x in db.collections if x.class_hash == H(cls) and x.name_hash == H(name))
        return c.required_offset, db.required_size(H(cls))

    tires = []
    for dst, src in (('mustanggt', 'slr'), ('mustanggt_top', 'slr_top')):
        do, size = span('tires', dst)
        so, _ = span('tires', src)
        buf[do:do+size] = db.bin[so:so+size]
        tires.append((do, size))
    field = next(x for x in db.classes[H('transmission')].fields if x.name_hash == H('DIFFERENTIAL'))
    diffs = []
    for name in ('mustanggt', 'mustanggt_top'):
        base = span('transmission', name)[0] + field.offset + 8
        for i in range(3):
            struct.pack_into('<f', buf, base+4*i, 0.7)
            diffs.append(base+4*i)
    inside = lambda o: any(a <= o < a+n for a, n in tires) or o in diffs
    covered, out = set(), []
    for line in text.split('\n'):
        m = PL.match(line)
        if m and inside(int(m.group(4), 16)):
            k, o = m.group(2), int(m.group(4), 16)
            val = struct.unpack_from(FMT[k], buf, o)[0]
            covered.update(range(o, o+struct.calcsize(FMT[k])))
            line = m.group(1)+k+m.group(3)+m.group(4)+m.group(5)+(short(val) if k == 'float' else str(val))
        out.append(line)
    text = '\n'.join(out)
    for (a, n), label in zip(tires, ('tires/default/mustanggt', 'tires/default/mustanggt/mustanggt_top')):
        extra = []
        for k in range(a, a+n, 2):
            if k not in covered and buf[k:k+2] != db.bin[k:k+2]:
                extra.append('patch\tint16\tbin:0x%x\t%d' % (k, struct.unpack_from('<h', buf, k)[0]))
        if extra:
            head = '## Node: '+label+'\n##---------------------------------------------------\n'
            assert text.count(head) == 1
            text = text.replace(head, head+'\n## YAW_CONTROL header (capacidade, quantidade, tamanho): ativa a curva de controle de giro do SLR\n'+'\n'.join(extra)+'\n')
    text = text.replace('## Fusion Titanium 2018: aro 18 (padrao de fabrica). ASPECT_RATIO 35->40 mantem o diametro do pneu (661 mm).',
                        '## Pneus do Mercedes-Benz SLR McLaren (v2.10 teste): 295/30 aro 19 no original, 295/35 aro 19 no melhorado.')
    text = text.replace('## Fusion (item 13): STEERING, YAW_SPEED e YAW_CONTROL copiados do Mustang GT (doador Shelby, 1.700 kg) para curvas menos sensiveis.',
                        '## Fusion v2.10 (teste): bloco de pneus inteiro do SLR (aderencia, GRIP_SCALE, YAW_CONTROL, YAW_SPEED, STEERING). Diferenciais 0,7/0,7/0,7.')
    Path(target).write_bytes(text.encode('utf-8'))


if __name__ == '__main__':
    main(*sys.argv[1:4])
