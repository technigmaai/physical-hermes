# Firmware for ESP32-S3-Touch-AMOLED-2.16

Current firmware: **0.2.0-sessions.1**, with a Sessions browser, +/KEY controls, and header/footer padding for the device's physical rounded screen corners. See [Sessions and buttons](../docs/7-sessions-and-buttons.md) and [the layout change](../docs/6-rounded-layout.md).

For first installation, flash [`waveshare-216/hermes-gadget-esp32s3-touch-amoled-216-0.2.0-sessions.1.bin`](waveshare-216/hermes-gadget-esp32s3-touch-amoled-216-0.2.0-sessions.1.bin) at `0x0`. This merged image includes bootloader, partitions, OTA data and app, and clears settings. See [the walkthrough](../docs/2-flash-hermes.md).

For an already paired board, use the **`-app.bin` through `hermes gadget update`** to preserve Wi-Fi and pairing.

| Property | Value |
|---|---|
| Board | Waveshare / SpotPear ESP32-S3-Touch-AMOLED-2.16 |
| Display | CO5300 480×480 AMOLED over QSPI, rounded physical opening |
| Layout | 48-pixel extra side insets in the header and footer; full-width central content |
| Touch / audio / power | CST9220 / ES8311 + ES7210 / AXP2101 |
| Flash / PSRAM | 16 MB / 8 MB octal |
| PlatformIO environment | `esp32s3-touch-amoled-216` |
| Embedded board identity | `esp32s3-touch-amoled-2.16` |
| SDK base commit | `63e664c9920321b44390e8161535008e4f73513b` |
| Local overlay | `device-customizations.patch` |
| Merged size | 1,513,776 bytes |
| App size | 1,382,704 bytes; 31.9% of each OTA slot remains free |
| Merged SHA-256 | `3a1274fdbcc46ba9042e711a96c54ffbd6299ef48a867e57b1cfe25b2834523b` |

This is a local PlatformIO 6.2.0 / ESP-IDF 6.1.0 build of the pinned source plus the overlay. [`SOURCE.json`](waveshare-216/SOURCE.json) records provenance and the patch checksum; [`manifest.json`](waveshare-216/manifest.json) and [`SHA256SUMS`](waveshare-216/SHA256SUMS) record artifact hashes. The earlier upstream CI baseline is recorded in [`UPSTREAM-CI.json`](waveshare-216/UPSTREAM-CI.json). Keep the matching `hermes-gadget-0.2.0-sessions.1-licenses.zip` with redistributed binaries.

## Rebuild

```bash
git submodule update --init --recursive
python3.10 -m venv .venv-build
source .venv-build/bin/activate
python -m pip install -r requirements-build.txt
python scripts/build.py
```

Use Python 3.10–3.12. The first build downloads several GB of ESP-IDF tools. The wrapper checks the SDK pin, exports its tracked source to a generated directory under `build/`, applies the device overlay, and builds only the 2.16-inch profile. Toolchain files stay in `build/platformio/` by default. New release files go to `build/waveshare-216/`; the `sdk/` submodule remains clean.

Use `python scripts/build.py --prepare-only` to prepare source without compiling. The overlay contains a regression test that passes with all 265 portable core cases. Update the distributed binary, manifest, checksums, source record and licenses together when publishing another build.

Relevant upstream paths:

- `firmware/esp32/main/board.cpp`: `CONFIG_HG_BOARD_AMOLED_216`
- `firmware/esp32/main/port_amoled.cpp`: `kInit480`, 480×480 window, MADCTL `0xA0`
- `firmware/core/src/ui.cpp`: header/footer fitting
- `firmware/esp32/boards/esp32s3-touch-amoled-216/sdkconfig.defaults`

## Original 1.28-inch assets

`hermes-gadget-spotpear-128-box-0.2.0.bin` and `spotpear-128-box.patch` remain from RegeneratusLabs for attribution and reference. They target GC9A01 240×240, CST816D and an ES8311 analog microphone. The old patch was based on SDK commit `eae9b19e398f69eefdc7125990f553302e8f32d0`. Do not apply it to this board or the newer SDK.
