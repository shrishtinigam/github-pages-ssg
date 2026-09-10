"""Build the complete portfolio and assert its essential public routes."""

from pathlib import Path
import subprocess
import json
import re
import sys
import tempfile
import unittest


class PelicanBuildTest(unittest.TestCase):
    """Smoke-test the real Pelican build in isolated output storage."""

    def test_expected_routes_and_content_are_generated(self):
        """Keep the original collections and exclude the unwanted fourth post."""
        root = Path(__file__).parents[1]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            subprocess.run(
                [sys.executable, "-m", "pelican", "content", "-s", "publishconf.py", "-o", str(output), "-t", "theme", "--fatal", "warnings"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            )
            expected_routes = [
                "index.html",
                "about/index.html",
                "posts/index.html",
                "posts/semantic-versioning-p1/index.html",
                "posts/semantic-versioning-p2/index.html",
                "posts/semantic-versioning-p3/index.html",
                "projects/index.html",
                "projects/microservices-based-web-app/index.html",
                "projects/pathfinding-algorithms-visualizer/index.html",
                "projects/dyslexic-char-recognition/index.html",
                "projects/chronic-kidney-disease-pred/index.html",
                "projects/mner-xlm-roberta/index.html",
            ]
            for route in expected_routes:
                self.assertTrue((output / route).exists(), route)
            self.assertFalse((output / "posts/semantic-versioning/index.html").exists())
            homepage = (output / "index.html").read_text(encoding="utf-8")
            self.assertIn("Microservices Based E-Commerce Web App", homepage)
            self.assertIn("Node.js", homepage)
            self.assertIn("Get Semantic Versioning Right in Your Python Library - Part 3", homepage)
            self.assertIn("Pathfinding Algorithms Visualizers (SFML)", homepage)
            post = (output / "posts/semantic-versioning-p1/index.html").read_text()
            for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', post, re.S):
                data = json.loads(block)
                if data.get("@type") == "BlogPosting":
                    self.assertEqual(data["keywords"], "python, software versioning, pep standards")


if __name__ == "__main__":
    unittest.main()
