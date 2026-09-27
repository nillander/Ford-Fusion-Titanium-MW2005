import sys
import numpy as np
from PIL import Image
import geo, mwsoup, pgr, persp

dump, texture_dir, output = sys.argv[1:4]
parts = geo.load(dump)
def select(name):
    if not name.endswith('_A'):
        return False
    if 'KIT0' in name and 'KIT00' not in name:
        return False
    return any(s in name for s in ('BODY_A', 'HOOD_A', 'HEADLIGHT_A', 'HEADLIGHT_GLASS_A', 'RIGHT_SIDE_MIRROR_A', 'BASE_A'))

soup = mwsoup.soup(parts, select)
centres = soup['P'][soup['F']].mean(axis=1)
keep = (centres[:, 0] > 1.40) & (centres[:, 2] > 0.25)
for key in ('F', 'tex', 'part', 'grp'):
    soup[key] = soup[key][keep]
print('render triangles', len(soup['F']), flush=True)
T = persp.tex(texture_dir)
P, N, UV, tex = pgr.subdiv(soup, 2)
cams = [
    ((3.2, 2.7, 0.88), (2.02, 0.70, 0.57), 17),
    ((3.2, -2.7, 0.88), (2.02, -0.70, 0.57), 17),
    ((3.15, 0.0, 0.92), (2.0, 0.0, 0.54), 32),
]
W, H = 780, 540
result = Image.new('RGB', (W*3, H))
for i, (eye, target, fov) in enumerate(cams):
    img = pgr.shot(P, N, UV, tex, T, eye, target, fov, W, H)
    result.paste(img, (i*W, 0))
result.save(output)
