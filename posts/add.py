from site_config import POSTS_DIR
from pathlib import Path
from db_utils.posts import create_tables, insert_post, archive_post, post_exists
import re

def slugify(filename: str) -> str:
    s = Path(filename).stem.lower()
    s = re.sub(r'[^a-z0-9-]', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')


def parse_markdown(file_path):
    """Extract slug, title, body, and optional summary from a markdown file."""
    slug = slugify(file_path.name)
    body_md = file_path.read_text(encoding="utf-8").strip()
    lines = body_md.splitlines()

    if not lines:
        raise ValueError(f"{file_path} is empty")

    # First line as title
    title = lines[0].lstrip("#").strip()

    # Second line as summary if available
    summary = lines[1].strip() if len(lines) > 1 and lines[1].strip() else None

    return slug, title, body_md, summary


def add_new_posts():
    """Add posts that do not exist in the database."""
    for file in POSTS_DIR.glob("*.md"):
        try:
            slug, title, body_md, summary = parse_markdown(file)
        except ValueError as e:
            print(f"[SKIP] {e}")
            continue

        if not post_exists(slug):
            print(f"[NEW] Adding post: {slug}")
            insert_post(slug, title, body_md, summary)
        else:
            print(f"[SKIP] Already exists: {slug}")


def rewrite_all_posts():
    """Archive all existing posts and rewrite everything from content/."""
    for file in POSTS_DIR.glob("*.md"):
        try:
            slug, title, body_md, summary = parse_markdown(file)
        except ValueError as e:
            print(f"[SKIP] {e}")
            continue

        if post_exists(slug):
            print(f"[REWRITE] Archiving existing post: {slug}")
            archive_post(slug)
        print(f"[INSERT] Adding post: {slug}")
        insert_post(slug, title, body_md, summary)


