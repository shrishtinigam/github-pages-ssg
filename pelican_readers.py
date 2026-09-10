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
        metadata = self._normalize_metadata(source_path, post.metadata)
        self._validate_metadata(source_path, metadata)
        metadata = self._process_dates_and_defaults(source_path, metadata)
        metadata = self._set_routes_and_template(source_path, metadata)
        metadata = {name: self.process_metadata(name, value) for name, value in metadata.items()}
        renderer = markdown.Markdown(**self.settings["MARKDOWN"])
        return renderer.convert(post.content), metadata

    def _normalize_metadata(self, source_path, raw_metadata):
        """Normalize metadata names and infer the collection from the path."""
        metadata = {str(key).strip().lower().replace(" ", "_"): value for key, value in raw_metadata.items()}
        relative = Path(source_path).relative_to(Path(self.settings["PATH"]))
        if relative.parts:
            metadata.setdefault("category", relative.parts[0])
        return metadata

    def _validate_metadata(self, source_path, metadata):
        """Validate fields shared by pages, posts, and projects."""
        for field in ("title", "slug"):
            if not isinstance(metadata.get(field), str) or not metadata[field].strip():
                self._fail(source_path, f"{field.title()} must be a nonempty string")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", metadata["slug"]):
            self._fail(source_path, "Slug must contain lowercase letters, numbers, and hyphens only")
        if metadata.get("category") not in ("pages", "posts", "projects"):
            self._fail(source_path, "Category must be pages, posts, or projects")
        for field in ("summary", "skills", "image", "duration", "project_type", "link", "template"):
            if field in metadata and not isinstance(metadata[field], str):
                self._fail(source_path, f"{field} must be a string")
        if "tags" in metadata:
            tags = metadata["tags"]
            if not isinstance(tags, (str, list)) or (isinstance(tags, list) and
                    any(not isinstance(tag, str) or not tag.strip() for tag in tags)):
                self._fail(source_path, "Tags must be a string or a list of nonempty strings")
        if "order" in metadata:
            try:
                if isinstance(metadata["order"], (bool, float)):
                    raise ValueError
                metadata["order"] = int(metadata["order"])
            except (ValueError, TypeError):
                self._fail(source_path, "Order must be an integer")
        if metadata["category"] == "posts" and not metadata.get("date"):
            self._fail(source_path, "Date is required for posts")

    def _process_dates_and_defaults(self, source_path, metadata):
        """Apply Pelican's date types and defaults required by the templates."""
        if isinstance(metadata.get("tags"), list):
            metadata["tags"] = ", ".join(metadata["tags"])
        if metadata["category"] == "projects":
            metadata.setdefault("date", "2000-01-01")
        for field in ("date", "updated"):
            if field not in metadata:
                continue
            try:
                parsed = self.process_metadata("date", str(metadata[field]))
                metadata[field] = str(metadata[field]) if field == "date" else parsed.strftime("%b %d, %Y")
            except (ValueError, TypeError, AttributeError) as exc:
                self._fail(source_path, f"{field.title()} is invalid: {exc}")
        return metadata

    @staticmethod
    def _set_routes_and_template(source_path, metadata):
        """Set collection-specific URLs and the default template."""
        if metadata.get("category") == "projects":
            slug = metadata.get("slug", Path(source_path).stem)
            metadata["url"] = f"projects/{slug}/"
            metadata["save_as"] = f"projects/{slug}/index.html"
        metadata.setdefault("template", "page" if metadata.get("category") == "pages" else ("project" if metadata.get("category") == "projects" else "article"))
        return metadata

    @staticmethod
    def _fail(source_path, message):
        """Raise a validation error that identifies the source document."""
        raise ValueError(f"{source_path}: {message}")
