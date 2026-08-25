#!/usr/bin/env python3
"""
Build the public CVs (PDF and HTML) from the private CV Markdown.

Source of truth stays ~/Documents/CV/current/. This script never writes there.
It reads the Markdown, applies the redactions listed in REDACTIONS below, and
renders into cv/ — PDF via Quarto's Typst engine (no LaTeX required) and a
self-contained HTML version for reading in the browser. BOTH come from the same
redacted source, so they cannot drift apart.

    python3 tools/build-cv-pdf.py

Every redaction is declared, with a reason, so the difference between the
private CV and the public one is auditable rather than implicit.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CV_SRC = Path.home() / "Documents" / "CV" / "current"
OUT = ROOT / "cv"


def find_quarto():
    """Prefer a system Quarto (Homebrew, /usr/local/bin) and fall back to the
    user-local copy under ~/.local. Either works; this just means the script
    keeps running whichever way Quarto is installed."""
    found = shutil.which("quarto")
    if found:
        return found
    for candidate in (
        Path("/usr/local/bin/quarto"),
        Path("/opt/homebrew/bin/quarto"),
        Path.home() / ".local" / "bin" / "quarto",
    ):
        if candidate.exists():
            return str(candidate)
    sys.exit("Quarto not found. Install it with: brew install --cask quarto")


QUARTO = find_quarto()

# (pattern, replacement, reason). Patterns are regexes applied to the raw
# Markdown with re.MULTILINE | re.DOTALL.
REDACTIONS = [
    (r"\s*\|\s*\+65 8058 9233", "",
     "mobile number — the site carries the institutional email only"),
    (r"Singapore \(Permanent Resident\)", "Singapore",
     "residency status is not public information"),
    (r"\*\*External Reviewer\*\* — Sport Singapore.*?heat resilience roadmap\.\n\n", "",
     "Sport Singapore / SEA Games review, removed from the public site at "
     "Michèle's request"),
    (r"\s*External reviewer, Sport Singapore SEA Games 2025 heat resilience report ·", "",
     "same, in the short CV's service line"),
    (r"\s*External reviewer, Sport Singapore SEA Games 2025 Heat Resilience Report\.", "",
     "same, alternative casing"),
]

HEADER = """---
from: markdown+hard_line_breaks
format:
  typst:
    papersize: a4
    margin:
      x: 1.9cm
      y: 1.9cm
    fontsize: 9.5pt
    mainfont: "Georgia"
    colorlinks: true
    linkcolor: '#8F411F'
  html:
    theme: cosmo
    embed-resources: true
    toc: true
    toc-depth: 2
    fontsize: 1rem
    linkcolor: '#8F411F'
toc: false
---

"""


def redact(text, label):
    applied = []
    for pattern, replacement, reason in REDACTIONS:
        new, n = re.subn(pattern, replacement, text, flags=re.M | re.S)
        if n:
            applied.append(f"    − {reason}  ({n}×)")
            text = new
    print(f"  {label}:")
    print("\n".join(applied) if applied else "    (nothing matched)")
    return text


def build(name):
    src = CV_SRC / f"{name}.md"
    if not src.exists():
        sys.exit(f"missing {src}")
    text = redact(src.read_text(), src.name)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        qmd = tmp / f"{name}.qmd"
        qmd.write_text(HEADER + text)
        OUT.mkdir(exist_ok=True)

        for fmt, ext in (("typst", "pdf"), ("html", "html")):
            r = subprocess.run(
                [QUARTO, "render", str(qmd), "--to", fmt],
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                print(r.stdout[-3000:], r.stderr[-3000:], file=sys.stderr)
                sys.exit(f"quarto failed on {name} ({fmt})")
            produced = tmp / f"{name}.{ext}"
            if not produced.exists():
                sys.exit(f"no {ext.upper()} produced for {name}")
            shutil.copy(produced, OUT / f"{name}.{ext}")
            kb = (OUT / f"{name}.{ext}").stat().st_size // 1024
            print(f"    → cv/{name}.{ext} ({kb} KB)")
    print()


def verify():
    """Nothing redacted may survive into anything in cv/. Fail loudly if it does."""
    import fitz

    tripwires = ["8058", "9233", "Permanent Resident", "SEA Games", "Sport Singapore"]
    bad = []
    for f in sorted(OUT.iterdir()):
        if f.suffix == ".pdf":
            text = "".join(page.get_text() for page in fitz.open(f))
        elif f.suffix in (".html", ".md"):
            text = f.read_text(errors="ignore")
        else:
            continue
        for t in tripwires:
            if t in text:
                bad.append(f"{f.name}: contains {t!r}")
    if bad:
        print("REDACTION CHECK FAILED:", file=sys.stderr)
        for b in bad:
            print(f"  {b}", file=sys.stderr)
        sys.exit(1)
    print("Redaction check passed: no private details in anything under cv/.")


if __name__ == "__main__":
    print(f"Reading {CV_SRC}\n")
    for n in ("master-cv", "short-cv"):
        build(n)
    verify()
    print("Done. Check the output before publishing — see OPEN-ITEMS.md.")
