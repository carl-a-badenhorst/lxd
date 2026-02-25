"""
Generates workshop-slides.pdf for the cross-functional learning design workshop.

Slide format: 16:9 (254mm x 143mm / 1920x1080 equivalent scaled to A4-landscape width)
Design system: minimalist utilitarian — monochrome, strict type scale, geometric accents only.

Slide inventory (35 slides):
  00  Title
  01  Agenda overview
  02  Diagnostic norm
  --- PHASE 1 ---
  03  Phase 1 header
  04  Writing prompt 1A
  05  Writing prompt 1B
  06  The operational definition (reveal)
  07  Unpacking the definition
  08  Writing prompt 1C
  --- PHASE 2 ---
  09  Phase 2 header
  10  Recall task
  11  Reveal: three commitments
  12  Commitment 1 — Memory precedes complex thinking
  13  Commitment 2 — Retrieval strengthens memory
  14  Commitment 3 — Cognitive load must be managed
  15  Role-based application prompt
  16  Worked example setup
  17  Worked example reveal
  --- PHASE 3 ---
  18  Phase 3 header
  19  Role clarification prompts
  20  Cross-role perspective taking
  21  Transition to Phase 4
  --- PHASE 4 ---
  22  Phase 4 header
  23  Diagnostic norm reminder
  24  Stage 1 — Identify
  25  Stage 2 — Diagnose misalignment
  26  Break slide
  --- PHASE 5 ---
  27  Phase 5 header
  28  Redesign map overview
  29  Learning science justification prompt
  --- PHASE 6 ---
  30  Phase 6 header
  31  Gallery walk protocol
  --- PHASE 7 ---
  32  Phase 7 header
  33  Individual commitments prompt
  34  30-day follow-up plan
  35  Closing retrieval task
  36  Close
"""

from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak, Frame, BaseDocTemplate, PageTemplate
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os

# ─── Canvas dimensions ────────────────────────────────────────────────────────
# True 16:9 at a print-friendly size
SLIDE_W = 338 * mm   # ~1920px equivalent
SLIDE_H = 190 * mm   # ~1080px equivalent

# Margins (generous for breathing room)
ML = 18 * mm
MR = 18 * mm
MT = 16 * mm
MB = 14 * mm

# ─── Design tokens ────────────────────────────────────────────────────────────
INK        = HexColor("#111111")
MID        = HexColor("#444444")
LIGHT      = HexColor("#888888")
RULE_CLR   = HexColor("#CCCCCC")
FIELD_BG   = HexColor("#F5F5F5")
ACCENT     = HexColor("#111111")   # kept monochrome; accent is weight + size
WHITE      = white
HIGHLIGHT  = HexColor("#E8E8E8")   # light block for callout boxes

# ─── Type scale (pt) ──────────────────────────────────────────────────────────
T_HERO     = 46
T_DISPLAY  = 32
T_TITLE    = 22
T_BODY     = 13
T_SMALL    = 10
T_MICRO    = 8
T_LABEL    = 9

HERO_LEAD   = 52
DISP_LEAD   = 38
TITLE_LEAD  = 28
BODY_LEAD   = 19
SMALL_LEAD  = 14

# ─── Fonts ────────────────────────────────────────────────────────────────────
F_BOLD      = "Helvetica-Bold"
F_REG       = "Helvetica"
F_ITALIC    = "Helvetica-Oblique"
F_BI        = "Helvetica-BoldOblique"


# ─── Low-level drawing helpers ────────────────────────────────────────────────

def bg(c, color=WHITE):
    c.setFillColor(color)
    c.rect(0, 0, SLIDE_W, SLIDE_H, fill=1, stroke=0)


def hline(c, y, x0=None, x1=None, color=RULE_CLR, lw=0.5):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(x0 or ML, y, x1 or SLIDE_W - MR, y)


def phase_chip(c, text, x=ML, y=None):
    """Small all-caps label above a heading."""
    y = y or SLIDE_H - MT - 7 * mm
    c.setFont(F_BOLD, T_LABEL)
    c.setFillColor(LIGHT)
    c.drawString(x, y, text.upper())


def heading(c, text, x=ML, y=None, font=F_BOLD, size=T_DISPLAY, color=INK, align="left"):
    y = y or SLIDE_H - MT - 20 * mm
    c.setFont(font, size)
    c.setFillColor(color)
    if align == "left":
        c.drawString(x, y, text)
    elif align == "center":
        c.drawCentredString(SLIDE_W / 2, y, text)
    elif align == "right":
        c.drawRightString(SLIDE_W - MR, y, text)


def body_text(c, text, x=ML, y=None, font=F_REG, size=T_BODY, color=INK, max_width=None, align="left"):
    y = y or SLIDE_H / 2
    max_w = max_width or (SLIDE_W - ML - MR)
    c.setFont(font, size)
    c.setFillColor(color)
    if align == "left":
        c.drawString(x, y, text)
    elif align == "center":
        c.drawCentredString(SLIDE_W / 2, y, text)


def multiline(c, lines, x=ML, y_start=None, font=F_REG, size=T_BODY, leading=None, color=INK, indent=0):
    lead = leading or (size * 1.5)
    y = y_start or (SLIDE_H / 2 + len(lines) * lead / 2)
    c.setFont(font, size)
    c.setFillColor(color)
    for line in lines:
        c.drawString(x + indent, y, line)
        y -= lead
    return y


def bullet_list(c, items, x=ML, y_start=None, font=F_REG, size=T_BODY, leading=None, color=INK, marker="—"):
    lead = leading or (size * 1.7)
    y = y_start
    c.setFont(font, size)
    c.setFillColor(color)
    for item in items:
        c.drawString(x, y, f"{marker}  {item}")
        y -= lead
    return y


def callout_box(c, text, x=ML, y=None, w=None, h=None, bg_color=HIGHLIGHT, font=F_BI, size=T_BODY, color=INK):
    bw = w or (SLIDE_W - ML - MR)
    bh = h or 18 * mm
    by = y or SLIDE_H / 2 - bh / 2
    c.setFillColor(bg_color)
    c.setStrokeColor(RULE_CLR)
    c.setLineWidth(0.5)
    c.roundRect(x, by, bw, bh, 2 * mm, fill=1, stroke=0)
    # Left rule accent
    c.setFillColor(INK)
    c.rect(x, by, 2.5, bh, fill=1, stroke=0)
    # Text
    c.setFont(font, size)
    c.setFillColor(color)
    text_y = by + bh / 2 - size * 0.35
    c.drawString(x + 6 * mm, text_y, text)


