# Maintenance instructions

## Scope and source of truth

- Edit the framework-free site directly in `static-html/`. Do not introduce a
  package manager, build pipeline, or templating system for routine edits.
- See `README.md` for the repository map, preview, checks, and deployment.
  Keep it visitor-facing; maintain assistant-specific rules here.
- Preserve unrelated work. Do not replace public binary assets or publish
  local supporting records unless requested. Everything in `static-html/`,
  including portrait originals, is intentionally public.

## Content

- Keep projects newest first. Maintain each `.project-block`'s `data-title`,
  `data-authors`, `data-tags`, and `data-date` for search. Dates need not be
  displayed. Use original project dates, not later awards or acceptances;
  store submission, acceptance, and award events separately. An arXiv submission
  date does not establish when research began.
- Start research tags with the arXiv primary subject where applicable, followed
  by a few specific, defensible topics. Preserve `arXiv` capitalization and
  bold `Tairan Wang` in displayed authors, not plain search metadata.
- Local paper downloads are labelled `PDF`, followed by `arXiv` where available
  and `Conference` for accepted papers with a verified paper-specific page.
  Retain dedicated thesis/presentation labels and icon classes. Use the existing
  monochrome SVG icons in `resources/icons/`, not emoji.
- News is manually maintained, newest first, with semantic event dates and
  project-anchor links where relevant. Display months while preserving known
  exact dates in metadata. Preserve its capped, scrollable responsive layout.
- One blog card per article, even with translations. Maintain `data-title`,
  `data-desc`, and `data-tags`, including translated search terms; use optional
  `data-article` and `data-languages` for multilingual articles. Link to the
  default language and put a normal-link `.language-switch` inside each
  translation, with `lang`, `hreflang`, and `aria-current="page"`. Omit the
  switcher for single-language articles.
- Keep blog assets under `images/blog/<article>/`; no shared `common/` folder.
  Preserve pre-rendered KaTeX and its CSS dependencies, including large
  one-line HTML sections.
- New-window links require `rel="noopener noreferrer"` alongside
  `target="_blank"`. Preserve local link paths when moving assets.

## Shared styles and layout

- All pages load `assets/style.css`, which imports base, layout, and component
  layers. Use the appropriate existing layer and `--site-*` tokens in
  `base.css`; scope generic class names such as `.description` to components.
- Ordinary anchors inherit global colour, hover, and keyboard-focus styles.
  `default-link` is a component hook, not required for basic link styling.
  Navigation, cards, News, logos, and social buttons have intentional overrides.
- Update the shared CSS version query in all HTML pages and all three imports
  together. The style tests check consistency. BTTF translations share
  `assets/blog-bttf.css`, scoped to `.bttf-article`, without global overrides.
- Navigation is duplicated: update Home, Projects, the blog index, and every
  article together. Keep the site usable without JavaScript except optional
  enhancements such as search and carousel controls.
- Check desktop and mobile after layout edits: navigation wraps only when
  links cannot fit; badges never break internally; search aligns with cards;
  blog titles/descriptions stay clamped to two lines; portraits and biography
  do not overlap.

## Portraits

- Store untouched sources in `resources/personal/portraits/originals/` and
  900×1200 (3:4) crops in `display/`, with month-based filenames. Home uses
  only display crops in newest-first `.photo-slide` figures, with ISO
  `data-date`, descriptive `data-label`, and dated captions.
- Keep the shared 225×300 desktop frame, natural proportions, and consistent
  head size/top clearance. Crop using ordinary image tools; do not retouch or
  regenerate faces, stretch photos, or add per-photo CSS crop offsets.
- Existing crop rectangles `(x, y, width, height)` before resizing:
  September 2026 `(15, 210, 990, 1320)`; June 2025 `(440, 350, 2040, 2720)`.
- Preserve carousel dots, keyboard navigation, and native touch scrolling.
  Latest portrait is the default; no autoplay.

## CV

- Edit `cv/resume.tex` in place. Track TeX source, not compiler artifacts or
  local `cv/resume.pdf`. Keep `cv/supporting-documents/` private and ignored.
- Compile and visually inspect the current document, then explicitly export
  it to `static-html/resources/personal/resume.pdf`. An editor preview alone
  does not update the website download. Keep biography edits separately scoped.
- Use `\cvLink` for dark-blue underlined links and `\cvResource` for upright,
  square-bracketed resource labels. Research links start with `[PDF]` pointing
  directly to the PDF, then `[arXiv]` or a linked venue name. Keep authorship
  labels separate and upright; do not rely on viewer-specific link borders.
- Include months in research dates; use actual research periods when known.
  HoarePrompt's period is May 2024–Jan 2025, not its award or acceptance date.
- After replacing the published PDF, run `python3 scripts/update_resume_date.py`.
  It generates the Home date in `D Mon YYYY` using the PDF's last content-change
  commit in London time (local mtime for an uncommitted PDF). Preserve full
  Actions checkout history; do not substitute deployment time or browser fetching.

## Verification and publishing

- Run the checks in `README.md`; check JavaScript syntax for JS edits. Inspect
  affected pages at desktop and narrow mobile widths for visual changes.
- Commit/push only when requested. A push to `master` automatically deploys
  through `.github/workflows/deploy-pages.yml`; confirm the matching Actions
  run succeeds before reporting deployment complete.
- Only `static-html/` is uploaded. Keep validation and least-privilege deploy
  permissions intact. Do not recreate `gh-pages`, use the old subtree workflow,
  or force-push `master`.
