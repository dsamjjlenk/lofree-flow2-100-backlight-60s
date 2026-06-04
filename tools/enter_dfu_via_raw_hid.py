#!/usr/bin/env python3
import sys
import time

try:
    import hid
except ImportError:
    print("Missing Python package: hidapi")
    print("Install it with:")
    print("  py -3 -m pip install hidapi")
    sys.exit(2)


VID = 0x388D
PID = 0x0003
RAW_USAGE_PAGE = 0xFF60
RAW_USAGE = 0x61
CMD_BOOTLOADER_JUMP = 0x0B


def main() -> int:
    matches = [
        dev
        for dev in hid.enumerate(VID, PID)
        if dev.get("usage_page") == RAW_USAGE_PAGE and dev.get("usage") == RAW_USAGE
    ]

    print(f"RAW HID matches: {len(matches)}")
    if not matches:
        print("Flow2 RAW HID interface 0xFF60/0x61 was not found.")
        print("Connect Lofree Flow2 100 by USB in wired mode, close VIA, then try again.")
        return 2

    device = hid.device()
    device.open_path(matches[0]["path"])
    device.set_nonblocking(True)

    deadline = time.time() + 0.2
    while time.time() < deadline:
        device.read(32, 20)
        time.sleep(0.01)

    packet = [0x00, CMD_BOOTLOADER_JUMP] + [0xFE] * 31
    written = device.write(packet)
    print(f"BootloaderJump write bytes: {written}")

    time.sleep(0.2)
    try:
        response = device.read(32, 200)
        print(f"Response: {response}")
    finally:
        device.close()

    print()
    print("If the command succeeded, the keyboard should now appear as:")
    print("  VID_342D PID_DFA0")
    print("  WB Device in DFU Mode")
    return 0


if __name__ == "__main__":
    sys.exit(main())
