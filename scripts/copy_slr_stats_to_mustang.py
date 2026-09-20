"""Copy Mercedes-Benz SLR McLaren VLT performance onto mustanggt.

Keeps ecar visual fields (Fusion tire offsets / ride height) untouched.
"""
from __future__ import annotations

import hashlib
import shutil
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vlt_util import VltDatabase, hash_name, unpack_vpak

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"D:\Program Files (x86)\Electronic Arts\Need For Speed Most Wanted Black Edition")
ATTR = GAME / "GLOBAL" / "ATTRIBUTES.BIN"
FE = GAME / "GLOBAL" / "FE_ATTRIB.BIN"
BACKUP = ROOT / "work" / "game-backup" / "pre-slr-stats-GLOBAL"

PERFORMANCE_CLASSES = (
    "engine",
    "transmission",
    "tires",
    "brakes",
    "chassis",
    "induction",
)
COLLECTION_PAIRS = (
    ("engine", "slr", "mustanggt"),
    ("engine", "slr_top", "mustanggt_top"),
    ("transmission", "slr", "mustanggt"),
    ("transmission", "slr_top", "mustanggt_top"),
    ("tires", "slr", "mustanggt"),
    ("tires", "slr_top", "mustanggt_top"),
    ("brakes", "slr", "mustanggt"),
    ("brakes", "slr_top", "mustanggt_top"),
    ("chassis", "slr", "mustanggt"),
    ("chassis", "slr_top", "mustanggt_top"),
    ("induction", "slr", "mustanggt_base"),
    ("induction", "slr_top", "mustanggt_top"),
    ("pvehicle", "slr", "mustanggt"),
)
# Copy every pvehicle optional except identity-only leftovers.
# HandlingRating (AACBE2E7), TurboSND and engineaudio live here, not in the required blob.
PVEHICLE_OPTIONALS = None
SKIP_CLASSES = {hash_name("ecar")}


def backup_globals() -> None:
    BACKUP.mkdir(parents=True, exist_ok=True)
    for path in (ATTR, FE):
        target = BACKUP / path.name
        if not target.exists():
            shutil.copy2(path, target)
            print("backed up", path.name)


def optional_size(database: VltDatabase, class_hash: int, field_hash: int) -> int:
    item = database.classes[class_hash]
    for field in item.fields:
        if field.name_hash == field_hash:
            count = field.count if field.count > 0 else 1
            payload = field.length * count
            # VLT arrays store used/max plus the payload.
            return payload + (8 if field.is_array or count > 1 else 0)
    return 0


def copy_bytes(destination: bytearray, source: bytes, dest_offset: int, source_offset: int, size: int) -> int:
    destination[dest_offset : dest_offset + size] = source[source_offset : source_offset + size]
    return size


def copy_required(database: VltDatabase, class_name: str, source_name: str, dest_name: str) -> int:
    class_hash = hash_name(class_name)
    source = database.find_collections(class_hash, hash_name(source_name))
    dest = database.find_collections(class_hash, hash_name(dest_name))
    if not source or not dest or source[0].required_offset is None or dest[0].required_offset is None:
        print("missing collection", class_name, source_name, dest_name)
        return 0
    size = database.required_size(class_hash)
    if size <= 0:
        print("no required size", class_name)
        return 0
    copy_bytes(database.bin, bytes(database.bin), dest[0].required_offset, source[0].required_offset, size)
    print(f"copied {class_name}/{source_name} -> {dest_name} {size} bytes @0x{dest[0].required_offset:X}")
    return size


