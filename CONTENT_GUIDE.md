# Content guide

Your existing format is unchanged: **YAML between `---` lines, followed by
Markdown or raw HTML**. Keep the field names and ordering below. Nothing here
renames fields, converts old files, or introduces a new metadata schema.

## Start here

From the activated environment, in the SSG checkout:

```sh
spg new post "My useful Python technique"
spg new project "My engineering project"
spg validate
spg dev
```

Omit the title to be prompted for **only the title** in an interactive terminal.
Slug is derived automatically; use `--slug my-slug` to choose it yourself.
Noninteractive commands require a title. Files are never overwritten.
`spg new page "Page title"` is also available, but see the About-layout warning
below. Without activation on Windows, use `.\.venv\Scripts\spg.exe`.

The CLI reads these same reusable files from the checkout; no second set of
starter metadata is hidden in Python:

| Starter | Copy destination | Required fields |
| --- | --- | --- |
| `content-templates/post.md` | `content/posts/<slug>.md` | Title, Slug, Date |
| `content-templates/project.md` | `content/projects/<slug>.md` | Title, Slug |
| `content-templates/page.md` | `content/pages/<slug>.md` | Title, Slug |
| `content-templates/posts-index.md` | Reference for existing `content/pages/posts.md` | Title, Slug, Template for the listing layout |
| `content-templates/projects-index.md` | Reference for existing `content/pages/projects.md` | Title, Slug, Template for the listing layout |

You can copy starters manually instead. Replace their placeholder values and
body. They live **outside `content/`**, so they are not published. Optional fields
have comments; uncomment a field to use it or remove it entirely. Do not leave
an optional field as a bare `Updated:` or `Duration:`: YAML treats that as null,
which is not a valid date/string. Dates in the copyable starters are examples;
the CLI sets a new post's Date to today in the existing `Mon DD, YYYY` style.

## Blog posts

Field order follows the existing posts: Title → Slug → Date → Updated → Summary
→ Tags. Updated is optional even though the existing posts use it.

| Field | Required? | What it controls / accepted value |
| --- | --- | --- |
| `Title` | Yes | Nonempty string; post heading, browser title, listing links, JSON-LD headline. |
| `Slug` | Yes | Lowercase letters/numbers separated by single hyphens; URL `/posts/<slug>/`. Keep stable after publishing. |
| `Date` | Yes | Publication label, newest-first ordering, feeds, structured data. Existing style: `Sep 10, 2025`; ISO dates are also already accepted. |
| `Updated` | No | Last-updated labels and structured data; same date syntax. Omit if never updated. |
| `Summary` | No | Homepage/blog-list excerpt and JSON-LD description; string. Existing summary HTML remains supported. |
| `Tags` | No | Tag labels on posts and cards, and JSON-LD keywords. Existing block list of strings; comma-separated strings are also already accepted. |

Copy-paste example:

```markdown
---
Title: My useful Python technique
Slug: my-useful-python-technique
Date: Nov 13, 2026
# Updated: Nov 14, 2026
Summary: A practical technique with a worked example.
Tags:
  - python
  - engineering
---

## The technique

Explain the problem and show a concrete example.
```

## Projects

Existing order: Title → optional Page Title → Slug → Project Type → Duration
→ Summary → Skills → Image → Order. Link is additionally supported by the
current templates and can be placed after Order.

| Field | Required? | What it controls / accepted value |
| --- | --- | --- |
| `Title` | Yes | Nonempty string; project cards and browser title. The detail template does not create an h1: put the detail heading in the body. |
| `Page Title` | No | Existing legacy field stored as metadata, but **not read by current templates**. It does not change the detail heading or browser title. |
| `Slug` | Yes | URL `/projects/<slug>/`; same slug rules as posts. |
| `Project Type` | No | Category-like label on project cards and detail pages; string, e.g. `University Project`. |
| `Duration` | No | Display text on cards and details. Quote a bare year: `Duration: "2026"`. |
| `Summary` | No | Project-card description; string. |
| `Skills` | No | String displayed on details. Existing content uses `Python · SQL`; retain that convention. Current cards split only on commas, so a middle-dot string is one card tag. This helper does not change that rendering. |
| `Image` | No | Thumbnail filename under `theme/static/images/projects/`. `Image: ""` selects the existing placeholder. Omitting the field instead defaults to `<slug>.jpg`, which must exist. |
| `Order` | No | Integer for ascending card order; defaults to 999. Existing numeric strings are also accepted by the reader. Avoid decimal values and booleans. |
| `Link` | No | String URL for the card action and the detail-page “View Project” link. Without it, the card action links to the local detail page. |

