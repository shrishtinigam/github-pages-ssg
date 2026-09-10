from pathlib import Path
import subprocess
import tempfile
import unittest


class PelicanBuildTest(unittest.TestCase):
    def test_expected_routes_and_content_are_generated(self):
        root = Path(__file__).parents[1]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            subprocess.run(
                [str(root / ".venv/bin/pelican"), "content", "-s", "publishconf.py", "-o", str(output), "-t", "theme"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue((output / "index.html").exists())
            self.assertTrue((output / "about/index.html").exists())
            self.assertTrue((output / "posts/semantic-versioning-p1/index.html").exists())
            self.assertTrue((output / "projects/microservices-based-web-app/index.html").exists())
            self.assertFalse((output / "posts/semantic-versioning/index.html").exists())
            homepage = (output / "index.html").read_text(encoding="utf-8")
            self.assertIn("Ticket House", homepage)
            self.assertIn("Node.js", homepage)


if __name__ == "__main__":
    unittest.main()
