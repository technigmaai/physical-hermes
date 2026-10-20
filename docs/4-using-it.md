# Using it

## Talking

**Hold the button marked BOOT, speak, release.** Use the label on your ESP32-S3-Touch-AMOLED-2.16; its button positions differ from the original robot.

Replies appear on screen and are spoken aloud at the same time. Click +/KEY or swipe down to cancel a reply.

## Conversations

Double-click **+/KEY** to start a fresh conversation. Hold **+/KEY for two seconds** to open Sessions. Click +/KEY to move through the list and BOOT to select, or swipe and tap the screen. Hold +/KEY again to return without switching.

See [Sessions and buttons](7-sessions-and-buttons.md) for the full map and matching Mac plugin installation.

## It's a real Hermes

The robot isn't a limited assistant — it's a full client for your agent. Everything Hermes can do, it can do:

> "What's on my calendar today?"
> "Add milk to the shopping list."
> "Summarise the news."
> "Remind me at 6 to take the bins out."

Tools, memory, skills and scheduled jobs all work. It shares your Hermes brain, so it knows what you've talked about elsewhere.

## Settings on the device

Hold the screen's title bar for one second to open settings for:

- Volume
- Screen brightness
- Talk mode — **hold** or **tap**
- Battery indicator style
- Screen timeout
- Wi-Fi setup

## Battery

Portable use requires a compatible battery connected to the board's battery header. The AXP2101 supplies battery and charging information. Battery operation, charging accuracy and runtime remain unverified for this experimental profile.

Use a screen timeout to reduce display power. This profile does not enable CPU light sleep. A short PWR press controls screen sleep; check wake behavior on your hardware before relying on it.

## Over-the-air updates

Once connected, the plugin can send an app-only image for this exact board using `hermes gadget update`. Keep a USB recovery path. App-only OTA has been exercised on this device; rollback still requires physical validation; never send the original 1.28-inch image to this board.

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
