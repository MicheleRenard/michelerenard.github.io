# Open items — before going live

Everything here needs Michèle's decision or input. The site is complete and
renders without them, but should not be published until they are resolved.

## Needs content

- [x] **Profile photo.** `images/profile.jpg`, from `~/Downloads/MRENARD Profile
      Picture.jpeg`, resized to 800px wide. Swap the file if you want a different
      shot; no other change needed.
- [ ] **Favicon.** `images/favicon.png` is a generated placeholder mark. Replace
      or remove.

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

- [ ] **Every claim on `collaborate.qmd` is a draft written from the CV, not from
      you.** In particular: what you actually want to receive email about, whether
      you are open to prospective students right now, and the "what I will not be
      much use for" box. Rewrite in your own words before publishing.
- [ ] **The ECRO partnership paragraph.** The site describes the portfolio in
      general terms and does not name the industry partner. Confirm that even this
      framing is appropriate to publish while the pilot is being finalised.
- [ ] **NUS Medicine communications policy.** Check whether there is guidance on
      staff personal sites, use of the NUS name, or describing NRF-funded work.
      Worth doing as an ECRO Lead specifically.
- [ ] **Unpublished figures.** No unpublished results are on the site beyond what
      is already in press releases and public abstracts — but confirm that the
      "122 participants / 10,303 person-nights" framing is fine to state publicly
      before the primary analysis is published.
- [ ] **The public CV PDFs still say more than the site does.** The site no
      longer claims direct supervision and no longer mentions the Sport Singapore
      SEA Games review — but `cv/master-cv.html` and `cv/short-cv.html`, which the
      CV page links publicly, still carry both, along with named supervisees. Those
      files are built from `../CV/current/`, which is yours to decide about. Either
      trim a public variant of the CV or drop the direct links and offer the CV on
      request.

## Decisions

- [ ] **Repository name.** `michelerenard.github.io` gives the clean root URL and
      is the assumption throughout. The alternative is a project repo (e.g.
      `website`) served at `michelerenard.github.io/website/`, which is worse.
- [ ] **Custom domain?** Optional, ~S$20/year, can be added at any time without
      changing anything else.
- [ ] **Blog / notes section?** Deliberately omitted. Easy to add later
      (`quarto` has a listing page type), but an empty or stale blog is worse than
      no blog. Add it only if you actually want to write.
- [ ] **Dark mode?** Quarto supports a light/dark toggle. Omitted to keep the
      prototype focused; roughly half a day to do properly.
- [ ] **Public CV variant.** The CV pages currently link the same HTML as the
      private build, contact block included. Decide whether to trim it (see
      *Privacy* in README.md).

## Known gaps

- The publication list is hand-maintained in `publications.qmd`. It could be
  generated from ORCID/Crossref into a `.bib` file and rendered by Quarto's
  citation support — worth doing at the next update cycle if the manual copy
  proves annoying.
