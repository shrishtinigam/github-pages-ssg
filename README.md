# Portfolio Pelican SSG

The standalone Python static-site generator for `shrishtinigam.github.io`.
It uses Pelican for content parsing, URL generation, feeds, and static output;
the custom theme preserves the existing portfolio design.

## Authoring workflow

```text
write Markdown → add images → make check → make build → deploy output/
```

Content lives in `content/posts/`, `content/projects/`, `content/pages/`, and
`content/images/`.

Posts use YAML front matter:

```markdown
---
Title: My post
Slug: my-post
Date: 2025-01-01
Summary: A short description shown on listing pages.
Tags:
  - python
  - systems
---

## The article

Write normal Markdown here. Raw HTML is also supported when preserving an
existing section requires it.
```

Projects use the same format with project-specific fields:

```markdown
---
Title: My project
Slug: my-project
Project Type: Personal Project
Duration: 2025
Summary: A short project-card description.
Skills: Python · Docker · PostgreSQL
Image: my-project.jpg
---
```

Put project images in `theme/static/images/projects/` or shared images in
`content/images/`. Theme assets are copied to `static/`; content images to `images/`.

## Local setup

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
source .venv/bin/activate
make check
make test
make build
```

`make build` writes the generated site to the sibling directory
`../pelican-output/`, outside this SSG repository. Do not place a Git
repository inside generated output.

The installed `spg check` command validates a checkout in temporary storage.
Use `spg build --output ../my-site-build` to build into a fresh, empty directory.
Use `--project /path/to/github-pages-ssg` when running outside the checkout.
The installed package includes the Pelican reader and adapter; the checkout
provides editable content, configuration, and theme files. The old database
CLI is no longer the installed `spg` entry point.

Every document requires a nonempty Title and a lowercase, hyphenated Slug.
Posts require a valid Date; Updated is optional. Tags may be a string or a
list of strings, and project Order must be an integer. Undated projects use
an internal placeholder date required by Pelican; it is not shown on cards.
Shared images in `content/images/` are published under `/images/`; project
thumbnails in `theme/static/images/projects/` retain their `/static/` paths.

## Preserved routes

- `/`
- `/about/`
- `/projects/`
- `/projects/<slug>/`
- `/posts/`
- `/posts/<slug>/`

The theme, CSS, JavaScript, images, navigation, theme toggle, cards, footer,
and existing content are kept compatible with the current published site.
