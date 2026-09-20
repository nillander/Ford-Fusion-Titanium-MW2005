import json
from pathlib import Path

src = json.loads(Path("reference/source-structure.json").read_text())
for mesh in src["meshes"]:
    bone = mesh["dominant_bone"].lower()
    if "exh" in bone or "escape" in bone:
        print(
            f"{mesh['key']:28} bone={mesh['dominant_bone']:16} "
            f"sh={mesh['shader']:2} tris={mesh['triangles']:5} origin={mesh['origin']}"
        )
