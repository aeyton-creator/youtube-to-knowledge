"""Build the Commodities Handbook PDF from the Markdown files in commodities/sections/.

Usage:
    python commodities/build_pdf.py            # writes commodities/output/Commodities_Handbook.pdf
    python commodities/build_pdf.py -o my.pdf

Layout:
    sections/<NN_part_name>/<NN_chapter>.md
    - Each folder is a Part (e.g. 02_energy -> "Energy"); an optional _title.txt in the folder
      overrides that title. A file may also sit directly in sections/.
    - Each file is a chapter; its first "# " line is the chapter title.
    - Files and folders are ordered by their numeric prefix.

Supported Markdown subset: #/##/### headings, paragraphs, "- " bullets (indent 2 spaces
for a sub-bullet), "1. " numbered lists, | tables |, "> " callouts, **bold**, *italic*, `code`.
"""

import argparse
import datetime as dt
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether, NextPageTemplate, PageBreak, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parent
SECTIONS = ROOT / "sections"
DEFAULT_OUT = ROOT / "output" / "Commodities_Handbook.pdf"

NAVY = colors.HexColor("#14213D")
ACCENT = colors.HexColor("#B8860B")
LIGHT = colors.HexColor("#F3F1EA")
GRID = colors.HexColor("#C9C4B5")
CALLOUT = colors.HexColor("#FFF7E0")

SMALL_WORDS = {"and", "of", "the", "for", "in", "on", "to", "a"}


FONT_CANDIDATES = [
    # (directory, regular, bold, italic, bold-italic) — first complete set found wins.
    (ROOT / "fonts", "Body.ttf", "Body-Bold.ttf", "Body-Italic.ttf", "Body-BoldItalic.ttf"),
    (Path("/usr/share/fonts/truetype/liberation"), "LiberationSans-Regular.ttf",
     "LiberationSans-Bold.ttf", "LiberationSans-Italic.ttf", "LiberationSans-BoldItalic.ttf"),
    (Path("/usr/share/fonts/truetype/dejavu"), "DejaVuSans.ttf", "DejaVuSans-Bold.ttf",
     "DejaVuSans-Oblique.ttf", "DejaVuSans-BoldOblique.ttf"),
    (Path("/System/Library/Fonts/Supplemental"), "Arial.ttf", "Arial Bold.ttf",
     "Arial Italic.ttf", "Arial Bold Italic.ttf"),
    (Path("/Library/Fonts"), "Arial.ttf", "Arial Bold.ttf", "Arial Italic.ttf",
     "Arial Bold Italic.ttf"),
    (Path("C:/Windows/Fonts"), "arial.ttf", "arialbd.ttf", "ariali.ttf", "arialbi.ttf"),
]


def register_fonts():
    """Embed a Unicode TrueType family (needed for ≈ − ≥ → ⅛) or fall back to Helvetica."""
    for d, *files in FONT_CANDIDATES:
        paths = [d / f for f in files]
        if all(p.exists() for p in paths):
            names = ["Body", "Body-Bold", "Body-Italic", "Body-BoldItalic"]
            for n, p in zip(names, paths):
                pdfmetrics.registerFont(TTFont(n, str(p)))
            pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold",
                                          italic="Body-Italic", boldItalic="Body-BoldItalic")
            return "Body", "Body-Bold"
    print("Warning: no Unicode font found; some symbols may not render. "
          "Drop a TTF family into commodities/fonts/ (see FONT_CANDIDATES).")
    return "Helvetica", "Helvetica-Bold"


BODY_FONT, BOLD_FONT = register_fonts()


