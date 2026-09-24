"""Give the Fusion in the mustanggt slot SLR power and M3 GTR drivability.

Keeps the Fusion wheel positions. Engine, gearbox and induction come from the
Mercedes-Benz SLR McLaren. Chassis, tires, brakes, mass, inertia and the ecar
ride (height, camber, skid width, dive, squat, roll) come from the protagonist
BMW M3 GTR. The hero car has no upgrade tier, so both tiers share that
drivability. The Mod Loader reapplies ATTRIBUTES.MWPS at launch, so that
script is rewritten to the same values.
"""
from __future__ import annotations

import hashlib
import re
import shutil
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from copy_slr_stats_to_mustang import copy_bytes, copy_matching_optionals, copy_required, patch_vpak, report_engine
from vlt_util import VltDatabase, hash_name, unpack_vpak

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"D:\Program Files (x86)\Electronic Arts\Need For Speed Most Wanted Black Edition")
ATTR = GAME / "GLOBAL" / "ATTRIBUTES.BIN"
FE = GAME / "GLOBAL" / "FE_ATTRIB.BIN"
MWPS = GAME / "ADDONS" / "CARS_REPLACE" / "MUSTANGGT" / "ATTRIBUTES.MWPS"
FUSION = ROOT / "versions" / "performance" / "fusion-mustang"
M3 = ROOT / "versions" / "performance" / "m3gtr"
HYBRID = ROOT / "versions" / "performance" / "slr-m3gtr"

POWER = (
    ("engine", "slr", "mustanggt"),
    ("engine", "slr_top", "mustanggt_top"),
    ("transmission", "slr", "mustanggt"),
    ("transmission", "slr_top", "mustanggt_top"),
    ("induction", "slr", "mustanggt_base"),
    ("induction", "slr_top", "mustanggt_top"),
)
HANDLING = ("tires", "brakes", "chassis")
DESTINATIONS = ("mustanggt", "mustanggt_top")
ECAR_HANDLING = ("RideHeight", "CamberFront", "CamberRear", "TireSkidWidth", "BodyDive", "BodySquat", "BodyRoll")
PATCH_LINE = re.compile(r"^(patch\s+(\w+)\s+bin:(0x[0-9a-fA-F]+)\s+)(\S+)(\s*)$")


def copy_field(database: VltDatabase, class_name: str, source_name: str, dest_name: str, field_name: str) -> tuple[int, int]:
    class_hash = hash_name(class_name)
    source = database.find_collections(class_hash, hash_name(source_name))[0]
    dest = database.find_collections(class_hash, hash_name(dest_name))[0]
    field = next(item for item in database.classes[class_hash].fields if item.name_hash == hash_name(field_name))
    size = field.length * (field.count if field.count else 1)
    copy_bytes(database.bin, bytes(database.bin), dest.required_offset + field.offset, source.required_offset + field.offset, size)
    print(f"copied {class_name}.{field_name} {source_name} -> {dest_name} {size} bytes")
    return dest.required_offset + field.offset, size


def backup_current() -> None:
    FUSION.mkdir(parents=True, exist_ok=True)
    for source, name in ((ATTR, "ATTRIBUTES.BIN"), (FE, "FE_ATTRIB.BIN"), (MWPS, "ATTRIBUTES.MWPS")):
        target = FUSION / name
        if not target.exists():
            shutil.copy2(source, target)
            print("backed up", name)


def spans_for(database: VltDatabase, pairs: tuple[tuple[str, str, str], ...]) -> list[tuple[int, int]]:
    spans = []
    for class_name, _source_name, dest_name in pairs:
        found = database.find_collections(hash_name(class_name), hash_name(dest_name))
        if not found or found[0].required_offset is None:
            continue
        start = found[0].required_offset
        spans.append((start, start + database.required_size(hash_name(class_name))))
    return spans


