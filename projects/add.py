from pathlib import Path
import re

from site_config import ROOT, PROJECTS_DIR
from db_utils.projects import create_tables, insert_project, archive_project, project_exists

# ---------- Helpers ----------
def slugify(filename: str) -> str:
    """Convert filename to a URL-friendly slug."""
    s = Path(filename).stem.lower()
    s = re.sub(r'[^a-z0-9-]', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

# parse project markdown
def parse_markdown(file_path: Path):
    """Extract slug, title, project_type, summary, duration, skills, and description from a markdown file."""
    slug = slugify(file_path.name)
    body_md = file_path.read_text(encoding="utf-8").strip()
    lines = body_md.splitlines()

    if not lines:
        raise ValueError(f"{file_path} is empty")

    title = lines[0].lstrip("#").strip()
    project_type = lines[1].strip() if len(lines) > 1 and lines[1].strip() else "Personal Project"
    summary = lines[2].strip() if len(lines) > 2 and lines[2].strip() else ""
    duration = lines[3].strip() if len(lines) > 3 and lines[3].strip() else ""
    skills = lines[4].strip() if len(lines) > 4 and lines[4].strip() else ""
    description_md = "\n".join(lines[5:]).strip() if len(lines) > 5 else ""

    return slug, title, project_type, summary, duration, skills, description_md


# ---------- Operations ----------
def add_new_projects():
    """Add projects that do not exist in the database."""
    for file in PROJECTS_DIR.glob("*.md"):
        try:
            slug, title, project_type, summary, duration, skills, description_md = parse_markdown(file)
        except ValueError as e:
            print(f"[SKIP] {e}")
            continue

        if not project_exists(slug):
            print(f"[NEW] Adding project: {slug}")
            insert_project(slug, title, project_type, summary, duration, skills, description_md)
        else:
            print(f"[SKIP] Already exists: {slug}")


def rewrite_all_projects():
    """Archive all existing projects and rewrite everything from projects_content/."""
    for file in PROJECTS_DIR.glob("*.md"):
        try:
            slug, title, project_type, summary, duration, skills, description_md = parse_markdown(file)
        except ValueError as e:
            print(f"[SKIP] {e}")
            continue

        if project_exists(slug):
            print(f"[REWRITE] Archiving existing project: {slug}")
            archive_project(slug)
        print(f"[INSERT] Adding project: {slug}")
        insert_project(slug, title, project_type, summary, duration, skills, description_md)
