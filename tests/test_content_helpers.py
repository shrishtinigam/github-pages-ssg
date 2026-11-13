"""Keep optional authoring helpers aligned with the existing reader/schema."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import frontmatter
from portfolio_cli import main
from test_workflow import ROOT, checkout, cli


class ContentHelpersTest(unittest.TestCase):
    def test_all_starters_use_existing_schema_and_build(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            project.mkdir()
            checkout(project)
            destinations = {"post": "posts/new-starter.md", "project": "projects/new-starter.md",
                            "page": "pages/about.md", "posts-index": "pages/posts.md",
                            "projects-index": "pages/projects.md"}
            for kind, destination in destinations.items():
                text = (project / "content-templates" / f"{kind}.md").read_text(encoding="utf-8")
                (project / "content" / destination).write_text(text, encoding="utf-8")
            result = cli("validate", "--project", project)
            self.assertEqual(result.returncode, 0, result.stderr)
            result = cli("check", "--project", project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            # Every commented metadata example must also be valid when enabled.
            for destination in destinations.values():
                source = project / "content" / destination
                prefix, metadata, body = source.read_text(encoding="utf-8").split("---", 2)
                metadata = "\n".join(line[2:] if line.startswith("# ") else line
                                     for line in metadata.split("\n"))
                source.write_text("---".join([prefix, metadata, body]), encoding="utf-8")
            result = cli("validate", "--project", project)
            self.assertEqual(result.returncode, 0, result.stderr)
            result = cli("check", "--project", project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_generator_uses_template_comments_order_and_optional_title_prompt(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            project.mkdir()
            checkout(project)
            template = project / "content-templates/project.md"
            template.write_text(template.read_text(encoding="utf-8") + "\nCustom starter body.\n", encoding="utf-8")
            with patch("sys.stdin.isatty", return_value=True), patch("builtins.input", return_value='Project: "quoted" # title') as prompt:
                self.assertEqual(main(["new", "project", "--project", str(project)]), 0)
                prompt.assert_called_once_with("Title: ")
            generated = project / "content/projects/project-quoted-title.md"
            text = generated.read_text(encoding="utf-8")
            self.assertIn("Custom starter body.", text)
            self.assertIn("# Page Title:", text)
            self.assertEqual(list(frontmatter.loads(text).metadata),
                             ["Title", "Slug", "Project Type", "Duration", "Summary", "Skills", "Image", "Order"])
            self.assertEqual(frontmatter.loads(text)["Title"], 'Project: "quoted" # title')
            self.assertIn("Skills: Python · SQL", text)
            self.assertEqual(cli("new", "page", "Another biography", "--project", project).returncode, 0)
            self.assertEqual(cli("validate", "--project", project).returncode, 0)

    def test_validation_reports_multiple_existing_reader_errors_without_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            project.mkdir()
            checkout(project)
            bad = {
                "posts/missing-date.md": "---\nTitle: Missing date\nSlug: missing-date\n---\nBody",
                "projects/bad-duration.md": "---\nTitle: Example\nSlug: example\nDuration: 2026\n---\nBody",
                "pages/broken-yaml.md": "---\nTitle: [bad\nSlug: bad\n---\nBody",
            }
            for name, text in bad.items():
                (project / "content" / name).write_text(text, encoding="utf-8")
            before = {p: p.read_bytes() for p in (project / "content").rglob("*.md")}
            result = cli("validate", "--project", project)
            self.assertEqual(result.returncode, 1)
            for name in bad:
                self.assertIn(Path(name).name, result.stderr)
            self.assertIn("Date", result.stderr)
            self.assertIn("duration", result.stderr)
            self.assertIn("CONTENT_GUIDE.md", result.stderr)
            self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_legacy_metadata_is_accepted_without_new_whitelist(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            project.mkdir()
            checkout(project)
            target = project / "content/projects/legacy-fields.md"
            target.write_text('---\nTitle: Legacy\nPage Title: Original title\nSlug: legacy-fields\n'
                              'Duration: "2026"\nSkills: Python · SQL\nOrder: "7"\n'
                              'Custom Legacy Field: retained\n---\nBody', encoding="utf-8")
            result = cli("validate", "--project", project)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_title_does_not_block_noninteractive_use(self):
        result = subprocess.run([sys.executable, "-m", "portfolio_cli", "new", "post"],
                                cwd=ROOT, input="", capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Supply a title", result.stderr)


if __name__ == "__main__":
    unittest.main()
