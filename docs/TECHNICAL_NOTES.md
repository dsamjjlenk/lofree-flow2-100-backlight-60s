# Technical Notes

## Device

Target keyboard:

```text
Lofree Flow2 100 / OE926
Normal USB ID: VID_388D PID_0003
DFU USB ID:    VID_342D PID_DFA0
```

VIA RAW HID:

```text
Usage page: 0xFF60
Usage:      0x61
```

## Firmware

Official OE926 v14 Intel HEX SHA256:

```text
5586079676271B13ABC74B8CB04AE35C32FC9C3BF5FA9D06FF3FC45C1AA65594
```

Official OE926 v14 parsed BIN SHA256:

```text
387C3C5F1E5003D96B642EBAEE8A224099EF33D99C01845ECAD2E1F28D676047
```

Official parsed BIN length:

```text
61828 bytes
0xF184 bytes
```

Patched 60-second BIN SHA256:

```text
FC7C6CEFE8284075EC427689CD2B213C844B538A5FCB96DFFCA30E0442B61D07
```

## Patch

The stock timeout constant is used in the LED/backlight handler around:

```text
0x08004038: ldr r0, [r4]
0x0800403A: bl timer_elapsed
0x0800403E: movw r3, #0x2710
0x08004042: cmp r0, r3
```

Patch:

```text
Image offset: 0x403E
Flash addr:   0x0800403E

Old bytes: 42 F2 10 73
New bytes: 4E F6 60 23
```

Meaning:

```text
0x2710 = 10000 ms = 10 seconds
0xEA60 = 60000 ms = 60 seconds
```

Only 4 bytes differ from the official OE926 v14 image.

## Why not 5 minutes with the same patch?

The current instruction is:

```text
movw r3, #imm16
```

It can hold a maximum value of:

```text
0xFFFF = 65535 ms
```

Five minutes would be:

```text
300000 ms = 0x493E0
```

That does not fit in this single instruction. A 5-minute patch needs a larger logic change.

## Flash command

The verified flash command is:

```powershell
wb32-dfu-updater_cli.exe -s 0x08000000 -D .\dist\oe926_via_v14_backlight_timeout_60s.bin
```

Readback verification:

```powershell
wb32-dfu-updater_cli.exe -s 0x08000000 -Z 61828 -U .\dist\verify_readback_0x08000000_61828.bin
```

Reset:

```powershell
wb32-dfu-updater_cli.exe -R
```