def copy_matching_optionals(database: VltDatabase, class_name: str, source_name: str, dest_name: str, allowed: set[int] | None) -> int:
    class_hash = hash_name(class_name)
    source = database.find_collections(class_hash, hash_name(source_name))[0]
    dest = database.find_collections(class_hash, hash_name(dest_name))[0]
    dest_by_hash = {item.name_hash: item for item in dest.optionals}
    changed = 0
    for optional in source.optionals:
        if allowed is not None and optional.name_hash not in allowed:
            continue
        target = dest_by_hash.get(optional.name_hash)
        if target is None:
            continue
        source_offset = database.pointers.get(optional.pointer)
        dest_offset = database.pointers.get(target.pointer)
        size = optional_size(database, class_hash, optional.name_hash)
        if source_offset is None or dest_offset is None or size <= 0:
            print(f"skip optional {class_name} {optional.name_hash:08X}")
            continue
        copy_bytes(database.bin, bytes(database.bin), dest_offset, source_offset, size)
        changed += size
        print(f"copied {class_name} optional {optional.name_hash:08X} {size} bytes")
    return changed


def patch_vpak(path: Path, database: VltDatabase, raw_offset: int) -> None:
    data = bytearray(path.read_bytes())
    data[raw_offset : raw_offset + len(database.bin)] = database.bin
    path.write_bytes(data)
    print("wrote", path, "sha256", hashlib.sha256(data).hexdigest())


def report_engine(database: VltDatabase, name: str) -> None:
    collection = database.find_collections(hash_name("engine"), hash_name(name))[0]
    offset = collection.required_offset
    torque = [struct.unpack_from("<f", database.bin, offset + index * 4)[0] for index in range(9)]
    redline = struct.unpack_from("<f", database.bin, offset + 0x58)[0]
    print(f"{name} torque={ [round(value, 1) for value in torque] } redline={redline:.0f}")


def main() -> None:
    backup_globals()

    attr_data = ATTR.read_bytes()
    entry, raw, vlt = unpack_vpak(attr_data)[0]
    database = VltDatabase(raw, vlt)
    print("before")
    report_engine(database, "slr")
    report_engine(database, "mustanggt")

    copied = 0
    for class_name, source_name, dest_name in COLLECTION_PAIRS:
        copied += copy_required(database, class_name, source_name, dest_name)
    copied += copy_matching_optionals(database, "pvehicle", "slr", "mustanggt", None)

    print("after")
    report_engine(database, "mustanggt")
    report_engine(database, "slr")

    patch_vpak(ATTR, database, entry.bin_offset)

    fe_data = FE.read_bytes()
    fe_entry, fe_raw, fe_vlt = unpack_vpak(fe_data)[0]
    frontend = VltDatabase(fe_raw, fe_vlt)
    # Class layout lives in ATTRIBUTES; reuse it for FE collection 85885722.
    frontend.classes[0x85885722] = database.classes[0x85885722]
    source = [item for item in frontend.collections if item.name_hash == hash_name("slr") and item.class_hash == 0x85885722]
    dest = [item for item in frontend.collections if item.name_hash == hash_name("mustanggt") and item.class_hash == 0x85885722]
    if source and dest and source[0].required_offset is not None and dest[0].required_offset is not None:
        size = database.required_size(0x85885722)
        copy_bytes(frontend.bin, bytes(frontend.bin), dest[0].required_offset, source[0].required_offset, size)
        print(f"copied FE 85885722/slr -> mustanggt {size} bytes")
        dest_by_hash = {item.name_hash: item for item in dest[0].optionals}
        for optional in source[0].optionals:
            target = dest_by_hash.get(optional.name_hash)
            source_offset = frontend.pointers.get(optional.pointer)
            dest_offset = frontend.pointers.get(target.pointer) if target else None
            optional_bytes = optional_size(database, 0x85885722, optional.name_hash)
            if target and source_offset is not None and dest_offset is not None and optional_bytes:
                copy_bytes(frontend.bin, bytes(frontend.bin), dest_offset, source_offset, optional_bytes)
                print(f"copied FE optional {optional.name_hash:08X} {optional_bytes} bytes")
        patch_vpak(FE, frontend, fe_entry.bin_offset)
    else:
        print("FE slr/mustanggt collections not found")

    print("total required+optional bytes copied in ATTR", copied)


if __name__ == "__main__":
    main()
