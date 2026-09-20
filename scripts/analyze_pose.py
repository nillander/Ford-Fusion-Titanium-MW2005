"""Estimate articulated panel orientation from source vertex positions."""
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
src = json.loads((ROOT / "reference/source-structure.json").read_text())
groups = {}
for item in src["meshes"]:
    if item.get("origin") != "main":
        continue
    arr = np.load(ROOT / "work/source-meshes" / f"{item['key']}.npz")
    pos = arr["vertices"]["Position"]
    groups.setdefault(item["dominant_bone"], []).append(pos)

for name, chunks in groups.items():
    p = np.concatenate(chunks)
    centered = p - p.mean(axis=0)
    _, values, vh = np.linalg.svd(centered, full_matrices=False)
    print(name, "n", len(p), "center", np.round(p.mean(0), 4).tolist(),
          "range", np.round(np.ptp(p, axis=0), 4).tolist(),
          "axes", np.round(vh, 4).tolist(), "sv", np.round(values, 2).tolist())
