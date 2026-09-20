import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[1]


def summarize(path, label):
    parts = json.loads(path.read_text())
    print(f"=== {label} part names ===")
    for part in parts:
        name = part["name"]
        mesh = part["mesh"]
        print(f"{name:55} tris={mesh['TriangleCount']:6} groups={len(mesh['Groups'])}")
    print()


summarize(root / "work/donor-geometry.json", "donor")

compiled = json.loads((root / "work/compiled-geometry.json").read_text())
print("=== compiled names containing WHEEL/RIM/TIRE ===")
for part in compiled:
    name = part["name"]
    if any(token in name for token in ("WHEEL", "RIM", "TIRE", "BRAKE")):
        print(name, part["mesh"]["TriangleCount"])

nascar = json.loads((root / "work/nascar-geometry.json").read_text())
body = next(part for part in nascar if part["name"] == "SUPRA_KIT00_BODY_A")
print("\n=== NASCAR BODY_A ===")
print("shaders", [hex(shader) for shader in body["info"]["Shaders"]])
print("textures", [hex(texture) for texture in body["info"]["Textures"]])
print("groups", len(body["mesh"]["Groups"]))
for index, group in enumerate(body["mesh"]["Groups"]):
    print(
        f" group {index} tris={group['TriangleCount']} verts={group['VertexCount']} "
        f"tex={group.get('TextureIndex0')} sh={group.get('ShaderIndex0')} "
        f"x=({group['BoundsMin']['x']:.2f},{group['BoundsMax']['x']:.2f}) "
        f"y=({group['BoundsMin']['y']:.2f},{group['BoundsMax']['y']:.2f}) "
        f"z=({group['BoundsMin']['z']:.2f},{group['BoundsMax']['z']:.2f})"
    )

verts = body["mesh"]["Vertices"]
indices = body["mesh"]["Indices"]
front = [vertex for vertex in verts if vertex["Position"]["x"] > 1.8]
print("front verts x>1.8", len(front))
if front:
    xs = [vertex["Position"]["x"] for vertex in front]
    ys = [vertex["Position"]["y"] for vertex in front]
    zs = [vertex["Position"]["z"] for vertex in front]
    print(
        f"front bounds x=({min(xs):.2f},{max(xs):.2f}) "
        f"y=({min(ys):.2f},{max(ys):.2f}) z=({min(zs):.2f},{max(zs):.2f})"
    )

fusion_body = next(part for part in compiled if part["name"] == "MUSTANGGT_KIT00_BODY_A")
print("\n=== Fusion BODY_A front x>1.8 ===")
fverts = [vertex for vertex in fusion_body["mesh"]["Vertices"] if vertex["Position"]["x"] > 1.8]
if fverts:
    xs = [vertex["Position"]["x"] for vertex in fverts]
    ys = [vertex["Position"]["y"] for vertex in fverts]
    zs = [vertex["Position"]["z"] for vertex in fverts]
    print(
        f"count={len(fverts)} x=({min(xs):.2f},{max(xs):.2f}) "
        f"y=({min(ys):.2f},{max(ys):.2f}) z=({min(zs):.2f},{max(zs):.2f})"
    )

donor_window = next(part for part in json.loads((root / "work/donor-geometry.json").read_text()) if "FRONT_WINDOW_A" in part["name"])
print("\n=== donor FRONT_WINDOW shaders ===", [hex(shader) for shader in donor_window["info"]["Shaders"]])
print("donor FRONT_WINDOW textures", [hex(texture) for texture in donor_window["info"]["Textures"]])
