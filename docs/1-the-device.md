# The device

## Buy it

**[ESP32-S3 1.28" AI Voice Chat Robot](https://s.click.aliexpress.com/e/_c3d38V2l)** — about AU$36.

It arrives as a finished little robot with a round screen and a face. Out of the box it wants to register with a Chinese cloud service. We're going to replace all of that.

Choose the **touch** version if you're offered a choice — swipe-to-cancel uses it.

## What's inside

| Part | What it is |
|---|---|
| Processor | ESP32-S3R8 — dual core, 240 MHz, 8 MB PSRAM |
| Storage | 16 MB flash |
| Screen | 1.28" round IPS, 240×240, GC9A01 controller |
| Touch | CST816D capacitive (touch version) |
| Speaker | ES8311 codec + NS4150B amplifier |
| Microphone | Analog MEMS, wired into the ES8311 |
| Battery | LiPo, charged over USB-C |
| Extras | MicroSD slot, status LED, power button |

Everything above is driven by the firmware in this repo. There is nothing left over and nothing missing.

## What you get for your money

- A screen, a speaker, a microphone, a battery and a case — assembled.
- A published schematic and pin table (we used them; you can too).
- Firmware built from open source, so the board is genuinely yours to reprogram.

Comparable dev boards with all of that cost more and come as bare PCBs.

## Things worth knowing

**It's 2.4 GHz Wi-Fi only.** The ESP32-S3 has no 5 GHz radio. If your home network is 5 GHz-only, enable the 2.4 GHz band or join it to a combined network.

**The battery is real.** Unplug it and it keeps running. You can carry it around the house.

**The stock firmware talks to `api.tenclass.net`** — a vendor cloud, for speech recognition and over-the-air updates. Replacing the firmware is the whole point of this project: afterwards it talks only to your Hermes.

**Keep the original firmware if you want it back.** Before flashing anything, save a copy of what's on it:

```bash
esptool.py --chip esp32s3 read_flash 0 0x1000000 stock-firmware.bin
```

Takes about 80 seconds. Restoring it later is a single `write_flash`.

---

Next: **[Flash Hermes →](2-flash-hermes.md)**
