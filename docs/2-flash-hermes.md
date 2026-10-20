# Flash the 2.16-inch board

Use **ESP32-S3-Touch-AMOLED-2.16** only. The original `spotpear-128-box` image targets different hardware.

## Prepare

From this repository:

```bash
python3 -m venv .venv-flash
source .venv-flash/bin/activate
python -m pip install -r requirements-flash.txt
python -m serial.tools.list_ports -v
python scripts/flash.py --check
```

Connect a USB-C **data** cable, close other serial monitors and identify the port. Typical ports are `/dev/cu.usbmodem...` on macOS, `/dev/ttyACM0` on Linux and `COM3` on Windows.

## Back up and flash

```bash
python scripts/flash.py --port /dev/cu.usbmodem83201
```

Replace the example port. The script verifies the packaged checksums and exact board tag, requires 16 MB flash and disabled Secure Boot/flash encryption, saves two matching full-flash reads, then writes and verifies the new image. Backups and SHA-256 records stay in ignored `backups/`; retain a separate private copy for rollback.

To back up without writing, add `--backup-only`. The merged image replaces the bootloader, partition table, OTA metadata and application from `0x0`, clearing settings in that range. No separate erase is needed. The `-app.bin` is for later compatible OTA updates, not a first USB install.

To install directly without a factory backup:

```bash
python scripts/flash.py --port /dev/cu.usbmodem83201 --skip-backup
```

The script defaults to esptool's bundled v1 stub after v2 read transfers stalled on this device. `--stub-version 2` selects the alternate implementation. The esptool version is pinned because its stub selector is an internal option.

After a verified backup, manual installation is also possible:

```bash
python -m esptool --chip esp32s3 --port /dev/cu.usbmodem83201 --baud 460800 write-flash 0x0 firmware/waveshare-216/hermes-gadget-esp32s3-touch-amoled-216-0.2.0-sessions.1.bin
python -m esptool --chip esp32s3 --port /dev/cu.usbmodem83201 verify-flash 0x0 firmware/waveshare-216/hermes-gadget-esp32s3-touch-amoled-216-0.2.0-sessions.1.bin
```

If USB download fails, hold **BOOT**, reconnect USB while holding it, then release and check the port again. Keep power connected throughout backup and flashing. If a backup stops, do not proceed to writing; retry with a stable cable. A ROM read can help with stub-transfer issues:

```bash
python -m esptool --chip esp32s3 --port /dev/cu.usbmodem83201 --no-stub read-flash 0x0 0x1000000 backups/stock-rom.bin
```

## Verify startup

The screen should show Hermes setup. On the USB console at 115200, check for `CO5300 480x480 ready`, `codecs: speaker ready, microphones ready (es7210)`, `touch ready`, `AXP2101 reporting ready` and board identity `esp32s3-touch-amoled-2.16`.

Run `diag` on the console. Check actual screen orientation/colors, touch, microphone capture and audible replies; startup messages alone do not prove these work.

## Restore factory firmware

Use the verified backup from this same device:

```bash
python -m esptool --chip esp32s3 --port /dev/cu.usbmodem83201 write-flash 0x0 backups/YOUR-VERIFIED-STOCK.bin
python -m esptool --chip esp32s3 --port /dev/cu.usbmodem83201 verify-flash 0x0 backups/YOUR-VERIFIED-STOCK.bin
```

Next: [Connect to Hermes](3-connect-to-hermes.md).
