# delete_post.py
import sys
from db_utils.posts import post_exists, archive_post

def delete_post(slug: str) -> None:
    """Move a post to deleted_posts and remove it from posts."""
    if not post_exists(slug):
        print(f"❌ No post found with slug '{slug}'")
        return

    archive_post(slug)
    print(f"🗑️ Post '{slug}' moved to deleted_posts.")



