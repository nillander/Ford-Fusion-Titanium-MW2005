"""Bake a clean black border into the existing plate rectangle of BADGING.

Both plates sample this region.  Their blue Mercosul band, Brazil flag and
NEWZERA lettering stay exactly as they are; only an outer black outline is
added, replacing the separate frame geometry.
"""
import struct
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "v1prime" / "scripts"))
from dxt import write_dds_like

src, dst = map(Path, sys.argv[1:3])
with Image.open(src) as source:
    image = source.convert("RGBA")

# index 21 (base_ptq) occupies the lower-left cell of the 2x2 BADGING atlas.
# Its actual plate UV rectangle was fitted in BuildV1PrimeB.cs.
x0, y0, x1, y1 = 73, 690, 443, 805
draw = ImageDraw.Draw(image)
border = 7
radius = 12
draw.rounded_rectangle((x0, y0, x1, y1), radius=radius,
                       outline=(8, 9, 11, 255), width=border)
# The project encoder emits the same single-mip DXT3 layout as the original
# BADGING payload (Pillow's Windows build writes an uncompressed DDS instead).
write_dds_like(src, dst, np.asarray(image, dtype=np.uint8))
