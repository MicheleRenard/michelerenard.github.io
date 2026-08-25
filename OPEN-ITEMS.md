# Open items — before going live

Everything here needs Michèle's decision or input. The site is complete and
renders without them, but should not be published until they are resolved.

## Needs content

- [ ] **Profile photo.** `images/profile.svg` is a placeholder. Replace with a
      real photo (portrait crop, roughly 4:5, at least 800px wide) and update the
      image path in `index.qmd`.
- [ ] **Favicon.** `images/favicon.png` is a generated placeholder mark. Replace
      or remove.

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
- [ ] **Supervisees named on the site.** `research.qmd` does not name them;
      `collaborate.qmd` refers to them only by topic. If you want them named and
      linked, ask each of them first.

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
