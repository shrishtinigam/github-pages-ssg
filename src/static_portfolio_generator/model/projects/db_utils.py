"""
Database utilities for managing projects in a static portfolio generator.
Provides CRUD operations and archive functionality.
"""

import sqlite3
from jinja2 import Template
from typing import Optional, Tuple, List
from datetime import datetime
from static_portfolio_generator.controller.config import (
    SCHEMA_PATH,
    DB_PATH,
    DATETIME_FORMAT,
)
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# ---------- SQL QUERIES ---------- #
class Queries:
    INSERT_PROJECT = """
        INSERT INTO projects
        (slug, title, project_type, summary, duration, skills, description_md)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    UPDATE_PROJECT = """
        UPDATE projects
        SET title = ?, project_type = ?, summary = ?, duration = ?, skills = ?, description_md = ?, updated_at = CURRENT_TIMESTAMP
        WHERE slug = ?
    """

    ARCHIVE_PROJECT = """
        INSERT INTO deleted_projects
        (id, slug, title, project_type, summary, duration, skills, description_md, created_at, updated_at, deleted_at)
        SELECT id, slug, title, project_type, summary, duration, skills, description_md, created_at, updated_at, ?
        FROM projects
        WHERE slug = ?
    """

    DELETE_PROJECT = "DELETE FROM projects WHERE slug = ?"
    CHECK_PROJECT_EXISTS = "SELECT 1 FROM projects WHERE slug = ?"
    FETCH_PROJECT = "SELECT * FROM projects WHERE slug = ?"
    FETCH_ALL_PROJECTS = "SELECT * FROM projects ORDER BY created_at DESC"


# ---------- Connection ---------- #
def get_connection() -> sqlite3.Connection:
    """
    Return a new SQLite connection.
    """
    return sqlite3.connect(DB_PATH)


# ---------- Create Tables ---------- #
def create_tables() -> None:
    """
    Run projects.sql to ensure projects and deleted_projects tables exist.
    """
    schema_path = SCHEMA_PATH / "projects" / "projects.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")
    schema_sql = Template(schema_sql).render(datetime_format=DATETIME_FORMAT)

    with get_connection() as con:
        con.executescript(schema_sql)
        con.commit()


# ---------- CRUD Operations ---------- #
def insert_project(
    slug: str,
    title: str,
    project_type: str = "Personal Project",
    summary: Optional[str] = None,
    duration: Optional[str] = None,
    skills: Optional[str] = None,
    description_md: str = "",
) -> None:
    """
    Insert a new project into the projects table.

    :param slug: Unique slug for the project.
    :param title: Project title.
    :param project_type: Type of project.
    :param summary: Optional summary.
    :param duration: Optional duration.
    :param skills: Optional skills string.
    :param description_md: Markdown description.
    """
    try:
        with get_connection() as con:
            con.execute(
                Queries.INSERT_PROJECT,
                (slug, title, project_type, summary, duration, skills, description_md),
            )
            con.commit()
            logger.info(f"Project '{slug}' inserted successfully.")
    except sqlite3.IntegrityError:
        logger.info(f"Project with slug '{slug}' already exists.")
    except Exception as e:
        logger.info(f"Error inserting project '{slug}': {e}")


def update_project(
    slug: str,
    title: str,
    project_type: str,
    summary: Optional[str] = None,
    duration: Optional[str] = None,
    skills: Optional[str] = None,
    description_md: str = "",
) -> None:
    """
    Update an existing project by slug.
    """
    try:
        with get_connection() as con:
            con.execute(
                Queries.UPDATE_PROJECT,
                (title, project_type, summary, duration, skills, description_md, slug),
            )
            con.commit()
            logger.info(f"Project '{slug}' updated successfully.")
    except Exception as e:
        logger.info(f"Error updating project '{slug}': {e}")


def archive_project(slug: str, deleted_at: Optional[str] = None) -> None:
    """
    Move a project from projects to deleted_projects by slug.

    :param slug: Unique slug for the project.
    :param deleted_at: Optional deletion timestamp. Uses current time if None.
    """
    if deleted_at is None:
        deleted_at = datetime.now().strftime(DATETIME_FORMAT)

    try:
        with get_connection() as con:
            con.execute(Queries.ARCHIVE_PROJECT, (deleted_at, slug))
            con.execute(Queries.DELETE_PROJECT, (slug,))
            con.commit()
            logger.info(f"Project '{slug}' archived successfully.")
    except Exception as e:
        logger.info(f"Error archiving project '{slug}': {e}")


# ---------- Select ---------- #
def project_exists(slug: str) -> bool:
    """
    Check if a project exists by slug.

    :param slug: The slug to check.
    :return: True if exists, False otherwise.
    """
    with get_connection() as con:
        cur = con.execute(Queries.CHECK_PROJECT_EXISTS, (slug,))
        return cur.fetchone() is not None


def fetch_project(slug: str) -> Optional[Tuple]:
    """
    Fetch a single project by slug.

    :param slug: The slug to fetch.
    :return: Tuple representing the project or None.
    """
    with get_connection() as con:
        cur = con.execute(Queries.FETCH_PROJECT, (slug,))
        return cur.fetchone()


def fetch_all_projects() -> List[Tuple]:
    """
    Fetch all projects ordered by creation date descending.

    :return: List of tuples representing projects.
    """
    with get_connection() as con:
        cur = con.execute(Queries.FETCH_ALL_PROJECTS)
        return cur.fetchall()
