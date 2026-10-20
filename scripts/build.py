#!/usr/bin/env python3
"""Rebuild the exact 2.16-inch board from the pinned SDK source."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SDK_COMMIT = "63e664c9920321b44390e8161535008e4f73513b"
SDK = ROOT / "sdk"
PROJECT = SDK / "firmware" / "esp32"


def main():
    if not (SDK / ".git").exists():
        sys.exit("Run git submodule update --init --recursive first")
    actual = subprocess.check_output(["git", "-C", str(SDK), "rev-parse", "HEAD"], text=True).strip()
    if actual != SDK_COMMIT:
        sys.exit(f"SDK is at {actual}; expected {SDK_COMMIT}")
    subprocess.run([sys.executable, "-m", "platformio", "run", "-e", "esp32s3-touch-amoled-216"],
                   cwd=PROJECT, check=True)
    subprocess.run([sys.executable, "tools/package_release.py", "--board", "esp32s3-touch-amoled-216",
                    "--out", str(ROOT / "build" / "waveshare-216")], cwd=PROJECT, check=True)


if __name__ == "__main__":
    main()
