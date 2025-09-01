-- SQLite schema for blog posts
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    summary TEXT,
    body_md TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT
);

-- Deleted posts archive
CREATE TABLE IF NOT EXISTS deleted_posts (
    id INTEGER,
    slug TEXT,
    title TEXT,
    summary TEXT,
    body_md TEXT,
    created_at TEXT,
    updated_at TEXT,
    deleted_at TEXT DEFAULT (datetime('now'))
);
