"""Build the Putting Manual PDF from manual.txt (simple markup) using reportlab.

Markup (one block per blank-line-separated paragraph unless noted):
  # Title                 chapter (new page)
  ## Title                section
  ### Title               sub-section
  - text                  bullet (consecutive lines)
  [JJ] text / [PK] text / [BOTH] text   coach callout
  !KEY text               key-takeaway box
  !DRILL Title            drill box until !END (lines; "- " bullets allowed)
  !TABLE                  table until !END ("a | b | c", first row header)
  !FIG name               diagram
  !SRC text               source note (small italic)
  !PAGEBREAK
"""
import re
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                PageBreak, Table, TableStyle, KeepTogether, Flowable,
                                NextPageTemplate)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics.shapes import Drawing, Line, String, Circle, PolyLine, Rect, Polygon
from reportlab.graphics import renderPDF

FD = "/usr/share/fonts/truetype/dejavu/"
LD = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("DV", LD + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("DV-B", LD + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DV-I", LD + "LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("DV-BI", LD + "LiberationSans-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("DVS-B", FD + "DejaVuSerif-Bold.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-BI")

GREEN = colors.HexColor("#1f5c3a")
GREEN_L = colors.HexColor("#e8f2ec")
JJC = colors.HexColor("#1d4e89")
JJL = colors.HexColor("#e7eef8")
PKC = colors.HexColor("#8a3b12")
PKL = colors.HexColor("#f8ede6")
BOTHC = colors.HexColor("#5b4a8a")
BOTHL = colors.HexColor("#efecf7")
GOLD = colors.HexColor("#b38b2d")
GOLDL = colors.HexColor("#fbf5e4")
GREY = colors.HexColor("#555555")

W, H = A4
M = 18 * mm

ss = {}
ss["body"] = ParagraphStyle("body", fontName="DV", fontSize=9.6, leading=13.6, spaceAfter=5)
ss["bullet"] = ParagraphStyle("bullet", parent=ss["body"], leftIndent=12, bulletIndent=2, spaceAfter=2.5)
ss["h1"] = ParagraphStyle("h1", fontName="DVS-B", fontSize=22, leading=27, textColor=GREEN, spaceAfter=10)
ss["h2"] = ParagraphStyle("h2", fontName="DV-B", fontSize=13.5, leading=17, textColor=GREEN, spaceBefore=10, spaceAfter=5, keepWithNext=1)
ss["h3"] = ParagraphStyle("h3", fontName="DV-B", fontSize=10.8, leading=14, textColor=colors.black, spaceBefore=6, spaceAfter=3, keepWithNext=1)
ss["call"] = ParagraphStyle("call", parent=ss["body"], fontSize=9.2, leading=12.8, spaceAfter=0)
ss["src"] = ParagraphStyle("src", fontName="DV-I", fontSize=7.6, leading=10, textColor=GREY, spaceAfter=6)
ss["toc1"] = ParagraphStyle("toc1", fontName="DV-B", fontSize=10.5, leading=16, leftIndent=0)
ss["toc2"] = ParagraphStyle("toc2", fontName="DV", fontSize=9, leading=12.5, leftIndent=14, textColor=GREY)
ss["cell"] = ParagraphStyle("cell", parent=ss["body"], fontSize=8.6, leading=11.2, spaceAfter=0)
ss["cellh"] = ParagraphStyle("cellh", parent=ss["cell"], fontName="DV-B", textColor=colors.white)


def fmt(t):
    """Escape, then apply **bold** and *italic*."""
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    return t


class Doc(BaseDocTemplate):
    def __init__(self, fn):
        super().__init__(fn, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=20 * mm,
                         bottomMargin=18 * mm, title="The Putting Manual",
                         author="Compiled from James Jankowski (JJ Putting) & Phil Kenyon videos",
                         subject="Putting: setup, stroke, speed, green reading, practice, mental game")
        fr = Frame(M, 18 * mm, W - 2 * M, H - 38 * mm, id="f")
        self.addPageTemplates([PageTemplate("cover", [Frame(0, 0, W, H, id="c", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=cover_page),
                               PageTemplate("main", [fr], onPage=main_page)])
        self.chapter = ""

    def beforeDocument(self):
        self.chapter = "Contents"

    def afterFlowable(self, f):
        if isinstance(f, Paragraph):
            sn = f.style.name
            if sn == "h1":
                self.chapter = f.getPlainText()
                key = "c%d" % id(f)
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(self.chapter, key, level=0)
                self.notify("TOCEntry", (0, self.chapter, self.page, key))
            elif sn == "h2":
                key = "s%d" % id(f)
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(f.getPlainText(), key, level=1, closed=True)
                self.notify("TOCEntry", (1, f.getPlainText(), self.page, key))


def cover_page(c, doc):
    c.saveState()
    c.setFillColor(GREEN)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # green-like contour lines
    c.setStrokeColor(colors.HexColor("#2c7a4f"))
    c.setLineWidth(1)
    for i in range(14):
        c.ellipse(W * 0.55 - 30 * i, H * 0.25 - 14 * i, W * 0.55 + 40 * i + 60, H * 0.25 + 12 * i + 30, stroke=1, fill=0)
    # hole + ball path
    c.setFillColor(colors.black)
    c.circle(W * 0.72, H * 0.27, 9, fill=1, stroke=0)
    c.setStrokeColor(colors.white)
    c.setDash(3, 4)
    c.setLineWidth(1.6)
    p = c.beginPath()
    p.moveTo(W * 0.22, H * 0.12)
    p.curveTo(W * 0.38, H * 0.36, W * 0.62, H * 0.38, W * 0.72, H * 0.27)
    c.drawPath(p)
    c.setDash()
    c.setFillColor(colors.white)
    c.circle(W * 0.22, H * 0.12, 6, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(M, H - 70 * mm, 40 * mm, 2.2 * mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("DVS-B", 40)
    c.drawString(M, H - 92 * mm, "The Putting")
    c.drawString(M, H - 110 * mm, "Manual")
    c.setFont("DV", 13)
    c.drawString(M, H - 126 * mm, "Everything in putting, compiled from the YouTube teaching of")
    c.setFont("DV-B", 13)
    c.drawString(M, H - 134 * mm, "James Jankowski (JJ Putting)  &  Phil Kenyon")
    c.setFont("DV", 9.5)
    c.setFillColor(colors.HexColor("#cfe3d6"))
    c.drawString(M, H - 146 * mm, "Setup  ·  Aim  ·  Stroke  ·  Speed  ·  Green reading  ·  Equipment  ·  Practice  ·  Mental game")
    c.setFont("DV-I", 8)
    c.drawString(M, 14 * mm, "Unofficial study guide. Not affiliated with or endorsed by either coach. Ideas credited to source videos throughout.")
    c.restoreState()


def main_page(c, doc):
    c.saveState()
    c.setStrokeColor(GREEN)
    c.setLineWidth(0.6)
    c.line(M, H - 13 * mm, W - M, H - 13 * mm)
    c.setFont("DV", 7.8)
    c.setFillColor(GREY)
    c.drawString(M, H - 11 * mm, "THE PUTTING MANUAL")
    c.drawRightString(W - M, H - 11 * mm, doc.chapter)
    c.drawCentredString(W / 2, 10 * mm, str(doc.page))
    c.restoreState()


def box(flows, bg, border, pad=7, left_bar=True):
    t = Table([[flows]], colWidths=[W - 2 * M])
    st = [("BACKGROUND", (0, 0), (-1, -1), bg), ("LEFTPADDING", (0, 0), (-1, -1), pad + 3),
          ("RIGHTPADDING", (0, 0), (-1, -1), pad), ("TOPPADDING", (0, 0), (-1, -1), pad - 1),
          ("BOTTOMPADDING", (0, 0), (-1, -1), pad)]
    if left_bar:
        st.append(("LINEBEFORE", (0, 0), (0, -1), 3, border))
    else:
        st.append(("BOX", (0, 0), (-1, -1), 0.8, border))
    t.setStyle(TableStyle(st))
    return t


def callout(who, text):
    col, bg, label = {"JJ": (JJC, JJL, "JAMES JANKOWSKI"), "PK": (PKC, PKL, "PHIL KENYON"),
                      "BOTH": (BOTHC, BOTHL, "BOTH COACHES")}[who]
    p = Paragraph('<font name="DV-B" color="%s" size="7.4">%s</font><br/>%s' % (col.hexval().replace("0x", "#"), label, fmt(text)), ss["call"])
    return [Spacer(1, 2), box([p], bg, col), Spacer(1, 6)]


def keybox(text):
    p = Paragraph('<font name="DV-B" color="%s" size="7.4">KEY POINT</font><br/>%s' % (GOLD.hexval().replace("0x", "#"), fmt(text)), ss["call"])
    return [Spacer(1, 2), box([p], GOLDL, GOLD), Spacer(1, 6)]


def drillbox(title, lines):
    fl = [Paragraph('<font name="DV-B" color="#1f5c3a" size="7.4">DRILL</font>  <font name="DV-B" size="10">%s</font>' % fmt(title), ss["call"]), Spacer(1, 3)]
    for ln in lines:
        if ln.startswith("- "):
            fl.append(Paragraph(fmt(ln[2:]), ss["bullet"], bulletText="•"))
        else:
            fl.append(Paragraph(fmt(ln), ParagraphStyle("d", parent=ss["call"], spaceAfter=3)))
    return [Spacer(1, 2), KeepTogether([box(fl, GREEN_L, GREEN, left_bar=False)]), Spacer(1, 7)]


def table(rows):
    data = []
    for i, r in enumerate(rows):
        cells = [c.strip() for c in r.split("|")]
        data.append([Paragraph(fmt(c), ss["cellh"] if i == 0 else ss["cell"]) for c in cells])
    n = len(data[0])
    fr = {2: [0.76, 0.24], 3: [0.26, 0.37, 0.37]}.get(n, [1.0 / n] * n)
    t = Table(data, colWidths=[(W - 2 * M) * f for f in fr], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), GREEN),
                           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f6f4")]),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c9d6cd")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return [Spacer(1, 3), t, Spacer(1, 8)]


# ---------------- diagrams ----------------
def _arrow(d, x1, y1, x2, y2, col):
    d.add(Line(x1, y1, x2, y2, strokeColor=col, strokeWidth=1.2))


def fig_two_thirds():
    # path y = a(t - t^p) with (2/3)^p = 1/3: ball leaves along the aim line, and at 2/3 of the
    # way its offset from the baseline is exactly half the aim line's offset (PK / AimPoint rule)
    import math
    w, h = W - 2 * M, 185
    d = Drawing(w, h)
    bx, by = 40, 32
    hx, hy = w - 70, 32
    L = hx - bx
    p = math.log(1 / 3) / math.log(2 / 3)
    a = 95.0
    y = lambda t: a * (t - t ** p)
    pts = []
    for i in range(0, 101):
        t = i / 100
        pts += [bx + L * t, by + y(t)]
    d.add(Line(bx, by, hx, hy, strokeColor=colors.grey, strokeWidth=1, strokeDashArray=[3, 3]))
    d.add(Line(bx, by, hx, by + a, strokeColor=PKC, strokeWidth=1.4))
    d.add(PolyLine(pts, strokeColor=GREEN, strokeWidth=2.4))
    t = 2 / 3
    x23 = bx + L * t
    off = y(t)
    d.add(Line(x23, by, x23, by + 2 * off, strokeColor=GOLD, strokeWidth=1.1, strokeDashArray=[2, 2]))
    d.add(Circle(x23, by + off, 4, fillColor=GOLD, strokeColor=None))
    d.add(Circle(x23, by + 2 * off, 3.2, fillColor=PKC, strokeColor=None))
    ta = (1 / p) ** (1 / (p - 1))
    d.add(Circle(bx + L * ta, by + y(ta), 3, fillColor=colors.white, strokeColor=colors.grey))
    d.add(String(bx + L * ta - 12, by + y(ta) + 8, "apex", fontName="DV", fontSize=7.5, fillColor=GREY))
    d.add(String(x23 + 6, by + off / 2 - 3, "d", fontName="DV-B", fontSize=9, fillColor=GOLD))
    d.add(String(x23 + 6, by + 1.5 * off - 3, "d", fontName="DV-B", fontSize=9, fillColor=GOLD))
    d.add(String(x23 - 26, by - 14, "2/3 of the way", fontName="DV", fontSize=7.5, fillColor=GREY))
    d.add(Circle(bx, by, 5, fillColor=colors.white, strokeColor=colors.black))
    d.add(Circle(hx, hy, 7, fillColor=colors.black, strokeColor=None))
    d.add(String(bx - 8, by - 14, "ball", fontName="DV", fontSize=7.5, fillColor=GREY))
    d.add(String(hx - 8, hy - 18, "hole", fontName="DV", fontSize=7.5, fillColor=GREY))
    d.add(String(hx - 40, by + a + 6, "aim point (hole high)", fontName="DV-B", fontSize=8, fillColor=PKC))
    d.add(String(bx + L * 0.4, by + 6, "baseline (straight line to hole)", fontName="DV", fontSize=7.5, fillColor=GREY))
    d.add(String(bx + L * 0.12, by + y(0.25) + 2, "ball path", fontName="DV-B", fontSize=8, fillColor=GREEN))
    d.add(String(bx + L * 0.33, by + a * 0.42 + 8, "start line", fontName="DV-B", fontSize=8, fillColor=PKC))
    d.add(String(0, h - 10, "Uphill is to the top of the page. The ball starts on the start line and curves from the moment it stops skidding.", fontName="DV-I", fontSize=7.5, fillColor=GREY))
    return d


def fig_accel():
    w, h = W - 2 * M, 175
    d = Drawing(w, h)
    x0, y0, gw, gh = 55, 30, w - 80, 110
    mid = y0 + gh / 2
    d.add(Line(x0, mid, x0 + gw, mid, strokeColor=colors.grey, strokeWidth=0.8))
    d.add(Line(x0, y0, x0, y0 + gh, strokeColor=colors.grey, strokeWidth=0.8))
    d.add(String(x0 - 52, y0 + gh - 4, "toward", fontName="DV", fontSize=7.5, fillColor=GREY))
    d.add(String(x0 - 52, y0 + gh - 13, "target", fontName="DV", fontSize=7.5, fillColor=GREY))
    d.add(String(x0 - 52, mid - 3, "zero", fontName="DV", fontSize=7.5, fillColor=GREY))
    d.add(String(x0 - 52, y0 + 4, "away", fontName="DV", fontSize=7.5, fillColor=GREY))
    good = [0, -0.35, -0.25, 0.1, 0.6, 1.0, 0.85, 0.55, 0.25, 0.05, 0.0, 0.0, -0.15, -0.35, -0.3, -0.1]
    bad = [0, -0.12, -0.08, 0.0, 0.05, 0.12, 0.2, 0.4, 0.7, 0.95, 0.9, 0.5, -0.2, -0.3, -0.15, -0.05]
    for prof, col, dash, wdt in [(bad, PKC, [4, 3], 1.6), (good, GREEN, None, 2.4)]:
        pts = []
        for i, v in enumerate(prof):
            pts += [x0 + gw * i / 15, mid + v * gh * 0.45]
        d.add(PolyLine(pts, strokeColor=col, strokeWidth=wdt, strokeDashArray=dash))
    for idx, lab in [(0, "address"), (5, "top / transition"), (10, "impact"), (15, "finish")]:
        x = x0 + gw * idx / 15
        d.add(Line(x, y0, x, y0 + gh, strokeColor=colors.HexColor("#dddddd"), strokeWidth=0.6))
        d.add(String(x - 16, y0 - 13, lab, fontName="DV", fontSize=7.5, fillColor=GREY))
    d.add(Rect(x0 + 10, y0 + gh + 18, 12, 3, fillColor=GREEN, strokeColor=None))
    d.add(String(x0 + 26, y0 + gh + 16, "Efficient: most acceleration in the transition, about zero at impact (putter coasts)", fontName="DV", fontSize=7.5))
    d.add(Rect(x0 + 10, y0 + gh + 6, 12, 3, fillColor=PKC, strokeColor=None))
    d.add(String(x0 + 26, y0 + gh + 4, "Common fault: slow backstroke, then 'hit' at the ball (acceleration peaks near impact)", fontName="DV", fontSize=7.5))
    return d


def fig_arc():
    import math
    w, h = W - 2 * M, 130
    d = Drawing(w, h)
    cx, cy = w / 2, 30
    k = 26.0 / (170 ** 2)
    d.add(Line(20, cy, w - 20, cy, strokeColor=colors.grey, strokeWidth=1, strokeDashArray=[3, 3]))
    d.add(String(w - 75, cy - 12, "target line", fontName="DV", fontSize=7.5, fillColor=GREY))
    pts = []
    for i in range(-45, 46):
        x = cx + i * 4
        pts += [x, cy + k * (x - cx) ** 2]
    d.add(PolyLine(pts, strokeColor=GREEN, strokeWidth=2.2))
    for x in [cx - 160, cx - 90, cx, cx + 90, cx + 160]:
        yv = cy + k * (x - cx) ** 2
        ang = math.atan(2 * k * (x - cx))
        Lh = 13
        ux, uy = -math.sin(ang), math.cos(ang)
        d.add(Line(x - ux * Lh, yv - uy * Lh, x + ux * Lh, yv + uy * Lh, strokeColor=PKC, strokeWidth=2.6))
    d.add(Circle(cx + 12, cy, 5, fillColor=colors.white, strokeColor=colors.black))
    d.add(String(cx - 215, cy + 50, "backstroke: up & inside, face opens", fontName="DV", fontSize=7.5, fillColor=GREY))
    d.add(String(cx - 215, cy + 40, "relative to the target, square to the arc", fontName="DV", fontSize=7.5, fillColor=GREY))
    d.add(String(cx + 75, cy + 50, "through: back inside, face closes", fontName="DV", fontSize=7.5, fillColor=GREY))
    d.add(String(cx + 75, cy + 40, "relative to the target, square to the arc", fontName="DV", fontSize=7.5, fillColor=GREY))
    d.add(String(cx - 30, cy - 16, "square at impact", fontName="DV-B", fontSize=7.5, fillColor=GREEN))
    d.add(String(20, h - 10, "Seen from above (golfer at the top of the picture). Red bars = putter face.", fontName="DV-I", fontSize=7.5, fillColor=GREY))
    return d


def fig_entry():
    w, h = W - 2 * M, 125
    d = Drawing(w, h)
    x0, y0, gw, gh = 55, 22, w - 90, 85
    d.add(Line(x0, y0, x0 + gw, y0, strokeColor=colors.grey))
    d.add(Line(x0, y0, x0, y0 + gh, strokeColor=colors.grey))
    d.add(String(x0 - 48, y0 + gh - 6, "ball speed", fontName="DV", fontSize=7.5, fillColor=GREY))
    d.add(String(x0 + gw - 70, y0 - 12, "distance rolled", fontName="DV", fontSize=7.5, fillColor=GREY))
    pts = [x0, y0 + gh * 0.95, x0 + gw * 0.10, y0 + gh * 0.76, x0 + gw * 0.80, y0 + gh * 0.17, x0 + gw * 0.90, y0]
    d.add(PolyLine(pts, strokeColor=GREEN, strokeWidth=2.4))
    d.add(Line(x0, y0 + gh * 0.17, x0 + gw * 0.8, y0 + gh * 0.17, strokeColor=GOLD, strokeWidth=0.8, strokeDashArray=[2, 2]))
    d.add(String(x0 + 6, y0 + gh * 0.17 + 4, "about 1 mph: ideal speed as the ball reaches the hole", fontName="DV-B", fontSize=7.5, fillColor=GOLD))
    d.add(String(x0 + gw * 0.12, y0 + gh * 0.9, "skid", fontName="DV", fontSize=7.5, fillColor=GREY))
    d.add(String(x0 + gw * 0.42, y0 + gh * 0.58, "true roll: steady deceleration", fontName="DV", fontSize=7.5, fillColor=GREY))
    d.add(String(x0 + gw * 0.83, y0 + gh * 0.42, "decay phase:", fontName="DV-B", fontSize=7.5, fillColor=PKC))
    d.add(String(x0 + gw * 0.83, y0 + gh * 0.32, "slows fast,", fontName="DV", fontSize=7.5, fillColor=PKC))
    d.add(String(x0 + gw * 0.83, y0 + gh * 0.22, "breaks more", fontName="DV", fontSize=7.5, fillColor=PKC))
    return d


FIGS = {"two_thirds": fig_two_thirds, "accel": fig_accel, "arc": fig_arc, "entry": fig_entry}


class FigFlow(Flowable):
    def __init__(self, d):
        super().__init__()
        self.d = d
        self.width, self.height = d.width, d.height

    def draw(self):
        renderPDF.draw(self.d, self.canv, 0, 0)


def parse(path):
    story = []
    lines = open(path, encoding="utf-8").read().split("\n")
    i = 0
    para = []
    bullets = []

    def flush():
        nonlocal para, bullets
        if para:
            story.append(Paragraph(fmt(" ".join(para)), ss["body"]))
            para = []
        if bullets:
            for b in bullets:
                m = re.match(r"^(\d+)\. (.*)", b)
                if m:
                    story.append(Paragraph(fmt(m.group(2)), ss["bullet"], bulletText=m.group(1) + "."))
                else:
                    story.append(Paragraph(fmt(b), ss["bullet"], bulletText="•"))
            story.append(Spacer(1, 4))
            bullets = []

    while i < len(lines):
        ln = lines[i].rstrip()
        s = ln.strip()
        if not s:
            flush()
        elif s.startswith("%%"):
            pass
        elif s.startswith("# "):
            flush()
            story += [PageBreak(), Paragraph(fmt(s[2:]), ss["h1"]),
                      HR()]
        elif s.startswith("## "):
            flush()
            story.append(Paragraph(fmt(s[3:]), ss["h2"]))
        elif s.startswith("### "):
            flush()
            story.append(Paragraph(fmt(s[4:]), ss["h3"]))
        elif s.startswith("- "):
            if para:
                flush()
            bullets.append(s[2:])
        elif re.match(r"^\d+\. ", s):
            if para:
                flush()
            bullets.append(s)
        elif re.match(r"^\[(JJ|PK|BOTH)\]", s):
            flush()
            who = re.match(r"^\[(JJ|PK|BOTH)\]", s).group(1)
            story += callout(who, s[len(who) + 2:].strip())
        elif s.startswith("!KEY "):
            flush()
            story += keybox(s[5:])
        elif s.startswith("!SRC "):
            flush()
            story.append(Paragraph(fmt("Sources: " + s[5:]), ss["src"]))
        elif s.startswith("!FIG "):
            flush()
            story += [Spacer(1, 4), FigFlow(FIGS[s[5:].strip()]()), Spacer(1, 8)]
        elif s == "!PAGEBREAK":
            flush()
            story.append(PageBreak())
        elif s.startswith("!DRILL ") or s == "!TABLE":
            flush()
            kind = "drill" if s.startswith("!DRILL") else "table"
            title = s[7:] if kind == "drill" else ""
            block = []
            i += 1
            while lines[i].strip() != "!END":
                if lines[i].strip():
                    block.append(lines[i].strip())
                i += 1
            story += drillbox(title, block) if kind == "drill" else table(block)
        else:
            if bullets:
                # continuation of bullet
                bullets[-1] += " " + s
            else:
                para.append(s)
        i += 1
    flush()
    return story


class HR(Flowable):
    def __init__(self):
        super().__init__()
        self.height = 10

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.height

    def draw(self):
        self.canv.setStrokeColor(GOLD)
        self.canv.setLineWidth(2)
        self.canv.line(0, 6, 40 * mm, 6)


def build(src, out):
    doc = Doc(out)
    toc = TableOfContents()
    toc.levelStyles = [ss["toc1"], ss["toc2"]]
    toc.dotsMinLevel = 0
    story = [NextPageTemplate("main"), PageBreak(),
             Paragraph("Contents", ParagraphStyle("h1toc", parent=ss["h1"])), HR(), toc]
    story += parse(src)
    doc.multiBuild(story)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
