from pathlib import Path

SITE_TITLE = "shrishtinigam.github.io"
BASE_URL = 'C:/Users/meher/Projects/github-pages/root'# 'https://shrishtinigam.github.io' # "C:/Users/meher/Projects/github-pages/root" # e.g.  (optional, used for absolute links if set)
DESCRIPTION = "Performance, Projects, Perspective"
AUTHOR = "Meher Shrishti Nigam"

# Root folder of the repo (project root)
ROOT = Path(__file__).parent.parent.resolve()

# Content folders
CONTENT_DIR = ROOT / "content"             # Root content folder
POSTS_DIR = CONTENT_DIR / "posts"          # Individual blog posts
PROJECTS_DIR = CONTENT_DIR / "projects"    # Individual project files
SCHEMA_PATH = ROOT / "model"
DB_PATH =  ROOT / "data"
OUTPUT_DIR = ROOT / "root"
STATIC_DIR = ROOT / "static"
TEMPLATES_DIR = ROOT / "templates"