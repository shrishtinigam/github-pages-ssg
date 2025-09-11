import sqlite3
from datetime import datetime, timezone
from typing import Optional, Tuple, List
from static_portfolio_generator.controller.site_config import SCHEMA_PATH, DB_PATH

# Database path
DB_PATH = DB_PATH / "site.db"


# ---------- Connection ----------
def get_connection() -> sqlite3.Connection:
    """Return a new SQLite connection."""
    return sqlite3.connect(DB_PATH)


# ---------- Create Tables ----------
def create_tables() -> None:
    """Create projects and deleted_projects tables if they don't exist."""
    schema_path = SCHEMA_PATH / "projects.sql"
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as con:
        con.executescript(schema_path.read_text(encoding="utf-8"))
        con.commit()


# ---------- Insert ----------
def insert_project(
    slug: str,
    title: str,
    project_type: str = "Personal Project",
    summary: Optional[str] = None,
    duration: Optional[str] = None,
    skills: Optional[str] = None,
    description_md: str = "",
) -> None:
    """Insert a new project into the projects table."""
    try:
        with get_connection() as con:
            con.execute(
                """
                INSERT INTO projects (slug, title, project_type, summary, duration, skills, description_md)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (slug, title, project_type, summary, duration, skills, description_md),
            )
            con.commit()
    except sqlite3.IntegrityError:
        print(f"❌ Project with slug '{slug}' already exists.")


# ---------- Update ----------
def update_project(
    slug: str,
    title: str,
    project_type: str,
    summary: Optional[str] = None,
    duration: Optional[str] = None,
    skills: Optional[str] = None,
    description_md: str = "",
) -> None:
    """Update an existing project by slug."""
    with get_connection() as con:
        con.execute(
            """
            UPDATE projects
            SET title = ?, project_type = ?, summary = ?, duration = ?, skills = ?, description_md = ?, updated_at = CURRENT_TIMESTAMP
            WHERE slug = ?
            """,
            (title, project_type, summary, duration, skills, description_md, slug),
        )
        con.commit()


# ---------- Archive ----------
def archive_project(slug: str, deleted_at: Optional[str] = None) -> None:
    """
    Move a project from projects to deleted_projects by slug.
    Optional `deleted_at` allows overriding the deletion timestamp.
    """
    if deleted_at is None:
        deleted_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as con:
        con.execute(
            """
            INSERT INTO deleted_projects 
            (id, slug, title, project_type, summary, duration, skills, description_md, created_at, updated_at, deleted_at)
            SELECT id, slug, title, project_type, summary, duration, skills, description_md, created_at, updated_at, ?
            FROM projects WHERE slug = ?
            """,
            (deleted_at, slug),
        )
        con.execute("DELETE FROM projects WHERE slug = ?", (slug,))
        con.commit()


# ---------- Select ----------
def project_exists(slug: str) -> bool:
    """Check if a project exists by slug."""
    with get_connection() as con:
        cur = con.execute("SELECT 1 FROM projects WHERE slug = ?", (slug,))
        return cur.fetchone() is not None


def fetch_project(slug: str) -> Optional[Tuple]:
    """Fetch a single project by slug."""
    with get_connection() as con:
        cur = con.execute("SELECT * FROM projects WHERE slug = ?", (slug,))
        return cur.fetchone()


def fetch_all_projects() -> List[Tuple]:
    """Fetch all projects ordered by creation date descending."""
    with get_connection() as con:
        cur = con.execute("SELECT * FROM projects ORDER BY created_at DESC")
        return cur.fetchall()
