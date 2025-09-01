"""
interface.py — Unified CLI for managing posts and projects

This script provides a single entry point to manage your blog posts and portfolio projects
stored in the SQLite database. You can add, rewrite, delete, and initialize tables for both
posts and projects.

Usage:
------

1. Initialize the database tables (posts + projects):
    python interface.py --init-db

2. Posts Management:

    a) Add new posts from markdown files (skip existing):
        python interface.py --add-posts

    b) Rewrite all posts (archive existing, re-insert all markdown files):
        python interface.py --rewrite-posts

    c) Delete a post by slug:
        python interface.py --delete-post <slug>

3. Projects Management:

    a) Add new projects from markdown files (skip existing):
        python interface.py --add-projects

    b) Rewrite all projects (archive existing, re-insert all markdown files):
        python interface.py --rewrite-projects

    c) Delete a project by slug:
        python interface.py --delete-project <slug>

Arguments & Options:
--------------------
--init-db           Initialize database tables (posts + projects)
--add-posts         Add new posts only (existing posts are skipped)
--rewrite-posts     Archive and re-add all posts
--delete-post <slug> Delete a post by its slug
--add-projects      Add new projects only (existing projects are skipped)
--rewrite-projects  Archive and re-add all projects
--delete-project <slug> Delete a project by its slug

Notes:
------
- Markdown files for posts are read from: content/posts/*.md
- Markdown files for projects are read from: content/projects/*.md
- Deleted posts/projects are moved to their respective archive tables.
- This interface allows you to manage all content from a single command-line entry point.
"""

import sys
import argparse
from entities.posts import add_new_posts, rewrite_all_posts, delete_post as delete_post_slug
from entities.projects import add_new_projects, rewrite_all_projects, delete_project as delete_project_slug
from db_utils.init_db import instantiate_tables

class ContentManager:
    """Interface to manage posts and projects in one place."""

    @staticmethod
    def init_db():
        """Ensure all tables exist."""
        instantiate_tables()

    # -------- Posts ----------
    @staticmethod
    def add_posts(hard=False):
        if hard:
            rewrite_all_posts()
        else:
            add_new_posts()

    @staticmethod
    def delete_post(slug: str):
        delete_post_slug(slug)

    # -------- Projects ----------
    @staticmethod
    def add_projects(hard=False):
        if hard:
            rewrite_all_projects()
        else:
            add_new_projects()

    @staticmethod
    def delete_project(slug: str):
        delete_project_slug(slug)


def main():
    parser = argparse.ArgumentParser(description="Manage blog posts and projects.")
    
    parser.add_argument("--init", action="store_true", help="Initialize database tables")
    
    # Posts commands
    parser.add_argument("--add-posts", action="store_true", help="Add new posts from content/")
    parser.add_argument("--rewrite-posts", action="store_true", help="Rewrite all posts (archive old, reinsert new)")
    parser.add_argument("--delete-post", type=str, help="Delete a post by slug")
    
    # Projects commands
    parser.add_argument("--add-projects", action="store_true", help="Add new projects from content/")
    parser.add_argument("--rewrite-projects", action="store_true", help="Rewrite all projects (archive old, reinsert new)")
    parser.add_argument("--delete-project", type=str, help="Delete a project by slug")
    
    args = parser.parse_args()
    manager = ContentManager()

    # -------- Execute commands ----------
    if args.init:
        manager.init_db()

    # Posts
    if args.add_posts:
        manager.add_posts()
    if args.rewrite_posts:
        manager.add_posts(hard=True)
    if args.delete_post:
        manager.delete_post(args.delete_post)

    # Projects
    if args.add_projects:
        manager.add_projects()
    if args.rewrite_projects:
        manager.add_projects(hard=True)
    if args.delete_project:
        manager.delete_project(args.delete_project)

if __name__ == "__main__":
    main()