def format_value(kind: str, blob: bytes) -> str:
    if kind == "float":
        value = struct.unpack("<f", blob[:4])[0]
        return f"{value:.6g}"
    if kind == "int32":
        return str(struct.unpack_from("<i", blob)[0])
    if kind == "int16":
        return str(struct.unpack_from("<h", blob)[0])
    if kind == "int8":
        return str(struct.unpack_from("<b", blob)[0])
    raise ValueError(kind)


def rewrite_mwps(database: VltDatabase, spans: list[tuple[int, int]]) -> str:
    lines = MWPS.read_text(encoding="utf-8").splitlines(keepends=True)
    changed = 0
    rewritten = []
    for line in lines:
        match = PATCH_LINE.match(line.rstrip("\r\n"))
        if not match:
            rewritten.append(line)
            continue
        offset = int(match.group(3), 16)
        if not any(start <= offset < end for start, end in spans):
            rewritten.append(line)
            continue
        kind = match.group(2)
        width = {"float": 4, "int32": 4, "int16": 2, "int8": 1}[kind]
        value = format_value(kind, database.bin[offset : offset + width])
        newline = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
        rewritten.append(f"{match.group(1)}{value}{match.group(5)}{newline}")
        changed += 1
    print("rewrote", changed, "MWPS patches")
    return "".join(rewritten)


def main() -> None:
    backup_current()
    entry, raw, vlt = unpack_vpak(ATTR.read_bytes())[0]
    database = VltDatabase(raw, vlt)
    print("before")
    report_engine(database, "mustanggt")
    report_engine(database, "slr")
    report_engine(database, "bmwm3gtr")

    handling_pairs = tuple((class_name, "bmwm3gtr", dest_name) for class_name in HANDLING for dest_name in DESTINATIONS)
    for class_name, source_name, dest_name in handling_pairs:
        copy_required(database, class_name, source_name, dest_name)
    for class_name, source_name, dest_name in POWER:
        copy_required(database, class_name, source_name, dest_name)
    for field_name in ("MASS", "TENSOR_SCALE"):
        copy_field(database, "pvehicle", "bmwm3gtr", "mustanggt", field_name)
    copy_matching_optionals(database, "pvehicle", "bmwm3gtr", "mustanggt", {hash_name("HandlingRating")})
    for field_name in ECAR_HANDLING:
        copy_field(database, "ecar", "bmwm3gtr", "mustanggt", field_name)

    covered = spans_for(database, handling_pairs + POWER)
    mass_start, mass_size = copy_field(database, "pvehicle", "bmwm3gtr", "mustanggt", "MASS")
    scale_start, scale_size = copy_field(database, "pvehicle", "bmwm3gtr", "mustanggt", "TENSOR_SCALE")
    covered.extend(((mass_start, mass_start + mass_size), (scale_start, scale_start + scale_size)))
    for field_name in ECAR_HANDLING:
        start, size = copy_field(database, "ecar", "bmwm3gtr", "mustanggt", field_name)
        covered.append((start, start + size))
    handling = database.find_collections(hash_name("pvehicle"), hash_name("mustanggt"))[0]
    for optional in handling.optionals:
        if optional.name_hash == hash_name("HandlingRating"):
            start = database.pointers[optional.pointer]
            covered.append((start, start + 8))

    print("after")
    report_engine(database, "mustanggt")
    report_engine(database, "mustanggt_top")
    report_engine(database, "slr")

    text = rewrite_mwps(database, covered)
    HYBRID.mkdir(parents=True, exist_ok=True)
    (HYBRID / "ATTRIBUTES.MWPS").write_text(text, encoding="utf-8", newline="")
    MWPS.write_text(text, encoding="utf-8", newline="")
    patch_vpak(ATTR, database, entry.bin_offset)
    shutil.copy2(ATTR, HYBRID / "ATTRIBUTES.BIN")
    if not (HYBRID / "FE_ATTRIB.BIN").exists():
        shutil.copy2(FE, HYBRID / "FE_ATTRIB.BIN")
    for folder in (FUSION, M3, HYBRID):
        if not folder.exists():
            continue
        for path in folder.iterdir():
            print(folder.name, path.name, hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
