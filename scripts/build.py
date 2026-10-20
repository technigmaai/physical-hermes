#!/usr/bin/env python3
"""Rebuild the exact 2.16-inch board from the pinned SDK source."""

import argparse
import hashlib
import io
import os
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SDK_COMMIT = "63e664c9920321b44390e8161535008e4f73513b"
SDK = ROOT / "sdk"
PATCH = ROOT / "firmware" / "waveshare-216" / "device-customizations.patch"


def prepare_source():
    """Apply our overlay to a generated checkout; leave the pinned SDK clean."""
    fingerprint = hashlib.sha256(PATCH.read_bytes()).hexdigest()[:12]
    source = ROOT / "build" / f"sdk-rounded-{fingerprint}"
    ready = source / ".physical-hermes-prepared"
    if not ready.exists() or ready.read_text().splitlines()[0] != SDK_COMMIT:
        source.mkdir(parents=True, exist_ok=True)
        archive = subprocess.check_output(["git", "-C", str(SDK), "archive", SDK_COMMIT])
        with tarfile.open(fileobj=io.BytesIO(archive)) as contents:
            contents.extractall(source, filter="data")
        subprocess.run(["git", "init", "--quiet", str(source)], check=True)
        subprocess.run(["git", "-C", str(source), "apply", str(PATCH)], check=True)
        ready.write_text(f"{SDK_COMMIT}\n{fingerprint}\n")
    return source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare-only", action="store_true", help="Prepare the patched source without building")
    args = parser.parse_args()
    if not (SDK / ".git").exists():
        sys.exit("Run git submodule update --init --recursive first")
    actual = subprocess.check_output(["git", "-C", str(SDK), "rev-parse", "HEAD"], text=True).strip()
    if actual != SDK_COMMIT:
        sys.exit(f"SDK is at {actual}; expected {SDK_COMMIT}")
    source = prepare_source()
    project = source / "firmware" / "esp32"
    print(f"Patched source: {source}", flush=True)
    if args.prepare_only:
        return
    environment = dict(os.environ)
    environment.setdefault("PLATFORMIO_CORE_DIR", str(ROOT / "build" / "platformio"))
    subprocess.run([sys.executable, "-m", "platformio", "run", "-e", "esp32s3-touch-amoled-216"],
                   cwd=project, env=environment, check=True)
    subprocess.run([sys.executable, "tools/package_release.py", "--board", "esp32s3-touch-amoled-216",
                    "--out", str(ROOT / "build" / "waveshare-216")], cwd=project, env=environment, check=True)


if __name__ == "__main__":
    main()
