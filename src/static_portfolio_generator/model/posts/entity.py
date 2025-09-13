"""
Post entity for managing blog posts in a static portfolio generator.
Handles adding new posts, rewriting all posts, and deleting posts from the database.
"""

from static_portfolio_generator.controller.config import CONTENT_POSTS
from pathlib import Path
from static_portfolio_generator.model.posts.db_utils import (
    insert_post,
    archive_post,
    post_exists,
)
import re
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


class Post:
    # ---------- Utilities ---------- #
    @staticmethod
    def _slugify(filename: str) -> str:
        """
        Generate a URL-friendly slug from a filename.
        Converts to lowercase, replaces non-alphanumeric characters with
        hyphens, and collapses multiple hyphens.

        :param filename: The original filename.
        :return: A URL-friendly slug.
        """
        s = Path(filename).stem.lower()
        s = re.sub(r"[^a-z0-9-]", "-", s)
        s = re.sub(r"-+", "-", s)
        return s.strip("-")

    @classmethod
    def _parse_markdown(cls, file_path):
        """
        Extract slug, title, body, and optional summary from a markdown file.
        - The **first line** of the markdown file is used as the *post title*.
        - The **second line**, if present, is used as the *post summary*.
        - The **remainder** of the markdown file is treated as the *post body*.

        :param file_path: Path to the markdown file.
        :return: Tuple of (slug, title, body_md, summary)
        """
        slug = cls._slugify(file_path.name)
        body_md = file_path.read_text(encoding="utf-8").strip()
        lines = body_md.splitlines()

        if not lines:
            raise ValueError(f"{file_path} is empty")

        title = lines[0].lstrip("#").strip()
        summary = lines[1].strip() if len(lines) > 1 and lines[1].strip() else None

        # Drop title and summary from body lines
        body_lines = lines[1:] if not summary else lines[2:]
        body_md = "\n".join(body_lines).strip()

        return slug, title, body_md, summary

    # ---------- Class-level Helpers ---------- #
    def add_new_posts(self):
        """
        Add posts that do not exist in the posts table.
        Reads from markdown files in the CONTENT_POSTS.
        """
        for file in CONTENT_POSTS.glob("*.md"):
            try:
                slug, title, body_md, summary = self._parse_markdown(file)
            except ValueError as e:
                logger.info(f"[SKIP] {e}")
                continue

            insert_post(slug, title, body_md, summary)

    def rewrite_all_posts(self):
        """
        Archive all existing posts to deleted_posts table.
        Then re-add all posts to posts table.
        Reads from markdown files in the CONTENT_POSTS.
        """
        for file in CONTENT_POSTS.glob("*.md"):
            try:
                slug, title, body_md, summary = self._parse_markdown(file)
            except ValueError as e:
                logger.info(f"[SKIP] {e}")
                continue

            if post_exists(slug):
                logger.info(f"[REWRITE] Archiving existing post: {slug}")
                archive_post(slug)
            logger.info(f"[INSERT] Adding post: {slug}")
            insert_post(slug, title, body_md, summary)

    def delete_post(self, slug: str) -> None:
        """
        Moves a post from posts table to to deleted_posts table.
        :param slug: The slug of the post to delete.
        """
        if not post_exists(slug):
            logger.info(f"❌ No post found with slug '{slug}'")
            return

        archive_post(slug)
        logger.info(f"🗑️ Post '{slug}' moved to deleted_posts.")
