#!/usr/bin/env python3
"""Build _cv/Chenguang_Pan_CV.pdf from the Word CV, minus the parts that should not be public.

Usage (from the repository root):
    python3 _cv/build_cv_pdf.py                      # uses the default source path below
    python3 _cv/build_cv_pdf.py path/to/CV.docx      # or point it at another .docx
    python3 _cv/build_cv_pdf.py --html /tmp/cv.html  # also keep the intermediate HTML, to eyeball it

What it does
    1. pandoc converts the .docx to an HTML fragment (headings, tables and hyperlinks survive).
    2. Three redactions, because this PDF is intended for a public website even while it
       is parked in `_cv/`:
         - the personal phone number in the contact line
         - the References section, with the referees' names, titles and email addresses,
           replaced by "Available on request."
         - the appositive that names the mentees in the research-mentoring entry, so the PDF
           says "two doctoral students" like the homepage does
    3. Post-checks run unconditionally and the build FAILS rather than publishing a leak:
         - no email address survives except the author's own, from the contact block
         - no phone-number-shaped string survives
         - no personal names survive in the mentoring entry
       Each redaction is also declared required, so a source rewording that breaks a pattern
       stops the build instead of silently publishing more than intended.
    4. The fragment is wrapped in a print stylesheet and Chrome prints it to PDF.

Everything here is pattern-based on purpose: this repository is public, so the script must not
name the people it is redacting.

The folder is named `_cv`, and Jekyll never publishes a directory whose name starts with `_`,
so this script AND the PDF it writes stay out of the built site. Publishing is a separate,
deliberate step: copy the PDF into `files/` and link it from _pages/cv.md.

What it deliberately KEEPS: the author's own institutional email (conventional on a CV, and the
site already publishes an address) and the dollar amounts of his own awards (also conventional).

Requirements: pandoc (conda install -c conda-forge pandoc) and Google Chrome.
"""
from __future__ import annotations

import html
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))
DEFAULT_SRC = os.path.join(
    os.path.dirname(REPO),
    "CV_Resume",
    "CV_ChenguangPan_V5_0_Academic_NotreDame.docx",
)
# Written inside `_cv/`, which Jekyll never publishes. To publish it: copy the PDF to
# `files/` (whitelisted in _config.yml, so it serves at /files/<name>) and link it from
# _pages/cv.md. Kept unpublished by default so the file cannot go live by accident.
OUT_PDF = os.path.join(REPO, "_cv", "Chenguang_Pan_CV.pdf")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Section headings in the .docx are plain bold paragraphs; promote them to real headings.
HEADING_RE = re.compile(r"^<p><strong>([^<]+)</strong></p>$", re.M)
SUBHEADS = {
    "Peer-Reviewed Journal Articles",
    "Manuscripts Under Review",
    "Conference Proceedings and Technical Reports",
    "Conference Presentations",
    "Practitioner Publications",
}

PHONE_RE = re.compile(r"\s*\|?\s*\+\d[\d\s().-]{7,}\d")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.\w{2,}")
# "<N> doctoral students, Firstname Lastname and Firstname Lastname," -> drop the name list.
MENTEE_RE = re.compile(
    r"(doctoral students),\s*(?:<[^>]+>)*[A-Z][\w.-]+(?:\s+[A-Z][\w.-]+)+"
    r"(?:\s+and\s+[A-Z][\w.-]+(?:\s+[A-Z][\w.-]+)+)*\s*,\s*"
)
# A heading whose visible text is "References", however pandoc wrapped it.
REFS_RE = re.compile(
    r"<(p|h[1-6])\b[^>]*>(?:\s|<[^>]+>)*References(?:\s|<[^>]+>)*</\1>\s*(.*?)"
    r"(?=<(?:p|h[1-6])\b[^>]*>(?:\s|<[^>]+>)*[A-Z][^<]*(?:\s|<[^>]+>)*</(?:p|h[1-6])>|\Z)",
    re.S | re.I,
)