def make_styles():
    ss = getSampleStyleSheet()
    s = {}
    s["body"] = ParagraphStyle("body", parent=ss["Normal"], fontName=BODY_FONT, fontSize=9.2,
                               leading=12.6, spaceAfter=4)
    s["bullet"] = ParagraphStyle("bullet", parent=s["body"], leftIndent=12, bulletIndent=3,
                                 spaceAfter=1.5)
    s["bullet2"] = ParagraphStyle("bullet2", parent=s["bullet"], leftIndent=24, bulletIndent=15)
    s["part"] = ParagraphStyle("part", fontName=BOLD_FONT, fontSize=30, leading=36,
                               textColor=NAVY, alignment=TA_CENTER)
    s["h1"] = ParagraphStyle("h1", fontName=BOLD_FONT, fontSize=18, leading=22, textColor=NAVY,
                             spaceAfter=6)
    s["toctitle"] = ParagraphStyle("toctitle", parent=s["h1"])
    s["h2"] = ParagraphStyle("h2", fontName=BOLD_FONT, fontSize=12, leading=15, textColor=NAVY,
                             spaceBefore=9, spaceAfter=3)
    s["h3"] = ParagraphStyle("h3", fontName=BOLD_FONT, fontSize=10, leading=13,
                             textColor=ACCENT, spaceBefore=6, spaceAfter=2)
    s["cell"] = ParagraphStyle("cell", parent=s["body"], fontSize=8, leading=10, spaceAfter=0)
    s["cellh"] = ParagraphStyle("cellh", parent=s["cell"], fontName=BOLD_FONT,
                                textColor=colors.white)
    s["callout"] = ParagraphStyle("callout", parent=s["body"], spaceAfter=0)
    s["title"] = ParagraphStyle("title", fontName=BOLD_FONT, fontSize=34, leading=40,
                                textColor=NAVY, alignment=TA_CENTER)
    s["subtitle"] = ParagraphStyle("subtitle", fontName=BODY_FONT, fontSize=13, leading=18,
                                   textColor=colors.HexColor("#555555"), alignment=TA_CENTER)
    s["toc1"] = ParagraphStyle("toc1", fontName=BOLD_FONT, fontSize=11, leading=16,
                               textColor=NAVY, spaceBefore=6)
    s["toc2"] = ParagraphStyle("toc2", fontName=BODY_FONT, fontSize=9.5, leading=13, leftIndent=14)
    return s


STYLES = make_styles()


