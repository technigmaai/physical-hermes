"""Offline checks: reject bad images/protected devices and honor backup opt-out."""

import contextlib
import importlib.util
import io
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("flash", Path(__file__).parents[1] / "scripts/flash.py")
flash = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(flash)


class FlashChecks(unittest.TestCase):
    def test_packaged_image(self):
        with contextlib.redirect_stdout(io.StringIO()):
            image = flash.check_image()
        self.assertEqual(image.stat().st_size, 1508352)

    def test_corruption_rejected_before_usb(self):
        with tempfile.TemporaryDirectory() as directory:
            firmware = Path(directory) / "firmware"
            shutil.copytree(flash.FIRMWARE, firmware)
            image = next(p for p in firmware.glob("*.bin") if "-app" not in p.name)
            with image.open("r+b") as output:
                output.write(b"BAD!")
            with patch.object(flash, "FIRMWARE", firmware), patch.object(flash.subprocess, "run") as usb:
                with self.assertRaisesRegex(RuntimeError, "integrity"):
                    flash.check_image()
                usb.assert_not_called()

    def simulate(self, security):
        calls = []

        def run(command, **kwargs):
            calls.append(command)
            output = ""
            if "flash-id" in command:
                output = "Detected flash size: 16MB\n"
            elif "get-security-info" in command:
                output = security
            return subprocess.CompletedProcess(command, 0, output)

        with patch.object(flash.sys, "argv", ["flash.py", "--port", "FAKE", "--skip-backup"]), \
                patch.object(flash.subprocess, "run", side_effect=run), \
                contextlib.redirect_stdout(io.StringIO()):
            flash.main()
        return calls

    def test_skip_backup_writes_and_verifies_without_read(self):
        calls = self.simulate("Secure Boot: Disabled\nFlash Encryption: Disabled\n")
        self.assertFalse(any("read-flash" in call for call in calls))
        self.assertTrue(any("write-flash" in call for call in calls))
        self.assertTrue(any("verify-flash" in call for call in calls))

    def test_protected_flash_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "Secure Boot"):
            self.simulate("Secure Boot: Enabled\nFlash Encryption: Disabled\n")


if __name__ == "__main__":
    unittest.main()
