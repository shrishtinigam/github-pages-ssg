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


# ---------- SQL QUERIES ----------
class Queries:
    INSERT_POST = """
        INSERT INTO posts (slug, title, body_md, summary)
        VALUES (?, ?, ?, ?)
    """

    UPDATE_POST = """
        UPDATE posts
        SET title = ?, body_md = ?, summary = ?, updated_at = CURRENT_TIMESTAMP
        WHERE slug = ?
    """

    ARCHIVE_POST = """
        INSERT INTO deleted_posts 
            (id, slug, title, summary, body_md, created_at, updated_at, deleted_at)
        SELECT id, slug, title, summary, body_md, created_at, updated_at, ?
        FROM posts
        WHERE slug = ?
    """

    DELETE_POST = "DELETE FROM posts WHERE slug = ?"
    CHECK_POST_EXISTS = "SELECT 1 FROM posts WHERE slug = ?"
    FETCH_POST = "SELECT * FROM posts WHERE slug = ?"
    FETCH_ALL_POSTS = "SELECT * FROM posts ORDER BY created_at DESC"


# ---------- Connection ----------
def get_connection() -> sqlite3.Connection:
    """
    Return a new SQLite connection.
    """
    return sqlite3.connect(DB_PATH)


# ---------- Create Tables ----------
def create_tables() -> None:
    """
    Run posts.sql to ensure all tables exist.
    """
    schema_path = SCHEMA_PATH / "posts" / "posts.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")
    schema_sql = Template(schema_sql).render(datetime_format=DATETIME_FORMAT)

    with get_connection() as con:
        con.executescript(schema_sql)
        con.commit()


# ---------- CRUD Operations ----------
def insert_post(
    slug: str, title: str, body_md: str, summary: Optional[str] = None
) -> None:
    """
    Insert a new post into the posts table.

    :param slug: Unique slug for the post.
    :param title: Title of the post.
    :param body_md: Markdown content of the post.
    :param summary: Optional summary of the post.
    """
    try:
        with get_connection() as con:
            con.execute(Queries.INSERT_POST, (slug, title, body_md, summary))
            con.commit()
    except sqlite3.IntegrityError:
        logger.info(f"Error: A post with slug '{slug}' already exists.")
    except Exception as e:
        logger.info(f"Error inserting post '{slug}': {e}")


def update_post(
    slug: str, title: str, body_md: str, summary: Optional[str] = None
) -> None:
    """
    Update an existing post by slug.

    :param slug: Unique slug for the post.
    :param title: New title of the post.
    :param body_md: New markdown content of the post.
    :param summary: Optional new summary of the post.
    """
    try:
        with get_connection() as con:
            con.execute(Queries.UPDATE_POST, (title, body_md, summary, slug))
            con.commit()
    except Exception as e:
        logger.info(f"Error updating post '{slug}': {e}")


def archive_post(slug: str, deleted_at: Optional[str] = None) -> None:
    """
    Move a post from posts to deleted_posts by slug.

    :param slug: Unique slug for the post.
    :param deleted_at: Optional deletion timestamp. If None, uses current time.
    """
    if deleted_at is None:
        deleted_at = datetime.now().strftime(DATETIME_FORMAT)

    try:
        with get_connection() as con:
            con.execute(Queries.ARCHIVE_POST, (deleted_at, slug))
            con.execute(Queries.DELETE_POST, (slug,))
            con.commit()
    except Exception as e:
        logger.info(f"Error archiving post '{slug}': {e}")


# ---------- Select ----------
def post_exists(slug: str) -> bool:
    """
    Check if a post exists by slug.

    :param slug: The slug of the post to check.
    :return: True if the post exists, False otherwise.
    """
    with get_connection() as con:
        cur = con.execute(Queries.CHECK_POST_EXISTS, (slug,))
        return cur.fetchone() is not None


def fetch_post(slug: str) -> Optional[Tuple]:
    """
    Fetch a single post by slug.

    :param slug: The slug of the post to fetch.
    :return: A tuple representing the post, or None if not found.
    """
    with get_connection() as con:
        cur = con.execute(Queries.FETCH_POST, (slug,))
        return cur.fetchone()


def fetch_all_posts() -> List[Tuple]:
    """
    Fetch all posts ordered by creation date descending.

    :return: A list of tuples, each representing a post.
    """
    with get_connection() as con:
        cur = con.execute(Queries.FETCH_ALL_POSTS)
        return cur.fetchall()
