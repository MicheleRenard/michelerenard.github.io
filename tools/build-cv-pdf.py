#!/usr/bin/env python3
"""
Build the public PDF CVs from the private CV Markdown.

Source of truth stays ~/Documents/CV/current/. This script never writes there.
It reads the Markdown, applies the redactions listed in REDACTIONS below, and
renders PDFs into cv/ using Quarto's Typst engine (no LaTeX required).

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
QUARTO = Path.home() / ".local" / "bin" / "quarto"

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
        r = subprocess.run(
            [str(QUARTO), "render", str(qmd), "--to", "typst"],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            print(r.stdout[-3000:], r.stderr[-3000:], file=sys.stderr)
            sys.exit(f"quarto failed on {name}")
        pdf = tmp / f"{name}.pdf"
        if not pdf.exists():
            sys.exit(f"no PDF produced for {name}")
        OUT.mkdir(exist_ok=True)
        shutil.copy(pdf, OUT / f"{name}.pdf")
        kb = (OUT / f"{name}.pdf").stat().st_size // 1024
        print(f"    → cv/{name}.pdf ({kb} KB)\n")


if __name__ == "__main__":
    print(f"Reading {CV_SRC}\n")
    for n in ("master-cv", "short-cv"):
        build(n)
    print("Done. Check both PDFs before publishing — see OPEN-ITEMS.md.")
