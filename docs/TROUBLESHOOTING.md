# Troubleshooting

## The builder says my official firmware hash is different

Stop and check the file name.

The expected file is:

```text
oe926_via_100-key keyboard_v14.hex
```

Expected SHA256:

```text
5586079676271B13ABC74B8CB04AE35C32FC9C3BF5FA9D06FF3FC45C1AA65594
```

Do not use the 68-key or 84-key firmware.

## `check_keyboard.py` cannot find the keyboard

Try this:

1. Connect the keyboard by USB cable.
2. Switch the keyboard to wired mode.
3. Close VIA or any other app that may be using the keyboard.
4. Run the command again:

```powershell
py -3 .\tools\check_keyboard.py
```

## `hidapi` is missing

Install it:

```powershell
py -3 -m pip install hidapi
```

## DFU mode appears, but the flasher says `Not found device`

Windows may not have a WinUSB driver attached to the DFU device.

The DFU device is:

```text
VID_342D PID_DFA0
WB Device in DFU Mode
```

Install a WinUSB driver for that DFU device, then run:

```powershell
C:\msys64\mingw64\bin\wb32-dfu-updater_cli.exe -l
```

You want to see something like:

```text
Found DFU: [0x342D:0xDFA0]
```

## `wb32-dfu-updater_cli.exe` is missing

Install QMK MSYS:

<https://msys.qmk.fm/>

The QMK flashing documentation says `wb32-dfu-updater` is bundled with QMK MSYS:

<https://docs.qmk.fm/flashing.html>

After installing it, open a new PowerShell window and try again.

If it is installed in a custom location, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\flash_60s_wb32.ps1 -Wb32Path "C:\path\to\wb32-dfu-updater_cli.exe"
```

## The keyboard stays in DFU mode

Run:

```powershell
C:\msys64\mingw64\bin\wb32-dfu-updater_cli.exe -R
```

Then unplug and reconnect the keyboard.

## The backlight still turns off too fast

Check these points:

1. Confirm you flashed the patched BIN, not the original firmware.
2. Run the flasher again and make sure readback verification passes.
3. Confirm the keyboard is actually the Flow2 100 / OE926.
4. Test in wireless mode after unplugging the cable.

The verified 60-second patched BIN hash is:

```text
FC7C6CEFE8284075EC427689CD2B213C844B538A5FCB96DFFCA30E0442B61D07
```
