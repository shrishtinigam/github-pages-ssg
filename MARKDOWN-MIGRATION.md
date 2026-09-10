# Markdown migration

The portfolio website now has a Markdown-first generator on the
`feature/markdown-ssg` branch of the website repository. The intended authoring
workflow is:

```text
content/posts/*.md
content/projects/*.md
content/images/*
        ↓
python -m sitegen.cli build
        ↓
output/
```

This legacy generator remains available for historical reference. New site
content should use Markdown front matter and the generator maintained with the
website build.
