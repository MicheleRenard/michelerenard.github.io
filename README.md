# Personal website — source and procedure

Public site for Michèle Renard, built with [Quarto](https://quarto.org) and
deployed to GitHub Pages. The `.qmd` files in this directory are the source of
truth; `_site/` is generated output and is never hand-edited.

**Status: live** at <https://michelerenard.github.io> since 25 Aug 2026. Source on
the `main` branch; the rendered site is pushed to `gh-pages` by
`quarto publish gh-pages`. Outstanding items are in `OPEN-ITEMS.md`.

## Layout

```
Website/
├── _quarto.yml           site config — navbar, footer, theme, metadata
├── theme-light.scss      light palette (variables only)
├── theme-dark.scss       dark palette — same variable names, different values
├── theme-rules.scss      all styling rules, shared by both themes
├── index.qmd             home / about
├── research.qmd          research programmes and methods
├── publications.qmd      publication list
├── heat-and-sleep.qmd    plain-language explainer + media kit
├── tools.qmd             open tools and teaching material
├── collaborate.qmd       "working with me"
├── cv.qmd                CV landing page + summary
├── _publications-generated.md   GENERATED from ORCID. Never hand-edit.
├── references.bib        GENERATED from ORCID. Reusable BibTeX.
├── tools/                maintenance scripts (see below)
├── cv/                   public CV PDFs and HTML
├── images/               profile photo, favicon, social preview card
└── _site/                GENERATED. Never edit; gitignored.
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

The repo exists and Pages is configured to serve the `gh-pages` branch. To
publish a change:

```bash
git add -A && git commit -m "..." && git push       # source
python3 -c "" ; quarto publish gh-pages --no-prompt  # rendered site
```

Two gotchas, both already handled but worth knowing if this is ever rebuilt:
`quarto publish gh-pages --no-prompt` fails unless the `gh-pages` branch already
exists (create it as an empty orphan branch first), and GitHub defaults Pages to
serving `main`, which serves the *source* rather than the built site — it has
been switched to `gh-pages`.

A custom domain (e.g. `michelerenard.com`) can be added later by putting the
domain in a `CNAME` file at the repo root and pointing DNS at GitHub. Nothing
else changes.

## The three maintenance scripts

All three are safe to re-run at any time; each prints what it did.

```bash
python3 tools/update-publications.py   # ORCID + Crossref → publication list
python3 tools/build-cv-pdf.py          # ../CV/current/*.md → cv/*.pdf
python3 tools/make-og-image.py         # → images/og-image.png
```

**`update-publications.py`** reads the public ORCID record, resolves each DOI
against Crossref, and writes both `_publications-generated.md` (what the site
renders) and `references.bib` (for reuse). Publishers deposit inconsistent
metadata, so the script carries three small correction tables — `NAME_FIXES` for
surnames split across the wrong field, `PROTECTED` for words that survive the
conversion to sentence case, and `OVERRIDES` for per-DOI fixes. It also carries
`EXCLUDE` (preprints, errata and abstract collections that should not appear as
publications) and `ORCID_GAPS` (papers on the CV but missing from ORCID). Read
what it prints: it tells you what it excluded and why.

**`build-cv-pdf.py`** renders the public CV PDFs from the private Markdown via
Quarto's Typst engine — no LaTeX needed. It never writes to the CV repo. Every
difference between the private CV and the public PDF is declared in the
`REDACTIONS` list at the top of the script, with a reason, and the script prints
each one as it applies it.

**`make-og-image.py`** builds the 1200×630 card that LinkedIn, Slack and email
clients show when the link is shared. Re-run it if the palette, role line or
photo changes.

## Keeping it current

Tie site updates to the **CV cadence — February and August** (see
`../CV/README.md`). The CV update procedure already gathers the evidence; the
site is the last step of the same cycle:

1. Update `../CV/current/master-cv.md` and `short-cv.md` as usual, and run
   `../CV/build.sh`.
2. `cp ../CV/build/*.html cv/` and `python3 tools/build-cv-pdf.py`.
3. `python3 tools/update-publications.py` — the peer-reviewed list looks after
   itself. Then update the **under review** and **in preparation** sections of
   `publications.qmd` by hand, since those have no DOI to fetch.
4. Update the **Currently** and **Recent** sections of `index.qmd`. These are the
   two blocks that make a site look alive or abandoned; if nothing else gets
   done, do these.
5. `quarto render`, check locally in both light and dark, then
   `quarto publish gh-pages`.

Off-cycle, update whenever something lands that you would want on a CV tomorrow
— an accepted paper, a grant, a new role, media coverage.

## Design notes

The theme is split three ways: `theme-light.scss` and `theme-dark.scss` define
the same set of variables with different values, and `theme-rules.scss` holds
every rule. Nothing in the rules file hard-codes a colour, which is what lets one
set of rules serve both themes — keep it that way when editing. The palette is deliberately narrow: warm off-white paper, deep slate ink,
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
