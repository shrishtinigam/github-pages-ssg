"""
This class-based implementation provides a unified interface to build the static site
from posts, projects, and about content stored in the database and markdown files.
"""

import shutil
from datetime import datetime
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound

from static_portfolio_generator.controller.config import (
    SITE_TITLE,
    BASE_URL,
    DESCRIPTION,
    AUTHOR,
    OUTPUT_DIR,
    TEMPLATES_DIR,
    STATIC_DIR,
    CONTENT_DIR,
)
from static_portfolio_generator.model.posts.db_utils import fetch_all_posts
from static_portfolio_generator.model.projects.db_utils import fetch_all_projects


class SiteBuilder:
    """
    Builds a static site from entities and generic content.

    Features
    --------
    - Loads posts and projects from the database.
    - Reads about content from markdown files.
    - Converts markdown to HTML.
    - Uses Jinja2 templates to render pages.

    Attributes
    ----------
    output_dir : Path
        Directory to output the static site.
    templates_dir : Path
        Directory containing Jinja2 templates.
    static_dir : Path
        Directory containing static assets (CSS, JS, images).
    content_dir : Path
        Directory containing markdown content files.
    env : Environment
        Jinja2 environment for template rendering.
    """

    def __init__(self):
        self.output_dir: Path = Path(OUTPUT_DIR)
        self.templates_dir: Path = Path(TEMPLATES_DIR)
        self.static_dir: Path = Path(STATIC_DIR)
        self.content_dir: Path = Path(CONTENT_DIR)
        self.env: Environment = self._get_env()

    # ------------------ Public API ------------------ #
    def build(self):
        """Main entry point to build the static site."""
        self._ensure_dirs()
        self._copy_static()

        posts = self._load_posts()
        projects = self._load_projects()
        about_summary_html = self._load_about_summary()
        about_html = self._load_about()

        self._build_index(posts, projects, about_summary_html)
        self._build_about_page(about_html)
        self._build_projects_page(projects)
        self._build_posts_page(posts)
        self._build_individual_post_pages(posts)
        self._build_individual_project_pages(projects)

        print(
            f"Built {len(posts)} posts and {len(projects)} projects into: {self.output_dir}"
        )

    # ------------------ Private Helpers ------------------ #
    def _ensure_dirs(self):
        """Ensure necessary output directories exist."""
        (self.output_dir / "posts").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "projects").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "static").mkdir(parents=True, exist_ok=True)

    def _copy_static(self):
        """Copy static assets to output directory."""
        dst = self.output_dir / "static"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(self.static_dir, dst)

    def _get_env(self) -> Environment:
        """Set up Jinja2 environment."""
        return Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )

    @staticmethod
    def _parse_datetime(dt_str: str) -> str:
        """
        Convert datetime string to human-readable format.

        :param dt_str: Datetime string from the database.
        :return: Formatted date string like 'Jan 01, 2023' or empty string if input is empty.
        """
        if not dt_str:
            return ""
        try:
            dt = datetime.fromisoformat(dt_str)
        except ValueError:
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%b %d, %Y")

    def _load_posts(self):
        """
        Fetch posts from DB and convert markdown to HTML.
        """
        rows = fetch_all_posts()
        posts = []
        for r in rows:
            slug, title, summary, body_md, created_at, updated_at = (
                r[1],
                r[2],
                r[3],
                r[4],
                r[5],
                r[6],
            )
            summary_text = summary or (body_md[:200] + "...")
            posts.append(
                {
                    "slug": slug,
                    "title": title,
                    "summary_html": self._markdown_to_html(summary_text),
                    "body_html": self._markdown_to_html(body_md),
                    "created_at": self._parse_datetime(created_at),
                    "updated_at": self._parse_datetime(updated_at),
                }
            )
        return posts

    @staticmethod
    def _parse_end_date(duration: str) -> datetime:
        """
        Return datetime object for the end of a duration string.

        :param duration: Duration string like "Jan 2020 - Dec 2021" or "Feb 2019 - Present"
        :return: datetime object for the end date, or datetime.min if parsing fails.
        """
        try:
            end_part = duration.split("-")[-1].strip()
            return datetime.strptime(end_part, "%b %Y")
        except Exception:
            return datetime.min

    def _load_projects(self):
        """
        Fetch projects from DB and convert markdown to HTML.
        """
        rows = fetch_all_projects()
        projects = []
        for r in rows:
            (
                slug,
                title,
                project_type,
                summary,
                duration,
                skills,
                description_md,
                created_at,
                updated_at,
            ) = (r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9])
            projects.append(
                {
                    "slug": slug,
                    "title": title,
                    "project_type": project_type,
                    "summary": summary,
                    "duration": duration,
                    "skills": skills,
                    "description_html": self._markdown_to_html(description_md),
                    "created_at": self._parse_datetime(created_at),
                    "updated_at": self._parse_datetime(updated_at),
                    "link": None,
                }
            )
        projects.sort(
            key=lambda p: self._parse_end_date(p.get("duration", "")), reverse=True
        )
        return projects

    def _load_about_summary(self) -> str:
        """
        Load about_summary.md and convert each line to HTML.
        """
        about_file = self.content_dir / "about_summary.md"
        if not about_file.exists():
            return "<p>About me content not found.</p>"

        lines = [
            line.strip()
            for line in about_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        html_lines = [self._markdown_to_html(line) for line in lines]
        return "<br>".join(html_lines)

    def _load_about(self) -> str:
        """
        Load about.md and convert markdown content to HTML.
        """
        about_file = self.content_dir / "about.md"
        if not about_file.exists():
            return "<p>About content not found.</p>"
        return self._markdown_to_html(about_file.read_text(encoding="utf-8"))

    @staticmethod
    def _markdown_to_html(md_text: str) -> str:
        """
        Convert markdown text to HTML.
        """
        return markdown.markdown(
            md_text,
            extensions=["fenced_code", "tables", "codehilite", "toc"],
            output_format="html5",
        )

    # ------------------ Page Builders ------------------ #
    def _build_index(self, posts, projects, about_summary_html):
        """
        Build the index.html page with posts, projects, and about summary.

        :param posts: List of post dictionaries.
        :param projects: List of project dictionaries.
        :param about_summary_html: HTML string for the about summary.
        """
        try:
            template = self.env.get_template("index.html")
            html = template.render(
                site_title=SITE_TITLE,
                description=DESCRIPTION,
                author=AUTHOR,
                about_html=about_summary_html,
                posts=posts,
                projects=projects,
                base_url=BASE_URL.rstrip("/"),
            )
            (self.output_dir / "index.html").write_text(html, encoding="utf-8")
        except TemplateNotFound:
            print("❌ Error: 'index.html' template not found.")

    def _build_about_page(self, about_html: str):
        about_dir = self.output_dir / "about"
        about_dir.mkdir(parents=True, exist_ok=True)
        try:
            template = self.env.get_template("about.html")
            html = template.render(
                site_title=SITE_TITLE,
                description=DESCRIPTION,
                author=AUTHOR,
                about_html=about_html,
                base_url=BASE_URL.rstrip("/"),
            )
            (about_dir / "index.html").write_text(html, encoding="utf-8")
        except TemplateNotFound:
            print("❌ Error: 'about.html' template not found.")

    def _build_projects_page(self, projects):
        projects_dir = self.output_dir / "projects"
        projects_dir.mkdir(parents=True, exist_ok=True)
        try:
            template = self.env.get_template("projects.html")
            html = template.render(
                site_title=SITE_TITLE,
                description=DESCRIPTION,
                author=AUTHOR,
                projects=projects,
                base_url=BASE_URL.rstrip("/"),
            )
            (projects_dir / "index.html").write_text(html, encoding="utf-8")
        except TemplateNotFound:
            print("❌ Error: 'projects.html' template not found.")

    def _build_posts_page(self, posts):
        posts_dir = self.output_dir / "posts"
        posts_dir.mkdir(parents=True, exist_ok=True)
        try:
            template = self.env.get_template("posts.html")
            html = template.render(
                site_title=SITE_TITLE,
                description=DESCRIPTION,
                author=AUTHOR,
                posts=posts,
                base_url=BASE_URL.rstrip("/"),
            )
            (posts_dir / "index.html").write_text(html, encoding="utf-8")
        except TemplateNotFound:
            print("❌ Error: 'posts.html' template not found.")

    def _build_individual_post_pages(self, posts):
        try:
            template = self.env.get_template("post.html")
        except TemplateNotFound:
            print("❌ Error: 'post.html' template not found.")
            return

        for post in posts:
            post_dir = self.output_dir / "posts" / post["slug"]
            post_dir.mkdir(parents=True, exist_ok=True)
            html = template.render(
                site_title=SITE_TITLE,
                description=DESCRIPTION,
                author=AUTHOR,
                post=post,
                base_url=BASE_URL.rstrip("/"),
            )
            (post_dir / "index.html").write_text(html, encoding="utf-8")

    def _build_individual_project_pages(self, projects):
        try:
            template = self.env.get_template("project.html")
        except TemplateNotFound:
            print("❌ Error: 'project.html' template not found.")
            return

        for proj in projects:
            proj_dir = self.output_dir / "projects" / proj["slug"]
            proj_dir.mkdir(parents=True, exist_ok=True)
            html = template.render(
                site_title=SITE_TITLE,
                description=DESCRIPTION,
                author=AUTHOR,
                project=proj,
                base_url=BASE_URL.rstrip("/"),
            )
            (proj_dir / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    builder = SiteBuilder()
    builder.build()