def inline(text):
    """Escape XML and convert **bold**, *italic*, `code` to ReportLab markup."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r'<font face="Courier">\1</font>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", text)
    return text


def pretty_name(stem):
    words = re.sub(r"^\d+[_-]?", "", stem).replace("_", " ").replace("-", " ").split()
    return " ".join(w if (i and w in SMALL_WORDS) else w[:1].upper() + w[1:]
                    for i, w in enumerate(words))


class Doc(BaseDocTemplate):
    def __init__(self, path, **kw):
        super().__init__(str(path), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                         topMargin=20 * mm, bottomMargin=18 * mm,
                         title="Commodities Handbook", author="Commodities Desk", **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([
            PageTemplate("cover", [frame], onPage=lambda c, d: None),
            PageTemplate("body", [frame], onPageEnd=self._decorate),
        ])
        self.current_chapter = ""

    def beforeDocument(self):
        self.current_chapter = ""

    def _decorate(self, canv, doc):
        w, h = A4
        canv.saveState()
        canv.setStrokeColor(ACCENT)
        canv.setLineWidth(0.6)
        canv.line(self.leftMargin, h - 13 * mm, w - self.rightMargin, h - 13 * mm)
        canv.setFont(BODY_FONT, 7.5)
        canv.setFillColor(colors.HexColor("#666666"))
        canv.drawString(self.leftMargin, h - 11.5 * mm, "COMMODITIES HANDBOOK")
        canv.drawRightString(w - self.rightMargin, h - 11.5 * mm, self.current_chapter)
        canv.drawCentredString(w / 2, 10 * mm, str(doc.page))
        canv.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            name = flowable.style.name
            if name in ("part", "h1"):
                text = flowable.getPlainText()
                level = 0 if name == "part" else 1
                key = f"k{id(flowable)}"
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=level, closed=level == 0)
                self.notify("TOCEntry", (level, text, self.page, key))
                self.current_chapter = text if name == "h1" else ""


def column_widths(rows, avail):
    """Never break inside a word; share remaining width in proportion to text length."""
    pad = 14  # default cell padding is 6pt each side
    ncols = len(rows[0])

    def width(text, header):
        plain = re.sub(r"[*`]", "", text)
        return stringWidth(plain, BOLD_FONT if header else BODY_FONT, 8)

    mins, weights = [], []
    for j in range(ncols):
        words = [(w, i == 0) for i, r in enumerate(rows) for w in r[j].split()]
        mins.append(max([width(w, h) for w, h in words] or [0]) + pad)
        weights.append(max(min(max(len(r[j]) for r in rows), 60), 6))
    if sum(mins) >= avail:
        return [avail * m / sum(mins) for m in mins]
    # Give each column its preferred share, but at least its minimum.
    widths = mins[:]
    free = [j for j in range(ncols)]
    while True:
        rest = avail - sum(widths[j] for j in range(ncols) if j not in free)
        share = {j: rest * weights[j] / sum(weights[k] for k in free) for j in free}
        pinned = [j for j in free if share[j] < mins[j]]
        if not pinned:
            for j in free:
                widths[j] = share[j]
            return widths
        free = [j for j in free if j not in pinned]


def parse_table(lines):
    rows = []
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    if not rows:
        return None
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    data = [[Paragraph(inline(c), STYLES["cellh" if i == 0 else "cell"]) for c in r]
            for i, r in enumerate(rows)]
    avail = A4[0] - 36 * mm
    widths = column_widths(rows, avail)
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.4, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return t


def callout(text):
    t = Table([[Paragraph(inline(text), STYLES["callout"])]], colWidths=[A4[0] - 36 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CALLOUT),
        ("LINEBEFORE", (0, 0), (0, -1), 3, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def md_to_flowables(md_text):
    out = []
    lines = md_text.splitlines()
    i = 0
    para = []

    def flush():
        if para:
            out.append(Paragraph(inline(" ".join(para)), STYLES["body"]))
            para.clear()

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s or s.startswith("<!--"):
            flush()
            if s.startswith("<!--"):
                while i < len(lines) and "-->" not in lines[i]:
                    i += 1
            i += 1
            continue
        m = re.match(r"^(#{1,3})\s+(.*)", s)
        if m:
            flush()
            level = len(m.group(1))
            style = STYLES[f"h{level}"]
            p = Paragraph(inline(m.group(2)), style)
            if level == 1:
                out.append(p)
            else:
                # Keep headings with the first block that follows them.
                out.append(("keep", p))
            i += 1
            continue
        if s.startswith("|"):
            flush()
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i])
                i += 1
            t = parse_table(block)
            if t:
                out.append(t)
                out.append(Spacer(1, 5))
            continue
        if s.startswith(">"):
            flush()
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(lines[i].strip()[1:].strip())
                i += 1
            out.append(callout(" ".join(block)))
            out.append(Spacer(1, 5))
            continue
        bm = re.match(r"^(\s*)[-*]\s+(.*)", ln)
        nm = re.match(r"^(\s*)(\d+)\.\s+(.*)", ln)
        if bm or nm:
            flush()
            indent = len((bm or nm).group(1))
            text = bm.group(2) if bm else nm.group(3)
            bullet = "•" if bm else nm.group(2) + "."
            if indent >= 2:
                bullet = "–" if bm else bullet
            # Continuation lines (indented, not a new bullet).
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(
                    r"^\s*([-*]|\d+\.)\s+", lines[i]) and lines[i].startswith(" "):
                text += " " + lines[i].strip()
                i += 1
            out.append(Paragraph(inline(text), STYLES["bullet2" if indent >= 2 else "bullet"],
                                 bulletText=bullet))
            continue
        para.append(s)
        i += 1
    flush()

    # Resolve ("keep", heading) markers.
    final = []
    j = 0
    while j < len(out):
        item = out[j]
        if isinstance(item, tuple):
            nxt = out[j + 1] if j + 1 < len(out) and not isinstance(out[j + 1], tuple) else None
            final.append(KeepTogether([item[1], nxt]) if nxt else item[1])
            j += 2 if nxt else 1
        else:
            final.append(item)
            j += 1
    return final


def collect():
    """Return [(part_title or None, [chapter paths])] in order."""
    parts = []
    loose = sorted(p for p in SECTIONS.glob("*.md"))
    for p in loose:
        parts.append((None, [p]))
    for d in sorted(p for p in SECTIONS.iterdir() if p.is_dir()):
        files = sorted(d.glob("*.md"))
        if files:
            # Optional _title.txt overrides the title derived from the folder name.
            custom = d / "_title.txt"
            title = custom.read_text(encoding="utf-8").strip() if custom.exists() else None
            parts.append((title or pretty_name(d.name), files))
    # Loose files and folders interleave by numeric prefix.
    def key(entry):
        title, files = entry
        ref = files[0] if title is None else files[0].parent
        return ref.name
    return sorted(parts, key=key)


def build(out_path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc = Doc(out_path)
    story = []

    parts = collect()
    n_chapters = sum(len(f) for _, f in parts)
    story += [Spacer(1, 70 * mm), Paragraph("Commodities Handbook", STYLES["title"]),
              Spacer(1, 8 * mm),
              Paragraph("Specialist reference across energy, metals, agriculture, "
                        "softs, livestock and environmental markets", STYLES["subtitle"]),
              Spacer(1, 30 * mm),
              Paragraph(f"Edition built {dt.date.today():%d %B %Y} &nbsp;·&nbsp; "
                        f"{n_chapters} chapters", STYLES["subtitle"]),
              NextPageTemplate("body"), PageBreak()]

    toc = TableOfContents()
    toc.levelStyles = [STYLES["toc1"], STYLES["toc2"]]
    story += [Paragraph("Contents", STYLES["toctitle"]), toc, PageBreak()]

    for title, files in parts:
        if title:
            story += [Spacer(1, 90 * mm), Paragraph(title, STYLES["part"]), PageBreak()]
        for f in files:
            story += md_to_flowables(f.read_text(encoding="utf-8"))
            story.append(PageBreak())

    doc.multiBuild(story)
    return out_path


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("-o", "--output", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    print(f"Wrote {build(args.output)}")
