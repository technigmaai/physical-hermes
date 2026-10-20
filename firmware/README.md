# Firmware for ESP32-S3-Touch-AMOLED-2.16

Use [`waveshare-216/hermes-gadget-esp32s3-touch-amoled-216-0.2.0.bin`](waveshare-216/hermes-gadget-esp32s3-touch-amoled-216-0.2.0.bin) for first USB installation at `0x0`. It includes bootloader, partitions, OTA data and application. See [the walkthrough](../docs/2-flash-hermes.md).

| Property | Value |
|---|---|
| Board | Waveshare / SpotPear ESP32-S3-Touch-AMOLED-2.16 |
| Display | CO5300 480×480 AMOLED over QSPI |
| Touch / audio / power | CST9220 / ES8311 + ES7210 / AXP2101 |
| Flash / PSRAM | 16 MB / 8 MB octal |
| PlatformIO environment | `esp32s3-touch-amoled-216` |
| Embedded board identity | `esp32s3-touch-amoled-2.16` |
| SDK commit | `63e664c9920321b44390e8161535008e4f73513b` |
| Merged size | 1,508,352 bytes |
| Merged SHA-256 | `e9646b0c8873414d3d527a256af775193867bf90089d75ac697cfaa959dd23d5` |

This is a [successful upstream CI build](https://github.com/Adolanium/hermes-gadget-sdk/actions/runs/39287216026/job/118177569454), not a local compilation or the older published v0.2.0 release. It retains version string 0.2.0. [`SOURCE.json`](waveshare-216/SOURCE.json) records provenance; [`manifest.json`](waveshare-216/manifest.json) and [`SHA256SUMS`](waveshare-216/SHA256SUMS) record hashes. Distribute the matching licenses archive with the binary. The board remains experimental pending complete physical validation.

## Rebuild or modify

```bash
git submodule update --init --recursive
python3 -m venv .venv-build
source .venv-build/bin/activate
python -m pip install -r requirements-build.txt
python scripts/build.py
```

Use Python 3.10–3.12, matching upstream's tested tooling. The first build downloads the ESP-IDF toolchain. The wrapper verifies the SDK commit and builds only `esp32s3-touch-amoled-216`. New artifacts go to `build/waveshare-216/`, leaving the included CI artifacts intact. For a modified build, update the distributed binary, manifest, checksums, source record and licenses together before flashing.

Relevant paths inside `sdk/`:

- `firmware/esp32/main/board.cpp`: `CONFIG_HG_BOARD_AMOLED_216`
- `firmware/esp32/main/port_amoled.cpp`: `kInit480`, 480×480 window, MADCTL `0xA0`
- `firmware/esp32/boards/esp32s3-touch-amoled-216/sdkconfig.defaults`
- `firmware/esp32/platformio.ini`: `[env:esp32s3-touch-amoled-216]`

The existing upstream profile drives the correct hardware. **Do not apply `spotpear-128-box.patch` to it.**

## Original 1.28-inch assets

`hermes-gadget-spotpear-128-box-0.2.0.bin` and `spotpear-128-box.patch` remain from RegeneratusLabs for attribution and reference. They target GC9A01 240×240, CST816D and an ES8311 analog microphone. The old patch was based on SDK commit `eae9b19e398f69eefdc7125990f553302e8f32d0`.
