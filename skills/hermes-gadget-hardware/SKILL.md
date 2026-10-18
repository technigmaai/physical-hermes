---
name: hermes-gadget-hardware
description: "Use when porting, flashing or pairing Hermes Gadget."
version: 1.0.0
author: Hermes Agent
license: MIT
category: software-development
platforms: [linux]
tags:
  - esp32
  - esp-idf
  - platformio
  - firmware
  - hermes-gadget
  - hardware
metadata:
  hermes:
    tags: [esp32, esp-idf, platformio, firmware, hermes-gadget, hardware]
    related_skills: [consumer-device-verification, chinese-consumer-electronics]
---

# Hermes Gadget hardware

Hermes Gadget is an **independent community SDK** (`Adolanium/hermes-gadget-sdk`), not a Nous project
— say so when recommending it. ESP32-S3 firmware in C++ over ESP-IDF, built per board with
PlatformIO, plus a Hermes plugin that serves the device over a websocket. It is young and moves fast:
check the repo's `firmware/esp32/boards/` directory for the real profile list rather than trusting a
release note.

Layout: `firmware/esp32/` (one PlatformIO env per board; `main/` is the HAL; `boards/<name>/` holds
per-board `sdkconfig.defaults`; `boards/<name>.json` is the browser-installer manifest),
`firmware/drivers/` (shared code already on the include path), `docs/`, `plugin/`.

## Pick hardware the SDK already drives

Cheapest fun targets are the XiaoZhi/DeepSeek AI chat toys: ESP32-S3, a small SPI panel, mic and
speaker in a finished case with a battery. Many are the SDK's own reference build (ST7789 + INMP441 +
MAX98357A), so the port is a pin table rather than new driver code.

Before buying, read `main/board.hpp` and check four enums — `LcdController`, `SpeakerCodec`,
`MicCodec`, `TouchController`. They list exactly what is supported. A board matching on all four is a
configuration-only port; one needing a new panel or codec driver is a different-sized job. Prefer a
board whose audio front-end reuses an existing codec pair: voice is the point of the device, and a
board with no microphone is text-only.

## Identify what actually arrived

Never infer the board from the listing. See `consumer-device-verification` for the networked-device
treatment; the short version:

1. **LAN:** ping-sweep, then `ip neigh`; resolve the OUI. An Espressif OUI means an ESP32.
2. **USB:** ESP32-S3 enumerates as `303a:1001` "USB JTAG/serial debug unit", reporting the WiFi MAC
   as its serial number. Both interfaces sharing one MAC confirms identity.
3. **Dump the whole flash first** — it is the rollback image *and* the hardware map:
   `esptool --chip esp32s3 read_flash 0 0x1000000 stock.bin` (~80 s at ~1.6 Mbit/s).
4. `strings stock.bin | grep -iE "gc9a01|st77|es8311|es7210|inmp441|max98357|cst816"` names the panel
   and codec. The binary usually names its own upstream board, e.g.
   `./main/boards/<vendor>/<board>/config.h`.
5. `strings | grep -oE "https?://..."` lists every endpoint it talks to.

## Port a board

Vendor firmware is usually built from open-source XiaoZhi (`78/xiaozhi-esp32`), and vendor wikis
publish schematics and pin tables. **Read those before reverse-engineering anything** — the vendor's
`config.h` is authoritative for pin numbers, mirror/invert flags and sample rates, and the schematic
settles electrical questions. Cross-check both: they disagree usefully, because a schematic shows a
net while only `config.h` shows the value that actually works on the shipped panel.

File-by-file recipe, board-profile skeleton and field-by-field decisions:
`references/porting-a-board.md`.

## Flash and pair

```bash
cd firmware/esp32
pio run -e <env>                 # build
pio run -e <env> -t upload       # BOOT does not need holding; esptool resets over USB-JTAG
```

`BOOT` need not be held: esptool drives the USB-Serial-JTAG reset itself. If a user reports the BOOT
button "doing nothing", flash anyway before debugging the button — the button is for the vendor
firmware, not for us.

