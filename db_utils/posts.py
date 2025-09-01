import sqlite3
from typing import Optional, Tuple, List
from datetime import datetime
from site_config import SCHEMA_PATH, DB_PATH

DB_PATH = DB_PATH / "site.db"

# ---------- Connection ----------
def get_connection() -> sqlite3.Connection:
    """Return a new SQLite connection."""
    return sqlite3.connect(DB_PATH)

# ---------- Create Tables ----------
def create_tables() -> None:
    """Run schema.sql to ensure all tables exist."""
    schema_path = SCHEMA_PATH / "posts.sql"
    with get_connection() as con:
        con.executescript(schema_path.read_text(encoding="utf-8"))
        con.commit()

# ---------- Insert ----------
def insert_post(slug: str, title: str, body_md: str, summary: Optional[str] = None) -> None:
    """Insert a new post into the posts table."""
    try:
        with get_connection() as con:
            con.execute(
                """
                INSERT INTO posts (slug, title, body_md, summary)
                VALUES (?, ?, ?, ?)
                """,
                (slug, title, body_md, summary),
            )
            con.commit()
    except sqlite3.IntegrityError:
        print(f"❌ Error: A post with slug '{slug}' already exists.")
    except Exception as e:
        print(f"❌ Error inserting post '{slug}': {e}")

def update_post(slug: str, title: str, body_md: str, summary: Optional[str] = None) -> None:
    """Update an existing post by slug."""
    try:
        with get_connection() as con:
            con.execute(
                """
                UPDATE posts
                SET title = ?, body_md = ?, summary = ?, updated_at = CURRENT_TIMESTAMP
                WHERE slug = ?
                """,
                (title, body_md, summary, slug),
            )
            con.commit()
    except Exception as e:
        print(f"❌ Error updating post '{slug}': {e}")

# ---------- Archive ----------
def archive_post(slug: str, deleted_at: Optional[str] = None) -> None:
    """
    Move a post from posts to deleted_posts by slug.
    Safely copies it before deleting from posts.
    Optional `deleted_at` allows overriding the deletion timestamp.
    """
    if deleted_at is None:
        # Use SQLite-compatible timestamp
        deleted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with get_connection() as con:
            con.execute(
                """
                INSERT INTO deleted_posts (id, slug, title, summary, body_md, created_at, updated_at, deleted_at)
                SELECT id, slug, title, summary, body_md, created_at, updated_at, ?
                FROM posts WHERE slug = ?
                """,
                (deleted_at, slug),
            )
            con.execute("DELETE FROM posts WHERE slug = ?", (slug,))
            con.commit()
    except Exception as e:
        print(f"❌ Error archiving post '{slug}': {e}")


# ---------- Select ----------
def post_exists(slug: str) -> bool:
    """Check if a post exists by slug."""
    with get_connection() as con:
        cur = con.execute("SELECT 1 FROM posts WHERE slug = ?", (slug,))
        return cur.fetchone() is not None


def fetch_post(slug: str) -> Optional[Tuple]:
    """Fetch a single post by slug."""
    with get_connection() as con:
        cur = con.execute("SELECT * FROM posts WHERE slug = ?", (slug,))
        return cur.fetchone()


def fetch_all_posts() -> List[Tuple]:
    """Fetch all posts ordered by creation date descending."""
    with get_connection() as con:
        cur = con.execute("SELECT * FROM posts ORDER BY created_at DESC")
        return cur.fetchall()
