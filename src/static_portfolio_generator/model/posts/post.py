from dataclasses import dataclass
from typing import Optional
@dataclass
class PostData:
    slug: str
    title: str
    body_md: str
    created_at: str
    summary: Optional[str] = None
    thumbnail_url: Optional[str] = None
    tags: Optional[str] = None
    author: str = "Meher"
