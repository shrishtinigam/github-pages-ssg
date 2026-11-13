# My website: how to update it

This is the source for **[shrishtinigam.github.io](https://shrishtinigam.github.io/)**.

**The usual routine: create or edit a file → preview it → check it → push it.**

You do not need to remember the metadata fields or copy generated HTML.
Use the starter commands below.

## First: open the right folder

Open PowerShell and run:

```powershell
cd "C:\Users\DELL\Local Documents\Codex\github-pages-ssg"
```

All commands below run from this folder unless stated otherwise.
They use the Python environment directly, so **you do not need to activate it**.

If you are setting this up on a new computer, follow [First-time setup](#first-time-setup) first.

## 1. Write a blog post

```powershell
.\.venv\Scripts\spg.exe new post "My new blog post"
```

This creates:

```text
content/posts/my-new-blog-post.md
```

Open that file in your editor:

1. Fill in the short description and tags at the top.
2. Replace the example body with your writing.
3. Save the file.

The command fills in the title, URL slug, and today's date. Comments explain the
other fields. Do not leave example text in the file when publishing.

**What is a slug?** The URL-friendly name. For example, `my-new-blog-post`
becomes `/posts/my-new-blog-post/`. Keep a published file's Slug unchanged so
old links keep working.

## 2. Add a project

```powershell
.\.venv\Scripts\spg.exe new project "My new project"
```

Open the new file in `content/projects/`. Fill in its description, skills,
duration, and body.

For a project thumbnail:

1. Put the image in `theme/static/images/projects/`.
2. Set `Image: my-image.jpg` in the project's metadata.

Leave `Image: ""` if you want the existing placeholder instead.
Write a year as `Duration: "2026"`, with quotes.

**Forgot what a field means?** Open [CONTENT_GUIDE.md](CONTENT_GUIDE.md).
Reusable, annotated examples are in [content-templates/](content-templates/).
You never need to copy an old article just to remember its fields.

## 3. Edit something already on the website

All these paths are inside this SSG repository:

| I want to change… | Edit… |
| --- | --- |
| An existing blog post | Its file in `content/posts/` |
| An existing project | Its file in `content/projects/` |
| My About biography | `content/pages/about.md` |
| Homepage introduction, job, or employer | `theme/templates/index.html` |
| Career milestones | `theme/templates/page.html` |
| Email, social links, or footer | `theme/templates/base.html` |
| Site name, author, or description | `pelicanconf.py` |
| Colours, spacing, or other styling | `theme/static/css/style.css` |
| Profile photo | `theme/static/images/profile.png` |

Existing files support both Markdown and raw HTML. You do not need to convert them.

For an image inside a blog post, put it in `content/images/` and reference it like this:

```markdown
![Description of the image](/images/my-diagram.png)
```

The blog/project listing pages update automatically when you add content.
You do not need to edit `content/pages/posts.md` or `content/pages/projects.md`.

There is also a `new page` helper, but the current default page layout is
About-specific. It is not a general-purpose new-page designer. See the content guide.

## 4. Preview the website on my computer

```powershell
.\.venv\Scripts\spg.exe dev
```

Open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser.

- Keep PowerShell open while previewing.
- Edit and save your files.
- The website rebuilds automatically.
- **Refresh the browser** to see the changes.
- Press **Ctrl+C** in PowerShell when finished.

This only shows the site on your computer. It does not publish anything.

If port 8000 is busy:

```powershell
.\.venv\Scripts\spg.exe dev --port 8001
```

Then open http://127.0.0.1:8001/.
Restart preview after changing Python code or `pelicanconf.py`.
For Markdown, CSS, and template edits, saving is enough.

## 5. Check for mistakes before publishing

Stop preview with Ctrl+C, or open another PowerShell window in the same folder.

```powershell
.\.venv\Scripts\spg.exe validate
.\.venv\Scripts\spg.exe check
```

These commands are different:

| Command | What it does | Where do I see the result? |
| --- | --- | --- |
| `validate` | Checks Markdown metadata: missing fields, invalid dates/slugs, incorrect field types, or malformed YAML. It changes no files. | Messages and filenames in PowerShell. |
| `check` | Builds the whole website to catch build errors and warnings. Its temporary output is removed afterward. | Messages in PowerShell. There is no preview page to open. |
| `dev` | Builds and serves a local preview, rebuilding when files change. | Your browser at localhost, plus logs in PowerShell. |
| `build` | Saves a production copy of the generated website to a folder you choose. | Files on disk. It does not publish them. |

**To see the website, use dev. To test whether it builds, use check.**

If a check fails, read the filename and error, fix that file, and run the command again.
Metadata help is in [CONTENT_GUIDE.md](CONTENT_GUIDE.md).

After changing generator code, also run the tests:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

An optional Make-specific test may be skipped on Windows. Make is not required.

## 6. Publish changes to the website

**One-time GitHub setup must be complete first.** See the setup section below.

After editing, previewing, and passing checks:

```powershell
git status
git diff
git add content theme pelicanconf.py
git commit -m "Update website content"
git push origin main
```

What these commands mean:

- `status` lists changed files; `diff` shows what changed.
- `add` selects the changes for your commit.
- `commit` saves a local version.
- `push` sends your commits to GitHub.

These instructions assume you are on `main`. Check with `git branch --show-current`.
If using a feature branch, push that branch and merge its pull request into main
instead. Pull requests run checks but do not publish.

After pushing, GitHub does this:

```text
SSG main changes
    → SSG tests pass
    → website deployment is requested
    → website repository builds and tests the SSG source
    → GitHub Pages publishes the generated site
```

Watch these two Actions pages:

1. [SSG checks](https://github.com/shrishtinigam/github-pages-ssg/actions)
2. [Website deployment](https://github.com/shrishtinigam/shrishtinigam.github.io/actions)

A successful request is not the same as a successful deployment.
Wait for the website's **deploy** job to succeed, then visit the live site.

**You do not need to run build, copy HTML, or edit the deployment repository
for each new post.**

## 7. Push changes to the SSG itself

If you changed Python code, templates, documentation, dependencies, or workflows,
you still work in this same SSG repository.

Run the checks/tests above, then:

```powershell
git status
git diff
git add .
git commit -m "Improve website generator"
git push origin main
```

Review the changes before using `git add .`: it stages all unignored changes,
including any unfinished content. Never commit secrets or API tokens.

Once publishing is configured, an SSG push to main also starts the website
deployment process. Both code and content live in this repository.

## 8. Do I ever need build?

Only if you want a saved production export for inspection or another purpose:

```powershell
.\.venv\Scripts\spg.exe build --output ../my-site-export
```

That creates a sibling folder, outside this repository.
The destination must be empty. Choose a fresh folder for another export;
do not delete an unfamiliar folder just to make the command succeed.

Without `--output`, the default is `../pelican-output/`.
Never point output at either Git repository.

For everyday work, **dev + check + push is enough**.

## First-time setup

### On a new computer

Install Git and Python **3.12** (minimum supported: 3.11).

Clone the SSG if you do not already have it:

```powershell
git clone https://github.com/shrishtinigam/github-pages-ssg.git
cd github-pages-ssg
```

Create the local Python environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

You normally do this once per checkout. Run the install command again after
dependency changes. `constraints.txt` keeps the tested dependency versions
consistent between your computer and GitHub.

On macOS/Linux, use:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
source .venv/bin/activate
spg dev
```

With an activated environment, all the long Windows commands become shorter:
`spg new post "Title"`, `spg validate`, `spg check`, and `spg dev`.
The Windows examples above deliberately work without activation.

### Enable automatic publishing on GitHub — once

There are two repositories:

| Repository | Its job |
| --- | --- |
| `github-pages-ssg` | Your editable content, design, generator, and checks. Work here normally. |
| `shrishtinigam.github.io` | Runs the GitHub Pages deployment workflow. Its older content copies are not the source used by that workflow. |

The automatic workflow needs these steps. Local preview works without them.

**A. Put the prepared changes on GitHub.**

First push the SSG changes using section 7. Then push the accompanying deployment
changes from the website repository:

```powershell
cd "C:\Users\DELL\Local Documents\Codex\shrishtinigam.github.io"
git status
git diff
git add README.md .github/workflows/deploy.yml
git commit -m "Deploy from SSG main"
git push origin main
```

Do this only while those prepared changes are uncommitted; it is not an everyday
publishing step. The updated workflow reads SSG **main**, replacing the old
feature/markdown-ssg branch.

Return to your normal working folder afterward:

```powershell
cd "C:\Users\DELL\Local Documents\Codex\github-pages-ssg"
```

**B. Check the Pages setting.**

In **shrishtinigam.github.io → Settings → Pages**, choose **Source: GitHub Actions**.
Keep your existing domain settings. Any required approval on the github-pages
environment will pause a deployment until approved.

**C. Add the token that connects the two repositories.**

1. In your GitHub account's developer settings, create a **fine-grained personal
   access token**.
2. Set the owner to shrishtinigam and select only **shrishtinigam.github.io**.
3. Grant **Actions: Read and write**. No Contents write permission is needed.
4. Choose an expiration; remember to replace the token when it expires.
5. Open **github-pages-ssg → Settings → Secrets and variables → Actions**.
6. Add a repository secret named **SITE_DEPLOY_TOKEN** containing the token.

Store the token in GitHub Secrets, never in a project file. GitHub documents the
required permission for [workflow dispatch](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event).
The default GITHUB_TOKEN cannot trigger a workflow in this other repository.

**D. Test publishing.**

In the SSG's Actions tab, open **Test Pelican generator**, then **Run workflow**
on main. Confirm the SSG checks and the website's deployment both succeed.
Check the live site afterward.

Until the secret is configured, checks can pass while publishing is skipped
with a warning. An invalid or expired token causes an HTTP error in the publish job.

### Manual publishing fallback

Once both updated workflows are on GitHub, you can publish without the automatic
trigger token:

1. Push your changes to **github-pages-ssg/main**.
2. Open **shrishtinigam.github.io → Actions → Build and deploy portfolio**.
3. Select **Run workflow** on main.
4. Wait for the deploy job to succeed.

This builds the latest SSG main. You still do not copy files manually.

## If something goes wrong

| Problem | What to do |
| --- | --- |
| The spg executable is missing | Check that you are in the SSG folder, then follow first-time environment setup. |
| validate reports a metadata error | Open the named file. Use its starter comments or CONTENT_GUIDE.md to fix the field. |
| check succeeded, but I cannot see anything | Run dev and open localhost. Check only tests the build. |
| My saved change is not visible locally | Wait for rebuilding, then refresh the browser. Look at PowerShell for errors. |
| Port 8000 is already in use | Use dev --port 8001 and open localhost:8001. |
| build says output is not empty | Use dev for preview, or select a fresh export directory. |
| git says nothing to commit | Your files may already be committed, or you may be in the wrong repository. Check git status. |
| Git rejects my push | Check the reported authentication/branch error. Do not force-push to bypass it. |
| The live site did not change | Inspect both Actions pages, the token warning, the website deploy job, and the Pages source setting. |
| I edited content in shrishtinigam.github.io | Make the edit in github-pages-ssg instead; the deployment workflow uses that source. |
| An image is missing | Check its path, filename case, and project Image field. |

## Technical details, when needed

Pelican turns Markdown into a static website. The custom reader validates YAML
metadata; the compatibility adapter supplies existing card fields; Jinja
templates render the layout. CSS and images are copied with the output.

- `pelicanconf.py`: shared site settings.
- `publishconf.py`: production settings.
- `devconf.py`: local preview URLs.
- `portfolio_cli.py`: the spg commands.
- `pyproject.toml` and `constraints.txt`: dependencies and tested versions.

Existing URLs and content formats are preserved. Theme assets publish under
/static/ and shared content images under /images/. Feeds, robots.txt, and
sitemap.xml are generated automatically.

See [CONTENT_GUIDE.md](CONTENT_GUIDE.md) for metadata and
[AUDIT.md](AUDIT.md) for audit evidence and known issues, including missing
original image assets. Local checks do not prove a GitHub deployment succeeded;
the website's deploy job is the confirmation.