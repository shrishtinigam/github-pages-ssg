"""
SEO utilities for generating sitemap, robots.txt, and structured data.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict
import json


def generate_sitemap(base_url: str, posts: List[Dict], projects: List[Dict], output_dir: Path) -> None:
    """
    Generate sitemap.xml for the static site.
    
    :param base_url: Base URL of the site
    :param posts: List of post dictionaries
    :param projects: List of project dictionaries
    :param output_dir: Output directory for the sitemap
    """
    base_url = base_url.rstrip('/')
    
    # Start sitemap XML
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Homepage
    sitemap.append('  <url>')
    sitemap.append(f'    <loc>{base_url}/</loc>')
    sitemap.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
    sitemap.append('    <changefreq>weekly</changefreq>')
    sitemap.append('    <priority>1.0</priority>')
    sitemap.append('  </url>')
    
    # About page
    sitemap.append('  <url>')
    sitemap.append(f'    <loc>{base_url}/about/</loc>')
    sitemap.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
    sitemap.append('    <changefreq>monthly</changefreq>')
    sitemap.append('    <priority>0.8</priority>')
    sitemap.append('  </url>')
    
    # Projects page
    sitemap.append('  <url>')
    sitemap.append(f'    <loc>{base_url}/projects/</loc>')
    sitemap.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
    sitemap.append('    <changefreq>weekly</changefreq>')
    sitemap.append('    <priority>0.8</priority>')
    sitemap.append('  </url>')
    
    # Posts page
    sitemap.append('  <url>')
    sitemap.append(f'    <loc>{base_url}/posts/</loc>')
    sitemap.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
    sitemap.append('    <changefreq>daily</changefreq>')
    sitemap.append('    <priority>0.9</priority>')
    sitemap.append('  </url>')
    
    # Individual projects
    for project in projects:
        sitemap.append('  <url>')
        sitemap.append(f'    <loc>{base_url}/projects/{project["slug"]}/</loc>')
        if project.get('updated_at'):
            sitemap.append(f'    <lastmod>{project["updated_at"]}</lastmod>')
        sitemap.append('    <changefreq>monthly</changefreq>')
        sitemap.append('    <priority>0.7</priority>')
        sitemap.append('  </url>')
    
    # Individual posts
    for post in posts:
        sitemap.append('  <url>')
        sitemap.append(f'    <loc>{base_url}/posts/{post["slug"]}/</loc>')
        if post.get('updated_at'):
            sitemap.append(f'    <lastmod>{post["updated_at"]}</lastmod>')
        sitemap.append('    <changefreq>monthly</changefreq>')
        sitemap.append('    <priority>0.6</priority>')
        sitemap.append('  </url>')
    
    sitemap.append('</urlset>')
    
    # Write sitemap
    sitemap_path = output_dir / "sitemap.xml"
    sitemap_path.write_text('\n'.join(sitemap), encoding='utf-8')


def generate_robots_txt(base_url: str, output_dir: Path) -> None:
    """
    Generate robots.txt for the static site.
    
    :param base_url: Base URL of the site
    :param output_dir: Output directory for robots.txt
    """
    base_url = base_url.rstrip('/')
    
    robots = [
        "# Allow all crawlers",
        "User-agent: *",
        "Allow: /",
        "",
        "# Disallow admin or private directories (if any)",
        "# Disallow: /admin/",
        "",
        f"Sitemap: {base_url}/sitemap.xml",
    ]
    
    robots_path = output_dir / "robots.txt"
    robots_path.write_text('\n'.join(robots), encoding='utf-8')


def generate_structured_data_person(author: str, description: str, base_url: str) -> str:
    """
    Generate JSON-LD structured data for Person schema.
    
    :param author: Author name
    :param description: Site description
    :param base_url: Base URL of the site
    :return: JSON-LD string
    """
    base_url = base_url.rstrip('/')
    
    structured_data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": author,
        "url": base_url,
        "description": description,
        "jobTitle": "Software Engineer",
        "sameAs": [
            f"https://github.com/shrishtinigam",
            "https://linkedin.com/in/yourprofile",
            "https://twitter.com/yourhandle"
        ]
    }
    
    return json.dumps(structured_data, indent=2)


def generate_structured_data_blog_post(post: Dict, author: str, base_url: str) -> str:
    """
    Generate JSON-LD structured data for BlogPosting schema.
    
    :param post: Post dictionary
    :param author: Author name
    :param base_url: Base URL of the site
    :return: JSON-LD string
    """
    base_url = base_url.rstrip('/')
    
    structured_data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.get("title", "").replace("<p>", "").replace("</p>", "").strip(),
        "author": {
            "@type": "Person",
            "name": author
        },
        "url": f"{base_url}/posts/{post['slug']}/",
        "datePublished": post.get("created_at", ""),
        "dateModified": post.get("updated_at", post.get("created_at", "")),
        "description": post.get("summary_html", "").replace("<p>", "").replace("</p>", "").strip()[:200],
    }
    
    if post.get("tags"):
        structured_data["keywords"] = ", ".join(post["tags"])
    
    return json.dumps(structured_data, indent=2)


def generate_structured_data_website(site_title: str, description: str, author: str, base_url: str) -> str:
    """
    Generate JSON-LD structured data for WebSite schema.
    
    :param site_title: Site title
    :param description: Site description
    :param author: Author name
    :param base_url: Base URL of the site
    :return: JSON-LD string
    """
    base_url = base_url.rstrip('/')
    
    structured_data = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": site_title,
        "description": description,
        "url": base_url,
        "author": {
            "@type": "Person",
            "name": author
        },
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{base_url}/search?q={{search_term_string}}",
            "query-input": "required name=search_term_string"
        }
    }
    
    return json.dumps(structured_data, indent=2)
