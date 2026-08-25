# Open items — before going live

Everything here needs Michèle's decision or input. The site is complete and
renders without them, but should not be published until they are resolved.

## Needs content

- [x] **Profile photo.** `images/profile.jpg`, from `~/Downloads/MRENARD Profile
      Picture.jpeg`, resized to 800px wide. Swap the file if you want a different
      shot; no other change needed.
- [ ] **Favicon.** `images/favicon.png` is a generated placeholder mark. Replace
      or remove.

- [ ] **Every number on `heat-and-sleep.qmd` needs your sign-off.** I wrote that
      page from what is already public — the 28°C figure from *The Straits Times*,
      the ~10 minutes per 1°C from *Lianhe Zaobao*, and the 122 participants /
      10,303 person-nights already on the site. The interpretation, the
      "what this does not show" section and the threshold discussion are my
      wording from your CV and research description, not quotes from you. Read it
      as if a journalist were about to quote every sentence, because that is its
      purpose.
- [ ] **The media kit bio is written without pronouns**, because I do not know
      which you use. Set them, or leave it as is — it reads fine either way.

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
