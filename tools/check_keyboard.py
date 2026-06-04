#!/usr/bin/env python3
import sys

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


def main() -> int:
    devices = list(hid.enumerate(VID, PID))
    raw = [
        dev
        for dev in devices
        if dev.get("usage_page") == RAW_USAGE_PAGE and dev.get("usage") == RAW_USAGE
    ]

    print("Lofree Flow2 100 / OE926 keyboard check")
    print()
    print(f"USB VID/PID devices found: {len(devices)}")
    print(f"VIA RAW HID interface: {'found' if raw else 'not found'}")

    if devices:
        products = sorted({dev.get("product_string") or "" for dev in devices if dev.get("product_string")})
        if products:
            print("Product strings:")
            for product in products:
                print(f"  - {product}")

    print()
    if raw:
        print("Result: This looks like a Lofree Flow2 100 / OE926 in wired mode.")
        return 0

    print("Result: Not ready.")
    print("Connect the keyboard by USB, switch it to wired mode, close VIA, and try again.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
