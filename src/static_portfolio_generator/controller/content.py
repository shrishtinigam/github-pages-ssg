"""
static_site_generator
=====================

This module provides a unified interface to manage blog posts and projects
for the static portfolio site.

Features
--------

- Initialize the database tables.
- Add or rewrite posts and projects in the database.
- Delete posts or projects (soft delete via archiving).
- Combines functionality from the `posts` and `projects` entities.

Logging
-------
Basic logging is included for tracking operations.
"""

from static_portfolio_generator.model.posts.entity import Post
from static_portfolio_generator.model.common.init_db import instantiate_tables
from static_portfolio_generator.model.projects.entity import Project


class ContentGenerator:
    """
    Interface to manage posts and projects in one place.
    """

    def __init__(self):
        self.post = Post()
        self.project = Project()

    def init_db(self):
        """
        Ensure all tables exist in the database.
        """
        instantiate_tables()

    # -------- Posts ----------
    def add_posts_to_db(self, hard=False):
        """
        Add posts to the database.

        :param hard: If True, rewrite all posts (archive existing and re-add),
                     otherwise only add new posts. Default is False.
        """
        if hard:
            self.post.rewrite_all_posts()
        else:
            self.post.add_new_posts()

    def delete_post_from_db(self, slug):
        """
        Archive a post by slug.

        :param slug: The slug identifier of the post to delete.
        """
        self.post.delete_post(slug)

    # -------- Projects ----------
    def add_projects_to_db(self, hard=False):
        """
        Add projects to the database.

        :param hard: If True, rewrite all projects (archive existing and re-add),
                     otherwise only add new projects. Default is False.
        """
        if hard:
            self.project.rewrite_all_projects()
        else:
            self.project.add_new_projects()

    def delete_project_from_db(self, slug):
        """
        Archive a project by slug.

        :param slug: The slug identifier of the project to delete.
        """
        self.project.delete_project_slug(slug)
