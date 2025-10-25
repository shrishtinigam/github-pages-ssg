"""
Post entity for managing blog posts in a static portfolio generator.
Handles adding new posts, rewriting all posts, and deleting posts from the database.
"""


from typing import Optional
from pathlib import Path
import re
import logging
from datetime import datetime

from static_portfolio_generator.model.posts.db_utils import (
    insert_post,
    delete_post,
    update_post,
    post_exists,
)

from static_portfolio_generator.controller.config import CONTENT_POSTS, DATETIME_FORMAT
from static_portfolio_generator.model.posts.post import PostData

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
    def _parse_markdown(cls, file_path: Path) -> PostData:
        """
        Extract slug, title, body, and optional metadata from a markdown file.

        Expected markdown format:
        1. **First line**: post title (required)
        2. **Second line**: created date in string format (required)
        3. **Third line**: summary (optional)
        4. **Fourth line**: thumbnail URL (optional)
        5. **Fifth line**: comma-separated list of tags (optional)
        6. **Remaining lines**: post body (required)

        :param file_path: Path to the markdown file.
        :return: PostData object.
        """
        slug = cls._slugify(file_path.name)
        content = file_path.read_text(encoding="utf-8").strip()
        lines = content.splitlines()

        if len(lines) < 6:
            raise ValueError(f"{file_path} must have at least 6 lines (title, date, summary, thumbnail, tags, body)")


        title = lines[0].lstrip("#").strip()
    
        # Validate created_at format
        created_at_str = lines[1].strip()
        try:
            datetime.strptime(created_at_str, DATETIME_FORMAT)
        except ValueError:
            raise ValueError(f"{file_path} has an invalid date format: {created_at_str}")
        created_at = created_at_str  # keep as string for SQL

        summary = lines[2].strip()
        thumbnail_url = lines[3].strip()
        tags = lines[4].strip()
        body_md = "\n".join(lines[5:]).strip()

        if not body_md:
            raise ValueError(f"{file_path} has empty body content")

        return PostData(
            slug=slug,
            title=title,
            body_md=body_md,
            created_at=created_at,
            summary=summary,
            thumbnail_url=thumbnail_url,
            tags=tags,
        )

    # ---------- Class-level Helpers ---------- #
    def add_new_posts(self):
        """
        Add posts that do not exist in the posts table.
        Reads from markdown files in the CONTENT_POSTS directory.
        """
        for file in CONTENT_POSTS.glob("*.md"):
            try:
                post_data = self._parse_markdown(file)
            except ValueError as e:
                logger.info(f"[SKIP] {e}")
                continue

            self._insert_post_if_new(post_data)

    def rewrite_all_posts(self):
        """
        Adds or updates all posts from markdown files.
        Ensures database is in sync with markdown source files.
        """
        for file in CONTENT_POSTS.glob("*.md"):
            try:
                post_data = self._parse_markdown(file)
            except ValueError as e:
                logger.info(f"[SKIP] {e}")
                continue

            if post_exists(post_data.slug):
                update_post(post_data)
            else:
                self._insert_post_if_new(post_data)


    def delete_post(self, slug: str) -> None:
        """
        Deletes a post by slug from the posts table.

        :param slug: The slug of the post to delete.
        """
        if not post_exists(slug):
            logger.info(f"No post found with slug '{slug}'")
            return

        delete_post(slug)
        

    def _insert_post_if_new(self, post_data: PostData):
        """
        Insert a post into the database if it does not already exist.
        :param post_data: PostData object containing post details.
        :return: True if inserted, False if skipped.
        """
        if post_exists(post_data.slug):
            logger.info(f"[SKIP] Post '{post_data.slug}' already exists.")
            return False

        insert_post(post_data)
        return True

