from static_portfolio_generator.model.posts.entity import (
    add_new_posts,
    rewrite_all_posts,
    delete_post as delete_post_slug,
)
from static_portfolio_generator.model.common.init_db import instantiate_tables
from static_portfolio_generator.model.projects.entity import (
    add_new_projects,
    rewrite_all_projects,
    delete_project as delete_project_slug,
)


class StaticSiteGenerator:
    """
    Interface to manage posts and projects in one place.
    """

    @staticmethod
    def init_db():
        """Ensure all tables exist."""
        instantiate_tables()

    # -------- Posts ----------
    @staticmethod
    def add_posts_to_db(hard=False):
        if hard:
            rewrite_all_posts()
        else:
            add_new_posts()

    @staticmethod
    def delete_post_to_db(slug: str):
        delete_post_slug(slug)

    # -------- Projects ----------
    @staticmethod
    def add_projects_to_db(hard=False):
        if hard:
            rewrite_all_projects()
        else:
            add_new_projects()

    @staticmethod
    def delete_project_to_db(slug: str):
        delete_project_slug(slug)