def slide_number(c, n, total):
    c.setFont(F_REG, T_MICRO)
    c.setFillColor(LIGHT)
    c.drawRightString(SLIDE_W - MR, MB - 4 * mm, f"{n} / {total}")


def footer_bar(c, label=""):
    hline(c, MB - 1 * mm, lw=0.4, color=RULE_CLR)
    if label:
        c.setFont(F_REG, T_MICRO)
        c.setFillColor(LIGHT)
        c.drawString(ML, MB - 4 * mm, label)


def phase_header_slide(c, number, title, description, n, total, image_placeholder=False):
    bg(c, FIELD_BG)
    # Left black bar
    c.setFillColor(INK)
    c.rect(0, 0, 4 * mm, SLIDE_H, fill=1, stroke=0)
    # Phase number — large background numeral
    c.setFont(F_BOLD, 120)
    c.setFillColor(HexColor("#E0E0E0"))
    c.drawString(ML + 8 * mm, SLIDE_H / 2 - 38 * mm, number)
    # Phase label
    c.setFont(F_BOLD, T_LABEL)
    c.setFillColor(LIGHT)
    c.drawString(ML + 8 * mm, SLIDE_H - MT - 5 * mm, "PHASE")
    # Title
    c.setFont(F_BOLD, T_DISPLAY)
    c.setFillColor(INK)
    c.drawString(ML + 8 * mm, SLIDE_H - MT - 18 * mm, title)
    hline(c, SLIDE_H - MT - 22 * mm, x0=ML + 8 * mm, lw=1.2, color=INK)
    # Description
    c.setFont(F_REG, T_BODY)
    c.setFillColor(MID)
    y = SLIDE_H - MT - 32 * mm
    for line in _wrap(description, F_REG, T_BODY, SLIDE_W - ML - MR - 8 * mm - 10 * mm):
        c.drawString(ML + 8 * mm, y, line)
        y -= BODY_LEAD
    # Image placeholder hint (right column)
    if image_placeholder:
        px = SLIDE_W * 0.62
        pw = SLIDE_W * 0.34
        ph = SLIDE_H * 0.5
        py = (SLIDE_H - ph) / 2
        c.setFillColor(HexColor("#DEDEDE"))
        c.setStrokeColor(RULE_CLR)
        c.setLineWidth(0.5)
        c.rect(px, py, pw, ph, fill=1, stroke=1)
        c.setFont(F_REG, T_MICRO)
        c.setFillColor(LIGHT)
        c.drawCentredString(px + pw / 2, py + ph / 2 - 2 * mm, "[ IMAGE ]")
    footer_bar(c, "Designing Learning as a Cross-Functional Activity System")
    slide_number(c, n, total)


