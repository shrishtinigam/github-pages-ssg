-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    project_type TEXT DEFAULT 'Personal Project',
    summary TEXT,
    duration TEXT,
    skills TEXT,
    description_md TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now','utc')),
    updated_at TEXT
);

-- Deleted projects archive
CREATE TABLE IF NOT EXISTS deleted_projects (
    id INTEGER,
    slug TEXT,
    title TEXT,
    project_type TEXT,
    summary TEXT,
    duration TEXT,
    skills TEXT,
    description_md TEXT,
    created_at TEXT,
    updated_at TEXT,
    deleted_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now','utc'))
);