The serial console at 115200 (`pio device monitor`, or pyserial) carries the whole setup:
`set server ws://<host>:8765/gadget`, `set wifi_ssid` / `set wifi_pass`,
`wifi add "<ssid>" "<pass>"`, `get`/`set <key>`, `status`, `diag`, `say`, `talk`/`release`,
`wifi-setup`, `factory-reset`. `diag` reports `parts` (which subsystems came up) and `i2c` (addresses
that answered) — the fastest confirmation that a port works.

Hermes side:

```bash
hermes plugins install https://github.com/Adolanium/hermes-gadget-sdk/tree/main/plugin --enable --yes-deps
hermes config set platforms.gadget.enabled true     # then RESTART the gateway
hermes gadget info                                  # prints the device URL
hermes gadget pair                                   # approves a device showing a code
```

Config edits do not move the running listener — port 8765 only opens on a gateway restart.

**Never register or activate the vendor's cloud account.** Replacing the firmware is the point: no
activation is needed, and the vendor OTA path is a standing remote-code-push channel into the LAN.
For Wi-Fi credentials, prefer the device's own phone setup (`wifi-setup`) so the password goes from
the user's phone to the device and never through the chat transcript.

## Voice and audio on the device

The device has **no voice of its own**. The firmware only writes PCM to the codec
(`CodecSpeaker::write`); it never synthesises speech. Every word the user hears was produced by the
host's TTS provider and streamed over. So "change how the gadget sounds" is a **host TTS config
change**, and the platform hands it to the normal auto-TTS path.

```bash
grep -nE "^tts:|provider:|voice:" ~/.hermes/config.yaml   # what is actually configured
ls -la ~/.hermes/cache/piper-voices/                      # which voices are actually on disk
hermes config set tts.piper.voice en_US-ryan-high         # patch/write_file are REFUSED on config.yaml
python3 -m piper.download_voices en_US-ryan-high --download-dir ~/.hermes/cache/piper-voices
```

Voices auto-download on first use (300 s cap), so pre-downloading only shortens the first reply.

- **Verify synthesis before promising a voice.** Load the .onnx directly and write a scratch WAV:
  `PiperVoice.load(path).synthesize_wav(text, wave_file, syn_config=SynthesisConfig(length_scale=1.2))`.
  A path that exists is not a voice that renders, and a 120 MB model loads slowly enough to look hung.
- **Piper's catalogue is American/British/other nationalities only — there is no Caribbean voice and
  no accent knob.** A regional accent needs a cloning engine (XTTS, ElevenLabs) driven from a
  reference clip. Say that plainly instead of implying an accent is one config value away.
- **Deeper = slower.** `length_scale` (1.2–1.3) stretches phoneme timing and is what actually reads as
  a lower, heavier voice on the tiny speaker; `tts.piper.length_scale` sets it globally, or per call
  through `SynthesisConfig`. Voice choice matters less than people expect — `en_US-lessac-medium` is a
  male voice that most listeners read as female.
- **The speaker is a TTS sink, not an audio output.** There is no path for music or media to it, and
  the only device actions are `led.set`, `screen.brightness`, `speaker.volume`. When asked to play a
  song on the gadget, name an external speaker (phone, Bluetooth) instead of reaching for a playback
  tool that has nowhere to send the audio.
- **When the user reports the voice is wrong, read the pipeline before reasoning about it.** The
  configured voice, the installed voice files, and how the platform receives audio together decide
  the answer; answering from the intended config ("it's already a male voice") makes the user ask
  again. `adapter.py` and `tools/tts_tool_local.py` show the real path in a couple of greps.
- **Config is cached on the file signature**, so a scalar TTS value change is picked up on the next
  synthesis without restarting the gateway (unlike `platforms.gadget.*`, which needs a restart for
  the listener to move). If the old voice persists anyway, in-process voice caches are the suspect.

## Pitfalls

