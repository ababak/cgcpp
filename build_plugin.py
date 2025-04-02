"""
(c) Andriy Babak 2025

date: 02/04/2025
modified: 02/04/2025 13:19:52

Author: Andriy Babak
e-mail: ababak@gmail.com
------------------------------
description: cgcpp
------------------------------
"""

# /// script
# dependencies = [
#     "setuptools",
#     "toml",
# ]
# ///

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

import toml


def get_version() -> str:
    """Read package version from the pyproject.toml file."""
    with open("pyproject.toml", encoding="utf-8") as fd:
        pyproject = toml.load(fd)
    return pyproject["project"]["version"]


def get_build_name():
    """Parse the package and retreive the build name."""
    name = Path.cwd().name
    version = get_version()
    build_name = f"{name}-{version}"
    return build_name


def process():
    """Run the build step."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--rebuild",
        help="Rebuild the resources archive",
        action="store_true",
    )
    args = parser.parse_args()
    build_plugin(rebuild=args.rebuild)


def build_plugin(rebuild: bool = False) -> Path:
    """Run the build step."""
    root_path = Path(__file__).parent
    build_path = root_path / "build"
    build_name = get_build_name()
    archive_name = f"{build_name}.zip"
    staging_path = build_path / build_name
    plugin_zip_path = build_path / archive_name
    if plugin_zip_path.is_file() and not rebuild:
        print(f"Archive already exists: {plugin_zip_path}")
        return plugin_zip_path

    # Clean staging path
    print(f'Preparing to stage: "{build_name}"')
    shutil.rmtree(staging_path, ignore_errors=True)
    print(f'Building: "{build_name}"')
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", ".", "--target", staging_path]
    )
    # Generate plugin zip
    print(f'Archiving: "{build_name}"')
    plugin_zip_path = Path(
        shutil.make_archive(
            base_name=os.path.join(build_path, build_name),
            format="zip",
            root_dir=staging_path,
        )
    )
    print(f'Archive created: "{plugin_zip_path}"')
    return plugin_zip_path


if __name__ == "__main__":
    raise SystemExit(process())
