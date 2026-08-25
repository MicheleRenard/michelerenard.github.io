# Open items

**The site went live on 25 Aug 2026 at <https://michelerenard.github.io>.**
Everything below is still outstanding and now applies to a public page, so these
are live-site edits rather than pre-launch checks.

## Needs content

- [x] **Profile photo.** `images/profile.jpg`, from `~/Downloads/MRENARD Profile
      Picture.jpeg`, resized to 800px wide. Swap the file if you want a different
      shot; no other change needed.
- [ ] **Favicon.** `images/favicon.png` is a placeholder mark I generated — an
      ember circle over a night bar. Fine to leave; replace if you want something
      of your own. Regenerate nothing: it is a plain PNG.

- [ ] **The plain-language explainer and media kit are on hold** until the
      underlying work is finalised. The page was written and then removed at
      commit `f0d2f5a`; recover it with
      `git show 474bf7a:heat-and-sleep.qmd > heat-and-sleep.qmd`, then restore the
      navbar entry in `_quarto.yml` and the two links (in `index.qmd` and
      `collaborate.qmd`). Before it goes back, every number on it needs checking
      against what is published by then, and the interpretation needs rewriting in
      your words. Note the media kit — headshot, bios, topics — went with it, and
      does not depend on the findings; say the word and I will bring back just
      that part.

## Needs confirmation

- [x] **`collaborate.qmd` reviewed and approved as written** (25 Aug 2026). The
      draft stands; no rewrite needed.
- [ ] **The ECRO partnership paragraph.** The site describes the portfolio in
      general terms and does not name the industry partner. Confirm that even this
      framing is appropriate to publish while the pilot is being finalised.
- [x] **NUS Medicine communications** — checked 25 Aug 2026. No issue with
      holding a personal site from the School's perspective.
- [ ] **The "122 participants / 10,303 person-nights" framing is now live** on the
      home page and research page. It was already public via the June 2026 press
      coverage and conference abstracts, so this is not a new disclosure — but it
      is worth a second look now that it sits on a page under your own name.
- [ ] **The public CV PDFs still say more than the site does.** The site no
      longer claims direct supervision and no longer mentions the Sport Singapore
      SEA Games review — but `cv/master-cv.html` and `cv/short-cv.html`, which the
      CV page links publicly, still carry both, along with named supervisees. Those
      files are built from `../CV/current/`, which is yours to decide about. Either
      trim a public variant of the CV or drop the direct links and offer the CV on
      request.

## Decisions

- [x] **Repository name** — `michelerenard.github.io`, giving the clean root URL.
      Decided and created 25 Aug 2026.
- [ ] **Custom domain?** Optional, ~S$20/year, can be added at any time without
      changing anything else.
- [ ] **Blog / notes section?** Deliberately omitted. Easy to add later
      (`quarto` has a listing page type), but an empty or stale blog is worse than
      no blog. Add it only if you actually want to write.
- [x] **Dark mode** — built 25 Aug 2026. `theme-light.scss` and `theme-dark.scss`
      define the same variables; `theme-rules.scss` is shared.
- [x] **Public CV variant** — `tools/build-cv-pdf.py` now generates redacted PDF
      *and* HTML from the private Markdown, with a check that fails the build if
      anything redacted survives. The one remaining decision is the supervision
      language, above.

## Known gaps

- The publication list is hand-maintained in `publications.qmd`. It could be
  generated from ORCID/Crossref into a `.bib` file and rendered by Quarto's
  citation support — worth doing at the next update cycle if the manual copy
  proves annoying.
