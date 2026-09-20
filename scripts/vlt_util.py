"""Minimal VPak/VLT helpers for NFS Most Wanted ATTRIBUTES.BIN."""
from __future__ import annotations

import struct
from dataclasses import dataclass, field
from pathlib import Path


def jenkins32(raw: bytes) -> int:
    index = 0
    remaining = len(raw)
    alpha = beta = 0x9E3779B9
    gamma = 0xABCDEF00

    def mix(a: int, b: int, c: int) -> tuple[int, int, int]:
        a = (c >> 13) ^ ((a - b - c) & 0xFFFFFFFF)
        a &= 0xFFFFFFFF
        b = ((a << 8) & 0xFFFFFFFF) ^ ((b - c - a) & 0xFFFFFFFF)
        b &= 0xFFFFFFFF
        c = (b >> 13) ^ ((c - a - b) & 0xFFFFFFFF)
        c &= 0xFFFFFFFF
        a = (c >> 12) ^ ((a - b - c) & 0xFFFFFFFF)
        a &= 0xFFFFFFFF
        b = ((a << 16) & 0xFFFFFFFF) ^ ((b - c - a) & 0xFFFFFFFF)
        b &= 0xFFFFFFFF
        c = (b >> 5) ^ ((c - a - b) & 0xFFFFFFFF)
        c &= 0xFFFFFFFF
        a = (c >> 3) ^ ((a - b - c) & 0xFFFFFFFF)
        a &= 0xFFFFFFFF
        b = ((a << 10) & 0xFFFFFFFF) ^ ((b - c - a) & 0xFFFFFFFF)
        b &= 0xFFFFFFFF
        c = (b >> 15) ^ ((c - a - b) & 0xFFFFFFFF)
        c &= 0xFFFFFFFF
        return a, b, c

    while remaining >= 12:
        alpha = (alpha + struct.unpack_from("<I", raw, index)[0]) & 0xFFFFFFFF
        beta = (beta + struct.unpack_from("<I", raw, index + 4)[0]) & 0xFFFFFFFF
        gamma = (gamma + struct.unpack_from("<I", raw, index + 8)[0]) & 0xFFFFFFFF
        alpha, beta, gamma = mix(alpha, beta, gamma)
        index += 12
        remaining -= 12
    gamma = (gamma + len(raw)) & 0xFFFFFFFF
    blob = raw[index:]
    extras = (
        (11, "gamma", 24),
        (10, "gamma", 16),
        (9, "gamma", 8),
        (8, "beta", 24),
        (7, "beta", 16),
        (6, "beta", 8),
        (5, "beta", 0),
        (4, "alpha", 24),
        (3, "alpha", 16),
        (2, "alpha", 8),
        (1, "alpha", 0),
    )
    registers = {"alpha": alpha, "beta": beta, "gamma": gamma}
    for minimum, name, shift in extras:
        if remaining >= minimum:
            registers[name] = (registers[name] + (blob[minimum - 1] << shift)) & 0xFFFFFFFF
    alpha, beta, gamma = mix(registers["alpha"], registers["beta"], registers["gamma"])
    return gamma


def hash_name(name: str) -> int:
    return jenkins32(name.encode("ascii"))


@dataclass
class VPakEntry:
    name: str
    bin_offset: int
    bin_length: int
    vlt_offset: int
    vlt_length: int


def unpack_vpak(data: bytes) -> list[tuple[VPakEntry, bytes, bytes]]:
    magic, count, table_offset, table_length = struct.unpack_from("<4I", data, 0)
    if magic not in (0, 0x4B415056):
        raise ValueError(f"not a VPak (magic={magic:#x})")
    names: dict[int, str] = {}
    table = data[table_offset : table_offset + table_length]
    current = 0
    text = ""
    for index, byte in enumerate(table):
        if byte == 0:
            names[current] = text
            current = index + 1
            text = ""
        else:
            text += chr(byte)
    entries = []
    cursor = 16
    for _ in range(count):
        file_number, bin_length, vlt_length, bin_location, vlt_location = struct.unpack_from("<5I", data, cursor)
        cursor += 20
        entry = VPakEntry(names[file_number], bin_location, bin_length, vlt_location, vlt_length)
        entries.append((entry, data[bin_location : bin_location + bin_length], data[vlt_location : vlt_location + vlt_length]))
    return entries


@dataclass
class ClassField:
    name_hash: int
    type_hash: int
    offset: int
    length: int
    count: int
    flags: int

    @property
    def is_array(self) -> bool:
        return (self.flags & 0x1) != 0

    @property
    def is_optional(self) -> bool:
        return (self.flags & 0x2) == 0


@dataclass
class OptionalField:
    name_hash: int
    pointer: int
    flags1: int
    flags2: int
    embedded: bool


@dataclass
class Collection:
    name_hash: int
    class_hash: int
    parent_hash: int
    required_pointer: int
    required_offset: int | None
    optionals: list[OptionalField] = field(default_factory=list)


@dataclass
class VltClass:
    name_hash: int
    field_pointer: int
    field_offset: int | None
    total_fields: int
    fields: list[ClassField] = field(default_factory=list)


