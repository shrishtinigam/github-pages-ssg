from pathlib import Path

SITE_TITLE = "shrishtinigam.github.io"
BASE_URL = 'https://shrishtinigam.github.io' # "C:/Users/meher/Projects/website-push/"  # 
DESCRIPTION = "Performance, Projects, Perspective"
AUTHOR = "Meher Shrishti Nigam"

# Root folder of the repo (project root)
ROOT = Path(__file__).parent.parent.resolve()
REPO_ROOT = Path(__file__).parent.parent.parent.parent.resolve()

# Content folders
CONTENT_DIR = REPO_ROOT / "content"  # Root content folder
CONTENT_POSTS = CONTENT_DIR / "posts"  # Individual blog posts
CONTENT_PROJECTS = CONTENT_DIR / "projects"  # Individual project files
SCHEMA_PATH = ROOT / "model"
DB_PATH = REPO_ROOT / "data" / "site_data.db"  # SQLite database path
OUTPUT_DIR = "C:/Users/meher/Projects/website-push/"
STATIC_DIR = ROOT / "view" / "static"
TEMPLATES_DIR = ROOT / "view" / "templates"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"  # e.g. 2025-08-15 14:30:00
