"""Regression coverage for authoring errors and chronological collection order."""

from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

from pelican.settings import read_settings
from pelican_readers import FrontmatterMarkdownReader
from pelican_compat import _adapt


class ValidationTest(unittest.TestCase):
    """Exercise the reader with real Markdown files and Pelican settings."""

    def test_invalid_metadata_identifies_source(self):
        """Reject malformed fields instead of silently publishing incomplete pages."""
        cases = [
            ("Title: Example\nSlug: example", "Date"),
            ("Title: Example\nSlug: ../escape\nDate: 2025-01-01", "Slug"),
            ("Title: Example\nSlug: example\nDate: nonsense", "Date"),
            ("Title: Example\nSlug: example\nDate: 2025-01-01\nOrder: true", "Order"),
            ("Title: Example\nSlug: example\nDate: 2025-01-01\nTags: [3]", "Tags"),
            ("Slug: example\nDate: 2025-01-01", "Title"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "posts").mkdir()
            source = root / "posts/example.md"
            reader = FrontmatterMarkdownReader(read_settings(override={
                "PATH": str(root), "SITEURL": "https://example.com", "TIMEZONE": "UTC"}))
            for metadata, field in cases:
                with self.subTest(field=field):
                    source.write_text(f"---\n{metadata}\n---\nBody", encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, f"example.md:.*{field}"):
                        reader.read(str(source))

    def test_sorting_across_months_and_years(self):
        """Display formatting must never determine publication order."""
        articles = []
        for date in (datetime(2025, 9, 1), datetime(2026, 1, 1), datetime(2025, 12, 1)):
            articles.append(SimpleNamespace(
                date=date, metadata={}, title="Example", slug=str(date.year),
                content="body", category=SimpleNamespace(name="posts")))
        generator = SimpleNamespace(context={"articles": articles})
        _adapt(generator)
        self.assertEqual([item.date for item in generator.context["posts"]],
                         sorted([item.date for item in articles], reverse=True))
