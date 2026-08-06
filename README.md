# Personal Homepage — Agent Maintenance Guide

This repository contains Tairan Wang's personal homepage. It is a small,
framework-free static site intended to be edited directly and published with
GitHub Pages.

## Source of truth

All deployable files live in `static-html/`. There is no package manager,
template engine, build step, or generated `dist/` directory. Changes should be
made directly to the HTML, CSS, and JavaScript files in that directory.

```text
static-html/
├── index.html                  Home and biography
├── projects.html               Publications and projects
├── blog/
│   ├── index.html              Blog index
│   └── *.html                  Rendered blog articles
├── assets/
│   ├── style.css               Stylesheet entry point
│   ├── base.css                Global element styles
│   ├── layout.css              Navigation and page layout
│   └── components.css          Cards, tags, badges, and search controls
├── js/
│   ├── project-search.js       Client-side project filtering
│   └── blog-search.js          Client-side blog filtering
├── images/
│   └── blog/                   Covers and article-specific figures
└── resources/
    ├── personal/               Résumé, profile photo, and site logo
    ├── letters/                Recommendation letters
    ├── publications/           Local papers and presentation files
    ├── brands/                 Organization and company logos
    └── icons/                  Site and social icons
```

## Editing conventions

- Keep the site dependency-light and usable without JavaScript, except for the
  optional search filters.
- Navigation markup is duplicated across pages. If navigation changes, update
  `index.html`, `projects.html`, `blog/index.html`, and every blog article.
- All pages load `assets/style.css`, which imports the three CSS layers listed
  above. Put new rules in the most specific existing layer.
- Project search reads `data-title`, `data-authors`, and `data-tags` from every
  `.project-block`. Keep those attributes in sync with visible content.
- Blog search similarly reads `data-title`, `data-desc`, and `data-tags` from
  every `.card`.
- Use an arXiv primary subject as the first research tag where applicable, then
  add only specific, defensible topic tags.
- Preserve publication-name capitalization such as `arXiv` and prevent compact
  status badges from breaking internally across lines.
- Bold `Tairan Wang` in displayed project author lists, but keep search metadata
  as plain lowercase text.
- External links must use `target="_blank"` together with
  `rel="noopener noreferrer"`.
- Blog articles contain pre-rendered KaTeX markup and load KaTeX CSS from a CDN.
  Treat these files carefully: large one-line sections are expected.
- Keep blog figures inside the corresponding `images/blog/<article>/` folder.
  Do not introduce a shared `images/blog/common/` directory; duplicate small
  shared figures into each article folder so every article owns its resources.
- Binary assets such as the résumé, letters, profile photo, and logo are public
  site content. Do not replace them unless the task explicitly requests it.

## Local preview

From the repository root, run:

```sh
python3 -m http.server 4173 -d static-html
```

Then open:

- Home: <http://localhost:4173/>
- Projects: <http://localhost:4173/projects.html>
- Blog: <http://localhost:4173/blog/>

Check both desktop and narrow mobile widths after layout changes. At minimum,
confirm that navigation wraps only when its links no longer fit, search fields
align with their cards, status badges do not break internally, and all local
links and images resolve.

Useful non-visual checks:

```sh
git diff --check
python3 scripts/check_local_links.py
curl -I http://localhost:4173/
curl -I http://localhost:4173/projects.html
curl -I http://localhost:4173/blog/
```

## Publishing

The complete repository is kept on `master`. GitHub Pages serves the root of a
generated `gh-pages` branch containing only `static-html/`.

Commit and push the source first:

```sh
git add -A
git commit -m "update site"
git push origin master
```

Then publish the static subtree:

```sh
git subtree split --prefix static-html -b gh-pages
git push -f origin gh-pages
git branch -D gh-pages
```

Before creating the temporary branch, check that a local `gh-pages` branch does
not already exist. Force-pushing is limited to this generated deployment branch;
never force-push `master`.
