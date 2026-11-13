# Website workflow audit

Audited source commit 7dbda2b and deployment-repository commit 0bb2f2a.

## Existing architecture and publishing workflow

The SSG is already a small Pelican implementation, not the older database
system. Its custom reader supports YAML front matter, validates metadata, and
assigns collection routes. A compatibility adapter provides fields expected by
the existing Jinja cards. It is useful compatibility code, not a reason to rewrite.

Three posts, five projects, and three page descriptors generate twelve HTML
routes including the homepage. Existing content mixes Markdown and HTML.
Theme assets become /static/; shared content images become /images/.
Production builds retain the existing permalinks, Atom feed, robots, and sitemap.
All four direct dependencies have active uses: Pelican, Jinja2, Markdown, and
python-frontmatter.

Before changes, spg check used temporary output, and spg build required empty
sibling output. The SSG's Actions workflow ran checks/package tests but did not
deploy. The website repository already deployed Pages artifacts, checking out
the SSG's feature/markdown-ssg branch. Its push/manual triggers did not react to
source pushes. That feature branch and main had identical trees at audit time:
the branch reference was a future maintenance risk, not a failed current build.

The public Actions API confirmed an existing
[successful deployment](https://github.com/shrishtinigam/shrishtinigam.github.io/actions/runs/34512226846).
The live homepage returned successfully. These observations confirm the old
workflow ran, not that the proposed workflow has been deployed.

## Ranked findings and changes

1. **Publishing gap:** added a post-test dispatch and changed the destination
   workflow to consume source main. A narrowly scoped one-time token bridges the
   two repositories; no source migration or new canonical copy is needed.
2. **Preview gap:** added spg dev with local URLs, Pelican's watcher, and Python's
   HTTP server. Disposable output preserves the deliberate protection against
   overwriting unrelated directories. Refresh the browser after rebuilds.
3. **Windows tests:** the original Make-based test failed because Make is absent.
   That shortcut-specific test is now optional; independent CLI/build/preview
   tests cover essential behavior. CI targets Linux and Windows. Make's Python
   executable is quoted for paths containing spaces.
4. **Dependency drift:** added shared runtime constraints and documented Python
   3.12. The package minimum is 3.11, matching the tested Pelican release.
5. **Authoring friction:** added valid post/project starters, slug validation,
   and exclusive file creation. Documented professional-information locations.
6. **Duplicate historical code:** the deployment repo retains old source,
   generator code, and committed HTML not used by its workflow. Its README
   identifies those copies; no historical files were deleted.

## Optional follow-up, intentionally separate

- Supply missing favicon, Open Graph image, and XLM-RoBERTa confusion-matrix PNG.
  Original assets are unavailable in both repositories.
- Replace placeholder LinkedIn/Twitter URLs in homepage JSON-LD with verified
  profiles; consider ISO-format structured-data dates and page-specific social
  metadata. Existing metadata is preserved in this workflow change.
- Professional details span About Markdown, homepage, milestones, and footer.
  Locations are documented. A new data model would broaden the patch.
- The adapter has an unused about_html assignment; the active About template
  reads page.content. This does not break builds.
- Root-relative asset links assume the existing root-domain website. Hosting
  under a repository subpath would require a separate URL migration.

## Verification

- Before changes: production build and spg check passed. Three tests passed;
  one failed because Make was absent.
- After changes: seven tests passed, one optional Make test skipped on Windows.
  Tests exercise real HTTP preview, local links, Markdown/template rebuilding,
  starter creation, and output protections.
- All **29 generated files**, including **12 HTML pages**, were byte-for-byte
  identical to baseline. No output routes/assets added or removed; no source
  content or theme files changed.
- Inspected **246 local href/src references**. Navigation/page links resolve.
  Existing missing targets are the favicon and relative confusion-matrix PNG.
  The Open Graph image is also absent (referenced by meta content, not href/src).
- Both workflows passed **actionlint 1.7.12**. ShellCheck and Pyflakes were
  unavailable and disabled. Python dependency checks passed.
- A distributable wheel built and installed into an isolated target directory.
  Its installed spg command validated the source from outside the checkout;
  its module entrypoint also built production output from there successfully.
- **Not verified remotely:** the new dispatch, GitHub secrets, Pages settings,
  environment protections, or deployment of these changes. Nothing was pushed
  and no live settings were changed.

README.md is the maintenance guide; CONTRIBUTING.md would duplicate it.

## Files changed

In github-pages-ssg:

| File | Change |
| --- | --- |
| portfolio_cli.py | Preview and starter commands; existing output protection retained |
| devconf.py (new) | Local preview URL settings |
| constraints.txt (new) | Tested runtime versions |
| requirements.txt | Apply constraints on normal setup |
| pyproject.toml | Accurate minimum Python version |
| Makefile | Optional preview shortcut and quoted executable paths |
| tests/test_entrypoints.py | Skip only the Make-specific test when unavailable |
| tests/test_workflow.py (new) | Independent CLI and real HTTP preview regression tests |
| .github/workflows/test.yml | Windows/Linux tests and source-to-site dispatch |
| README.md | Returning-maintainer guide and GitHub setup |
| AUDIT.md (new) | Findings, evidence, and verification limits |

In shrishtinigam.github.io:

| File | Change |
| --- | --- |
| .github/workflows/deploy.yml | Use canonical main, shared dependency pins, and tests before deploy |
| README.md | Clarify deployment responsibilities and legacy copies |