CSS = """
@page { size: letter; margin: 0.62in 0.7in; }
* { box-sizing: border-box; }
body {
  margin: 0; font-family: "Source Serif 4", "Source Serif Pro", Palatino, "Palatino Linotype", Georgia, serif;
  font-size: 9.9pt; line-height: 1.34; color: #111; -webkit-print-color-adjust: exact;
}
h1 { font-size: 20pt; letter-spacing: 0.01em; margin: 0 0 2pt; font-weight: 700; }
.affil { margin: 0; font-size: 10pt; }
.contact { margin: 1pt 0 0; font-size: 9.4pt; color: #333; }
.updated { margin: 1pt 0 0; font-size: 8.4pt; color: #666; font-style: italic; }
.rule { border: 0; border-top: 1.1pt solid #111; margin: 7pt 0 8pt; }
h2 {
  font-size: 9.2pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;
  margin: 11pt 0 3pt; padding-bottom: 1.5pt; border-bottom: 0.5pt solid #999;
  break-after: avoid; page-break-after: avoid;
}
h2:first-of-type { margin-top: 4pt; }
h3 {
  font-size: 9.6pt; font-weight: 700; font-style: italic; margin: 7pt 0 2pt;
  break-after: avoid; page-break-after: avoid;
}
p { margin: 0 0 2.5pt; orphans: 2; widows: 2; }
ul { margin: 0 0 3pt; padding-left: 13pt; }
li { margin: 0 0 1.5pt; break-inside: avoid; page-break-inside: avoid; }
li > p { margin: 0 0 1pt; }
li ul { margin-top: 1pt; padding-left: 12pt; }
li li { color: #222; }
blockquote { margin: 0 0 3pt; padding: 0; }
table { width: 100%; border-collapse: collapse; margin: 0 0 2pt; }
col:first-child { width: 82%; }
td, th {
  vertical-align: top; text-align: left; font-weight: normal; padding: 0 0 2pt;
  break-inside: avoid; page-break-inside: avoid;
}
td[style*="right"], th[style*="right"] {
  text-align: right !important; white-space: nowrap; font-size: 9.2pt; color: #333; padding-left: 8pt;
}
thead th { border: 0; }
a { color: #1a3f6f; text-decoration: none; }
.refs { font-style: italic; color: #333; }
"""


def die(msg: str) -> None:
    sys.exit("REFUSING TO BUILD: " + msg)


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if p.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd[:3])}…\n{p.stdout}\n{p.stderr}")
    return p


def scrub(frag: str) -> tuple[str, list[str], set[str]]:
    """Redact everything that must not be public. Returns (html, removals, author_emails)."""
    removed: list[str] = []

    # The author's own contact block is the first three paragraphs; its addresses are allowed
    # to stay. Every other address in the document must be gone by the end of this function.
    head = "".join(re.findall(r"<p>.*?</p>", frag, re.S)[:3])
    author_emails = set(EMAIL_RE.findall(head))
    if not author_emails:
        print("  note: no email address found in the contact block")

    # 1. the personal phone number
    def drop_phone(m: re.Match) -> str:
        removed.append("phone number from the contact line")
        return ""

    frag, n_phone = PHONE_RE.subn(drop_phone, frag)
    if not n_phone:
        die("the phone-number pattern matched nothing. The CV's contact line may have been "
            "reworded; check it by hand and update PHONE_RE before publishing.")

    # 2. the References section, replaced by a one-line note
    m = REFS_RE.search(frag)
    if not m:
        die("the References section was not found. Either the CV no longer has one (then delete "
            "this check) or the heading markup changed and referee names and email addresses "
            "would have been published.")
    body = m.group(2)
    removed.append("References section (%d names, %d email addresses)"
                   % (len(re.findall(r"<strong>([^<]+)</strong>", body)), len(EMAIL_RE.findall(body))))
    frag = frag[:m.start()] + '<h2>References</h2>\n<p class="refs">Available on request.</p>\n' + frag[m.end():]

    # 3. the appositive naming the mentees in the research-mentoring entry
    frag, n_mentee = MENTEE_RE.subn(lambda mm: mm.group(1) + " ", frag)
    if n_mentee:
        removed.append("names of %d mentee(s) in the mentoring entry" % n_mentee)
    else:
        print("  note: no mentee name list matched (the entry may already be anonymous)")

    return frag, removed, author_emails


