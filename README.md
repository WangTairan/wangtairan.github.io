# Personal Homepage — Agent Maintenance Guide

This repository contains Tairan Wang's personal homepage. It is a small,
framework-free static site intended to be edited directly and published with
GitHub Pages.

## Source of truth

All deployable files live in `static-html/`. There is no package manager,
template engine, build step, or generated `dist/` directory. Changes should be
made directly to the HTML, CSS, and JavaScript files in that directory.

The editable CV source is maintained separately in `cv/resume.tex`; only its
published PDF belongs in the website resources. Do not move the source or
supporting academic records into `static-html/`.

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

### CV maintenance

```text
cv/
├── resume.tex                  Version-controlled editable source
├── resume.pdf                  Local compiled PDF (ignored)
├── build/                      Existing compiler artifacts (ignored)
└── supporting-documents/        Local transcript and certificate (ignored)
```

Edit `cv/resume.tex` when updating the CV. LaTeX source should be committed;
compiler logs, caches, and intermediate files should not. Keep supporting
academic records local unless their publication is explicitly requested.
Compile and inspect the PDF before copying it to
`static-html/resources/personal/resume.pdf`, the stable website download URL.
The editor's PDF preview does not automatically replace the downloadable
résumé. Whenever a CV update is published, export the approved current document
and update the website PDF explicitly. Source and website biography are
maintained separately; do not silently rewrite either during file imports.

### Website conventions

- Keep the site dependency-light and usable without JavaScript, except for the
  optional search filters.
- Home includes a manually maintained News panel, ordered newest first. Use
  semantic dates and link news items to project anchors where relevant. Its
  height is capped for scrolling; it sits beside the introduction on desktop
  and below it on narrower screens.
- Portraits live in `resources/personal/portraits/`, with untouched source files
  in `originals/` and 900×1200 (3:4) cropped files in `display/`, using
  month-based filenames such as `profile-2026-09.png`. Home references only
  `display/`. Add `.photo-slide` figures newest first in
  Home, with ISO `data-date`, a descriptive `data-label`, and a dated caption.
  The first (latest) portrait is the default; `photo-carousel.js` creates dots
  for all slides, supports keyboard navigation, and keeps the active dot in
  sync with native touch scrolling. Do not autoplay or stretch portraits.
  Crop files with ordinary image tools, aligning head size and top clearance;
  do not regenerate or retouch faces. Keep the shared 3:4 `.photo-frame` at
  225×300 on normal screens, without per-photo CSS crop offsets.
  Current source crop rectangles (x, y, width, height): September 2026 uses
  (15, 210, 990, 1320); June 2025 uses (440, 350, 2040, 2720), then downsamples
  to 900×1200. Original dimensions and bytes must remain unchanged.
- Navigation markup is duplicated across pages. If navigation changes, update
  `index.html`, `projects.html`, `blog/index.html`, and every blog article.
- All pages load `assets/style.css`, which imports the three CSS layers listed
  above. Put new rules in the most specific existing layer.
- Project search reads `data-title`, `data-authors`, `data-tags`, and `data-date`
  from every `.project-block`. Keep those metadata attributes accurate; project
  dates are stored for ordering and search but are not displayed.
  Use the project's original date, not later acceptance or award dates, for
  `data-date`; retain submission, acceptance, and award dates as separate event
  attributes. An arXiv first-submission date is a public record, not proof of
  when the underlying research began.
- Blog search similarly reads `data-title`, `data-desc`, and `data-tags` from
  every `.card`.
- Each article has one blog card, regardless of how many translations it has.
  Link the card to its default language (English for BTTF); include translated
  titles and keywords in search metadata. Optional `data-article` and
  `data-languages` attributes identify the article and its available versions.
  Multilingual articles include a `.language-switch` inside the article, with
  normal links to available versions, `lang`/`hreflang` language codes, and
  `aria-current="page"` on the current version. This works without JavaScript
  and supports any number of versions. Single-language articles omit the
  switcher entirely; do not create duplicate cards for translations.
- Use an arXiv primary subject as the first research tag where applicable, then
  add only specific, defensible topic tags.
- Preserve publication-name capitalization such as `arXiv` and prevent compact
  status badges from breaking internally across lines.
- Bold `Tairan Wang` in displayed project author lists, but keep search metadata
  as plain lowercase text.
- External links must use `target="_blank"` together with
  `rel="noopener noreferrer"`.
- Research papers use `Paper` for the local PDF and a separate `arXiv` link
  for the public abstract page when available. Theses and presentations without
  a corresponding public paper page retain their local links only.
- Project links use custom SVG icons from `resources/icons/` via the
  `paper-link`, `arxiv-link`, `thesis-link`, and `presentation-link` classes.
  Keep these monochrome, consistently sized icons instead of emoji.
- Accepted papers also use a `Conference` link with `conference-link` when an
  official paper-specific conference page is publicly accessible.
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

The complete repository is kept on `master`. The workflow at
`.github/workflows/deploy-pages.yml` automatically validates and deploys the
website on every push to `master`. It can also be run manually from the Actions
tab (select `master`). No framework build or dedicated deployment branch is
needed.

The workflow checks local HTML/CSS references and JavaScript syntax, then
uploads **only `static-html/`** as the Pages artifact. README, maintenance
scripts, workflow configuration, and Git history are not website files.
All public assets inside `static-html/`, including portrait originals, remain
included intentionally. A failed validation prevents deployment.

### One-time migration

1. Open the repository's **Settings → Pages → Build and deployment**.
2. Change **Source** from **Deploy from a branch** to **GitHub Actions**.
3. Commit and push the workflow to `master`, or run **Deploy website to GitHub
   Pages** manually from Actions if it was already pushed.
4. Wait for both jobs to pass, then verify the homepage, Projects, and Blog.
   If the `github-pages` environment has branch restrictions inherited from
   the old deployment, allow `master` in **Settings → Environments**.

No personal access token or added repository secret is required. Validation has
read-only source access; only the deployment job has Pages and OIDC permissions.
After the first successful Actions deployment has been verified, remove the
legacy remote `gh-pages` branch. It is no longer a publishing source or part of
the routine workflow. Do not recreate it or use the old subtree/force-push
procedure. Never remove `master` during deployment cleanup.

### Routine publishing

After reviewing changes and running the local checks, commit and push:

```sh
git add -A
git commit -m "update site"
git push origin master
```

That push starts deployment automatically. Check the Actions run for success
and the deployed URL; do not report the site as updated merely because a push
succeeded. Concurrent publishes are serialized so an active deployment is not
interrupted. Never force-push `master`.
