from pelican_readers import FrontmatterMarkdownReader

AUTHOR = "Meher Shrishti Nigam"
SITENAME = "shrishtinigam.github.io"
SITEURL = "https://shrishtinigam.github.io"
PATH = "content"
THEME = "theme"
OUTPUT_PATH = "../pelican-output/"
TIMEZONE = "America/Los_Angeles"
DEFAULT_LANG = "en"
DEFAULT_DATE_FORMAT = "%b %d, %Y"
ARTICLE_URL = "posts/{slug}/"
ARTICLE_SAVE_AS = "posts/{slug}/index.html"
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
THEME_STATIC_DIR = "static"
STATIC_PATHS = ["images"]
DIRECT_TEMPLATES = ["index"]
INDEX_SAVE_AS = "index.html"
# The portfolio has explicit collection pages; do not publish Pelican's
# auxiliary author/category/tag archives as extra public routes.
AUTHOR_SAVE_AS = ""
CATEGORY_SAVE_AS = ""
TAG_SAVE_AS = ""
ARCHIVES_SAVE_AS = ""
FEED_ALL_ATOM = "feeds/all.atom.xml"
DELETE_OUTPUT_DIRECTORY = True
LOAD_CONTENT_CACHE = False

JINJA_FILTERS = {}
READERS = {"md": FrontmatterMarkdownReader}
PLUGIN_PATHS = ["."]
PLUGINS = ["pelican_compat"]
JINJA_GLOBALS = {
    "site_title": SITENAME,
    "base_url": SITEURL,
    "author": AUTHOR,
    "description": "Performance, Projects, Perspective",
}
