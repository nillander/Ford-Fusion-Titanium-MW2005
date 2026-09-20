"""Normalize the Shelby donor into the retail MW geometry layout used by V2.

The supplied Shelby MODLOADER geometry contains its solid chunks as one JDLZ
stream after an uncompressed part catalogue.  V2 never changes that donor.
This script expands that stream into a V2-only working copy with the catalogue
followed by ordinary sibling solid chunks, which the MW compiler can inspect.
"""
from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
V2 = PROJECT / "versions" / "v2-mustang-shelby"
SOURCE = PROJECT / "source" / "fusion-2017-dev"
DONOR = PROJECT / "donor" / "ford_mustang_shelby" / "MODLOADER" / "ADDONS" / "CARS_REPLACE" / "MUSTANGGT"
WORK = V2 / "work"
REFERENCE = V2 / "reference"


def decompress_jdlz(data: bytes) -> bytes:
    if len(data) < 16 or data[:4] != b"JDLZ" or data[4] != 2:
        raise ValueError("JDLZ header ausente ou inválido")
    unpacked_size = struct.unpack_from("<I", data, 8)[0]
    packed_size = struct.unpack_from("<I", data, 12)[0]
    if packed_size < 16 or packed_size > len(data):
        raise ValueError("Tamanho JDLZ inválido")
    flags1 = flags2 = 1
    source = memoryview(data)[:packed_size]
    output = bytearray(unpacked_size)
    in_pos = 16
    out_pos = 0
    while out_pos < unpacked_size:
        if flags1 == 1:
            flags1 = source[in_pos] | 0x100
            in_pos += 1
        if flags2 == 1:
            flags2 = source[in_pos] | 0x100
            in_pos += 1
        if flags1 & 1:
            a, b = source[in_pos], source[in_pos + 1]
            in_pos += 2
            if flags2 & 1:
                length, back = b + ((a & 0xF0) << 4) + 3, (a & 0x0F) + 1
            else:
                length, back = (a & 0x1F) + 3, b + ((a & 0xE0) << 3) + 17
            if back > out_pos or out_pos + length > unpacked_size:
                raise ValueError("Referência JDLZ fora do fluxo")
            for i in range(length):
                output[out_pos + i] = output[out_pos + i - back]
            out_pos += length
            flags2 >>= 1
        else:
            output[out_pos] = source[in_pos]
            out_pos += 1
            in_pos += 1
        flags1 >>= 1
    return bytes(output)


def digest(path: Path) -> dict[str, object]:
    return {"bytes": path.stat().st_size, "sha256": hashlib.file_digest(path.open("rb"), "sha256").hexdigest()}


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    REFERENCE.mkdir(parents=True, exist_ok=True)
    geometry = DONOR / "GEOMETRY.BIN"
    textures = DONOR / "TEXTURES.BIN"
    data = geometry.read_bytes()
    stream_offset = data.find(b"JDLZ")
    if stream_offset < 0:
        raise ValueError("O GEOMETRY.BIN do Shelby não contém sólidos JDLZ")
    retail = bytearray(data[:stream_offset])
    packed_offset = stream_offset
    solid_count = 0
    while packed_offset + 16 <= len(data):
        if data[packed_offset:packed_offset + 4] != b"JDLZ":
            raise ValueError(f"Sólido JDLZ ausente em 0x{packed_offset:X}")
        packed_size = struct.unpack_from("<I", data, packed_offset + 12)[0]
        retail.extend(decompress_jdlz(data[packed_offset:packed_offset + packed_size]))
        solid_count += 1
        padding = (-len(retail)) % 0x80
        if padding:
            if padding < 8:
                raise ValueError("Alinhamento de sólido Shelby inválido")
            retail.extend(struct.pack("<II", 0, padding - 8))
            retail.extend(b"\0" * (padding - 8))
        packed_offset = (packed_offset + packed_size + 0x7F) & ~0x7F
        # Toolkit exports leave zero-filled alignment pages between some
        # compressed solids, occasionally carrying a small page marker.
        # Each valid JDLZ container begins on 0x80; those intervening bytes
        # belong to the compressed container and are not part of retail data.
        while packed_offset < len(data) and data[packed_offset:packed_offset + 4] != b"JDLZ":
            packed_offset += 0x80
    # Retail MW keeps the catalogue bounded by its original root length and
    # places the individual solid chunks as siblings after it.
    if retail[:4] != b"\x00@\x13\x80":
        raise ValueError("Catálogo Shelby inesperado após descompressão")
    # The compressed export reserves one 0x80-aligned page before its first
    # JDLZ solid.  Retail MW represents that page as the empty-solid marker.
    empty_chunk = stream_offset - 0x80
    if empty_chunk < 8:
        raise ValueError("Separador de sólidos Shelby ausente")
    struct.pack_into("<II", retail, empty_chunk, 0x80134008, 0)
    struct.pack_into("<II", retail, empty_chunk + 8, 0, 0x70)
    struct.pack_into("<I", retail, 4, empty_chunk - 8)
    target = WORK / "shelby-retail.bin"
    target.write_bytes(retail)
    manifest = {
        "version": "v2-mustang-shelby",
        "source": {str(SOURCE.relative_to(PROJECT)): digest(SOURCE / "fusion" / "dlc.rpf")},
        "donor_geometry": {str(geometry.relative_to(PROJECT)): digest(geometry)},
        "donor_textures": {str(textures.relative_to(PROJECT)): digest(textures)},
        "retail_geometry": digest(target),
        "jdlz_offset": stream_offset,
        "solid_count": solid_count,
    }
    (REFERENCE / "input-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Shelby V2 retail donor: {target} ({len(retail)} bytes)")


if __name__ == "__main__":
    main()