- **A new managed component needs three edits, not one.** `main/idf_component.yml` (fetch it),
  `main/CMakeLists.txt` `PRIV_REQUIRES` (put its include directory on the app's path), and the
  `#include`. Skip `PRIV_REQUIRES` and the component downloads correctly into `managed_components/`
  while the compiler still reports the header missing.
- **Editing `PRIV_REQUIRES` does not invalidate PlatformIO's CMake cache.** The log shows
  "Reading CMake configuration…" and goes straight to compiling, so the identical error reappears and
  a correct fix looks wrong. Delete `.pio/build/<env>/` to force a reconfigure. To see what a file
  really gets: `pio run -e <env> -v > vb.log 2>&1`, then
  `grep -m1 "<file>.cpp" vb.log | tr ' ' '\n' | grep -oE "managed_components/[^/ ]+"`.
- **Managed component headers do not follow IDF's naming convention.** IDF's own driver is
  `esp_lcd_panel_st7789.h`, but the managed GC9A01 component ships `esp_lcd_gc9a01.h` (no `panel_`).
  `ls managed_components/<name>/include/` and use the real filename rather than extrapolating from a
  similar driver. A correct include path plus an invented filename produces exactly the same
  "No such file or directory" as a missing dependency — fix one, re-test, then fix the next.
- **Check whether the touchscreen shares the codec's I2C bus.** Boards often put the codec on one pin
  pair (15/14) and the panel on another (11/7). `TouchConfig` has no bus fields by default; add
  `bus_sda`/`bus_scl` and bring up a second master on `I2C_NUM_1`. Symptom of getting this wrong:
  `hg.touch: touch controller at 0xNN did not answer`, with the diag `i2c` list showing only the codec
  — scanning the wrong wires finds nothing at *any* address, so it looks like absent hardware.
- **A battery board with no power-latch GPIO breaks `LatchPower::begin`.** It unconditionally calls
  `gpio_set_level((gpio_num_t)cfg.enable, 1)` and `1ULL << cfg.enable`; with `enable = -1` that is a
  bogus pin mask that can collide with the flash bus, and the port aborts at startup. Guard with
  `if (cfg.enable >= 0)` and make `power_off()` refuse when there is no latch. Also check charge
  polarity: the driver reads charge status **active-low**, so a board driving it active-high reads
  inverted and needs a polarity flag.
- **One ES8311 with no ES7210 is a supported topology.** Analog microphones wired into the speaker
  codec's own ADC is `MicCodec::Es8311`, where one codec handle covers both directions. Do not write a
  new driver for it — read `port_codec.cpp` first, it may already describe the board's exact wiring.
- **Take mirror/invert flags from the vendor's config, never by guessing.** `DISPLAY_MIRROR_X`,
  `DISPLAY_BACKLIGHT_OUTPUT_INVERT` and the panel init's `invert_color`/`mirror` calls are the values
  the board ships with. Round panels usually need `invert_color(true)`. Backlights are frequently
  active-low.
- **The shared `partitions.csv` caps the app at 2 MB per OTA slot** so images stay interchangeable
  across boards. On a 16 MB board that wastes most of the flash, and a build near 66% of the slot has
  little headroom. Do not resize casually — but know the space exists if custom assets are ever wanted.

## Long builds

The first `pio run` pulls roughly 1.5–2 GB (two toolchains plus `framework-espidf`), which dominates
the first run and can dwarf the actual compile.

- **Set `persist_on_release=true` on the background build job.** Without it, session cleanup or
  compaction can kill the download mid-flight; it then dies at the same point on every retry with
  nothing in the log, which reads exactly like a network stall. Check the download cache size to tell
  a stall from a kill.
- Redirect to a file and print the tail on exit. Piping through `| tail` masks the exit code and
  defeats `set -e`, so a failed step looks like a success.
- PlatformIO's tool-manager progress writes with `\r` and does not flush to a redirected file; judge
  progress from the cache size, not the log.
- Check a tool's flags before use (`pio pkg install` has no `-v`), and open each build job with a
  guard that greps for its own precondition, so a silent no-op becomes a loud abort.
- Prefer a dedicated venv on a Python version PlatformIO supports; a too-new system Python is the
  usual reason a first install misbehaves.

## Reference Files

- `references/porting-a-board.md` — the file-by-file port recipe, board-profile skeleton, how to
  decide each hardware field, and the boot-log lines that prove a port works.
