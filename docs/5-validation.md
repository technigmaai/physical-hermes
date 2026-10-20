# Local installation report — 2026-10-20

Target identified by owner: ESP32-S3-Touch-AMOLED-2.16. PCB revision not established.

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

Factory backup was explicitly declined by the owner. Earlier read attempts did not produce a verified full backup. Flashed directly using esptool 5.3.0 with its bundled v1 stub after default v2 read transfers stopped. Full logs remain private and ignored; provisioning credentials are not included here.

These are startup checks plus the owner's display confirmation, not complete physical validation. Touch coordinates and gestures, microphone capture, audible speaker playback, pairing, network recovery, battery behavior, OTA/rollback and a long session remain to be checked. This board profile remains experimental.
