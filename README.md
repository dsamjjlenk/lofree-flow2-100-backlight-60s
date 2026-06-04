# Lofree Flow2 100 Backlight 60s Firmware

Ready-to-flash firmware for the **Lofree Flow2 100 / OE926** that makes the wireless backlight stay on for about **60 seconds** instead of the stock 10 seconds.

This is meant to be simple: download, check your model, enter DFU, flash, done.

## Who This Is For

Use this only for:

```text
Keyboard: Lofree Flow2 100
Model:    OE926
USB ID:   VID_388D PID_0003
```

Do **not** use it for:

```text
Flow2 68
Flow2 84
Any other Lofree keyboard
Any keyboard with a different USB ID
```

## What It Does

The stock firmware turns the wireless backlight off after about 10 seconds.

This firmware changes that timeout to about 60 seconds.

Only 4 bytes are changed:

```text
Address: 0x0800403E
Offset:  0x403E

Before: 42 F2 10 73  -> 10000 ms
After:  4E F6 60 23  -> 60000 ms
```

## Ready Firmware Files

The ready firmware is included here:

```text
firmware/oe926_via_v14_backlight_timeout_60s.bin
firmware/oe926_via_v14_backlight_timeout_60s.hex
```

Hashes:

```text
BIN SHA256: FC7C6CEFE8284075EC427689CD2B213C844B538A5FCB96DFFCA30E0442B61D07
HEX SHA256: 357EA7EBB60CF9C6984344EE022CC9EE7FF890145D60A2B03E6664D3E0B9393B
```

The BIN was flashed to a real Flow2 100, read back from the keyboard, and verified byte-for-byte.

## Super Simple Windows Guide

### Step 1. Install tools

Install:

- Python 3
- QMK MSYS: <https://msys.qmk.fm/>

Then open PowerShell and run:

```powershell
py -3 -m pip install hidapi
```

QMK's flashing documentation says the WB32 flasher is bundled with QMK MSYS:

<https://docs.qmk.fm/flashing.html>

### Step 2. Plug in the keyboard

1. Connect the keyboard with the USB cable.
2. Switch the keyboard to wired mode.
3. Close VIA or any other keyboard configuration app.

### Step 3. Check that it is the right keyboard

Run:

```powershell
py -3 .\tools\check_keyboard.py
```

Good result:

```text
VIA RAW HID interface: found
Result: This looks like a Lofree Flow2 100 / OE926 in wired mode.
```

### Step 4. Enter DFU mode

Run:

```powershell
py -3 .\tools\enter_dfu_via_raw_hid.py
```

After this, the keyboard should appear as:

```text
VID_342D PID_DFA0
WB Device in DFU Mode
```

### Step 5. Flash the ready firmware

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\flash_60s_wb32.ps1
```

The script will:

- check the ready firmware SHA256
- flash it to the keyboard
- read it back from the keyboard
- compare the readback hash
- reset the keyboard back to normal mode

Success looks like:

```text
Download completed!
Readback verified
Done. Keyboard should return as VID_388D PID_0003.
```

## Test After Flashing

1. Disconnect the USB cable.
2. Use Bluetooth or 2.4 GHz mode.
3. Turn on the backlight.
4. Stop typing.
5. Wait.

The backlight should now turn off after about **60 seconds**, not about 10 seconds.

## Optional: Rebuild The Firmware Yourself

If you do not want to trust a ready-made BIN, you can rebuild it from the official Lofree Flow2 100 v14 firmware.

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\build_60s_from_official.ps1
```

Select the official file:

```text
oe926_via_100-key keyboard_v14.hex
```

Known official HEX SHA256:

```text
5586079676271B13ABC74B8CB04AE35C32FC9C3BF5FA9D06FF3FC45C1AA65594
```

The builder creates the same 60-second BIN hash:

```text
FC7C6CEFE8284075EC427689CD2B213C844B538A5FCB96DFFCA30E0442B61D07
```

## Restore Stock

To restore the stock 10-second behavior, flash the official OE926 v14 firmware again.

## Troubleshooting

See:

- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Technical notes](docs/TECHNICAL_NOTES.md)
- [FAQ](FAQ.md)

## Disclaimer

This is an unofficial community project. It is not made by or affiliated with Lofree.

Firmware flashing always has risk. Check the model before flashing.

## License

Scripts and documentation are MIT licensed.

The included patched firmware is provided as an unofficial community modification for Flow2 100 / OE926 users.
