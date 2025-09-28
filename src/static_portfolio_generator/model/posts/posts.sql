-- Blog posts
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    summary TEXT,
    body_md TEXT NOT NULL,

    -- Metadata
    author TEXT DEFAULT 'Meher',
    created_at TEXT NOT NULL DEFAULT (strftime('{{datetime_format}}','now','utc')),
    updated_at TEXT,

    -- New Enhancements
    thumbnail_url TEXT,  -- preview image for list views
    tags TEXT            -- comma-separated array of tags
);
