"""
spg — Unified CLI for managing posts, projects, experiences, and building the static site

This command-line tool provides a single entry point to manage your blog posts, portfolio projects,
and professional experiences stored in the SQLite database. You can add, rewrite, delete,
initialize tables, and build the static site.

Usage:
------
1. Initialize database tables (all domains):
    spg init-db

2. Posts Management:

    a) Add new posts from Markdown files (skip existing):
        spg --add-posts

    b) Rewrite all posts (archive existing and re-insert all Markdown files):
        spg --rewrite-posts

    c) Delete a post by slug:
        spg --delete-post <slug>

3. Projects Management:

    a) Add new projects from Markdown files (skip existing):
        spg --add-projects

    b) Rewrite all projects (archive existing and re-insert all Markdown files):
        spg --rewrite-projects

    c) Delete a project by slug:
        spg --delete-project <slug>

4. Experiences Management:

    a) Add new experiences from Markdown files (skip existing):
        spg --add-experiences

    b) Rewrite all experiences (archive existing and re-insert all Markdown files):
        spg --rewrite-experiences

    c) Delete an experience by slug:
        spg --delete-experience <slug>

5. Build the static site:
    spg --build

Commands:
---------
init-db                     Initialize database tables (all domains)
add-posts                    Add new posts only (existing posts are skipped)
rewrite-posts                Archive and re-add all posts
delete-post <slug>           Delete a post by its slug
add-projects                 Add new projects only (existing projects are skipped)
rewrite-projects             Archive and re-add all projects
delete-project <slug>        Delete a project by its slug
add-experiences              Add new experiences only (existing experiences are skipped)
rewrite-experiences          Archive and re-add all experiences
delete-experience <slug>     Delete an experience by its slug
build                        Build the static site into output/

Notes:
------
- Markdown files for posts are read from: content/posts/*.md
- Markdown files for projects are read from: content/projects/*.md
- Markdown files for experiences are read from: content/experiences/*.md
- Deleted content is moved to their respective archive tables.
- This CLI provides a single, unified interface to manage content and build the static site.
"""

import argparse

from static_portfolio_generator.controller.content import ContentGenerator
from static_portfolio_generator.controller.builder import SiteBuilder


def spg():
    parser = argparse.ArgumentParser(
        description="Unified CLI to manage posts, projects, experiences, and build site",
    )

    parser.add_argument(
        "--init-db", action="store_true", help="Initialize all database tables"
    )

    # Posts commands
    parser.add_argument("--add-posts", action="store_true", help="Add new posts")
    parser.add_argument(
        "--rewrite-posts", action="store_true", help="Rewrite all posts"
    )
    parser.add_argument("--delete-post", type=str, help="Delete a post by slug")

    # Projects commands
    parser.add_argument("--add-projects", action="store_true", help="Add new projects")
    parser.add_argument(
        "--rewrite-projects", action="store_true", help="Rewrite all projects"
    )
    parser.add_argument("--delete-project", type=str, help="Delete a project by slug")

    # Experiences commands
    parser.add_argument(
        "--add-experiences", action="store_true", help="Add new experiences"
    )
    parser.add_argument(
        "--rewrite-experiences", action="store_true", help="Rewrite all experiences"
    )
    parser.add_argument(
        "--delete-experience", type=str, help="Delete an experience by slug"
    )

    # Build site command
    parser.add_argument("--build", action="store_true", help="Build the static site")

    args = parser.parse_args()
    content_generator = ContentGenerator()
    site_builder = SiteBuilder()

    # Database init
    if args.init_db:
        content_generator.init_db()

    # Posts operations
    if args.add_posts:
        content_generator.add_posts_to_db()
    if args.rewrite_posts:
        content_generator.add_posts_to_db(hard=True)
    if args.delete_post:
        content_generator.delete_post_from_db(args.delete_post)

    # Projects operations
    if args.add_projects:
        content_generator.add_projects_to_db()
    if args.rewrite_projects:
        content_generator.add_projects_to_db(hard=True)
    if args.delete_project:
        content_generator.delete_project_from_db(args.delete_project)

    """
    # Experiences operations
    if args.add_experiences:
        content_generator.add_experiences()
    if args.rewrite_experiences:
        content_generator.add_experiences(hard=True)
    if args.delete_experience:
        content_generator.delete_experience(args.delete_experience)
    """
    # Build static site
    if args.build:
        site_builder.build()


if __name__ == "__main__":
    main()