Copy-paste example:

```markdown
---
Title: My engineering project
# Page Title: A longer project name
Slug: my-engineering-project
Project Type: Personal Project
Duration: "2026"
Summary: What I built and the problem it solves.
Skills: Python · SQL
Image: ""
Order: 6
# Link: https://github.com/example/project
---

# My engineering project

## Overview

Describe the project and its results.
```

## About and collection pages

The existing About document uses only Title then Slug:

```markdown
---
Title: About Me
Slug: about
---

Write your biography in Markdown or raw HTML.
```

**The default `page.html` is About-specific**, with a fixed About browser title,
“About Me” heading, and milestones. Its body comes from the Markdown file, but
Title does not replace those fixed labels. Creating another page with `spg new
page` reuses that same layout; it does not create a new general-purpose design
or add navigation. Edit the existing About file directly for biography updates.
Career milestones still live in `theme/templates/page.html`.

The collection descriptors already exist; these examples are references, not
instructions to overwrite them:

```yaml
---
Title: Blog Posts
Slug: posts
Template: posts
---
```

```yaml
---
Title: Projects
Slug: projects
Template: projects
---
```

`Template` is a template name **without `.html`**. These collection templates
list articles automatically and ignore the descriptor's body. Title and Slug
are required metadata; Template selects the collection layout. No new post or
project requires editing these descriptors.

## Existing shared/advanced fields

The starters include commented examples so you do not have to remember these:

| Field | Existing behavior |
| --- | --- |
| `Category` | Inferred from the first folder under content: posts, projects, or pages. Those are the only values accepted by the custom reader. Omit it normally; overriding it can alter collection behavior. |
| `Template` | Defaults to article for posts, project for projects, page for pages. Override only with a compatible existing template; validate alone cannot check Jinja compatibility. |
| `Date` on projects/pages | Optional; accepted by Pelican, not shown by current project/page templates. Undated projects get an internal 2000-01-01 fallback required by Pelican. It can affect feeds; do not copy it into source files. |
| `Updated` / `Tags` on projects/pages | Accepted by the reader but not displayed by their current templates. |
| `Summary` on pages | Accepted, but not displayed by the current page/collection templates. |

Project-specific strings are also accepted as unused metadata on other content
types; that does not make them visible there. The reader does not maintain a
closed field whitelist: additional metadata passes to Pelican. This guide covers
the existing site's authored fields and reader/theme-supported fields, not every
possible Pelican feature. No unknown-field rejection or new metadata field has
been introduced. Reader normalization of names remains unchanged; use the
existing spellings above for consistency.

## Images, checks, and common mistakes

Shared images: put `diagram.png` in `content/images/`, then write
`![Description](/images/diagram.png)`. Project thumbnails use the Image field
and `theme/static/images/projects/`. Match filename case exactly.

```sh
spg validate  # Fast metadata-only check; reports all invalid files, writes nothing.
spg check     # Full existing Pelican build in temporary output.
```

Validation reuses the unchanged production reader. It checks required fields,
slug format, dates, string fields, Tags, Order, Category, and malformed YAML.
Errors name the source file and field; a nonzero exit code means something needs
fixing. It does not reject unknown fields, enforce a new field order, detect every
typo, check image existence, or guarantee URLs/template behavior. Use the starter
spellings, preview, and run the full build too.

- Missing Title/Slug/Date: copy the exact required field from the matching starter.
- `Duration: 2026` fails: use `Duration: "2026"`.
- A title containing `: ` needs quotes, e.g. `Title: "Python: a practical guide"`.
- `Slug: My_Project` fails: use `Slug: my-project`.
- Use `Tags:` followed by string list items, not numeric or empty list items.
- Use `Order: 6`, not `Order: 6.5` or `Order: true`.
- To omit an optional date, remove/comment its line instead of using an empty value.
- Renaming an existing Slug changes its URL. Do not use starters to replace old
  content or collection descriptors.
