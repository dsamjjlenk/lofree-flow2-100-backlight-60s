#!/usr/bin/env python3
import argparse
import hashlib
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


BASE_ADDRESS = 0x08000000
PATCH_OFFSET = 0x403E
OLD_BYTES = bytes.fromhex("42 F2 10 73")
NEW_BYTES = bytes.fromhex("4E F6 60 23")

EXPECTED_OFFICIAL_HEX_SHA256 = "5586079676271B13ABC74B8CB04AE35C32FC9C3BF5FA9D06FF3FC45C1AA65594"
EXPECTED_OFFICIAL_BIN_SHA256 = "387C3C5F1E5003D96B642EBAEE8A224099EF33D99C01845ECAD2E1F28D676047"
EXPECTED_PATCHED_BIN_SHA256 = "FC7C6CEFE8284075EC427689CD2B213C844B538A5FCB96DFFCA30E0442B61D07"

OUTPUT_BIN_NAME = "oe926_via_v14_backlight_timeout_60s.bin"
OUTPUT_HEX_NAME = "oe926_via_v14_backlight_timeout_60s.hex"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def parse_intel_hex(text: str) -> bytes:
    memory = {}
    upper = 0

    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        if not line.startswith(":"):
            raise ValueError(f"Line {line_no}: not an Intel HEX record")

        count = int(line[1:3], 16)
        address = int(line[3:7], 16)
        record_type = int(line[7:9], 16)
        data = bytes.fromhex(line[9 : 9 + count * 2])
        checksum = int(line[9 + count * 2 : 11 + count * 2], 16)

        total = count + (address >> 8) + (address & 0xFF) + record_type + sum(data) + checksum
        if total & 0xFF:
            raise ValueError(f"Line {line_no}: bad Intel HEX checksum")

        if record_type == 0x00:
            absolute = upper + address
            offset = absolute - BASE_ADDRESS
            if offset < 0:
                raise ValueError(f"Line {line_no}: unexpected address 0x{absolute:08X}")
            for index, value in enumerate(data):
                memory[offset + index] = value
        elif record_type == 0x01:
            break
        elif record_type == 0x04:
            if len(data) != 2:
                raise ValueError(f"Line {line_no}: bad extended linear address record")
            upper = ((data[0] << 8) | data[1]) << 16
        elif record_type == 0x05:
            if len(data) != 4:
                raise ValueError(f"Line {line_no}: bad start linear address record")
        else:
            raise ValueError(f"Line {line_no}: unsupported HEX record type {record_type}")

    if not memory:
        raise ValueError("No firmware data found in Intel HEX file")

    size = max(memory.keys()) + 1
    result = bytearray(size)
    for offset, value in memory.items():
        result[offset] = value
    return bytes(result)


def make_hex_record(record_type: int, address: int, data: bytes) -> str:
    total = len(data) + (address >> 8) + (address & 0xFF) + record_type + sum(data)
    checksum = (-total) & 0xFF
    return f":{len(data):02X}{address:04X}{record_type:02X}{data.hex().upper()}{checksum:02X}"


def to_intel_hex(binary: bytes) -> str:
    records = [make_hex_record(0x04, 0x0000, bytes([0x08, 0x00]))]
    for offset in range(0, len(binary), 16):
        chunk = binary[offset : offset + 16]
        records.append(make_hex_record(0x00, offset & 0xFFFF, chunk))
    records.append(":00000001FF")
    return "\r\n".join(records) + "\r\n"


def load_firmware(path: Path) -> tuple[bytes, str, str]:
    raw = path.read_bytes()
    raw_hash = sha256(raw)
    suffix = path.suffix.lower()

    if suffix == ".hex":
        binary = parse_intel_hex(raw.decode("ascii"))
        parsed_hash = sha256(binary)
        return binary, raw_hash, parsed_hash

    return raw, raw_hash, raw_hash


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build Lofree Flow2 100 / OE926 v14 firmware with a 60-second backlight timeout."
    )
    parser.add_argument("official_firmware", type=Path, help="Official OE926 v14 .hex or parsed .bin")
    parser.add_argument("--out-dir", type=Path, default=Path("dist"), help="Output directory")
    parser.add_argument("--allow-unknown-source", action="store_true")
    args = parser.parse_args()

    binary, file_hash, parsed_hash = load_firmware(args.official_firmware)

    print(f"Input file: {args.official_firmware}")
    print(f"Input file SHA256: {file_hash}")
    print(f"Parsed BIN SHA256: {parsed_hash}")

    source_ok = (
        file_hash == EXPECTED_OFFICIAL_HEX_SHA256
        or file_hash == EXPECTED_OFFICIAL_BIN_SHA256
        or parsed_hash == EXPECTED_OFFICIAL_BIN_SHA256
    )

    if not source_ok and not args.allow_unknown_source:
        raise SystemExit(
            "This does not match the known official Flow2 100 / OE926 v14 firmware.\n"
            "Stop and check that you selected the OE926 100-key v14 file."
        )

    current = binary[PATCH_OFFSET : PATCH_OFFSET + len(OLD_BYTES)]
    if current != OLD_BYTES:
        raise SystemExit(
            f"Patch location mismatch at 0x{PATCH_OFFSET:X}: "
            f"got {current.hex(' ').upper()}, expected {OLD_BYTES.hex(' ').upper()}"
        )

    patched = bytearray(binary)
    patched[PATCH_OFFSET : PATCH_OFFSET + len(NEW_BYTES)] = NEW_BYTES
    patched = bytes(patched)
    patched_hash = sha256(patched)

    if patched_hash != EXPECTED_PATCHED_BIN_SHA256 and not args.allow_unknown_source:
        raise SystemExit(
            "Patched BIN SHA256 mismatch.\n"
            f"Got:      {patched_hash}\n"
            f"Expected: {EXPECTED_PATCHED_BIN_SHA256}"
        )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_bin = args.out_dir / OUTPUT_BIN_NAME
    out_hex = args.out_dir / OUTPUT_HEX_NAME
    out_bin.write_bytes(patched)
    out_hex.write_text(to_intel_hex(patched), encoding="ascii", newline="")

    print()
    print(f"Wrote BIN: {out_bin}")
    print(f"Wrote HEX: {out_hex}")
    print(f"Patched BIN SHA256: {patched_hash}")
    print("Patch: 0x2710 / 10000 ms -> 0xEA60 / 60000 ms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
