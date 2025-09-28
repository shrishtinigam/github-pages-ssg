import sqlite3
from jinja2 import Template
from typing import Optional, Tuple, List
from datetime import datetime
from static_portfolio_generator.model.posts.post import PostData
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
    """
    SQL query definitions for interacting with the `posts` table.
    """

    INSERT_POST = """
        INSERT INTO posts (slug, title, summary, body_md, author, created_at, thumbnail_url, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    UPDATE_POST = """
        UPDATE posts
        SET title = ?, summary = ?, body_md = ?, updated_at = ?,
            thumbnail_url = ?, tags = ?
        WHERE slug = ?
    """

    DELETE_POST = "DELETE FROM posts WHERE slug = ?"
    CHECK_POST_EXISTS = "SELECT 1 FROM posts WHERE slug = ?"
    FETCH_POST = "SELECT * FROM posts WHERE slug = ?"
    FETCH_ALL_POSTS = "SELECT * FROM posts ORDER BY created_at DESC"
    FETCH_POSTS_BY_TAGS = """
    SELECT *
    FROM posts
    WHERE tags IS NOT NULL
      AND (
        -- Each tag must match exactly or as part of a comma-separated list
        {} 
      )
    ORDER BY created_at DESC
"""



# ---------- Connection ----------
def get_connection() -> sqlite3.Connection:
    """
    Return a new SQLite connection to the configured database path.
    """
    return sqlite3.connect(DB_PATH)


# ---------- Create Tables ----------
def create_tables() -> None:
    """
    Execute the schema SQL file to ensure the `posts` table exists.
    Renders Jinja2 template with the configured datetime format.
    """
    schema_path = SCHEMA_PATH / "posts" / "posts.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")
    schema_sql = Template(schema_sql).render(datetime_format=DATETIME_FORMAT)

    with get_connection() as con:
        con.executescript(schema_sql)
        con.commit()


# ---------- CRUD Operations ----------
def insert_post(post: PostData) -> None:
    """
    Insert a new post into the posts table.

    :param slug: Unique slug for the post.
    :param title: Title of the post.
    :param body_md: Markdown content of the post.
    :param summary: Optional short summary of the post.
    :param author: Name of the post author (defaults to 'Meher').
    :param created_at: Optional created date string; if None, uses current datetime.
    :param thumbnail_url: Optional URL/path to a thumbnail image.
    :param tags: Optional comma-separated list of tags.
    """
    try:
        with get_connection() as con:
            con.execute(
                Queries.INSERT_POST,
                (
                    post.slug,
                    post.title,
                    post.summary,
                    post.body_md,
                    post.author,
                    post.created_at,
                    post.thumbnail_url,
                    post.tags,
                ),
            )
            con.commit()
            logger.info(f"[INSERT] Added post: {post.slug}")
    except sqlite3.IntegrityError:
        logger.info(f"Error: A post with slug '{post.slug}' already exists.")
    except Exception as e:
        logger.info(f"Error inserting post '{post.slug}': {e}")


def update_post(post: PostData) -> None:
    """
    Update an existing post by slug.

    :param slug: Unique slug for the post.
    :param title: New title of the post.
    :param body_md: Updated markdown content.
    :param summary: Optional updated summary of the post.
    :param thumbnail_url: Optional updated thumbnail URL.
    :param tags: Optional updated tags string.
    """
    updated_at = datetime.now().strftime(DATETIME_FORMAT)
    try:
        with get_connection() as con:
            con.execute(
                Queries.UPDATE_POST,
                (
                    post.title,
                    post.summary,
                    post.body_md,
                    updated_at,
                    post.thumbnail_url,
                    post.tags,
                    post.slug,
                ),
            )
            con.commit()
            logger.info(f"[UPDATE] Updated post: {post.slug}")
    except Exception as e:
        logger.info(f"Error updating post '{post.slug}': {e}")


def delete_post(slug: str) -> None:
    """
    Permanently delete a post by slug.

    :param slug: Unique slug for the post.
    """
    try:
        with get_connection() as con:
            con.execute(Queries.DELETE_POST, (slug,))
            con.commit()
            logger.info(f"Post '{slug}' was deleted from database.")
    except Exception as e:
        logger.info(f"Error deleting post '{slug}': {e}")


# ---------- Select ----------
def post_exists(slug: str) -> bool:
    """
    Check if a post exists in the database by slug.

    :param slug: The slug of the post to check.
    :return: True if the post exists, False otherwise.
    """
    with get_connection() as con:
        cur = con.execute(Queries.CHECK_POST_EXISTS, (slug,))
        return cur.fetchone() is not None


def fetch_post(slug: str) -> Optional[Tuple]:
    """
    Fetch a single post by slug.

    :param slug: The slug of the post.
    :return: A tuple representing the post, or None if not found.
    """
    with get_connection() as con:
        cur = con.execute(Queries.FETCH_POST, (slug,))
        return cur.fetchone()


def fetch_all_posts() -> List[Tuple]:
    """
    Fetch all posts ordered by creation date (descending).

    :return: A list of tuples, each representing a post row.
    """
    with get_connection() as con:
        cur = con.execute(Queries.FETCH_ALL_POSTS)
        return cur.fetchall()

def fetch_posts_by_tags(tags: List[str]) -> List[Tuple]:
    """
    Fetch all posts that match any of the given tags.
    
    :param tags: List of tags to filter by.
    :return: A list of tuples representing the posts that match any of the tags.
    """
    if not tags:
        return []

    # Build the dynamic WHERE clause: tags LIKE ? OR tags LIKE ? ...
    where_clause = " OR ".join(["tags LIKE ?" for _ in tags])
    sql = Queries.FETCH_POSTS_BY_TAGS.format(where_clause)

    # Prepare the parameters: wrap each tag with wildcards for partial match
    params = [f"%{tag}%" for tag in tags]

    try:
        with get_connection() as con:
            cur = con.execute(sql, params)
            return cur.fetchall()
    except Exception as e:
        logger.info(f"Error fetching posts by tags {tags}: {e}")
        return []
