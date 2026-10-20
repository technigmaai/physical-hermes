# ESP32-S3-Touch-AMOLED-2.16 hardware

Target: Waveshare / SpotPear **ESP32-S3-Touch-AMOLED-2.16**, Waveshare SKU 33969. It has a 480×480 framebuffer with a physically rounded rectangular screen opening, unlike the original Physical Hermes circular 1.28-inch robot.

| Part | Selected configuration |
|---|---|
| MCU / memory | ESP32-S3R8 at 240 MHz, 16 MB flash, 8 MB octal PSRAM at 80 MHz |
| Display | CO5300, 480×480 RGB565, QSPI at 40 MHz; no framebuffer offset |
| Display pins | CS 12, SCLK 38, D0 4, D1 5, D2 6, D3 7, RESET 39 |
| Orientation | Vendor 480×480 initialization table, MADCTL `0xA0` |
| Rounded-corner layout | 48-pixel additional side insets for header/footer text; full-width central content |
| Shared I2C | SDA 15, SCL 14, 400 kHz |
| Touch | CST9220 at `0x5A`; RESET 40, INT 11; mirror Y then swap X/Y |
| Speaker | ES8311 plus amplifier enable GPIO 46 |
| Microphones | ES7210 ADC, MIC1/MIC2 |
| Shared I2S | MCLK 42, BCLK 9, WS 45, speaker DOUT 8, microphone DIN 10 |
| Power | AXP2101 at `0x34`; charging and supply settings preserved |
| Buttons | BOOT GPIO 0: talk/select; +/KEY (KEY3) GPIO 18: cancel/session navigation; PWR via AXP2101: screen sleep/shutdown |
| Console | USB Serial/JTAG, 115200 |

The SDK uses a 480×480 PSRAM framebuffer and its actual AMOLED driver. Scaling the old 240×240 robot image would not work. The IMU, RTC and SD slot are not exposed by this profile. See [the button map](7-sessions-and-buttons.md).

Sources:

- [Vendor guide](https://spotpear.com/wiki/ESP32-S3-2.16-inch-AMOLED-Display-Capacitive-TouchScreen.html)
- [Waveshare example source](https://github.com/waveshareteam/ESP32-S3-Touch-AMOLED-2.16)
- Pinned [`board.cpp`](../sdk/firmware/esp32/main/board.cpp): `CONFIG_HG_BOARD_AMOLED_216`
- Pinned [`port_amoled.cpp`](../sdk/firmware/esp32/main/port_amoled.cpp): `kInit480`
- Pinned [`sdkconfig.defaults`](../sdk/firmware/esp32/boards/esp32s3-touch-amoled-216/sdkconfig.defaults)

Run `git submodule update --init --recursive` to populate source links. USB VID/PID `303A:1001` identifies Espressif USB Serial/JTAG, not the display model. Confirm the board label before flashing.

Next: [Flash Hermes](2-flash-hermes.md).
