# Porting a board to the Hermes Gadget SDK

Everything below is under `firmware/esp32/`.

## Files to touch

| File | What to add |
|---|---|
| `main/board.hpp` | new enum values (e.g. an `LcdController` entry), new fields on a `*Config` struct |
| `main/Kconfig.projbuild` | a `config HG_BOARD_<NAME>` bool inside the `HG_BOARD` choice |
| `main/board.cpp` | `#define HG_BOARD_NAME "<name>"` in the name chain, plus a `make()` branch |
| `main/port_display.cpp` | a panel branch when the controller is not ST7789/ILI9342/ST77916 |
| `main/port_touch.cpp` | a second I2C bus, when the panel is not on the codec's bus |
| `main/CMakeLists.txt` | any new managed component in `PRIV_REQUIRES` |
| `main/idf_component.yml` | the managed component dependency |
| `platformio.ini` | an `[env:<name>]` block |
| `boards/<name>/sdkconfig.defaults` | flash size, PSRAM mode/speed, console, `CONFIG_HG_BOARD_<NAME>=y` |
| `boards/<name>.json` | browser-installer manifest (copy an existing one; `hwids: [["0x303A", "0x1001"]]`) |
| `docs/hardware.md` | a board section: pin table plus a "First flash: what to check" list |

## Board profile skeleton

`make()` returns a `BoardConfig`. Only the fields that encode real hardware decisions:

```cpp
BoardConfig make() {
  BoardConfig b{};
  b.name = kBoardName;

  // Panel — mirror/invert/swap come from the vendor config, never guessed
  b.lcd.enabled = true;
  b.lcd.controller = LcdController::<X>;
  b.lcd.width = 240; b.lcd.height = 240;
  b.lcd.round = <bool>;
  b.lcd.mirror_x / mirror_y / swap_xy / invert = <from vendor config>;
  b.lcd.mosi / sclk / cs / dc / rst / backlight = <pins>;
  b.lcd.backlight_invert = <bool>;   // active-low is common
  b.lcd.spi_mhz = 40;

  b.i2c = {sda, scl, 400000};        // the codec's bus

  b.codec.enabled = true;
  b.codec.mclk / bclk / ws / dout / din / pa = <pins>;
  b.codec.mic = MicCodec::Es8311;    // one codec both ways; Es7210 for a separate MEMS ADC

  b.touch.enabled = true;
  b.touch.controller = TouchController::<X>;
  b.touch.addr / rst / int_gpio = <values>;
  b.touch.bus_sda = 11; b.touch.bus_scl = 7;   // ONLY if the panel has its own I2C pair
  b.touch.width = 240; b.touch.height = 240;
  b.touch.mirror_x = <match the panel's mirror>;

  b.latch_power = {true, adc, enable, charging, backlight, mv_ratio, max_battery_mv, power_off_supported};
  b.latch_power.charging_active_high = <bool>;

  b.status_led = <gpio>;
  b.buttons = {0, -1, -1, -1};       // a direct GPIO takes the first slot; BOOT = TALK
  b.talk_label = "BOOT";
  b.cancel_label = "Swipe down";
  return b;
}
```

## Deciding each field

- **`mv_ratio`** — read the divider off the schematic (two equal resistors → ratio 2).
  `max_battery_mv` is the pack's full-charge voltage (4200 for a LiPo).
- **`b.latch_power.enable`** — `-1` when the board has no latch GPIO, which also means
  `power_off_supported = false`. Requires the guard described in SKILL.md.
- **`b.codec.mic`** — `Es8311` for analog microphones into the speaker codec's ADC; `Es7210` when a
  separate MEMS ADC is fitted.
- **`b.buttons`** — a plain GPIO button takes the first slot; `-1` for the rest. A board with only
  BOOT is `{0, -1, -1, -1}`.
- **Touch `mirror_x`** — set it to match the panel's mirroring; a mirrored panel with an unmirrored
  touch layer gives inverted coordinates, and this is the line to flip.
- **Sample rates** — take them from the vendor config; the codec pair and the I2S bus must agree.

## Display drivers

`SpiDisplay` covers ST7789 (IDF built-in) plus managed ILI9342 and ST77916. Any other SPI controller
is a new branch calling `esp_lcd_new_panel_<chip>()` alongside the existing ones, plus the component
in `idf_component.yml` and `CMakeLists.txt`, and a `controller_name_` ternary for the log line.
RGB-parallel panels go through `port_rgb.cpp` / `port_parallel.cpp` instead and need `RgbTimings`
sourced from the panel datasheet.

## Verify the port

1. **Build.** Read the `Flash:` line — expect well under the 2 MB slot.
2. **Flash**, then capture the boot log at 115200 (reset the board first to get the sequence from the
   top). Redirected `cat` truncates; drive the port with pyserial and drain on a timer instead.
3. **Expect the four lines that prove it:** the panel's `ready` line, the codec's
   `speaker ready, microphones ready (<codec> <path>)`, the power line
   (`battery latch enabled; calibrated voltage available`), and
   `device hg-… ready (board <name>, fw <version>)`.
4. **`diag`** — `parts` should name display/microphone/speaker/touch as expected, and `i2c` should
   list the addresses you expect. Whatever reads `no` in `parts` is the thing to debug. `key: no` is
   normal for a board whose buttons are direct GPIOs rather than an I2C expander.
5. **Sanity-check a real reading.** A plausible `battery_mv` and a `charging` value that flips when
   you pull USB confirms the divider ratio and the charge polarity in one go.

## Flash layout notes

The shared `partitions.csv` keeps two app slots at `0x1f0000` each so images stay interchangeable
across boards. Erasing before the first flash is safe once the full stock dump is on disk — and it is
worth doing, because the vendor layout usually differs (an extra multi-megabyte assets partition, a
differently sized NVS).
