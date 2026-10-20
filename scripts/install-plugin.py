#!/usr/bin/env python3
"""Install this fork's matching gadget plugin without changing pairing/configuration."""
import argparse
import importlib.util
import os
from pathlib import Path
import shutil

spec = importlib.util.spec_from_file_location("physical_hermes_build", Path(__file__).with_name("build.py"))
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")))
    args = parser.parse_args()
    source = build.prepare_source() / "plugin"
    destination = args.home.expanduser().resolve() / "plugins" / "gadget"
    if not (destination / "plugin.yaml").exists():
        parser.error(f"Install/enable the gadget plugin in {args.home} first")
    if destination.is_symlink():
        parser.error("Plugin is linked to a source checkout; update that source instead")
    # Copy only plugin source/metadata. Identity and history live in plugin-data and state.db.
    for path in sorted(source.iterdir()):
        if path.is_file() and path.suffix in (".py", ".yaml", ".md"):
            temporary = destination / (path.name + ".physical-hermes-new")
            shutil.copyfile(path, temporary)
            temporary.replace(destination / path.name)
    print(f"Installed matching plugin in {destination}. Restart the Hermes gateway.")


if __name__ == "__main__":
    main()
