# Connect to Hermes

The ESP32-S3-Touch-AMOLED-2.16 is flashed and awake. Now it needs to find your Hermes.

Do this on the machine where Hermes is installed.

## 1. Install the Hermes plugin

The robot talks to Hermes over a websocket, using a plugin:

```bash
hermes plugins install https://github.com/Adolanium/hermes-gadget-sdk/tree/main/plugin --ref 63e664c9920321b44390e8161535008e4f73513b --enable --yes-deps
```

## 2. Turn the platform on and restart

```bash
hermes config set platforms.gadget.enabled true
hermes gateway restart
```

**The restart matters.** The listener doesn't move while the gateway is running — the port only opens when it restarts.

## 3. Get your device URL

```bash
hermes gadget info
```

It prints a line like:

```
device URL : ws://192.168.1.50:8765/gadget
```

**Write that down** — you'll type it into your phone in a moment. It's this machine's address on your network, and the robot needs it to find Hermes.

## 4. Open the firewall

This is the step people miss. The robot connects *to* your Hermes machine on **TCP port 8765**, and many systems block incoming connections by default.

**Linux (ufw):**

```bash
sudo ufw allow from 192.168.1.0/24 to any port 8765 proto tcp
```

Adjust `192.168.1.0/24` to match your network if it's different.

On macOS, allow incoming connections for the Hermes process when prompted, or add a rule in System Settings → Network → Firewall.

**Symptom of skipping this:** the robot sits on **Connecting…** forever while everything else looks correct.

## 5. Give it your Wi-Fi

The robot has no keyboard, so it borrows your phone. It's already broadcasting its own temporary network.

1. On your phone, open Wi-Fi settings and join the network called **`Hermes-XXXX`**. The password is shown on the robot's screen.
2. Your phone will warn there's no internet. Keep the connection anyway.
3. Open **http://192.168.4.1** in your phone's browser.
4. Enter:
   - your **2.4 GHz** Wi-Fi network name and password, and
   - the **device URL** from step 3
5. Tap **Check connection and save**. Give it up to 30 seconds.
6. When it reports success, reconnect your phone to your normal network.

Your Wi-Fi password goes straight from your phone to the robot. It never passes through any server, and the robot never sends it back.

> The temporary network closes after ten minutes. If it lapses, power-cycle the robot to reopen it.

## 6. Approve pairing

When the board shows a pairing code, run on your Hermes machine:

```bash
hermes gadget pair
```

Check that its code matches the device before approving. It should then show **Ready**. This command lists connected devices:

```bash
hermes gadget devices
```

should list it.

## 7. Talk to it

Hold the button marked **BOOT**, speak, and let go. Hermes hears you, thinks, and answers out loud. Button positions differ from the original 1.28-inch robot. Configure speech recognition and text-to-speech on the Hermes host; the device streams audio and does not run the language model locally.

## If it stays on "Connecting…"

Work through these in order:

| Check | Command |
|---|---|
| Is the listener actually up? | `ss -tlnp \| grep 8765` |
| Is the firewall letting it through? | `sudo ufw status` — look for your 8765 rule |
| Did you restart the gateway *after* enabling? | `hermes gateway restart` |
| Is the device URL right? | `hermes gadget info` — it must match your machine's LAN address |
| Are you on 2.4 GHz? | The ESP32-S3 can't see 5 GHz networks at all |

If your Hermes machine's IP address changes (a DHCP renewal), re-do step 5 with the new URL.

---

Next: **[Using it →](4-using-it.md)**
