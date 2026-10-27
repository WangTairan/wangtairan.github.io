# Tairan Wang — Personal Website

Source for [wangtairan.github.io](https://wangtairan.github.io/), featuring my
research, projects, blog, and CV.

Built with plain HTML, CSS, and JavaScript, and hosted on GitHub Pages.
No framework, package installation, or build step is required.

## Local preview

With Python 3 installed, run from the repository root:

```sh
sh scripts/serve.sh
```

Open [localhost:4173](http://localhost:4173/). Stop the server with `Ctrl+C`.

## Repository layout

```text
static-html/           Published website
  index.html           Home, biography, and news
  projects.html        Publications and projects
  blog/                Articles and blog index
  assets/              Shared stylesheets
  js/                  Search and portrait carousel
  images/blog/         Article covers and figures
  resources/           CV, portraits, papers, letters, logos, and icons
cv/resume.tex          Editable LaTeX CV source
scripts/               Preview, validation, and CV-date utilities
.github/workflows/     Automatic Pages deployment
AGENTS.md              Instructions for coding assistants
```

The website's downloadable CV is `static-html/resources/personal/resume.pdf`.
Compiled CV intermediates and supporting academic records stay local.

## Checks

```sh
git diff --check
python3 scripts/check_local_links.py
python3 -m unittest discover -s scripts -p 'test_*.py'
```

For layout changes, also check desktop and mobile previews.

## Deployment

Push reviewed changes to `master`. GitHub Actions validates the site and
publishes only `static-html/` to GitHub Pages; it also refreshes the static CV
update date. Check the [Actions run](https://github.com/WangTairan/wangtairan.github.io/actions)
to confirm deployment succeeded.

There is no separate deployment branch or manual subtree deployment.
