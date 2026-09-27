"""Patch one uncompressed DXT3 BADGING payload in-place in a MW TPK copy."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from merge_textures import read_pack

source, hash_text, dds, output = map(Path, sys.argv[1:5])
hash_value = int(str(hash_text), 16)
info, entries = read_pack(source)
old_payload, unpacked, flags, blank = entries[hash_value]
replacement_dds = dds.read_bytes()
if old_payload[:4] != b"RAWW":
    raise ValueError("BADGING payload is unexpectedly compressed")
# RAWW is followed by the DXT stream, then the 156-byte MW texture record.
# Validator recreates a normal 128-byte DDS header when extracting it, so only
# inject the DDS payload (not its synthetic header) and retain that record.
texture_offset = 16
replacement_blocks = replacement_dds[128:]
trailer_offset = texture_offset + len(replacement_blocks)
if len(old_payload) < trailer_offset:
    raise ValueError("replacement DXT payload size changed")
new_payload = old_payload[:texture_offset] + replacement_blocks + old_payload[trailer_offset:]
data = bytearray(source.read_bytes())
offset = data.find(old_payload)
if offset < 0 or data.find(old_payload, offset + 1) >= 0:
    raise ValueError("could not uniquely locate BADGING payload")
data[offset:offset + len(old_payload)] = new_payload
output.write_bytes(data)
_, verified = read_pack(output)
if verified[hash_value][0] != new_payload:
    raise ValueError("TPK verification failed")
