"""Build source texture atlases under hashes already known by the retail car slot."""
import json
import math
import shutil
import struct
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
source = json.loads((ROOT / "reference" / "source-structure.json").read_text())
out = ROOT / "work" / "mw-textures"
out.mkdir(exist_ok=True)

KNOWN = {
    "interior": "MUSTANGGT_INTERIOR",
    "plate": "MUSTANGGT_BADGING",
    "lights": "MUSTANGGT_KIT00_HEADLIG",
    "paint": "MUSTANGGT_SKIN1",
    "dark": "MUSTANGGT_LOGO",
    "detail": "MUSTANGGT_MISC",
}
GROUPS = {
    "interior": [0, 1, 3, 9, 10, 24, 25, 27, 28],
    "plate": [19, 20, 21],
    "lights": [2, 4, 14, 15, 26],
    "dark": [6, 11, 12, 18, 29, 30],
    "detail": [7, 8, 13, 17, 22, 23],
}


def load_source(index):
    texture = source["shaders"][index]["textures"].get("diffusesampler", "")
    path = ROOT / "work" / "source-textures" / f"{texture}.dds"
    if path.exists():
        image = Image.open(path).convert("RGBA")
    else:
        colour = (9, 10, 12, 255) if texture == "black" else (175, 175, 175, 255)
        image = Image.new("RGBA", (16, 16), colour)
    if index == 21:
        draw = ImageDraw.Draw(image)
        x0, y0, x1, y1 = (int(image.width * v) for v in (0.138, 0.345, 0.870, 0.573))
        draw.rectangle((x0, y0, x1, y1), fill=(242, 242, 238, 255), outline=(28, 55, 112, 255), width=max(2, image.width // 256))
        band = max(12, (y1 - y0) // 4)
        draw.rectangle((x0, y0, x1, y0 + band), fill=(18, 61, 155, 255))
        try:
            font_path = Path("C:/Windows/Fonts/arialbd.ttf")
            font = ImageFont.truetype(str(font_path), max(18, int((y1 - y0) * 0.42)))
            small = ImageFont.truetype(str(font_path), max(8, int(band * 0.52)))
        except OSError:
            font = small = ImageFont.load_default()
        draw.text(((x0 + x1) / 2, y0 + band * 0.48), "BRASIL", font=small, fill="white", anchor="mm")
        draw.text(((x0 + x1) / 2, y0 + band + (y1 - y0 - band) / 2), "NEWZERA", font=font, fill=(12, 12, 16, 255), anchor="mm")
    if index == 8:
        # The Fusion's front grille surround has collapsed UVs in the GTA source.
        # Feed it a neutral, high-contrast chrome field: this keeps the geometry
        # from looking like a blue transparent placeholder in the MW Chrome shader.
        image = Image.new("RGBA", (256, 256), (150, 154, 160, 255))
        draw = ImageDraw.Draw(image)
        for y in range(0, image.height, 24):
            draw.rectangle((0, y, image.width, y + 5), fill=(222, 225, 230, 255))
            draw.rectangle((0, y + 6, image.width, y + 15), fill=(82, 86, 92, 255))
            draw.rectangle((0, y + 16, image.width, y + 23), fill=(172, 176, 182, 255))
    return image


def save_dds(image, path):
    image.save(path, pixel_format="DXT3")
    data = bytearray(path.read_bytes())
    flags = struct.unpack_from("<I", data, 8)[0]
    struct.pack_into("<I", data, 8, (flags & ~8) | 0x80000)
    struct.pack_into("<I", data, 20, len(data) - 128)
    path.write_bytes(data)


rects = {}
atlas_size = 1024
for group, indices in GROUPS.items():
    columns = math.ceil(math.sqrt(len(indices)))
    rows = math.ceil(len(indices) / columns)
    cell_w, cell_h = atlas_size // columns, atlas_size // rows
    atlas = Image.new("RGBA", (atlas_size, atlas_size), (8, 8, 10, 255))
    for slot, index in enumerate(indices):
        col, row = slot % columns, slot // columns
        pad = 3
        x, y = col * cell_w + pad, row * cell_h + pad
        width, height = cell_w - pad * 2, cell_h - pad * 2
        image = load_source(index).resize((width, height), Image.Resampling.LANCZOS)
        atlas.paste(image, (x, y), image)
        rects[index] = [x / atlas_size, y / atlas_size, width / atlas_size, height / atlas_size]
    name = KNOWN[group]
    save_dds(atlas, out / f"{name}.dds")
    atlas.save(out / f"{name}.png")

# The brake-light geometry receives this known hash after mwgc compilation.
# Matching layouts keep the already transformed UV coordinates valid.
shutil.copy2(out / "MUSTANGGT_KIT00_HEADLIG.dds", out / "MUSTANGGT_KIT00_BRAKELI.dds")
shutil.copy2(out / "MUSTANGGT_KIT00_HEADLIG.png", out / "MUSTANGGT_KIT00_BRAKELI.png")

paint = Image.new("RGBA", (16, 16), (255, 255, 255, 255))
save_dds(paint, out / "MUSTANGGT_SKIN1.dds")
paint.save(out / "MUSTANGGT_SKIN1.png")

# Retain the donor wheel and driver payloads because those meshes stay in the car.
for name, hash_name in (("MUSTANGGT_TIRE", "5A04B8CC"), ("MUSTANGGT_DRIVER", "C961D064")):
    shutil.copy2(ROOT / "work" / "compiled-textures" / f"{hash_name}.dds", out / f"{name}.dds")

mapping = []
for i, shader_source in enumerate(source["shaders"]):
    texture = shader_source["textures"].get("diffusesampler", "")
    preset = shader_source["preset"]
    shader = "INTERIOR"
    if "paint" in preset:
        shader = "CARSKIN"
    elif i == 16:
        shader = "0x471a1dca"
    elif "lights" in preset:
        shader = "BRAKELIGHT" if texture.lower() in ("vermelho12", "vermelho") or i == 4 else "HEADLIGHT"
        if i in (14, 15, 26):
            shader = "0xa6348ee3"
    elif i in (7, 8, 13, 17, 19):
        shader = "CHROME"
    elif texture == "black":
        shader = "DULLPLASTIC"
    elif "brasil" in texture or texture == "base_ptq":
        shader = "LICENSEPLATE"
    if i in (0, 1, 3, 24, 25):
        shader = "INTERIOR"

    if i == 5:
        name = KNOWN["paint"]
    elif i == 16:
        # Replaced with the donor/global window hash after mwgc compilation.
        name = KNOWN["lights"]
    else:
        group = next((key for key, values in GROUPS.items() if i in values), "dark")
        name = KNOWN[group]
    mapping.append({"index": i, "source": texture, "preset": preset, "shader": shader,
                    "texture": name, "uv_rect": rects.get(i)})

names = [
    "MUSTANGGT_INTERIOR", "MUSTANGGT_BADGING", "MUSTANGGT_KIT00_BRAKELI",
    "MUSTANGGT_LOGO", "MUSTANGGT_MISC", "MUSTANGGT_TIRE",
    "MUSTANGGT_KIT00_HEADLIG", "MUSTANGGT_SKIN1", "MUSTANGGT_DRIVER",
]
config = ["[tpk]", "name=MUSTANGGT", "output=TEXTURES.BIN", ""]
for name in names:
    explicit = {
        "MUSTANGGT_KIT00_HEADLIG": "95DE5B23",
        "MUSTANGGT_KIT00_BRAKELI": "4B7D95B6",
    }.get(name)
    config.extend(["[texture]", f"name={name}", f"file={name}.dds"])
    if explicit:
        config.append(f"hash={explicit}")
    config.append("")
(out / "textures.txt").write_text("\n".join(config), encoding="ascii")
(ROOT / "reference" / "materials.json").write_text(json.dumps(mapping, indent=2), encoding="utf-8")
print("Prepared", len(mapping), "materials in donor-compatible atlases")
