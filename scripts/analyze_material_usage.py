"""Summarize source mesh use by material, dominant bone, triangle count and UV range."""
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
structure = json.loads((ROOT / "reference" / "source-structure.json").read_text())
materials = json.loads((ROOT / "reference" / "materials.json").read_text())

rows = defaultdict(lambda: {"meshes": 0, "vertices": 0, "triangles": 0, "uv_min": [999.0, 999.0], "uv_max": [-999.0, -999.0]})
for item in structure["meshes"]:
    shader = int(item["shader"])
    bone = item["dominant_bone"]
    data = np.load(ROOT / "work" / "source-meshes" / f"{item['key']}.npz")
    vertices = data["vertices"]
    uv = vertices["TexCoord0"]
    row = rows[(shader, bone)]
    row["meshes"] += 1
    row["vertices"] += len(vertices)
    row["triangles"] += len(data["indices"]) // 3
    row["uv_min"] = np.minimum(row["uv_min"], uv.min(axis=0)).tolist()
    row["uv_max"] = np.maximum(row["uv_max"], uv.max(axis=0)).tolist()

report = []
for (shader, bone), totals in rows.items():
    report.append({
        "shader": shader,
        "source": materials[shader]["source"],
        "mw_shader": materials[shader]["shader"],
        "bone": bone,
        **totals,
    })
report.sort(key=lambda row: (row["shader"], -row["triangles"], row["bone"]))
(ROOT / "reference" / "material-usage.json").write_text(json.dumps(report, indent=2))

for row in report:
    print(
        f"{row['shader']:02d} {row['source']:<24} {row['bone']:<24} "
        f"v={row['vertices']:7d} t={row['triangles']:7d} "
        f"uv={row['uv_min']}..{row['uv_max']}"
    )
