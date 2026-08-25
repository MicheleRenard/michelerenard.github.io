#!/usr/bin/env python3
"""
Regenerate the publication list from ORCID + Crossref.

Reads the public ORCID record, resolves each DOI against Crossref for complete
and correctly-cased metadata, and writes two files:

  references.bib              BibTeX, for reuse in manuscripts and elsewhere
  _publications-generated.md  formatted Markdown, included by publications.qmd

Run it, read the report it prints, then `quarto render`.

    python3 tools/update-publications.py

Nothing here touches the "under review" or "in preparation" sections of
publications.qmd — those have no DOI and stay hand-maintained.
"""

import json
import re
import sys
import urllib.request
from pathlib import Path

ORCID = "0000-0003-4517-1316"
SURNAME = "Renard"
ROOT = Path(__file__).resolve().parent.parent

# DOIs present on the ORCID record that should NOT appear in the peer-reviewed
# list, each with the reason. Anything new that appears in ORCID and is not
# here will be included, and the script will say so.
EXCLUDE = {
    "10.21203/rs.3.rs-6693988/v1":
        "Research Square preprint of the Gaelic football mixed-methods paper "
        "(the peer-reviewed version is still under review)",
    "10.1007/s40279-023-01893-2":
        "Erratum to the menstrual cycle review, not a separate publication",
    "10.1123/ijsnem.2020-0065":
        "Conference abstract collection (ISENC 2019), listed under "
        "conference presentations instead",
}

# Publications known to be missing from ORCID. Keeps them in the list until the
# ORCID record is fixed; remove an entry once ORCID carries it.
ORCID_GAPS = {
    "10.1016/j.appet.2025.108311":
        "Appetite (2025) scoping review — on the CV but absent from ORCID",
}


# Crossref records what publishers deposited, and publishers are inconsistent.
# These three tables correct what comes back. Each is small on purpose: if a
# correction is needed for more than a handful of records, fix it upstream.

# Surnames that some publishers deposit split across the given-name field, so
# "Ó Catháin, Ciarán" arrives as given="Ciarán Ó" family="Catháin".
NAME_FIXES = {
    "Catháin, C. Ó.": "Ó Catháin, C.",
    "Chéilleachair, N. N.": "Ní Chéilleachair, N.",
    "Cheilleachair, N. N.": "Ní Chéilleachair, N.",
}

# Words that survive the conversion of publisher title-case to sentence case.
# Words containing a digit (COVID-19) or written in full caps (PRISMA) are
# protected automatically and do not need listing.
PROTECTED = {
    "Gaelic", "Irish", "Ireland", "United", "Kingdom", "Republic", "British",
    "Singapore", "Singaporean", "European", "Australian", "American", "Asian",
    "English", "African", "Cochrane", "PROSPERO", "Nobel", "I",
}

# Per-DOI overrides for fields Crossref has wrong or is missing. Keys map onto
# the fields used for formatting: year, title, journal, volume, issue, page.
OVERRIDES = {
    # Crossref carries the 2026 print issue; the paper published online in 2025
    # and the CV dates it 2025.
    "10.1016/j.appet.2025.108311": {"year": 2025},
    # Article number, not deposited by the publisher.
    "10.1186/s44410-026-00030-0": {"page": "14"},
}


