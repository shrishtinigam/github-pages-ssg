from pathlib import Path

import frontmatter
from pelican.readers import MarkdownReader


class FrontmatterMarkdownReader(MarkdownReader):
    """Pelican Markdown reader supporting the site's YAML front matter."""

    file_extensions = ["md", "markdown", "mkd", "mdown"]

    def read(self, source_path):
        post = frontmatter.load(source_path)
        metadata = {str(key).strip().lower().replace(" ", "_"): value for key, value in post.metadata.items()}
        relative = Path(source_path).relative_to(Path(self.settings["PATH"]))
        if relative.parts:
            metadata.setdefault("category", relative.parts[0])
        if isinstance(metadata.get("tags"), list):
            metadata["tags"] = ", ".join(str(tag) for tag in metadata["tags"])
        metadata.setdefault("date", "2000-01-01")
        if metadata.get("category") == "projects":
            slug = metadata.get("slug", Path(source_path).stem)
            metadata["url"] = f"projects/{slug}/"
            metadata["save_as"] = f"projects/{slug}/index.html"
        metadata.setdefault("template", "page" if metadata.get("category") == "pages" else ("project" if metadata.get("category") == "projects" else "article"))
        import markdown
        self._md = markdown.Markdown(**self.settings["MARKDOWN"])
        metadata = {name: self.process_metadata(name, value) for name, value in metadata.items()}
        return self._md.convert(post.content), metadata
