# FAQ

## Is this for every Lofree Flow2?

No. It is only for:

```text
Lofree Flow2 100 / OE926 / VID_388D PID_0003
```

## Does this change my keymap?

No. It changes only the backlight idle timeout constant in the firmware.

## Does this fix the side touch slider?

No. This patch only changes the backlight timeout.

## Can I make it stay on forever?

Not with this simple 4-byte patch. The easy patch can go up to about 65.5 seconds. Anything longer needs a different firmware logic patch.

## Can I set it to 5 minutes?

Not with this exact one-instruction patch. Five minutes is 300000 ms, which does not fit into the existing 16-bit immediate instruction.

## Is this reversible?

Yes. Flash the official OE926 v14 firmware again to restore the stock 10-second timeout.

## Why is there also a builder script?

Because some people prefer to reproduce the patched firmware from the official Lofree file before flashing.

Most users can use the ready firmware in the `firmware` folder.

## Is Bluetooth or 2.4 GHz pairing changed?

No. The patch does not intentionally touch wireless pairing, keymaps, VIA data, or touch slider behavior.
