# Using it

## Talking

**Hold `boot`, speak, release.** That's the whole interaction. The button sits to the **right** of the USB-C port.

Replies appear on screen and are spoken aloud at the same time. Swipe down on the screen to cancel a reply mid-sentence.

## It's a real Hermes

The robot isn't a limited assistant — it's a full client for your agent. Everything Hermes can do, it can do:

> "What's on my calendar today?"
> "Add milk to the shopping list."
> "Summarise the news."
> "Remind me at 6 to take the bins out."

Tools, memory, skills and scheduled jobs all work. It shares your Hermes brain, so it knows what you've talked about elsewhere.

## Settings on the device

Swipe to open the settings screen for:

- Volume
- Screen brightness
- Talk mode — **hold** or **tap**
- Battery indicator style
- Screen timeout
- Wi-Fi setup

## Battery

Unplug it and it keeps going. The screen shows the charge level and whether it's charging.

The battery drains faster with the screen on. Set a **screen timeout** and it'll sleep between conversations and wake when you talk to it.

## Over-the-air updates

Once it's connected, your Hermes machine can push new firmware to it without a cable. Firmware updates arrive through the plugin — you won't need to re-flash.

## Speech

Speech recognition and text-to-speech come from your Hermes configuration, not from the robot. If you want to change voices or switch to a different provider, change it in Hermes — the robot picks it up automatically.

If replies are silent but appear on screen, check your Hermes speech setup (`hermes setup`, or the `stt:` and `tts:` sections of `config.yaml`).

## Common questions

**Nothing happens when I press `boot`.**
It needs Hermes to be reachable. If the screen says **Connecting…**, see [Connect to Hermes](3-connect-to-hermes.md) step 7.

**It worked yesterday and now it won't connect.**
Your Hermes machine's IP address probably changed. Run `hermes gadget info` and re-enter the new URL on the robot via Wi-Fi setup.

**The screen is dark.**
It's asleep. Press the `boot` button or the power button.

**It can't see my Wi-Fi network.**
The ESP32-S3 is 2.4 GHz only.

**I want to move it to another house.**
It stores up to five networks and joins whichever it can find. Add another through Wi-Fi setup, or through the USB console with `wifi add "<name>" "<password>"`.

**How do I factory-reset it?**
`factory-reset` clears the device key and all settings — over the USB console, or from the settings screen.
