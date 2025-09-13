"""
init_db
=======

Initialize the database for the static portfolio generator.

Features
--------

- Ensure the data directory exists.
- Create all tables for posts and projects.
- Sets up SQLite database at the configured path.
"""

from static_portfolio_generator.model.posts.db_utils import (
    create_tables as create_post_tables,
)
from static_portfolio_generator.model.projects.db_utils import (
    create_tables as create_project_tables,
)
from static_portfolio_generator.controller.config import DB_PATH


def ensure_data_dir() -> None:
    """
    Ensure that the data directory exists.

    Creates the directory tree for the database if it does not exist.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def instantiate_tables() -> None:
    """
    Initialize the database tables for posts and projects.

    This will:
    1. Ensure the data directory exists.
    2. Create tables for posts.
    3. Create tables for projects.
    """
    ensure_data_dir()

    # Create posts tables
    create_post_tables()

    # Create projects tables
    create_project_tables()

    print(f"📂 Initialized DB with posts and projects tables at: {DB_PATH.resolve()}")
