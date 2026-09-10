"""Keep Make's development shortcuts equivalent to the supported CLI."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class EntrypointTest(unittest.TestCase):
    """Exercise real builds and output protection through both interfaces."""

    def test_make_and_cli_build_same_site(self):
        """Generate identical HTML/CSS and reject existing unrelated output."""
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix="portfolio-entrypoints-") as directory:
            cli_output = Path(directory) / "cli"
            make_output = Path(directory) / "make"
            cli = [sys.executable, "-m", "portfolio_cli", "build", "--output", str(cli_output)]
            make = ["make", "build", f"PYTHON={sys.executable}", f"OUTPUT={make_output}"]
            for command in (cli, make):
                result = subprocess.run(command, cwd=root, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            files = [p.relative_to(cli_output) for p in cli_output.rglob("*")
                     if p.suffix in (".html", ".css")]
            self.assertTrue(files)
            for path in files:
                self.assertEqual((cli_output / path).read_bytes(), (make_output / path).read_bytes(), str(path))
            for command, output in ((cli, cli_output), (make, make_output)):
                sentinel = output / "keep.txt"
                sentinel.write_text("user file")
                result = subprocess.run(command, cwd=root, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(sentinel.read_text(), "user file")
            checked = subprocess.run([sys.executable, "-m", "portfolio_cli", "check"],
                                     cwd=root, capture_output=True, text=True)
            self.assertEqual(checked.returncode, 0, checked.stderr)
