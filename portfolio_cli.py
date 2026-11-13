"""Installed command for building a checked-out Pelican portfolio project."""

import argparse
from datetime import date
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from threading import Thread


def _new_content(args, parser):
    """Write a valid starter without overwriting an existing document."""
    title = args.title
    if title is None:
        if not sys.stdin.isatty():
            parser.error('Supply a title, for example: spg new post "My post"')
        title = input("Title: ")
    title = title.strip()
    if not title:
        parser.error("Title must not be empty")
    slug = args.slug or re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        parser.error("Use --slug with lowercase letters, numbers, and hyphens")
    target = args.project / "content" / {"post": "posts", "project": "projects", "page": "pages"}[args.kind] / f"{slug}.md"
    template = args.project / "content-templates" / f"{args.kind}.md"
    if not template.is_file():
        parser.error(f"Missing starter template: {template}. Restore content-templates/ from the checkout.")
    document_text = template.read_text(encoding="utf-8")
    replacements = {"Title": json.dumps(title, ensure_ascii=False), "Slug": slug}
    if args.kind == "post":
        today = date.today()
        month = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()[today.month - 1]
        replacements["Date"] = f"{month} {today.day:02d}, {today.year}"
    # Edit only the active front-matter values; preserve field names, order,
    # optional-field comments, and the reusable body exactly as written.
    parts = document_text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        parser.error(f"Invalid starter front matter in {template}")
    for field, value in replacements.items():
        parts[1] = re.sub(rf"^{field}:.*?(?= #|$)", lambda match: f"{field}: {value}", parts[1], flags=re.MULTILINE)
    document_text = "---".join(parts)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8") as document:
            document.write(document_text)
    except FileExistsError:
        parser.error(f"Already exists: {target}. Edit it or choose another --slug.")
    print(f"Created {target}")
    return 0


def _validate_content(project):
    """Report authoring errors using the unchanged production reader rules."""
    from pelican.settings import read_settings
    from pelican_readers import FrontmatterMarkdownReader
    from yaml import YAMLError

    settings = read_settings(path=str(project / "publishconf.py"), override={"PATH": str(project / "content")})
    reader = FrontmatterMarkdownReader(settings)
    errors = 0
    sources = sorted((project / "content").rglob("*.md"))
    for source in sources:
        try:
            reader.read(str(source))
        except (ValueError, TypeError, AttributeError, OSError, YAMLError) as error:
            errors += 1
            print(f"ERROR {source.relative_to(project)}: {error}\n"
                  "  See CONTENT_GUIDE.md and the matching content-templates/ starter.", file=sys.stderr)
    if errors:
        print(f"Found invalid metadata in {errors} of {len(sources)} files. No files changed.", file=sys.stderr)
        return 1
    print(f"Validated {len(sources)} Markdown files. No files changed. Use spg check for a full build.")
    return 0


def _preview(project, port):
    """Reuse Pelican's watcher and Python's server with isolated output."""
    from pelican import main as pelican_main

    previous_directory = Path.cwd()
    previous_url = os.environ.get("PORTFOLIO_PREVIEW_URL")
    with tempfile.TemporaryDirectory(prefix="portfolio-preview-") as temporary:
        os.environ["PORTFOLIO_PREVIEW_URL"] = f"http://127.0.0.1:{port}"
        try:
            os.chdir(project)
            command = ["content", "-s", "devconf.py", "-t", "theme", "-o", str(Path(temporary) / "output")]
            # Fail clearly on an invalid initial build before opening the server.
            checked = subprocess.call([sys.executable, "-m", "pelican", *command, "--fatal", "warnings"])
            if checked:
                return checked
            handler = partial(SimpleHTTPRequestHandler, directory=str(Path(temporary) / "output"))
            try:
                server = ThreadingHTTPServer(("127.0.0.1", port), handler)
            except OSError as error:
                print(f"Cannot serve port {port}: {error}. Try spg dev --port 8001.", file=sys.stderr)
                return 1
            thread = Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                print(f"Preview: http://127.0.0.1:{port} (save to rebuild; refresh your browser).", flush=True)
                pelican_main([*command, "--autoreload"])
            finally:
                server.shutdown()
                server.server_close()
                thread.join()
            return 0
        finally:
            os.chdir(previous_directory)
            if previous_url is None:
                os.environ.pop("PORTFOLIO_PREVIEW_URL", None)
            else:
                os.environ["PORTFOLIO_PREVIEW_URL"] = previous_url


def main(argv=None):
    """Build a project or validate it in temporary storage; return its exit code.

    The Python package provides the command and plugins. Content, theme, and
    configuration remain editable files in the selected project checkout.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("build", "check", "dev", "new", "validate"):
        subparser = commands.add_parser(command)
        subparser.add_argument("--project", type=Path, default=Path.cwd())
        if command == "build":
            subparser.add_argument("--output", type=Path)
        if command == "dev":
            subparser.add_argument("--port", type=int, default=8000)
        if command == "new":
            subparser.add_argument("kind", choices=("post", "project", "page"))
            subparser.add_argument("title", nargs="?")
            subparser.add_argument("--slug")
    args = parser.parse_args(argv)
    project = args.project.resolve()
    for required in ("content", "theme", "publishconf.py"):
        if not (project / required).exists():
            parser.error(f"Missing {required} in project {project}")
    args.project = project
    if args.command == "new":
        return _new_content(args, parser)
    if args.command == "validate":
        return _validate_content(project)
    if args.command == "dev":
        if not (project / "devconf.py").is_file():
            parser.error(f"Missing devconf.py in project {project}")
        if not 1 <= args.port <= 65535:
            parser.error("Port must be between 1 and 65535")
        return _preview(project, args.port)
    output = getattr(args, "output", None) or Path("../pelican-output")
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