def verify(frag: str, author_emails: set[str]) -> None:
    """Unconditional post-checks. Any hit aborts the build."""
    stray = {e for e in EMAIL_RE.findall(frag) if e not in author_emails}
    if stray:
        die("%d email address(es) other than the author's survived the scrub: %s"
            % (len(stray), ", ".join(sorted(stray))))

    if PHONE_RE.search(frag):
        die("a phone-number-shaped string survived the scrub.")

    text = re.sub(r"<[^>]+>", "", frag)
    if re.search(r"doctoral students,\s*[A-Z][\w.-]+\s+[A-Z]", text):
        die("a personal name still follows 'doctoral students' in the mentoring entry.")

    print("  post-checks passed: no third-party emails, no phone number, no mentee names")


def build_html(frag: str) -> str:
    paras = re.findall(r"<p>.*?</p>", frag, re.S)
    name = affil = contact = ""
    if paras:
        name = re.sub(r"</?(p|strong)>", "", paras[0]).strip()
        frag = frag.replace(paras[0], "", 1)
    if len(paras) > 1:
        affil = re.sub(r"</?p>", "", paras[1]).strip()
        frag = frag.replace(paras[1], "", 1)
    if len(paras) > 2:
        contact = re.sub(r"</?p>", "", paras[2]).strip().strip("| ").strip()
        frag = frag.replace(paras[2], "", 1)
    if not name:
        die("could not find the name paragraph; the .docx structure changed.")

    def promote(m: re.Match) -> str:
        title = m.group(1).strip()
        tag = "h3" if title in SUBHEADS else "h2"
        return f"<{tag}>{html.escape(title)}</{tag}>"

    frag = HEADING_RE.sub(promote, frag)
    # pandoc renders a link whose anchor text is an arrow glyph as "⇒"; make it read as a link
    frag = frag.replace(">⇒<", ">(link)<")

    head = (
        f"<h1>{html.escape(name)}</h1>\n"
        f'<p class="affil">{affil}</p>\n'
        f'<p class="contact">{contact}</p>\n'
        f'<p class="updated">Curriculum vitae &middot; updated September 2026</p>\n'
        f'<hr class="rule">\n'
    )
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>Chenguang Pan — Curriculum Vitae</title>"
        f"<style>{CSS}</style></head><body>\n{head}{frag}\n</body></html>"
    )


def main() -> None:
    argv = sys.argv[1:]
    keep_html = ""
    if "--html" in argv:
        i = argv.index("--html")
        keep_html = argv[i + 1] if len(argv) > i + 1 else os.path.join(REPO, "_cv", "preview.html")
        del argv[i:i + 2]
    src = argv[0] if argv else DEFAULT_SRC

    if not os.path.exists(src):
        sys.exit(f"source not found: {src}")
    if not shutil.which("pandoc"):
        sys.exit("pandoc is required: conda install -c conda-forge pandoc")
    if not os.path.exists(CHROME):
        sys.exit(f"Google Chrome not found at {CHROME}")

    print(f"source: {src}")
    with tempfile.TemporaryDirectory() as tmp:
        frag_path = os.path.join(tmp, "frag.html")
        run(["pandoc", "-f", "docx", "-t", "html", "--wrap=none", src, "-o", frag_path])
        frag = open(frag_path, encoding="utf-8").read()

        frag, removed, author_emails = scrub(frag)
        print("removed for the public version:")
        for r in removed:
            print("  -", r)
        verify(frag, author_emails)

        page = os.path.join(tmp, "cv.html")
        doc = build_html(frag)
        open(page, "w", encoding="utf-8").write(doc)
        if keep_html:
            open(keep_html, "w", encoding="utf-8").write(doc)
            print("kept intermediate HTML:", keep_html)

        os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
        run([
            CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            "--virtual-time-budget=10000", f"--print-to-pdf={OUT_PDF}", "file://" + page,
        ])

    print(f"wrote {os.path.relpath(OUT_PDF, REPO)} ({os.path.getsize(OUT_PDF) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
