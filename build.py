from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound
import markdown
import shutil
from datetime import datetime

from site_config import (
    SITE_TITLE,
    BASE_URL,
    DESCRIPTION,
    AUTHOR,
    OUTPUT_DIR,
    TEMPLATES_DIR,
    STATIC_DIR,
    CONTENT_DIR
)
from db_utils.posts import fetch_all_posts
from db_utils.projects import fetch_all_projects


def ensure_dirs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "posts").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "projects").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "static").mkdir(parents=True, exist_ok=True)


def copy_static():
    dst = OUTPUT_DIR / "static"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(STATIC_DIR, dst)


def get_env():
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )


def parse_datetime(dt_str: str) -> str:
    if not dt_str:
        return ""
    try:
        dt = datetime.fromisoformat(dt_str)
    except ValueError:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%b %d, %Y")


def load_posts():
    rows = fetch_all_posts()
    posts = []
    for r in rows:
        slug = r[1]
        title = r[2]
        summary = r[3] or (r[4][:200] + "...")
        body_md = r[4]
        summary_html = markdown.markdown(
            summary,
            extensions=["fenced_code", "tables", "codehilite", "toc"],
            output_format="html5",
        )
        body_html = markdown.markdown(
            body_md,
            extensions=["fenced_code", "tables", "codehilite", "toc"],
            output_format="html5",
        )
        posts.append({
            "slug": slug,
            "title": title,
            "summary_html": summary_html,
            "body_html": body_html,
            "created_at": parse_datetime(r[5]),
            "updated_at": parse_datetime(r[6]),
        })
    return posts

def parse_end_date(duration: str):
    """Return a datetime object from the end of the duration string."""
    try:
        # Example duration format: "May 2023 - Jun 2023"
        end_part = duration.split('-')[-1].strip()
        return datetime.strptime(end_part, "%b %Y")
    except Exception:
        return datetime.min  # fallback for missing/invalid duration

# load projects from DB
def load_projects():
    rows = fetch_all_projects()
    projects = []
    for r in rows:
        slug = r[1]
        title = r[2]
        project_type = r[3]        # matches schema: projects.project_type
        summary = r[4]             # summary field
        duration = r[5]            # duration field
        skills = r[6]              # skills field
        description_md = r[7]      # full description

        # Convert markdown to HTML
        description_html = markdown.markdown(
            description_md,
            extensions=["fenced_code", "tables", "codehilite", "toc"],
            output_format="html5",
        )

        projects.append({
            "slug": slug,
            "title": title,
            "project_type": project_type,
            "summary": summary,
            "duration": duration,
            "skills": skills,
            "description_html": description_html,
            "created_at": parse_datetime(r[8]),
            "updated_at": parse_datetime(r[9]),
            "link": None,
        })
    projects.sort(key=lambda p: parse_end_date(p.get("duration", "")), reverse=True)
    return projects

def load_about_summary() -> str:
    """Read about_summary.md and convert each line to a separate paragraph with Markdown parsing."""
    about_file = CONTENT_DIR / "about_summary.md"
    if not about_file.exists():
        return "<p>About me content not found.</p>"

    lines = [
        line.strip()
        for line in about_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    # Parse each line as Markdown and wrap in <p> for clarity
    html_lines = [
        markdown.markdown(line, extensions=["fenced_code", "tables", "codehilite"], output_format="html5")
        for line in lines
    ]

    return "<br>".join(html_lines)

def load_about() -> str:
    """
    Read about.md and convert its Markdown content to HTML.
    Returns a string of HTML.
    """
    about_file = CONTENT_DIR / "about.md"
    if not about_file.exists():
        return "<p>About content not found.</p>"

    md_text = about_file.read_text(encoding="utf-8")

    html = markdown.markdown(
        md_text,
        extensions=["fenced_code", "tables", "codehilite"],
        output_format="html5"
    )
    return html



def build():
    ensure_dirs()
    copy_static()
    env = get_env()

    posts = load_posts()
    projects = load_projects()
    about_summary_html = load_about_summary()
    about_html = load_about()

    # Build index page
    try:
        index_tpl = env.get_template("index.html")
        index_html = index_tpl.render(
            site_title=SITE_TITLE,
            description=DESCRIPTION,
            author=AUTHOR,
            about_html=about_summary_html,
            posts=posts,
            projects=projects,
            base_url=BASE_URL.rstrip("/"),
        )
        (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")
    except TemplateNotFound:
        print("❌ Error: 'index.html' template not found.")
        return
    # --- Dedicated About Page ---
    about_dir = OUTPUT_DIR / "about"
    about_dir.mkdir(parents=True, exist_ok=True)
    try:
        about_tpl = env.get_template("about.html")
        about_html_page = about_tpl.render(
            site_title=SITE_TITLE,
            description=DESCRIPTION,
            author=AUTHOR,
            about_html=about_html,
            base_url=BASE_URL.rstrip("/"),
        )
        (about_dir / "index.html").write_text(about_html_page, encoding="utf-8")
    except TemplateNotFound:
        print("❌ Error: 'about.html' template not found.")
    # --- Dedicated Projects Page ---
    projects_dir = OUTPUT_DIR / "projects"
    projects_dir.mkdir(parents=True, exist_ok=True)
    try:
        projects_tpl = env.get_template("projects.html")
        projects_html_page = projects_tpl.render(
            site_title=SITE_TITLE,
            description=DESCRIPTION,
            author=AUTHOR,
            projects=projects,
            base_url=BASE_URL.rstrip("/"),
        )
        (projects_dir / "index.html").write_text(projects_html_page, encoding="utf-8")
    except TemplateNotFound:
        print("❌ Error: 'projects.html' template not found.")

    # --- Dedicated Posts Page ---
    posts_dir = OUTPUT_DIR / "posts"
    posts_dir.mkdir(parents=True, exist_ok=True)
    try:
        posts_tpl = env.get_template("posts.html")
        posts_html_page = posts_tpl.render(
            site_title=SITE_TITLE,
            description=DESCRIPTION,
            author=AUTHOR,
            posts=posts,
            base_url=BASE_URL.rstrip("/"),
        )
        (posts_dir / "index.html").write_text(posts_html_page, encoding="utf-8")
    except TemplateNotFound:
        print("❌ Error: 'posts.html' template not found")
    # Build individual post pages
    try:
        post_tpl = env.get_template("post.html")
    except TemplateNotFound:
        print("❌ Error: 'post.html' template not found.")
        return

    for p in posts:
        post_dir = OUTPUT_DIR / "posts" / p["slug"]
        post_dir.mkdir(parents=True, exist_ok=True)
        html = post_tpl.render(
            site_title=SITE_TITLE,
            description=DESCRIPTION,
            author=AUTHOR,
            post=p,
            base_url=BASE_URL.rstrip("/"),
        )
        (post_dir / "index.html").write_text(html, encoding="utf-8")

    # Build individual project pages
    try:
        project_tpl = env.get_template("project.html")
    except TemplateNotFound:
        print("❌ Error: 'project.html' template not found.")
        return

    for proj in projects:
        proj_dir = OUTPUT_DIR / "projects" / proj["slug"]
        proj_dir.mkdir(parents=True, exist_ok=True)
        html = project_tpl.render(
            site_title=SITE_TITLE,
            description=DESCRIPTION,
            author=AUTHOR,
            project=proj,
            base_url=BASE_URL.rstrip("/"),
        )
        (proj_dir / "index.html").write_text(html, encoding="utf-8")

    print(f"✅ Built {len(posts)} posts and {len(projects)} projects into: {OUTPUT_DIR}")


if __name__ == "__main__":
    build()
