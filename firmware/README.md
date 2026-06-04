# Firmware Files

This folder contains the ready-to-flash Flow2 100 / OE926 firmware with the 60-second backlight timeout patch.

Use only for:

```text
Lofree Flow2 100 / OE926 / VID_388D PID_0003
```

`VID_388D PID_0003` is the shared USB vendor/product ID for this model, not a unique serial number from one PC.

Files:

```text
oe926_via_v14_backlight_timeout_60s.bin
oe926_via_v14_backlight_timeout_60s.hex
```

Hashes:

```text
BIN SHA256: FC7C6CEFE8284075EC427689CD2B213C844B538A5FCB96DFFCA30E0442B61D07
HEX SHA256: 357EA7EBB60CF9C6984344EE022CC9EE7FF890145D60A2B03E6664D3E0B9393B
```

The BIN was flashed to a real keyboard, read back, and verified byte-for-byte.
