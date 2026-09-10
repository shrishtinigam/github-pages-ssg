"""Adapt completed Pelican collections to the portfolio's template context."""

from datetime import datetime

from pelican import signals


def _date(value):
    """Format a date for display without changing its chronological value."""
    if not value:
        return ""
    if isinstance(value, datetime):
        return value.strftime("%b %d, %Y")
    return str(value)


class LegacyContent:
    """Expose Pelican content using the fields of the original templates."""

    def __init__(self, article):
        """Copy the fields used by the legacy templates from a Pelican article."""
        self._article = article
        self.metadata = article.metadata
        self.title = article.title
        self.slug = article.slug
        self.body_html = article.content
        self.description_html = article.content
        self.created_at = _date(article.date)
        self.date = article.date
        self.updated_at = _date(article.metadata.get("updated"))
        self.summary = article.metadata.get("summary", "")
        self.summary_html = self.summary
        self.tags = list(getattr(article, "tags", []) or [])
        self.project_type = article.metadata.get("project_type", "")
        self.duration = article.metadata.get("duration", "")
        self.skills = article.metadata.get("skills", "")
        self.image = article.metadata.get("image", f"{article.slug}.jpg")
        self.link = article.metadata.get("link")


def _adapt(generator, **kwargs):
    """Populate ordered collections after Pelican has read every article."""
    articles = generator.context.get("articles", [])
    posts = [LegacyContent(article) for article in articles if getattr(article.category, "name", "") == "posts"]
    projects = [LegacyContent(article) for article in articles if getattr(article.category, "name", "") == "projects"]
    posts.sort(key=lambda item: item.date, reverse=True)
    projects.sort(key=lambda item: int(item.metadata.get("order", 999)))
    generator.context["posts"] = posts
    generator.context["projects"] = projects
    page = generator.context.get("page")
    if page is not None:
        generator.context["about_html"] = page.content


def register():
    """Register once per completed article collection, including cached builds."""
    signals.article_generator_finalized.connect(_adapt)
