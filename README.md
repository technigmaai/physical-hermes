# Physical Hermes — ESP32-S3-Touch-AMOLED-2.16

Give Hermes Agent a voice device using the **Waveshare / SpotPear ESP32-S3-Touch-AMOLED-2.16**: a **480×480 CO5300 AMOLED**, CST9220 touch, two microphones, speaker output, 16 MB flash and 8 MB PSRAM.

This fork adapts [RegeneratusLabs/physical-hermes](https://github.com/RegeneratusLabs/physical-hermes) to your 2.16-inch board. The original targets a different 1.28-inch GC9A01 robot. **Use only the image in `firmware/waveshare-216/` for this board.**

The adaptation selects the SDK's exact `esp32s3-touch-amoled-216` profile: CO5300 480×480 initialization, QSPI pins, CST9220 coordinate transform, ES8311/ES7210 audio and AXP2101 power support. Firmware **0.2.0-rounded.1** adds header and footer margins for the physical rounded screen corners. The SDK is pinned as a [source submodule](sdk) at `63e664c9920321b44390e8161535008e4f73513b`, with our [layout overlay](firmware/waveshare-216/rounded-layout.patch) applied during builds. See [the hardware configuration](docs/1-the-device.md).

## Flash

Connect a USB-C data cable. From this repository:

```bash
python3 -m venv .venv-flash
source .venv-flash/bin/activate
python -m pip install -r requirements-flash.txt
python -m serial.tools.list_ports -v
python scripts/flash.py --check
python scripts/flash.py --port /dev/cu.usbmodem83201
```

Replace the example port with the actual board port. The script verifies the checksums and embedded board identity, checks flash size and security settings, saves **two matching full 16 MB backup reads**, then writes and verifies the merged image. Backups remain private in ignored `backups/`. USB IDs alone cannot identify the screen: confirm the printed board model first.

For a direct installation without a factory backup, add `--skip-backup`.

The first installation replaces the partition table and clears device settings. Read [Flash Hermes](docs/2-flash-hermes.md) for recovery and manual commands.

## Connect to Hermes

On the computer running Hermes Agent:

```bash
hermes plugins install https://github.com/Adolanium/hermes-gadget-sdk/tree/main/plugin --ref 63e664c9920321b44390e8161535008e4f73513b --enable --yes-deps
hermes config set platforms.gadget.enabled true
hermes gateway restart
hermes gadget info
```

Use the board's temporary Wi-Fi network to enter your 2.4 GHz Wi-Fi credentials and the device URL from `hermes gadget info`. Approve its pairing code on the Hermes host. The host must be reachable on TCP port 8765 and have speech recognition and text-to-speech configured. See [Connect to Hermes](docs/3-connect-to-hermes.md).

Hold **BOOT**, speak, then release. Hermes processes the request and streams its spoken answer to the board. See [Using it](docs/4-using-it.md).

## Firmware and source

- [Firmware, checksums and build provenance](firmware/waveshare-216/)
- [Rebuild instructions](firmware/README.md)
- [Local installation and validation report](docs/5-validation.md)
- [Rounded-corner layout and settings-preserving updates](docs/6-rounded-layout.md)
- [Original hardware-porting skill](skills/hermes-gadget-hardware/SKILL.md)

The included firmware is built locally from the pinned SDK plus the layout overlay. [SOURCE.json](firmware/waveshare-216/SOURCE.json) records the patch hash and build tools; the original upstream CI baseline is retained in [UPSTREAM-CI.json](firmware/waveshare-216/UPSTREAM-CI.json). All 253 portable core tests pass, including the corner-padding regression. The owner has confirmed pairing and real voice interaction on the original image. This port remains **experimental** pending complete touch, battery, recovery and long-session validation; see [the local report](docs/5-validation.md).

## Credits and licenses

Based on **Physical Hermes** by RegeneratusLabs and the **Hermes Gadget SDK** by Adolanium and contributors (MIT). The SDK is an independent community project, not affiliated with Nous Research. Board support follows Waveshare's published BSP and hardware. Hermes Agent is by Nous Research.

Keep [LICENSE](LICENSE) and the matching `hermes-gadget-0.2.0-rounded.1-licenses.zip` with redistributed firmware. The archive contains SDK and dependency notices. The original 1.28-inch binary and patch remain under `firmware/` for reference and must not be flashed to this board.
