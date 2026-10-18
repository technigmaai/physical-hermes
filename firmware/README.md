# Firmware

Two things live here: a ready-to-flash image, and the source patch that produced it.

## For most people: flash the prebuilt image

**`hermes-gadget-spotpear-128-box-0.2.0.bin`**

One file containing bootloader, partition table and application.

```bash
esptool.py --chip esp32s3 --baud 460800 write_flash 0x0 hermes-gadget-spotpear-128-box-0.2.0.bin
```

See [Flash Hermes](../docs/2-flash-hermes.md) for the walkthrough.

| | |
|---|---|
| Chip | ESP32-S3 |
| Flash size | 16 MB |
| Built with | ESP-IDF 6.1.0 / Hermes Gadget SDK 0.2.0 |
| Size | 1,480,960 bytes |
| SHA-256 | `7eecba2f9484b74f15c4221b944e4d274cafac3be13bd6a39b8786070f8fb080` |

## For the curious: build it yourself

This board isn't in the upstream SDK yet, so the port ships as a patch.

```bash
git clone https://github.com/Adolanium/hermes-gadget-sdk.git
cd hermes-gadget-sdk

# The patch is pinned to the commit it was built against. The SDK moves fast;
# a plain `git apply` against a newer main may not apply.
git checkout eae9b19e398f69eefdc7125990f553302e8f32d0

git apply /path/to/spotpear-128-box.patch

cd firmware/esp32
pio run -e spotpear-128-box -t upload
```

You'll need [PlatformIO](https://platformio.org) on **Python 3.12 or earlier** — PlatformIO doesn't yet support 3.14. The first build downloads roughly 1.5 GB of toolchain.

### What the patch adds

- A `spotpear-128-box` board profile: GC9A01 panel, CST816D touch, ES8311 running both the speaker and the microphone, battery on a 1:2 divider.
- A GC9A01 panel driver branch, plus the `esp_lcd_gc9a01` component.
- Support for a touchscreen on its own I2C bus (this board puts the panel on GPIO 11/7 and the codec on 15/14).
- Support for a battery with no latch GPIO, and a configurable charge-signal polarity.

None of that is specific to this robot — it's general capability the SDK was missing. It's intended to go upstream.

## Credits

Derived from the [Hermes Gadget SDK](https://github.com/Adolanium/hermes-gadget-sdk) (MIT). The board profile follows SpotPear's published schematic and the open-source [xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) board definition for this device.