def fetch(url, accept="application/json"):
    req = urllib.request.Request(url, headers={
        "Accept": accept,
        "User-Agent": f"michelerenard.github.io publication list (ORCID {ORCID})",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def orcid_dois():
    data = fetch(f"https://pub.orcid.org/v3.0/{ORCID}/works")
    dois = []
    for group in data.get("group", []):
        for eid in group.get("external-ids", {}).get("external-id", []):
            if eid.get("external-id-type") == "doi":
                dois.append(eid["external-id-value"].lower())
                break
    return dois


def crossref(doi):
    return fetch(f"https://api.crossref.org/works/{doi}")["message"]


def initials(given):
    parts = re.split(r"[\s\-]+", given.strip())
    out = []
    for p in parts:
        if p:
            out.append(f"{p[0].upper()}.")
    return " ".join(out)


def format_authors(authors):
    """CV house style: surname, initials; ampersand before the last; long author
    lists elided around Renard, M."""
    names, mine = [], None
    for i, a in enumerate(authors):
        family = a.get("family", "").strip()
        given = a.get("given", "").strip()
        name = f"{family}, {initials(given)}" if given else family
        name = NAME_FIXES.get(name, name)
        if family.lower() == SURNAME.lower():
            name = f"**{name}**"
            mine = i
        names.append(name)

    if len(names) > 8:
        head = names[:2]
        tail = [names[-1]]
        middle = []
        if mine is not None and mine >= 2 and mine < len(names) - 1:
            middle = ["…", names[mine], "…"]
        else:
            middle = ["…"]
        parts = head + middle + tail
        out = ""
        for p in parts:
            out += ("" if out.endswith("… ") or not out else ", ") + p
            if p == "…":
                out += " " if not out.endswith(" ") else ""
        return re.sub(r",\s*…\s*,?\s*", ", … ", ", ".join(head + middle + tail)).replace("… , ", "… ")

    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + f", & {names[-1]}"


def year_of(msg):
    if "_override_year" in msg:
        return msg["_override_year"]
    # Print year, which is what the CV uses. Where a paper appeared online in
    # an earlier year and that year is the one of record, use OVERRIDES.
    for key in ("published-print", "published-online", "issued", "created"):
        parts = msg.get(key, {}).get("date-parts", [[None]])
        if parts and parts[0] and parts[0][0]:
            return parts[0][0]
    return 0


def sentence_case(t):
    """Publisher title-case to sentence case, protecting proper nouns."""
    out, start_of_sentence = [], True
    for word in t.split(" "):
        core = word.strip("(),.;:?!\u2019'\"")
        keep = (
            start_of_sentence
            or core in PROTECTED
            or any(c.isdigit() for c in core)
            or (core.isupper() and len(core) > 1)
        )
        out.append(word if keep else word.lower())
        start_of_sentence = word.endswith((":", "?", "!", "."))
    return " ".join(out)


def title_of(msg):
    if "_override_title" in msg:
        return msg["_override_title"]
    t = (msg.get("title") or [""])[0]
    t = re.sub(r"\s+", " ", t).strip()
    return sentence_case(t)


def journal_of(msg):
    if "_override_journal" in msg:
        return msg["_override_journal"]
    c = msg.get("container-title") or [""]
    return c[0].strip()


def apply_overrides(msg):
    """Fold the OVERRIDES table into the record before anything formats it."""
    for field, value in OVERRIDES.get(msg.get("DOI", "").lower(), {}).items():
        if field in ("year", "title", "journal"):
            msg[f"_override_{field}"] = value
        else:
            msg[field] = value
    return msg


def format_entry(msg):
    authors = format_authors(msg.get("author", []))
    year = year_of(msg)
    title = title_of(msg)
    if not title.endswith((".", "?", "!")):
        title += "."
    journal = journal_of(msg)
    bits = f"{authors} ({year}). {title} *{journal}*"
    vol = msg.get("volume")
    issue = msg.get("issue")
    page = msg.get("page")
    if vol:
        bits += f", **{vol}**"
        if issue:
            bits += f"({issue})"
    if page:
        bits += f", {page.replace('-', '–')}"
    doi = msg.get("DOI", "")
    bits += f". [doi:{doi}](https://doi.org/{doi})"
    return bits


def bibtex_key(msg):
    author = (msg.get("author") or [{}])[0].get("family", "anon").lower()
    author = re.sub(r"[^a-z]", "", author)
    word = re.sub(r"[^a-z]", "", title_of(msg).split(" ")[0].lower()) or "untitled"
    return f"{author}{year_of(msg)}{word}"


def bibtex(msg):
    def esc(s):
        return s.replace("&", r"\&").replace("%", r"\%")
    authors = " and ".join(
        f"{a.get('family','')}, {a.get('given','')}".strip(", ")
        for a in msg.get("author", [])
    )
    fields = {
        "author": authors,
        "title": esc(title_of(msg)),
        "journal": esc(journal_of(msg)),
        "year": str(year_of(msg)),
        "volume": msg.get("volume"),
        "number": msg.get("issue"),
        "pages": (msg.get("page") or "").replace("-", "--") or None,
        "doi": msg.get("DOI"),
    }
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields.items() if v)
    return f"@article{{{bibtex_key(msg)},\n{body}\n}}\n"


def main():
    print(f"Reading ORCID {ORCID} …")
    found = orcid_dois()
    print(f"  {len(found)} DOI-bearing records\n")

    wanted, skipped, surprises = [], [], []
    for doi in found:
        if doi in EXCLUDE:
            skipped.append((doi, EXCLUDE[doi]))
        else:
            wanted.append(doi)

    for doi, why in ORCID_GAPS.items():
        if doi not in found:
            wanted.append(doi)
            surprises.append((doi, why))

    records = []
    for doi in wanted:
        try:
            records.append(apply_overrides(crossref(doi)))
            print(f"  ok   {doi}")
        except Exception as e:                                   # noqa: BLE001
            print(f"  FAIL {doi}: {e}", file=sys.stderr)

    records.sort(key=lambda m: (year_of(m), title_of(m)), reverse=True)

    md = ["::: {.pub-list}", ""]
    for i, m in enumerate(records, 1):
        md.append(f"{i}. {format_entry(m)}")
        md.append("")
    md += [":::", ""]
    md_path = ROOT / "_publications-generated.md"
    md_path.write_text(
        "<!-- GENERATED by tools/update-publications.py — do not edit by hand. -->\n\n"
        + "\n".join(md)
    )

    bib_path = ROOT / "references.bib"
    bib_path.write_text(
        "% GENERATED by tools/update-publications.py from ORCID + Crossref.\n\n"
        + "\n".join(bibtex(m) for m in records)
    )

    print(f"\nWrote {md_path.name} and {bib_path.name} — {len(records)} publications.")

    if skipped:
        print("\nDeliberately excluded:")
        for doi, why in skipped:
            print(f"  {doi}\n    {why}")
    if surprises:
        print("\nAdded from the gap list because ORCID does not have them:")
        for doi, why in surprises:
            print(f"  {doi}\n    {why}")
        print("\n  → Fix these at source by adding the work to your ORCID record,")
        print("    then delete the entry from ORCID_GAPS in this script.")
    print("\nNow run: quarto render")


if __name__ == "__main__":
    main()
