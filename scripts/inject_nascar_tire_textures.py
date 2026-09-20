"""Copy the NASCAR tire/rim texture payloads into the Fusion TEXTURES.BIN."""
import struct
from pathlib import Path

from merge_textures import chunk, read_pack

ROOT = Path(__file__).resolve().parents[1]
release = ROOT / "release/MUSTANGGT/TEXTURES.BIN"
nascar = ROOT / "donor/Fusion-NASCAR/ADDONS/CARS_REPLACE/SUPRA/TEXTURES.BIN"
wanted = {0x92A193DD, 0xC1560BAA}

info, current = read_pack(release)
_, donor_nascar = read_pack(nascar)
missing = {hash_value: donor_nascar[hash_value] for hash_value in wanted if hash_value not in current}
if not missing:
    print("NASCAR_TIRE_TEXTURES already present")
    raise SystemExit(0)
for hash_value in wanted:
    if hash_value not in donor_nascar:
        raise SystemError(f"NASCAR TPK missing {hash_value:08X}")

merged = current | missing
hashes = sorted(merged)
table_size = 24 * len(hashes)


def header(table):
    return chunk(0, b"\0" * 48) + chunk(
        0xB3310000,
        chunk(0x33310001, info)
        + chunk(0x33310002, b"".join(struct.pack("<II", hash_value, 0) for hash_value in hashes))
        + chunk(0x33310003, table),
    )


head = header(b"\0" * table_size)
pos = 8 + len(head)
padding = (-pos - 8) % 128
pre = chunk(0, b"\0" * padding)
pos += len(pre)
blocks = []
records = []
for hash_value in hashes:
    payload, unpacked, flags, blank = merged[hash_value]
    records.append(struct.pack("<6I", hash_value, pos, len(payload), unpacked, flags, blank))
    blocks.append(payload)
    pos += len(payload)
    pad = (-pos) % 128
    blocks.append(b"\0" * pad)
    pos += pad
result = chunk(0xB3300000, header(b"".join(records)) + pre + b"".join(blocks))
release.write_bytes(result)
print("NASCAR_TIRE_TEXTURES", {f"{hash_value:08X}": len(missing[hash_value][0]) for hash_value in missing})
