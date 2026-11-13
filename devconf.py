"""Local preview only; production URLs remain in pelicanconf.py."""

import os
from pelicanconf import *

SITEURL = os.environ.get("PORTFOLIO_PREVIEW_URL", "http://127.0.0.1:8000")
JINJA_GLOBALS = {**JINJA_GLOBALS, "base_url": SITEURL}
RELATIVE_URLS = False
