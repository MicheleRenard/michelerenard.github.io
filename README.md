# Personal website — source and procedure

Public site for Michèle Renard, built with [Quarto](https://quarto.org) and
deployed to GitHub Pages. The `.qmd` files in this directory are the source of
truth; `_site/` is generated output and is never hand-edited.

**Status: prototype.** Not yet published. See *Before going live* below.

## Layout

```
Website/
├── _quarto.yml      site config — navbar, footer, theme, metadata
├── styles.scss      the theme. Palette and typography live at the top.
├── index.qmd        home / about
├── research.qmd     research programmes and methods
├── publications.qmd publication list
├── tools.qmd        open tools and teaching material
├── collaborate.qmd  "working with me"
├── cv.qmd           CV landing page + summary
├── cv/              built CV HTML, copied from ../CV/build/
├── images/          profile photo (profile.jpg), favicon
└── _site/           GENERATED. Never edit; gitignored.
```

## Build and preview

Quarto is installed at `~/.local/quarto` with a symlink at `~/.local/bin/quarto`
(the Homebrew cask needs `sudo`, which an automated install cannot supply — to
switch to a system install later, run `brew install --cask quarto` yourself and
delete `~/.local/quarto`).

```bash
export PATH="$HOME/.local/bin:$PATH"

quarto preview     # live-reloading local preview, rebuilds as you edit
quarto render      # one-off build into _site/
```

## Deploying to GitHub Pages

The site is designed to live at `https://michelerenard.github.io`, which requires
a repository named exactly `michelerenard.github.io`.

```bash
gh repo create michelerenard.github.io --public --source=. --remote=origin
git add -A && git commit -m "Initial site"
git push -u origin main
quarto publish gh-pages
```

`quarto publish gh-pages` builds the site and pushes `_site/` to a `gh-pages`
branch, then GitHub serves it. First run asks for confirmation and configures the
branch; later runs are a single command.

A custom domain (e.g. `michelerenard.com`) can be added later by putting the
domain in a `CNAME` file at the repo root and pointing DNS at GitHub. Nothing
else changes.

## Keeping it current

Tie site updates to the **CV cadence — February and August** (see
`../CV/README.md`). The CV update procedure already gathers the evidence; the
site is the last step of the same cycle:

1. Update `../CV/current/master-cv.md` and `short-cv.md` as usual, and run
   `../CV/build.sh`.
2. Copy the rebuilt CV HTML across: `cp ../CV/build/*.html cv/`.
3. Reconcile `publications.qmd` against the master CV — peer-reviewed list,
   under review, in preparation.
4. Update the **Currently** and **Recent** sections of `index.qmd`. These are the
   two blocks that make a site look alive or abandoned; if nothing else gets
   done, do these.
5. `quarto render`, check locally, then `quarto publish gh-pages`.

Off-cycle, update whenever something lands that you would want on a CV tomorrow
— an accepted paper, a grant, a new role, media coverage.

## Design notes

The theme is a single SCSS file with everything configurable in the first 25
lines. The palette is deliberately narrow: warm off-white paper, deep slate ink,
one ember accent for heat and one teal-slate secondary for night. Two accents,
used sparingly, so the typography carries the page.

Headings are Source Serif 4; body text is Inter. Both load from Google Fonts with
system fallbacks.

Custom classes available in any `.qmd`:

| Class | Use |
|---|---|
| `.lead-in` | Larger serif opening paragraph |
| `.eyebrow` | Small-caps ember label above a section |
| `.grid-cards` / `.card-item` | Card grid; add `.night` for the teal variant |
| `.note-box` | Teal-bordered callout |
| `.pub-list` | Numbered publication list with badge numerals |
| `.status-tag` | Small outlined tag, e.g. "Under review" |
| `.btn-ember` / `.btn-outline-ink` | Buttons |

## Privacy

Unlike the CV repo, **this repo is public**. Two rules follow:

- The site carries the institutional email only. No phone number, no home
  address, no residency status — all of which appear in the CV Markdown and must
  not be copied across.
- The built CV HTML in `cv/` is derived from the master CV. Check each rebuild
  for the same details before committing. The site pages and the CV do not say the
  same things — the site describes support for early career researchers rather
  than direct supervision, and omits the Sport Singapore review — so a public
  variant of the CV, with the contact block and those items trimmed, is worth
  maintaining. See OPEN-ITEMS.md.
