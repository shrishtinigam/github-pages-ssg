"""Verify the everyday CLI on Windows and Unix, without Make or a live site."""

from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]


def checkout(target):
    for directory in ("content", "theme", "content-templates"):
        shutil.copytree(ROOT / directory, target / directory)
    for filename in ("pelicanconf.py", "publishconf.py", "devconf.py"):
        shutil.copy2(ROOT / filename, target / filename)


def cli(*args, cwd=ROOT):
    return subprocess.run([sys.executable, "-m", "portfolio_cli", *map(str, args)],
                          cwd=cwd, capture_output=True, text=True, encoding="utf-8")


class WorkflowTest(unittest.TestCase):
    def test_cli_protects_existing_output_and_source(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "site"
            result = cli("build", "--output", output)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            sentinel = output / "keep.txt"
            sentinel.write_text("user data", encoding="utf-8")
            self.assertNotEqual(cli("build", "--output", output).returncode, 0)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "user data")
            self.assertNotEqual(cli("build", "--output", ROOT / "content").returncode, 0)
            self.assertNotEqual(cli("build", "--output", ROOT.parent).returncode, 0)
            self.assertNotEqual(cli("check", "--output", output).returncode, 0)

    def test_new_content_builds_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project with spaces"
            project.mkdir()
            checkout(project)
            for kind in ("post", "project"):
                result = cli("new", kind, 'A title: "quoted"', "--slug", f"new-{kind}", "--project", project)
                self.assertEqual(result.returncode, 0, result.stderr)
            source = project / "content/posts/new-post.md"
            original = source.read_bytes()
            self.assertNotEqual(cli("new", "post", "Other", "--slug", "new-post", "--project", project).returncode, 0)
            self.assertEqual(source.read_bytes(), original)
            self.assertNotEqual(cli("new", "post", "Other", "--slug", "../escape", "--project", project).returncode, 0)
            result = cli("check", "--project", project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_preview_serves_locally_and_rebuilds_markdown_and_theme(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            project.mkdir()
            checkout(project)
            with socket.socket() as sock:
                sock.bind(("127.0.0.1", 0))
                port = sock.getsockname()[1]
            with (Path(directory) / "preview.log").open("w+", encoding="utf-8") as log:
                process = subprocess.Popen([sys.executable, "-m", "portfolio_cli", "dev", "--port", str(port),
                                            "--project", str(project)], cwd=ROOT, stdout=log, stderr=log)
                def wait_for(path, expected):
                    deadline = time.monotonic() + 25
                    while time.monotonic() < deadline:
                        try:
                            with urlopen(f"http://127.0.0.1:{port}{path}", timeout=1) as response:
                                body = response.read().decode("utf-8")
                                if expected in body:
                                    return body
                        except (URLError, TimeoutError, ConnectionError):
                            pass
                        if process.poll() is not None:
                            break
                        time.sleep(.25)
                    log.flush()
                    self.fail(f"Preview did not serve {path} with {expected!r}:\n" + (Path(directory) / "preview.log").read_text(encoding="utf-8"))
                try:
                    homepage = wait_for("/", f"http://127.0.0.1:{port}/projects")
                    self.assertNotIn('href="https://shrishtinigam.github.io', homepage)
                    wait_for("/static/css/style.css", "body")
                    # Let Pelican's initial watcher attach, then edit only the fixture.
                    time.sleep(1)
                    about = project / "content/pages/about.md"
                    about.write_text(about.read_text(encoding="utf-8") + "\n\nPreview rebuild marker.\n", encoding="utf-8")
                    wait_for("/about/", "Preview rebuild marker.")
                    template = project / "theme/templates/index.html"
                    template.write_text(template.read_text(encoding="utf-8").replace("Hi, I'm", "Theme rebuild marker"), encoding="utf-8")
                    wait_for("/", "Theme rebuild marker")
                finally:
                    process.terminate()
                    process.wait(timeout=10)

    def test_bad_preview_port_is_rejected(self):
        self.assertNotEqual(cli("dev", "--port", "0").returncode, 0)


if __name__ == "__main__":
    unittest.main()
