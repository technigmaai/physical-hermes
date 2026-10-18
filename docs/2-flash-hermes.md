# Flash Hermes

This puts the Hermes firmware onto the robot. It's a one-time step, takes about five minutes, and needs a computer.

## What you need

- The robot
- A USB-C **data** cable (charge-only cables won't work — it's the most common snag)
- Python on your computer

## 1. Install esptool

```bash
pip install esptool
```

## 2. Download the firmware

Grab the prebuilt image from this repo:

**`firmware/hermes-gadget-spotpear-128-box-0.2.0.bin`**

It's a single file — bootloader, partition table and application all in one. You don't need the toolchain, ESP-IDF, or PlatformIO.

## 3. Plug in and flash

Plug the robot into your computer with the USB-C cable, then:

```bash
esptool.py --chip esp32s3 --baud 460800 write_flash 0x0 hermes-gadget-spotpear-128-box-0.2.0.bin
```

It should find the port by itself and start writing. You'll see progress bars and a final `Hash of data verified.`

### If it can't find the robot

Some boards need a nudge into download mode:

1. Unplug the cable.
2. **Hold the `boot` button** — it's the one to the **right** of the USB-C socket (the left one is power).
3. Plug the cable back in while still holding `boot`.
4. Keep holding for a couple of seconds, then release.

Then run the flash command again.

## 4. Check it worked

Unplug and plug it back in. The screen should light up with the Hermes Gadget mascot, and it'll offer a Wi-Fi setup. If the screen stays dark, re-run the flash — nothing is permanently broken, the chip can always be reflashed.

## Changing your mind

To put it back exactly as it shipped, write your backup from step 4 of [The device](1-the-device.md):

```bash
esptool.py --chip esp32s3 write_flash 0x0 stock-firmware.bin
```

---

Next: **[Connect to Hermes →](3-connect-to-hermes.md)**
