"""Installed command for building a checked-out Pelican portfolio project."""

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile


def main(argv=None):
    """Build a project or validate it in temporary storage; return its exit code.

    The Python package provides the command and plugins. Content, theme, and
    configuration remain editable files in the selected project checkout.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "check"))
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if args.command == "check" and args.output is not None:
        parser.error("check uses temporary output; --output is only for build")
    project = args.project.resolve()
    for required in ("content", "theme", "publishconf.py"):
        if not (project / required).exists():
            parser.error(f"Missing {required} in project {project}")
    output = args.output or Path("../pelican-output")
    output = (output if output.is_absolute() else project / output).resolve()
    if output == project or project in output.parents or output in project.parents:
        parser.error("Output must be outside the project and cannot be its ancestor")
    if args.command == "build" and output.exists() and (not output.is_dir() or any(output.iterdir())):
        parser.error("Output must be empty; choose a fresh directory to protect existing files")
    with tempfile.TemporaryDirectory(prefix="portfolio-check-") as temporary:
        target = Path(temporary) / "output" if args.command == "check" else output
        return subprocess.call(
            [sys.executable, "-m", "pelican", "content", "-s", "publishconf.py",
             "-t", "theme", "-o", str(target), "--fatal", "warnings"], cwd=project
        )


if __name__ == "__main__":
    sys.exit(main())
