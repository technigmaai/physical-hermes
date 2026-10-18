# Physical Hermes

**Give your Hermes Agent a body.**

This turns a cheap AliExpress AI robot toy into a voice device for [Hermes Agent](https://hermes-agent.nousresearch.com) — running entirely on your own machine, using your own model, with no vendor cloud in the loop.

Hold one button, talk, and Hermes answers out loud. The robot's screen becomes Hermes's face, and the whole thing runs on its own battery.

---

## What you need

| | |
|---|---|
| **The robot** | [ESP32-S3 1.28" AI Voice Chat Robot](https://s.click.aliexpress.com/e/_c3d38V2l) — round screen, microphone, speaker, battery, touch. About AU$36. |
| **A USB-C cable** | Any *data* cable. Some charge-only cables won't work. |
| **A computer** | To flash it once. Any OS. |
| **Hermes Agent** | Installed and working, on a machine on the same network. |

That's it. No soldering, no extra parts, no subscriptions.

---

## Quick start

Three things happen: **flash the robot**, **tell it your Wi-Fi**, **connect it to Hermes**.

### 1. Flash the robot

Install esptool:

```bash
pip install esptool
```

Download the firmware from [`firmware/`](firmware/) in this repo, then flash it:

```bash
esptool.py --chip esp32s3 --baud 460800 write_flash 0x0 hermes-gadget-spotpear-128-box-0.2.0.bin
```

Plug the robot into your computer with the USB-C cable when you run that. If it won't connect, unplug it, **hold the `boot` button** (the one to the *right* of the USB-C port), plug it back in while still holding, then release.

[ Full walkthrough → ](docs/2-flash-hermes.md)

### 2. Tell it your Wi-Fi

The robot has no keyboard, so it borrows your phone:

1. Plug the robot in and wait for it to show a setup screen.
2. On your phone, join the Wi-Fi network called **`Hermes-XXXX`** — the password is shown on the robot's screen.
3. Open **http://192.168.4.1** and enter your home Wi-Fi details.

Your password goes straight from your phone to the robot. It never passes through any server.

### 3. Connect it to Hermes

On the machine running Hermes:

```bash
hermes plugins install https://github.com/Adolanium/hermes-gadget-sdk/tree/main/plugin --enable
hermes config set platforms.gadget.enabled true
hermes gateway restart
hermes gadget info
```

Then **allow the gadget port through your firewall** — this is the step most people miss:

```bash
# Linux (ufw)
sudo ufw allow from 192.168.1.0/24 to any port 8765 proto tcp
```

The robot connects within a few seconds and shows **Ready**.

Hold the **`boot`** button, talk, release. Hermes answers out loud.

[ Full walkthrough → ](docs/3-connect-to-hermes.md)

---

## What it does

| | |
|---|---|
| **Talk** | Hold `boot`, speak, release. Hermes hears you. |
| **Listen** | Replies are shown on screen *and* spoken aloud. |
| **Touch** | Swipe down to cancel a reply. |
| **Battery** | Unplugged and portable. Charge level shown on screen. |
| **Anything Hermes can do** | It's a real Hermes client — tools, memory, skills, cron. Ask it to check your calendar. |

Speech recognition and text-to-speech use whatever you already have configured in Hermes.

---

## Requirements on your Hermes machine

- **Port 8765 reachable from your LAN.** Bluetooth isn't used.
- **Speech configured.** Speech-to-text and text-to-speech, either through `hermes setup` or the `stt:` / `tts:` sections of `config.yaml`. Without it the robot still works, but replies are text-only.
- **`ffmpeg`** if your speech output isn't WAV.

---

## Documentation

| | |
|---|---|
| [The device](docs/1-the-device.md) | What the robot is, what's inside it, where to buy |
| [Flash Hermes](docs/2-flash-hermes.md) | Putting the firmware on, start to finish |
| [Connect to Hermes](docs/3-connect-to-hermes.md) | Wi-Fi, the plugin, the firewall, pairing |
| [Using it](docs/4-using-it.md) | Everyday use and settings |
| [The skill](skills/) | The agent skill used to port this board, reusable for others |

---

## Port it to a different robot

The board profile for this exact robot is in [`firmware/spotpear-128-box.patch`](firmware/) — a patch against the [Hermes Gadget SDK](https://github.com/Adolanium/hermes-gadget-sdk).

For a *different* robot, [`skills/hermes-gadget-hardware/`](skills/hermes-gadget-hardware/) is an agent skill that walks through identifying unknown hardware and porting it — reading the vendor's schematic and config, choosing the right driver enums, and knowing which parts need new code versus configuration. Point your agent at it.

---

## Credits

This builds on other people's work:

- **[Hermes Gadget SDK](https://github.com/Adolanium/hermes-gadget-sdk)** by Adolanium and contributors (MIT) — the firmware and the Hermes plugin. Independent community project, not affiliated with Nous Research.
- **[xiaozhi-esp32](https://github.com/78/xiaozhi-esp32)** — the open-source firmware the robot ships with. Its board definitions and SpotPear's published schematics are what made the port possible.
- **[SpotPear](https://spotpear.com)** — the robot itself, with schematics and pin tables published.
- **[Hermes Agent](https://hermes-agent.nousresearch.com)** by [Nous Research](https://nousresearch.com).

The firmware in `firmware/` is MIT, derived from the Hermes Gadget SDK. See [LICENSE](LICENSE).

---

<p align="center">
<b>Built by Hermes.</b><br>
<sub>Researched the hardware from a product listing, identified the board over the network, read the vendor's own schematic and firmware source, wrote the board port, fixed three bugs in the SDK to make it build, compiled and flashed the firmware, and wired the device into the gateway — start to finish, in one session.</sub>
</p>