class VltDatabase:
    def __init__(self, bin_data: bytes, vlt_data: bytes):
        self.bin = bytearray(bin_data)
        self.vlt = vlt_data
        self.pointers: dict[int, int] = {}
        self.classes: dict[int, VltClass] = {}
        self.collections: list[Collection] = []
        self._parse()

    def _parse(self) -> None:
        chunks = self._chunks(self.vlt)
        pointers_chunk = chunks.get(0x5074724E)
        expression_chunk = chunks.get(0x4578704E)
        if pointers_chunk is None or expression_chunk is None:
            raise ValueError("VLT missing PtrN/ExpN")
        self.pointers = self._parse_pointers(self.vlt, pointers_chunk)
        self._parse_expressions(self.vlt, expression_chunk)
        for item in self.classes.values():
            if item.field_offset is None:
                continue
            cursor = item.field_offset
            for _ in range(item.total_fields):
                name_hash, type_hash, offset, length, count, flags, _align = struct.unpack_from("<IIHHHBB", self.bin, cursor)
                item.fields.append(ClassField(name_hash, type_hash, offset, length, count, flags))
                cursor += 16

    def _chunks(self, data: bytes) -> dict[int, tuple[int, int]]:
        chunks = {}
        cursor = 0
        while cursor + 8 <= len(data):
            chunk_id, length = struct.unpack_from("<iI", data, cursor)
            if length < 8 or cursor + length > len(data):
                break
            chunks[chunk_id] = (cursor + 8, length - 8)
            cursor += length
            if cursor % 16:
                cursor += 16 - (cursor % 16)
        return chunks

    def _parse_pointers(self, data: bytes, span: tuple[int, int]) -> dict[int, int]:
        start, length = span
        cursor = start
        end = start + length
        mapping: dict[int, int] = {}
        load_vlt = False
        while cursor + 12 <= end:
            source, block_type, identifier, dest = struct.unpack_from("<iHHi", data, cursor)
            cursor += 12
            if block_type == 0:
                break
            if block_type == 2 and identifier in (0, 1):
                load_vlt = identifier == 0
                continue
            if load_vlt and block_type in (1, 3) and (block_type == 1 or identifier == 1):
                mapping[source] = dest
        return mapping

    def _parse_expressions(self, data: bytes, span: tuple[int, int]) -> None:
        start, length = span
        count = struct.unpack_from("<I", data, start)[0]
        cursor = start + 4
        records = []
        for _ in range(count):
            expression_id, expression_type, _zero, record_length, offset = struct.unpack_from("<5I", data, cursor)
            records.append((expression_type, offset))
            cursor += 20
        for expression_type, offset in records:
            if expression_type == 0x5E970CBC:
                name_hash, _collections, total_fields = struct.unpack_from("<III", data, offset)
                pointer = offset + 12
                self.classes[name_hash] = VltClass(name_hash, pointer, self.pointers.get(pointer), total_fields)
            elif expression_type == 0x8E112EB7:
                self.collections.append(self._read_collection(data, offset))

    def _read_collection(self, data: bytes, offset: int) -> Collection:
        name_hash, class_hash, parent_hash, count_optional, _num1, count_optional_again, type_count = struct.unpack_from("<IIIIIII", data, offset)
        pointer = offset + 28
        cursor = offset + 32
        cursor += 4 * type_count
        optionals = []
        for _ in range(count_optional):
            field_hash = struct.unpack_from("<I", data, cursor)[0]
            field_pointer = cursor + 4
            flags1, flags2 = struct.unpack_from("<hh", data, cursor + 8)
            embedded = (flags2 & 0x20) == 0 and (flags2 & 0x40) > 0
            optionals.append(OptionalField(field_hash, field_pointer, flags1, flags2, embedded))
            cursor += 12
        return Collection(
            name_hash=name_hash,
            class_hash=class_hash,
            parent_hash=parent_hash,
            required_pointer=pointer,
            required_offset=self.pointers.get(pointer),
            optionals=optionals,
        )

    def required_size(self, class_hash: int) -> int:
        item = self.classes[class_hash]
        end = 0
        for field in item.fields:
            if field.is_optional:
                continue
            end = max(end, field.offset + field.length)
        return end

    def find_collections(self, class_hash: int, name_hash: int) -> list[Collection]:
        return [item for item in self.collections if item.class_hash == class_hash and item.name_hash == name_hash]


def dump_named_collections(database: VltDatabase, names: list[str]) -> None:
    wanted = {hash_name(name): name for name in names}
    class_names = {hash_name(name): name for name in (
        "engine", "transmission", "tires", "brakes", "chassis", "pvehicle",
        "ecar", "induction", "nos", "aerodynamics",
    )}
    for collection in database.collections:
        name = wanted.get(collection.name_hash)
        if name is None:
            continue
        class_name = class_names.get(collection.class_hash, f"{collection.class_hash:08X}")
        print(
            f"{class_name}/{name} parent={collection.parent_hash:08X} "
            f"req=0x{collection.required_offset if collection.required_offset is not None else -1:X} "
            f"opt={len(collection.optionals)}"
        )
