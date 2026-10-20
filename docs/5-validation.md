# Local installation reports — 2026-10-20

Target identified by owner: ESP32-S3-Touch-AMOLED-2.16. PCB revision not established.

## Initial 0.2.0 installation

| Check | Result |
|---|---|
| USB discovery | Espressif USB Serial/JTAG, VID/PID `303A:1001` |
| Chip | ESP32-S3 QFN56, revision v0.2 |
| Memory | 16 MB flash; 8 MB octal PSRAM detected at boot |
| Security | Secure Boot and flash encryption disabled |
| Image | SDK `63e664c9920321b44390e8161535008e4f73513b`, `esp32s3-touch-amoled-216`, version string 0.2.0 |
| Source build | Upstream CI job successful; no local compilation claimed |
| Packaged checksums | Merged image, app image and license archive all verified |
| Image inspection | ESP32-S3 chip ID; exact board tag; app at `0x20000`; 32.2% free in each OTA slot |
| USB installation | 1,508,352 bytes written at `0x0`; device-side hash verification passed |
| Display startup | `CO5300 480x480 ready` |
| Display appearance | Owner confirmed the Hermes setup screen is visible and upright |
| Audio startup | `codecs: speaker ready, microphones ready (es7210)` |
| Touch startup | `touch ready, key off, encoder off` |
| Power startup | `AXP2101 reporting ready; charging and supply settings unchanged` |
| Firmware identity | `esp32s3-touch-amoled-2.16`, fw 0.2.0 |
| Serial diagnostic | Display `co5300`, microphone `es7210`, speaker `es8311`, touch present |
| I2C scan | `0x18`, `0x34`, `0x40`, `0x51`, `0x5a`, `0x6b` |
| Local tool tests | Four offline unit checks passed: packaged image, corrupted-image rejection, protected-flash rejection, backup opt-out |
| Hermes host | macOS; Hermes Agent 0.22.2, local revision `d923a5eb487a` |
| Gadget plugin | Installed and enabled from the same pinned SDK commit |
| Gateway | Started using Hermes CLI; launchd supervision confirmed; TCP port 8765 listening |
| Device server setting | Saved and read back over USB; points to the Mac's LAN gateway URL |

Factory backup was explicitly declined by the owner. Earlier read attempts did not produce a verified full backup. Flashed directly using esptool 5.3.0 with its bundled v1 stub after default v2 read transfers stopped. Full logs remain private and ignored; provisioning credentials are not included here.

After this installation the owner confirmed Wi-Fi setup, pairing and real interaction with Hermes. Their photo showed a spoken response and exposed clipping of the title and connection label at the physical rounded corners.

## Rounded-corner update: 0.2.0-rounded.1

- Source: pinned SDK plus `rounded-layout.patch`; local build using PlatformIO 6.2.0, Espressif32 8.0.0 and ESP-IDF 6.1.0. The `sdk/` submodule remains unchanged.
- Display change: 48-pixel corner insets for header/footer text; full 480×480 framebuffer and unchanged touch coordinates.
- Regression: the pixel test first failed on the old footer behavior, then passed with the fix. All 253 core cases pass, including circular layouts. Four flash-tool checks pass.
- Preview: production renderer inspected with an approximate rounded aperture; this is simulated evidence, not a physical screen measurement.
- Build: ESP32-S3 firmware and packaging succeeded; app 1,377,184 bytes, 32.2% OTA slot headroom. Image, app and license checksums verified.
- Installation: app-only update through the paired Hermes connection, with the existing OTA slots. No factory backup or settings erase was performed.
- Reconnection: Hermes reports `0.2.0-rounded.1` under the existing device identity.

This remains partial hardware validation. Exact touch coordinates, audio quality, battery behavior, forced network loss, OTA rollback and a long session remain unverified. The port stays experimental.