def _wrap(text, font, size, max_w):
    """Naïve word-wrap returning list of lines."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if stringWidth(test, font, size) <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def image_slot(c, x, y, w, h, label="IMAGE"):
    """Grey rectangle placeholder for a photo."""
    c.setFillColor(HexColor("#DEDEDE"))
    c.setStrokeColor(RULE_CLR)
    c.setLineWidth(0.5)
    c.rect(x, y, w, h, fill=1, stroke=1)
    c.setFont(F_REG, T_MICRO)
    c.setFillColor(LIGHT)
    c.drawCentredString(x + w / 2, y + h / 2 - 1.5 * mm, f"[ {label} ]")


# ─── Individual slide builders ────────────────────────────────────────────────

TOTAL = 37

def slide_00_title(c, n):
    bg(c, INK)
    # White background strip on right 40%
    c.setFillColor(WHITE)
    c.rect(SLIDE_W * 0.60, 0, SLIDE_W * 0.40, SLIDE_H, fill=1, stroke=0)
    # Image slot (left column)
    image_slot(c, 0, 0, SLIDE_W * 0.58, SLIDE_H, "COVER IMAGE")
    # Title block on white strip
    tx = SLIDE_W * 0.62
    c.setFont(F_BOLD, T_LABEL)
    c.setFillColor(LIGHT)
    c.drawString(tx, SLIDE_H - MT - 6 * mm, "WORKSHOP")
    c.setFont(F_BOLD, 24)
    c.setFillColor(INK)
    # Wrap title
    title_lines = ["Designing Learning", "as a Cross-Functional", "Activity System"]
    y = SLIDE_H - MT - 20 * mm
    for line in title_lines:
        c.drawString(tx, y, line)
        y -= 30
    hline(c, y - 4 * mm, x0=tx, lw=1.2, color=INK)
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(MID)
    c.drawString(tx, y - 10 * mm, "135-minute design workshop")
    slide_number(c, n, TOTAL)


def slide_01_agenda(c, n):
    bg(c)
    phase_chip(c, "Overview")
    heading(c, "Workshop agenda", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)

    phases = [
        ("Phase 1", "0–15 min",   "Framing the Shared Object"),
        ("Phase 2", "15–30 min",  "Learning Science Core"),
        ("Phase 3", "30–50 min",  "Role Mapping"),
        ("Phase 4", "50–75 min",  "Cross-Role Diagnosis"),
        ("—",       "75–85 min",  "Break"),
        ("Phase 5", "85–110 min", "Collaborative Redesign"),
        ("Phase 6", "110–125 min","Cross-Team Critique"),
        ("Phase 7", "125–135 min","Collaboration Charter & Closing"),
    ]
    col_w = [28 * mm, 28 * mm, SLIDE_W - ML - MR - 60 * mm]
    row_h = 14 * mm
    table_y = SLIDE_H - MT - 24 * mm
    x0 = ML

    from reportlab.pdfbase.pdfmetrics import stringWidth
    for i, (phase, time, title) in enumerate(phases):
        row_top = table_y - i * row_h
        # Alternating row shading
        if i % 2 == 0:
            c.setFillColor(FIELD_BG)
            c.rect(x0, row_top - row_h, SLIDE_W - ML - MR, row_h, fill=1, stroke=0)
        # Phase
        c.setFont(F_BOLD, T_SMALL)
        c.setFillColor(INK if phase != "—" else LIGHT)
        c.drawString(x0 + 3 * mm, row_top - row_h / 2 - T_SMALL * 0.35, phase)
        # Time
        c.setFont(F_REG, T_SMALL)
        c.setFillColor(MID)
        c.drawString(x0 + 30 * mm, row_top - row_h / 2 - T_SMALL * 0.35, time)
        # Title
        c.setFont(F_REG if phase == "—" else F_BOLD, T_SMALL)
        c.setFillColor(LIGHT if phase == "—" else INK)
        c.drawString(x0 + 60 * mm, row_top - row_h / 2 - T_SMALL * 0.35, title)

    footer_bar(c, "Designing Learning as a Cross-Functional Activity System")
    slide_number(c, n, TOTAL)


def slide_02_diagnostic_norm(c, n):
    bg(c)
    phase_chip(c, "Ground rule")
    heading(c, "Before we begin", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    # Large callout
    norm = "\u201cWe\u2019re diagnosing the system, not individuals."
    norm2 = "Misalignment is structural, not personal."
    norm3 = "Our goal is coherence, not blame.\u201d"
    y = SLIDE_H / 2 + 14 * mm
    for line in [norm, norm2, norm3]:
        c.setFont(F_BI, 15)
        c.setFillColor(INK)
        c.drawString(ML, y, line)
        y -= 21
    hline(c, y - 2 * mm, lw=0.5, color=RULE_CLR)
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(LIGHT)
    c.drawString(ML, y - 8 * mm, "Return to this norm whenever tension rises during diagnosis.")
    footer_bar(c, "Designing Learning as a Cross-Functional Activity System")
    slide_number(c, n, TOTAL)


def slide_03_p1_header(c, n):
    phase_header_slide(c, "1", "Framing the Shared Object",
        "We begin by surfacing what we already believe learning is — then replacing those beliefs with an operational definition.",
        n, TOTAL, image_placeholder=True)


def slide_04_prompt_1a(c, n):
    bg(c)
    phase_chip(c, "Phase 1 — Activity")
    heading(c, "Writing prompt 1A", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    callout_box(c,
        "Define learning in one sentence.",
        y=SLIDE_H / 2 + 12 * mm, h=14 * mm)
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(MID)
    c.drawString(ML, SLIDE_H / 2 - 2 * mm, "Write without looking at the glossary. 90 seconds. No discussion.")
    footer_bar(c, "Phase 1 — Framing the Shared Object")
    slide_number(c, n, TOTAL)


def slide_05_prompt_1b(c, n):
    bg(c)
    phase_chip(c, "Phase 1 — Activity")
    heading(c, "Writing prompt 1B", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    callout_box(c,
        "How do you know when learning has happened?",
        y=SLIDE_H / 2 + 12 * mm, h=14 * mm)
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(MID)
    c.drawString(ML, SLIDE_H / 2 - 2 * mm, "One sentence. Write, don\u2019t type. 90 seconds.")
    footer_bar(c, "Phase 1 — Framing the Shared Object")
    slide_number(c, n, TOTAL)


def slide_06_definition(c, n):
    bg(c, INK)
    # White right panel
    c.setFillColor(WHITE)
    c.rect(SLIDE_W * 0.48, 0, SLIDE_W * 0.52, SLIDE_H, fill=1, stroke=0)
    # Left: label
    c.setFont(F_BOLD, T_LABEL)
    c.setFillColor(HexColor("#888888"))
    c.drawString(ML, SLIDE_H - MT - 6 * mm, "THE OPERATIONAL DEFINITION")
    # Definition text on dark bg
    defn = [
        "\u201cLearning is durable change",
        "in knowledge structures",
        "that enables future participation",
        "and performance.\u201d",
    ]
    y = SLIDE_H / 2 + 28 * mm
    for line in defn:
        c.setFont(F_BI, 18)
        c.setFillColor(WHITE)
        c.drawString(ML, y, line)
        y -= 24
    # Right panel: key words
    rx = SLIDE_W * 0.52
    rw = SLIDE_W * 0.46
    c.setFont(F_BOLD, T_SMALL)
    c.setFillColor(MID)
    c.drawString(rx + 6 * mm, SLIDE_H - MT - 6 * mm, "THREE WORDS DOING THE WORK")
    hline(c, SLIDE_H - MT - 10 * mm, x0=rx + 6 * mm, x1=SLIDE_W - MR, lw=0.6, color=RULE_CLR)
    keywords = [
        ("Durable", "Not fleeting. Visible months later, not minutes after."),
        ("Knowledge structures", "Organised schemas in long-term memory, not isolated facts."),
        ("Enables future", "The test is what learners can do later, not during the session."),
    ]
    ky = SLIDE_H - MT - 20 * mm
    for kw, desc in keywords:
        c.setFont(F_BOLD, T_BODY)
        c.setFillColor(INK)
        c.drawString(rx + 6 * mm, ky, kw)
        ky -= BODY_LEAD * 0.8
        c.setFont(F_REG, T_SMALL)
        c.setFillColor(MID)
        for wl in _wrap(desc, F_REG, T_SMALL, rw - 12 * mm):
            c.drawString(rx + 6 * mm, ky, wl)
            ky -= SMALL_LEAD * 0.9
        ky -= 4 * mm
    slide_number(c, n, TOTAL)


def slide_07_unpack_definition(c, n):
    bg(c)
    phase_chip(c, "Phase 1 — Insight")
    heading(c, "Participation \u2260 learning", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    c.setFont(F_REG, T_BODY)
    c.setFillColor(MID)
    c.drawString(ML, SLIDE_H - MT - 28 * mm,
        "Most definitions of learning describe activity. Activity is what we hope causes learning.")
    # Two-column contrast
    col1_x = ML
    col2_x = SLIDE_W / 2 + 4 * mm
    col_w = SLIDE_W / 2 - ML - 8 * mm
    y_top = SLIDE_H - MT - 42 * mm

    for cx, label, items, is_strike in [
        (col1_x, "Activity completion", [
            "Watched the video",
            "Completed the quiz",
            "Attended the session",
            "Submitted the reflection",
        ], True),
        (col2_x, "Durable capability", [
            "Recalls and applies the concept 6 months later",
            "Transfers knowledge to a novel situation",
            "Performs competently under real conditions",
            "Judgment improves over time",
        ], False),
    ]:
        c.setFont(F_BOLD, T_SMALL)
        c.setFillColor(LIGHT if is_strike else INK)
        c.drawString(cx, y_top, label)
        hline(c, y_top - 3 * mm, x0=cx, x1=cx + col_w, lw=0.4)
        y = y_top - 10 * mm
        for item in items:
            c.setFont(F_REG, T_SMALL)
            c.setFillColor(LIGHT if is_strike else INK)
            c.drawString(cx, y, ("✕  " if is_strike else "✓  ") + item)
            y -= SMALL_LEAD * 1.1

    footer_bar(c, "Phase 1 — Framing the Shared Object")
    slide_number(c, n, TOTAL)


def slide_08_prompt_1c(c, n):
    bg(c)
    phase_chip(c, "Phase 1 — Activity")
    heading(c, "Writing prompt 1C", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)

    prompts = [
        ("1", "What must learners be able to do 6\u201312 months after your module, in real conditions?"),
        ("2", "What cognitive change must occur for that to be possible?"),
    ]
    y = SLIDE_H / 2 + 20 * mm
    for num, text in prompts:
        # Number circle
        c.setFillColor(INK)
        c.circle(ML + 4 * mm, y + 2 * mm, 4 * mm, fill=1, stroke=0)
        c.setFont(F_BOLD, T_SMALL)
        c.setFillColor(WHITE)
        c.drawCentredString(ML + 4 * mm, y + 0.5 * mm, num)
        # Prompt text
        lines = _wrap(text, F_REG, T_BODY, SLIDE_W - ML - MR - 14 * mm)
        c.setFont(F_REG, T_BODY)
        c.setFillColor(INK)
        ty = y + (len(lines) - 1) * BODY_LEAD / 2
        for line in lines:
            c.drawString(ML + 10 * mm, ty, line)
            ty -= BODY_LEAD
        y -= (len(lines) * BODY_LEAD + 12 * mm)

    c.setFont(F_REG, T_SMALL)
    c.setFillColor(MID)
    c.drawString(ML, MB + 14 * mm, "3 minutes individual writing. Share two or three responses before moving on.")
    footer_bar(c, "Phase 1 — Framing the Shared Object")
    slide_number(c, n, TOTAL)


def slide_09_p2_header(c, n):
    phase_header_slide(c, "2", "Learning Science Core",
        "Three commitments that every design decision in this room must be accountable to.",
        n, TOTAL, image_placeholder=True)


def slide_10_recall_task(c, n):
    bg(c, INK)
    c.setFont(F_BOLD, T_LABEL)
    c.setFillColor(HexColor("#888888"))
    c.drawString(ML, SLIDE_H - MT - 6 * mm, "PHASE 2 \u2014 RECALL TASK")
    c.setFont(F_BOLD, T_DISPLAY)
    c.setFillColor(WHITE)
    c.drawString(ML, SLIDE_H - MT - 20 * mm, "Close your notes.")
    hline(c, SLIDE_H - MT - 24 * mm, lw=1.2, color=WHITE)
    c.setFont(F_BI, 16)
    c.setFillColor(HexColor("#CCCCCC"))
    c.drawString(ML, SLIDE_H / 2 + 6 * mm,
        "Without looking, write the three learning science commitments")
    c.drawString(ML, SLIDE_H / 2 + 6 * mm - 22, "from the pre-work. Two minutes.")
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(HexColor("#666666"))
    c.drawString(ML, SLIDE_H / 2 - 20 * mm, "Silence is intentional. Do not help your neighbour.")
    slide_number(c, n, TOTAL)


def slide_11_reveal_commitments(c, n):
    bg(c)
    phase_chip(c, "Phase 2 — Reveal")
    heading(c, "The three commitments", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)

    items = [
        "Memory precedes complex thinking",
        "Retrieval strengthens memory",
        "Cognitive load must be managed",
    ]
    y = SLIDE_H / 2 + 24 * mm
    for i, item in enumerate(items, 1):
        c.setFont(F_BOLD, 28)
        c.setFillColor(HexColor("#E0E0E0"))
        c.drawString(ML, y + 4 * mm, str(i))
        c.setFont(F_BOLD, T_TITLE)
        c.setFillColor(INK)
        c.drawString(ML + 14 * mm, y, item)
        y -= 32

    c.setFont(F_REG, T_SMALL)
    c.setFillColor(LIGHT)
    c.drawString(ML, MB + 14 * mm,
        "How many did you get? These three commitments are the arbitration language for every design decision today.")
    footer_bar(c, "Phase 2 — Learning Science Core")
    slide_number(c, n, TOTAL)


def commitment_slide(c, n, number, title, body, implication):
    bg(c)
    # Large number watermark
    c.setFont(F_BOLD, 100)
    c.setFillColor(HexColor("#F0F0F0"))
    c.drawString(SLIDE_W - MR - 55 * mm, SLIDE_H / 2 - 30 * mm, number)
    # Labels
    phase_chip(c, f"Commitment {number}")
    heading(c, title, y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    # Body
    c.setFont(F_REG, T_BODY)
    c.setFillColor(INK)
    y = SLIDE_H - MT - 32 * mm
    for line in _wrap(body, F_REG, T_BODY, SLIDE_W - ML - MR - 20 * mm):
        c.drawString(ML, y, line)
        y -= BODY_LEAD
    # Implication box
    y -= 6 * mm
    ilines = _wrap("Design implication: " + implication, F_BI, T_SMALL, SLIDE_W - ML - MR - 14 * mm)
    box_h = len(ilines) * SMALL_LEAD + 6 * mm
    c.setFillColor(HIGHLIGHT)
    c.roundRect(ML, y - box_h, SLIDE_W - ML - MR, box_h + 2 * mm, 2 * mm, fill=1, stroke=0)
    c.setFillColor(INK)
    c.rect(ML, y - box_h, 2.5, box_h + 2 * mm, fill=1, stroke=0)
    ty = y - SMALL_LEAD * 0.5
    c.setFont(F_BI, T_SMALL)
    c.setFillColor(MID)
    for line in ilines:
        c.drawString(ML + 5 * mm, ty, line)
        ty -= SMALL_LEAD
    footer_bar(c, "Phase 2 — Learning Science Core")
    slide_number(c, n, TOTAL)


def slide_12_commitment1(c, n):
    commitment_slide(c, n, "1",
        "Memory precedes complex thinking",
        "You cannot analyse, evaluate or create with knowledge you cannot recall. "
        "Higher-order cognitive operations require accessible knowledge structures in long-term memory.",
        "Sequence instruction so foundational knowledge is encoded and retrievable before learners "
        "are asked to apply it in complex ways."
    )


def slide_13_commitment2(c, n):
    commitment_slide(c, n, "2",
        "Retrieval strengthens memory",
        "Actively recalling information from memory strengthens the neural pathways that make "
        "future recall easier. Re-reading or re-watching does not produce the same effect.",
        "Build retrieval opportunities into the design with specific timing, mechanisms and spacing. "
        "Retrieval is not a test event \u2014 it is an instructional strategy."
    )


def slide_14_commitment3(c, n):
    commitment_slide(c, n, "3",
        "Cognitive load must be managed",
        "Working memory is limited. Extraneous cognitive load \u2014 effort not contributing to "
        "schema formation \u2014 reduces the capacity available for learning. Complexity and novelty "
        "must be introduced deliberately, not simultaneously.",
        "Remove presentation elements that do not serve the learning objective. Manage the number "
        "of new concepts introduced at once. Use worked examples before independent problem-solving."
    )


def slide_15_role_application(c, n):
    bg(c)
    phase_chip(c, "Phase 2 — Role-based application")
    heading(c, "Apply the commitments to your work", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(MID)
    c.drawString(ML, SLIDE_H - MT - 28 * mm, "Form role-based groups. Discuss the three questions below. 10 minutes.")
    prompts = [
        "Where is retrieval structured in your typical design work? Name a specific artefact or moment.",
        "Where might cognitive load be excessive? Name a specific module, assessment or platform.",
        "Where is thinking hidden? Where do learners perform activity without their reasoning being visible?",
    ]
    y = SLIDE_H / 2 + 22 * mm
    for i, p in enumerate(prompts, 1):
        c.setFont(F_BOLD, T_SMALL)
        c.setFillColor(INK)
        c.drawString(ML, y, str(i) + ".")
        c.setFont(F_REG, T_SMALL)
        lines = _wrap(p, F_REG, T_SMALL, SLIDE_W - ML - MR - 10 * mm)
        ty = y
        for line in lines:
            c.drawString(ML + 6 * mm, ty, line)
            ty -= SMALL_LEAD
        y = ty - 5 * mm
    footer_bar(c, "Phase 2 — Learning Science Core")
    slide_number(c, n, TOTAL)


def slide_16_worked_example_setup(c, n):
    bg(c)
    phase_chip(c, "Phase 2 — Worked example")
    heading(c, "Diagnosis in practice", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(MID)
    c.drawString(ML, SLIDE_H - MT - 28 * mm, "Before we diagnose your work, let\u2019s practice on this case.")

    # Two boxes: outcome and assessment
    bw = (SLIDE_W - ML - MR - 8 * mm) / 2
    for i, (label, text) in enumerate([
        ("Module outcome", "Evaluate ethical frameworks"),
        ("Assessment", "Multiple-choice quiz on definitions"),
    ]):
        bx = ML + i * (bw + 8 * mm)
        by = SLIDE_H / 2 - 6 * mm
        c.setFillColor(FIELD_BG)
        c.setStrokeColor(RULE_CLR)
        c.setLineWidth(0.5)
        c.roundRect(bx, by, bw, 20 * mm, 2 * mm, fill=1, stroke=1)
        c.setFont(F_BOLD, T_MICRO)
        c.setFillColor(LIGHT)
        c.drawString(bx + 3 * mm, by + 17 * mm, label.upper())
        c.setFont(F_BOLD, T_BODY)
        c.setFillColor(INK)
        c.drawString(bx + 3 * mm, by + 9 * mm, text)

    c.setFont(F_BI, T_SMALL)
    c.setFillColor(MID)
    c.drawCentredString(SLIDE_W / 2, SLIDE_H / 2 - 14 * mm, "What is the misalignment? Write your answer before the next slide.")
    footer_bar(c, "Phase 2 — Learning Science Core")
    slide_number(c, n, TOTAL)


def slide_17_worked_example_reveal(c, n):
    bg(c)
    phase_chip(c, "Phase 2 — Worked example reveal")
    heading(c, "The diagnosis", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)

    rows = [
        ("Outcome demands", "Evaluation \u2014 apply a schema to a novel ethical situation"),
        ("Assessment tests", "Recognition memory \u2014 recall of labels and definitions"),
        ("Gap", "Schema application requires accessible knowledge AND practiced judgment. The assessment only tests the first condition."),
        ("Commitment violated", "Memory precedes complex thinking: the assessment never asks learners to think."),
    ]
    y = SLIDE_H - MT - 30 * mm
    for label, value in rows:
        c.setFont(F_BOLD, T_SMALL)
        c.setFillColor(MID)
        c.drawString(ML, y, label.upper())
        c.setFont(F_REG, T_BODY)
        c.setFillColor(INK)
        vlines = _wrap(value, F_REG, T_BODY, SLIDE_W - ML - MR - 45 * mm)
        vy = y
        for vl in vlines:
            c.drawString(ML + 42 * mm, vy, vl)
            vy -= BODY_LEAD
        y = min(vy, y - BODY_LEAD) - 3 * mm
        hline(c, y + 1.5 * mm, lw=0.3)

    footer_bar(c, "Phase 2 — Learning Science Core")
    slide_number(c, n, TOTAL)


def slide_18_p3_header(c, n):
    phase_header_slide(c, "3", "Role Mapping",
        "Each role mediates learning differently. Making those differences concrete is the first step toward genuine coordination.",
        n, TOTAL, image_placeholder=True)


def slide_19_role_clarification(c, n):
    bg(c)
    phase_chip(c, "Phase 3 — Role clarification")
    heading(c, "Work within your role group", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(MID)
    c.drawString(ML, SLIDE_H - MT - 27 * mm, "Use the prompts in your workbook. 15 minutes.")

    roles = [
        ("Curriculum Design",         "Alignment, sequencing, transfer"),
        ("Learning / Experience Design", "Cognitive operations, retrieval, visible reasoning"),
        ("Multimedia Design",          "Cognitive function, load, schema support"),
        ("Learning Technology",        "Affordances, constraints, analytics"),
    ]
    col_w = (SLIDE_W - ML - MR) / 2 - 4 * mm
    y = SLIDE_H / 2 + 22 * mm
    for i, (role, focus) in enumerate(roles):
        cx = ML if i % 2 == 0 else ML + col_w + 8 * mm
        cy = y if i < 2 else y - 26 * mm
        c.setFillColor(FIELD_BG)
        c.roundRect(cx, cy - 14 * mm, col_w, 18 * mm, 2 * mm, fill=1, stroke=0)
        c.setFont(F_BOLD, T_SMALL)
        c.setFillColor(INK)
        c.drawString(cx + 3 * mm, cy - 1 * mm, role)
        c.setFont(F_REG, T_MICRO)
        c.setFillColor(MID)
        c.drawString(cx + 3 * mm, cy - 7 * mm, focus)

    footer_bar(c, "Phase 3 — Role Mapping")
    slide_number(c, n, TOTAL)


def slide_20_perspective_taking(c, n):
    bg(c)
    phase_chip(c, "Phase 3 — Cross-role perspective taking")
    heading(c, "Pair with a different role", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    steps = [
        ("Step 1", "Describe a real design decision you made recently."),
        ("Step 2", "Your partner identifies which learning science commitment it serves \u2014 or violates."),
        ("Step 3", "Switch. 2 minutes per person."),
    ]
    y = SLIDE_H / 2 + 20 * mm
    for label, text in steps:
        c.setFont(F_BOLD, T_BODY)
        c.setFillColor(INK)
        c.drawString(ML, y, label)
        c.setFont(F_REG, T_BODY)
        c.setFillColor(MID)
        lines = _wrap(text, F_REG, T_BODY, SLIDE_W - ML - MR - 30 * mm)
        ty = y
        for line in lines:
            c.drawString(ML + 26 * mm, ty, line)
            ty -= BODY_LEAD
        y = ty - 5 * mm
    footer_bar(c, "Phase 3 — Role Mapping")
    slide_number(c, n, TOTAL)


def slide_21_transition_p4(c, n):
    bg(c, INK)
    c.setFont(F_BOLD, T_LABEL)
    c.setFillColor(HexColor("#888888"))
    c.drawString(ML, SLIDE_H - MT - 6 * mm, "TRANSITION")
    c.setFont(F_BOLD, 22)
    c.setFillColor(WHITE)
    c.drawString(ML, SLIDE_H / 2 + 16 * mm, "The question shifts.")
    hline(c, SLIDE_H / 2 + 10 * mm, lw=1, color=WHITE)
    c.setFont(F_REG, 16)
    c.setFillColor(HexColor("#AAAAAA"))
    c.drawString(ML, SLIDE_H / 2 - 2 * mm, "From: \u201cWhat does my role do?\u201d")
    c.setFont(F_BOLD, 16)
    c.setFillColor(WHITE)
    c.drawString(ML, SLIDE_H / 2 - 18 * mm, "To: \u201cWhere is the system failing the learner?\u201d")
    # Team assignment note
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(HexColor("#666666"))
    c.drawString(ML, MB + 14 * mm, "Mixed-role team assignments will now be revealed.")
    slide_number(c, n, TOTAL)


def slide_22_p4_header(c, n):
    phase_header_slide(c, "4", "Cross-Role Diagnosis",
        "Apply learning science as a shared diagnostic lens to real design artefacts you brought to this room.",
        n, TOTAL, image_placeholder=True)


def slide_23_diagnostic_norm_reminder(c, n):
    bg(c)
    phase_chip(c, "Phase 4 — Ground rule")
    heading(c, "Reminder before we begin", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    norm_lines = [
        "\u201cWe\u2019re diagnosing the system, not individuals.",
        "Misalignment is structural, not personal.",
        "Our goal is coherence, not blame.\u201d",
    ]
    y = SLIDE_H / 2 + 16 * mm
    for line in norm_lines:
        c.setFont(F_BI, 16)
        c.setFillColor(INK)
        c.drawString(ML, y, line)
        y -= 22
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(LIGHT)
    c.drawString(ML, MB + 14 * mm, "Point to specific elements in the artefact. Not general impressions.")
    footer_bar(c, "Phase 4 — Cross-Role Diagnosis")
    slide_number(c, n, TOTAL)


def slide_24_stage1_identify(c, n):
    bg(c)
    phase_chip(c, "Phase 4 \u2014 Stage 1")
    heading(c, "Identify", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(MID)
    c.drawString(ML, SLIDE_H - MT - 27 * mm, "5 minutes. Point to specific elements in the artefact.")
    questions = [
        "What must learners remember?",
        "Where is retrieval structured?",
        "Where is thinking visible?",
        "Where is cognitive load unnecessary?",
    ]
    y = SLIDE_H / 2 + 24 * mm
    for i, q in enumerate(questions, 1):
        c.setFont(F_BOLD, T_BODY)
        c.setFillColor(LIGHT)
        c.drawString(ML, y, str(i) + ".")
        c.setFont(F_REG, T_BODY)
        c.setFillColor(INK)
        c.drawString(ML + 8 * mm, y, q)
        y -= BODY_LEAD * 1.4
    footer_bar(c, "Phase 4 — Cross-Role Diagnosis")
    slide_number(c, n, TOTAL)


def slide_25_stage2_diagnose(c, n):
    bg(c)
    phase_chip(c, "Phase 4 \u2014 Stage 2")
    heading(c, "Diagnose misalignment", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(MID)
    c.drawString(ML, SLIDE_H - MT - 27 * mm, "20 minutes. Work through both questions.")
    questions = [
        ("5", "Where do role decisions contradict each other?",
         "List at least two contradictions."),
        ("6", "Which contradictions most impair learning?",
         "Rank by impact on the learner. This is your redesign focus."),
    ]
    y = SLIDE_H / 2 + 22 * mm
    for num, q, hint in questions:
        c.setFont(F_BOLD, 26)
        c.setFillColor(HexColor("#E8E8E8"))
        c.drawString(ML, y + 6 * mm, num)
        c.setFont(F_BOLD, T_BODY)
        c.setFillColor(INK)
        c.drawString(ML + 12 * mm, y, q)
        c.setFont(F_ITALIC, T_SMALL)
        c.setFillColor(MID)
        c.drawString(ML + 12 * mm, y - SMALL_LEAD, hint)
        y -= BODY_LEAD * 2 + 8 * mm
    footer_bar(c, "Phase 4 — Cross-Role Diagnosis")
    slide_number(c, n, TOTAL)


def slide_26_break(c, n):
    bg(c, FIELD_BG)
    c.setFont(F_BOLD, T_HERO)
    c.setFillColor(HexColor("#CCCCCC"))
    c.drawCentredString(SLIDE_W / 2, SLIDE_H / 2 + 4 * mm, "Break")
    c.setFont(F_REG, T_BODY)
    c.setFillColor(LIGHT)
    c.drawCentredString(SLIDE_W / 2, SLIDE_H / 2 - 14 * mm, "10 minutes")
    c.setFont(F_BI, T_SMALL)
    c.setFillColor(MID)
    c.drawCentredString(SLIDE_W / 2, MB + 16 * mm,
        "When you return: identify the one misalignment most blocking learning. That is your redesign focus.")
    slide_number(c, n, TOTAL)


def slide_27_p5_header(c, n):
    phase_header_slide(c, "5", "Collaborative Redesign",
        "Translate the diagnosis into a coherent, learning-science-grounded redesign. "
        "Seven sections. One capability object. All roles contributing.",
        n, TOTAL, image_placeholder=True)


def slide_28_redesign_map(c, n):
    bg(c)
    phase_chip(c, "Phase 5 — Redesign map")
    heading(c, "Seven sections. One coherent object.", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(MID)
    c.drawString(ML, SLIDE_H - MT - 27 * mm,
        "Use the template in your workbook. 25 minutes. Coherent \u003e complete.")

    sections = [
        ("1", "Capability Object"),
        ("2", "Retrieval Points"),
        ("3", "Visible Reasoning"),
        ("4", "Load Reduction"),
        ("5", "Media Justification"),
        ("6", "Platform Alignment"),
        ("7", "Connection to Programme"),
    ]
    col_count = 4
    cell_w = (SLIDE_W - ML - MR - (col_count - 1) * 4 * mm) / col_count
    cell_h = 18 * mm
    y_top = SLIDE_H / 2 + 20 * mm
    for i, (num, title) in enumerate(sections):
        row = i // col_count
        col = i % col_count
        cx = ML + col * (cell_w + 4 * mm)
        cy = y_top - row * (cell_h + 4 * mm)
        c.setFillColor(FIELD_BG)
        c.roundRect(cx, cy - cell_h, cell_w, cell_h, 2 * mm, fill=1, stroke=0)
        c.setFont(F_BOLD, T_LABEL)
        c.setFillColor(LIGHT)
        c.drawString(cx + 3 * mm, cy - 5 * mm, num + ".")
        c.setFont(F_BOLD, T_SMALL)
        c.setFillColor(INK)
        lines = _wrap(title, F_BOLD, T_SMALL, cell_w - 8 * mm)
        ty = cy - 11 * mm
        for line in lines:
            c.drawString(cx + 3 * mm, ty, line)
            ty -= SMALL_LEAD

    footer_bar(c, "Phase 5 — Collaborative Redesign")
    slide_number(c, n, TOTAL)


def slide_29_lsj_prompt(c, n):
    bg(c)
    phase_chip(c, "Phase 5 — Learning Science Justification")
    heading(c, "Before the gallery walk", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(MID)
    c.drawString(ML, SLIDE_H - MT - 28 * mm,
        "Complete the Learning Science Justification section. If you cannot answer these, "
        "the redesign is not yet grounded in science.")
    questions = [
        "What memory structures are strengthened by this redesign?",
        "Where is retrieval embedded, and at what intervals?",
        "What cognitive load decisions were made? What was added, what was removed, and why?",
    ]
    y = SLIDE_H / 2 + 18 * mm
    for q in questions:
        c.setFillColor(INK)
        c.circle(ML + 2.5 * mm, y + 1.5 * mm, 2.5 * mm, fill=1, stroke=0)
        c.setFont(F_REG, T_BODY)
        c.setFillColor(INK)
        lines = _wrap(q, F_REG, T_BODY, SLIDE_W - ML - MR - 10 * mm)
        ty = y
        for line in lines:
            c.drawString(ML + 8 * mm, ty, line)
            ty -= BODY_LEAD
        y = ty - 5 * mm
    footer_bar(c, "Phase 5 — Collaborative Redesign")
    slide_number(c, n, TOTAL)


def slide_30_p6_header(c, n):
    phase_header_slide(c, "6", "Cross-Team Critique",
        "Structured feedback grounded in learning science. Three notes per redesign. No general impressions.",
        n, TOTAL, image_placeholder=False)


def slide_31_gallery_walk(c, n):
    bg(c)
    phase_chip(c, "Phase 6 — Gallery walk protocol")
    heading(c, "Three notes. Every reviewer. Every redesign.", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(MID)
    c.drawString(ML, SLIDE_H - MT - 27 * mm, "Review at least two redesigns. 15 minutes.")

    notes = [
        (HexColor("#4A7C59"), "Green sticky", "Strength",
         "What aligns well with learning science? Name the commitment it serves."),
        (HexColor("#B8860B"), "Yellow sticky", "Tension",
         "Where might the design impair learning? Name the commitment it violates."),
        (HexColor("#2B5EA7"), "Blue sticky", "Clarification question",
         "What needs more explanation to evaluate the design?"),
    ]
    y = SLIDE_H / 2 + 24 * mm
    for color, sticky, label, desc in notes:
        c.setFillColor(color)
        c.roundRect(ML, y - 2 * mm, 3 * mm, 10 * mm, 1 * mm, fill=1, stroke=0)
        c.setFont(F_BOLD, T_BODY)
        c.setFillColor(INK)
        c.drawString(ML + 7 * mm, y + 5 * mm, label)
        c.setFont(F_REG, T_SMALL)
        c.setFillColor(MID)
        lines = _wrap(desc, F_REG, T_SMALL, SLIDE_W - ML - MR - 12 * mm)
        ty = y - 1 * mm
        for line in lines:
            c.drawString(ML + 7 * mm, ty, line)
            ty -= SMALL_LEAD
        y = ty - 8 * mm

    footer_bar(c, "Phase 6 — Cross-Team Critique")
    slide_number(c, n, TOTAL)


def slide_32_p7_header(c, n):
    phase_header_slide(c, "7", "Collaboration Charter",
        "Convert individual insight into concrete, accountable collective commitment.",
        n, TOTAL, image_placeholder=False)


def slide_33_commitments_prompt(c, n):
    bg(c)
    phase_chip(c, "Phase 7 — Individual commitments")
    heading(c, "Write before you share", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(MID)
    c.drawString(ML, SLIDE_H - MT - 27 * mm, "3 minutes. Individual writing first. No discussion until everyone has written.")
    prompts = [
        "One decision I will no longer make alone",
        "One role I need earlier in the design process",
        "One learning science principle I will use in future discussions",
        "One process change we will implement in the next design cycle",
    ]
    y = SLIDE_H / 2 + 22 * mm
    for p in prompts:
        c.setFont(F_REG, T_BODY)
        c.setFillColor(INK)
        c.drawString(ML, y, "\u2014  " + p)
        y -= BODY_LEAD * 1.5
    footer_bar(c, "Phase 7 — Collaboration Charter")
    slide_number(c, n, TOTAL)


def slide_34_followup_plan(c, n):
    bg(c)
    phase_chip(c, "Phase 7 — 30-day follow-up")
    heading(c, "In 4 weeks.", y=SLIDE_H - MT - 16 * mm)
    hline(c, SLIDE_H - MT - 20 * mm, lw=1, color=INK)
    c.setFont(F_REG, T_BODY)
    c.setFillColor(MID)
    c.drawString(ML, SLIDE_H - MT - 29 * mm, "We meet for 30 minutes. Each role shares three things.")
    items = [
        "One decision you made differently since the workshop",
        "One place where collaboration improved",
        "One remaining misalignment that needs addressing",
    ]
    y = SLIDE_H / 2 + 14 * mm
    for i, item in enumerate(items, 1):
        c.setFont(F_BOLD, T_TITLE)
        c.setFillColor(HexColor("#E0E0E0"))
        c.drawString(ML, y + 4 * mm, str(i))
        c.setFont(F_REG, T_BODY)
        c.setFillColor(INK)
        c.drawString(ML + 12 * mm, y, item)
        y -= BODY_LEAD * 1.8
    c.setFont(F_BI, T_SMALL)
    c.setFillColor(LIGHT)
    c.drawString(ML, MB + 14 * mm, "Calendar invitations go out today. This is not optional.")
    footer_bar(c, "Phase 7 — Collaboration Charter")
    slide_number(c, n, TOTAL)


def slide_35_closing_retrieval(c, n):
    bg(c, INK)
    c.setFont(F_BOLD, T_LABEL)
    c.setFillColor(HexColor("#888888"))
    c.drawString(ML, SLIDE_H - MT - 6 * mm, "CLOSING RETRIEVAL TASK")
    c.setFont(F_BOLD, T_DISPLAY)
    c.setFillColor(WHITE)
    c.drawString(ML, SLIDE_H - MT - 20 * mm, "No notes. Write three things.")
    hline(c, SLIDE_H - MT - 25 * mm, lw=1.2, color=WHITE)
    items = [
        "How you now define learning",
        "One way your role mediates cognitive change",
        "One collaboration commitment you are taking forward",
    ]
    y = SLIDE_H / 2 + 16 * mm
    for item in items:
        c.setFont(F_REG, 15)
        c.setFillColor(HexColor("#CCCCCC"))
        c.drawString(ML, y, "\u2014  " + item)
        y -= 24
    c.setFont(F_REG, T_SMALL)
    c.setFillColor(HexColor("#666666"))
    c.drawString(ML, MB + 14 * mm, "2 minutes. Silent. These are for you, not for the group.")
    slide_number(c, n, TOTAL)


def slide_36_close(c, n):
    bg(c, INK)
    # White strip
    c.setFillColor(WHITE)
    c.rect(0, 0, SLIDE_W * 0.42, SLIDE_H, fill=1, stroke=0)
    # Image slot
    image_slot(c, 0, 0, SLIDE_W * 0.40, SLIDE_H, "CLOSING IMAGE")
    # Right side
    rx = SLIDE_W * 0.44
    c.setFont(F_BOLD, T_LABEL)
    c.setFillColor(HexColor("#666666"))
    c.drawString(rx, SLIDE_H - MT - 6 * mm, "YOU LEAVE WITH")
    hline(c, SLIDE_H - MT - 10 * mm, x0=rx, lw=0.6, color=HexColor("#444444"))
    takeaways = [
        "A redesigned learning experience artefact",
        "A shared operational definition of learning",
        "Practical learning science commitments",
        "A cross-role collaboration charter",
        "A 30-day follow-up plan",
    ]
    y = SLIDE_H - MT - 20 * mm
    for t in takeaways:
        c.setFont(F_REG, T_SMALL)
        c.setFillColor(WHITE)
        c.drawString(rx, y, "\u2014  " + t)
        y -= SMALL_LEAD * 1.3
    slide_number(c, n, TOTAL)


# ─── Build ────────────────────────────────────────────────────────────────────

def build_slides(output_path):
    c = pdfcanvas.Canvas(output_path, pagesize=(SLIDE_W, SLIDE_H))
    c.setTitle("Designing Learning as a Cross-Functional Activity System — Workshop Slides")
    c.setAuthor("Learning Experience Design")

    slides = [
        slide_00_title,
        slide_01_agenda,
        slide_02_diagnostic_norm,
        slide_03_p1_header,
        slide_04_prompt_1a,
        slide_05_prompt_1b,
        slide_06_definition,
        slide_07_unpack_definition,
        slide_08_prompt_1c,
        slide_09_p2_header,
        slide_10_recall_task,
        slide_11_reveal_commitments,
        slide_12_commitment1,
        slide_13_commitment2,
        slide_14_commitment3,
        slide_15_role_application,
        slide_16_worked_example_setup,
        slide_17_worked_example_reveal,
        slide_18_p3_header,
        slide_19_role_clarification,
        slide_20_perspective_taking,
        slide_21_transition_p4,
        slide_22_p4_header,
        slide_23_diagnostic_norm_reminder,
        slide_24_stage1_identify,
        slide_25_stage2_diagnose,
        slide_26_break,
        slide_27_p5_header,
        slide_28_redesign_map,
        slide_29_lsj_prompt,
        slide_30_p6_header,
        slide_31_gallery_walk,
        slide_32_p7_header,
        slide_33_commitments_prompt,
        slide_34_followup_plan,
        slide_35_closing_retrieval,
        slide_36_close,
    ]

    for i, slide_fn in enumerate(slides, 1):
        slide_fn(c, i)
        c.showPage()

    c.save()
    print(f"Slides written to: {output_path}")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "workshop-slides.pdf")
    build_slides(out)
