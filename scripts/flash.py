#!/usr/bin/env python3
"""Check the 2.16-inch image, back up the connected board, then flash it."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
FIRMWARE = ROOT / "firmware" / "waveshare-216"
FLASH_BYTES = 0x1000000
BOARD = "esp32s3-touch-amoled-2.16"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_image():
    manifest = json.loads((FIRMWARE / "manifest.json").read_text())
    builds = manifest["builds"]
    if len(builds) != 1:
        raise RuntimeError("Expected exactly one board in the firmware manifest")
    board = builds[0]
    if (board["image_board"], board["chip"], board["flash_size"]) != (BOARD, "ESP32-S3", "16MB"):
        raise RuntimeError("Manifest does not describe the 2.16-inch ESP32-S3 board")
    for item in (board["image"], board["app"], manifest["licenses"]):
        path = FIRMWARE / item["path"]
        if path.parent != FIRMWARE or path.stat().st_size != item["size"] or digest(path) != item["sha256"]:
            raise RuntimeError(f"Firmware integrity check failed: {path.name}")
    image = FIRMWARE / board["image"]["path"]
    tag = b"HGBOARD=" + BOARD.encode() + b"\0"
    if tag not in image.read_bytes():
        raise RuntimeError("Image does not contain the exact 2.16-inch board identity")
    print(f"Verified {image.name}: 480x480 CO5300 / CST9220 / ES8311+ES7210", flush=True)
    return image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", help="Explicit USB serial port, e.g. /dev/cu.usbmodem83201")
    parser.add_argument("--check", action="store_true", help="Check files only; do not open USB")
    backup_mode = parser.add_mutually_exclusive_group()
    backup_mode.add_argument("--backup-only", action="store_true", help="Save and verify stock flash without writing")
    backup_mode.add_argument("--skip-backup", action="store_true", help="Write without saving factory firmware")
    parser.add_argument("--stub-version", choices=("1", "2"), default="1",
                        help="Bundled esptool stub; v1 avoids observed v2 read stalls on this device")
    args = parser.parse_args()
    image = check_image()
    if args.check:
        return
    if not args.port:
        parser.error("--port is required; confirm the board is ESP32-S3-Touch-AMOLED-2.16")
    command = [sys.executable, "-m", "esptool", "--chip", "esp32s3", "--port", args.port,
               "--baud", "460800", "--stub-version", args.stub_version, "--after", "no-reset"]

    def run(*arguments, capture=False):
        result = subprocess.run(command + list(arguments), check=True, text=True,
                                stdout=subprocess.PIPE if capture else None, stderr=subprocess.STDOUT)
        if capture:
            print(result.stdout, flush=True)
            return result.stdout

    identity = run("flash-id", capture=True)
    if not re.search(r"Detected flash size:\s+16MB\b", identity):
        raise RuntimeError("Expected 16 MB flash; refusing to write another configuration")
    security = run("get-security-info", capture=True)
    for feature in ("Secure Boot", "Flash Encryption"):
        if not re.search(rf"^{feature}:\s+Disabled\s*$", security, re.MULTILINE):
            raise RuntimeError(f"{feature} must be disabled; refusing to modify protected flash")

    if not args.skip_backup:
        backup_dir = ROOT / "backups"
        backup_dir.mkdir(exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup = backup_dir / f"stock-{stamp}.bin"
        second = backup.with_suffix(".verify.bin")
        run("read-flash", "0x0", hex(FLASH_BYTES), str(backup))
        run("read-flash", "0x0", hex(FLASH_BYTES), str(second))
        if backup.stat().st_size != FLASH_BYTES or second.stat().st_size != FLASH_BYTES or digest(backup) != digest(second):
            raise RuntimeError("Factory backup reads differ or are incomplete; no firmware was written")
        checksum = digest(backup)
        backup.with_suffix(".bin.sha256").write_text(f"{checksum}  {backup.name}\n")
        second.unlink()
        print(f"Factory backup verified by two identical reads: {backup}", flush=True)
    if args.backup_only:
        return
    # Recheck files immediately before writing. The merged image includes the
    # partition table and blanks NVS.
    check_image()
    run("write-flash", "0x0", str(image))
    run("verify-flash", "0x0", str(image))
    subprocess.run(command[:-2] + ["--after", "hard-reset", "get-security-info"], check=True)
    print("Firmware written and verified. Continue with docs/3-connect-to-hermes.md.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        sys.exit(str(exc))
