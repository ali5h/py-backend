import re
import os
import zipfile
from pathlib import Path
import tomllib


def normalize_project_name(name):
    # https://peps.python.org/pep-0503/#normalized-names
    return re.sub(r"[-_.]+", "-", name).lower()


def normalize_file_name_component(name):
    # https://peps.python.org/pep-0427/#escaping-and-unicode
    return re.sub(r"[^\w\d.]+", "_", name, flags=re.UNICODE)


def get_requires_for_build_editable(config_settings=None):
    """Report requirements for building editable installs."""
    return []


def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    """Build an editable wheel."""
    source_dir = Path(os.getcwd())
    with open(source_dir / "pyproject.toml", encoding="utf-8") as f:
        pyproject = tomllib.loads(f.read())
    name = normalize_project_name(pyproject["project"]["name"])
    fname = normalize_file_name_component(name)
    version = pyproject["project"]["version"]
    wheel_dir = Path(wheel_directory)
    wheel_dir.mkdir(parents=True, exist_ok=True)

    # Create the wheel file
    wheel_name = f"{fname}-{version}-py3-none-any.whl"
    wheel_path = wheel_dir / wheel_name

    with zipfile.ZipFile(wheel_path, "w") as wheel:
        # Add metadata
        dist_info = Path(f"{fname}-0.1.0.dist-info")
        wheel.writestr(str(dist_info / "RECORD"), "")
        wheel.writestr(
            str(dist_info / "METADATA"),
            "\n".join(
                [
                    "Metadata-Version: 2.4",
                    f"Name: {name}",
                    f"Version: {version}",
                    "Root-Is-Purelib: true",
                ]
            ),
        )

        wheel.writestr(
            str(dist_info / "WHEEL"),
            "\n".join(
                [
                    "Wheel-Version: 1.0",
                    "Generator: bdist_wheel 1.0",
                    "Root-Is-Purelib: true",
                    "Tag: py3-none-any",
                    "Build: 1",
                ]
            ),
        )
        # Add .pth file for editable installation
        wheel.writestr(
            f"_{name}.pth",
            "\n".join([f"{source_dir}"]),
        )

    return wheel_name
