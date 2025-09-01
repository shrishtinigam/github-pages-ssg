# init_db.py
from pathlib import Path
from db_utils.posts import create_tables as create_post_tables
from db_utils.projects import create_tables as create_project_tables

from site_config import ROOT

DB_PATH = ROOT / "data" / "site.db"

def ensure_data_dir() -> None:
    """Ensure the data directory exists."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def instantiate_tables() -> None:
    """Initialize the database: ensure data folder and all tables exist."""
    ensure_data_dir()
    
    # Create posts tables
    create_post_tables()
    
    # Create projects tables
    create_project_tables()
    
    print(f"📂 Initialized DB with posts and projects tables at: {DB_PATH.resolve()}")