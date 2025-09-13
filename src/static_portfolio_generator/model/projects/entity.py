"""
Project entity for managing projects in a static portfolio generator.
Handles adding new projects, rewriting all projects, and deleting projects from the database.
"""

from pathlib import Path
import re
from static_portfolio_generator.controller.config import CONTENT_PROJECTS
from static_portfolio_generator.model.projects.db_utils import (
    insert_project,
    project_exists,
    archive_project,
)
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


class Project:
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
    def _parse_markdown(cls, file_path: Path):
        """
        Extract slug, title, project_type, summary, duration, skills,
        and description from a markdown file.

        - The **first line** is used as the *project title*.
        - The **second line**, if present, is used as the *project type*.
        - The **third line**, if present, is used as the *summary*.
        - The **fourth line** is *duration*, fifth line is *skills*.
        - The **remainder** of the markdown file is treated as the *description*.

        :param file_path: Path to the markdown file.
        :return: Tuple of (slug, title, project_type, summary, duration, skills, description_md)
        """
        slug = cls._slugify(file_path.name)
        body_md = file_path.read_text(encoding="utf-8").strip()
        lines = body_md.splitlines()

        if not lines:
            raise ValueError(f"{file_path} is empty")

        title = lines[0].lstrip("#").strip()
        project_type = (
            lines[1].strip()
            if len(lines) > 1 and lines[1].strip()
            else "Personal Project"
        )
        summary = lines[2].strip() if len(lines) > 2 and lines[2].strip() else ""
        duration = lines[3].strip() if len(lines) > 3 and lines[3].strip() else ""
        skills = lines[4].strip() if len(lines) > 4 and lines[4].strip() else ""
        description_md = "\n".join(lines[5:]).strip() if len(lines) > 5 else ""

        return slug, title, project_type, summary, duration, skills, description_md

    # ---------- Class-level Helpers ---------- #
    def add_new_projects(self):
        """Add projects that do not exist in the database."""
        for file in CONTENT_PROJECTS.glob("*.md"):
            try:
                slug, title, project_type, summary, duration, skills, description_md = (
                    self._parse_markdown(file)
                )
            except ValueError as e:
                logger.info(f"[SKIP] {e}")
                continue

            insert_project(
                slug, title, project_type, summary, duration, skills, description_md
            )

    def rewrite_all_projects(self):
        """
        Archive all existing projects to deleted_projects table.
        Then re-add all projects from CONTENT_PROJECTS.
        """
        for file in CONTENT_PROJECTS.glob("*.md"):
            try:
                slug, title, project_type, summary, duration, skills, description_md = (
                    self._parse_markdown(file)
                )
            except ValueError as e:
                logger.info(f"[SKIP] {e}")
                continue

            if project_exists(slug):
                logger.info(f"[REWRITE] Archiving existing project: {slug}")
                archive_project(slug)
            logger.info(f"[INSERT] Adding project: {slug}")
            insert_project(
                slug, title, project_type, summary, duration, skills, description_md
            )

    def delete_project(self, slug: str) -> None:
        """
        Move a project from projects table to deleted_projects table.

        :param slug: The slug of the project to delete.
        """
        if not project_exists(slug):
            logger.info(f"No project found with slug '{slug}'")
            return

        archive_project(slug)
        logger.info(f"Project '{slug}' moved to deleted_projects.")
