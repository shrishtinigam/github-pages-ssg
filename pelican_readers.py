"""Read and validate the portfolio's YAML-front-matter Markdown documents."""

from pathlib import Path
import re

import frontmatter
import markdown
from pelican.readers import MarkdownReader


class FrontmatterMarkdownReader(MarkdownReader):
    """Pelican Markdown reader supporting the site's YAML front matter."""

    file_extensions = ["md", "markdown", "mkd", "mdown"]

    def read(self, source_path):
        """Return rendered HTML and validated metadata, with source-aware errors."""
        post = frontmatter.load(source_path)
        metadata = {str(key).strip().lower().replace(" ", "_"): value for key, value in post.metadata.items()}
        relative = Path(source_path).relative_to(Path(self.settings["PATH"]))
        if relative.parts:
            metadata.setdefault("category", relative.parts[0])
        def fail(message):
            """Identify the source file in every metadata validation error."""
            raise ValueError(f"{source_path}: {message}")

        for field in ("title", "slug"):
            if not isinstance(metadata.get(field), str) or not metadata[field].strip():
                fail(f"{field.title()} must be a nonempty string")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", metadata["slug"]):
            fail("Slug must contain lowercase letters, numbers, and hyphens only")
        if metadata["category"] not in ("pages", "posts", "projects"):
            fail("Category must be pages, posts, or projects")
        for field in ("summary", "skills", "image", "duration", "project_type", "link", "template"):
            if field in metadata and not isinstance(metadata[field], str):
                fail(f"{field} must be a string")
        if "tags" in metadata:
            tags = metadata["tags"]
            if not isinstance(tags, (str, list)) or (isinstance(tags, list) and
                    any(not isinstance(tag, str) or not tag.strip() for tag in tags)):
                fail("Tags must be a string or a list of nonempty strings")
        if "order" in metadata:
            try:
                if isinstance(metadata["order"], (bool, float)):
                    raise ValueError
                metadata["order"] = int(metadata["order"])
            except (ValueError, TypeError):
                fail("Order must be an integer")
        if metadata["category"] == "posts" and not metadata.get("date"):
            fail("Date is required for posts")
        if isinstance(metadata.get("tags"), list):
            metadata["tags"] = ", ".join(str(tag) for tag in metadata["tags"])
        # Undated projects need a Pelican article date, but it is never displayed.
        if metadata["category"] == "projects":
            metadata.setdefault("date", "2000-01-01")
        for field in ("date", "updated"):
            if field in metadata:
                try:
                    parsed = self.process_metadata("date", str(metadata[field]))
                    metadata[field] = str(metadata[field]) if field == "date" else parsed.strftime("%b %d, %Y")
                except (ValueError, TypeError, AttributeError) as exc:
                    fail(f"{field.title()} is invalid: {exc}")
        if metadata.get("category") == "projects":
            slug = metadata.get("slug", Path(source_path).stem)
            metadata["url"] = f"projects/{slug}/"
            metadata["save_as"] = f"projects/{slug}/index.html"
        metadata.setdefault("template", "page" if metadata.get("category") == "pages" else ("project" if metadata.get("category") == "projects" else "article"))
        self._md = markdown.Markdown(**self.settings["MARKDOWN"])
        metadata = {name: self.process_metadata(name, value) for name, value in metadata.items()}
        return self._md.convert(post.content), metadata
