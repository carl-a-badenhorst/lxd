"""
Generates learner-handout.pdf for the cross-functional learning design workshop.
Design system: minimalist utilitarian — monochrome, strict type scale, rule lines for write-in fields.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os

# ─── Design tokens ────────────────────────────────────────────────────────────

INK       = HexColor("#111111")
MID       = HexColor("#555555")
LIGHT     = HexColor("#999999")
RULE      = HexColor("#CCCCCC")
FIELD_BG  = HexColor("#F7F7F7")
WHITE     = white

PAGE_W, PAGE_H = A4
MARGIN_LEFT   = 20 * mm
MARGIN_RIGHT  = 20 * mm
MARGIN_TOP    = 22 * mm
MARGIN_BOTTOM = 18 * mm

BODY_W = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT

# Type scale (pt)
T_DISPLAY  = 20
T_TITLE    = 13
T_LABEL    = 9
T_BODY     = 9.5
T_SMALL    = 8
T_MICRO    = 7.5

LEADING_DISPLAY = 24
LEADING_TITLE   = 17
LEADING_BODY    = 14
LEADING_SMALL   = 12
LEADING_MICRO   = 11

# ─── Styles ───────────────────────────────────────────────────────────────────

def make_styles():
    s = {}

    s["display"] = ParagraphStyle(
        "display",
        fontName="Helvetica-Bold",
        fontSize=T_DISPLAY,
        leading=LEADING_DISPLAY,
        textColor=INK,
        spaceAfter=2 * mm,
    )
    s["subtitle"] = ParagraphStyle(
        "subtitle",
        fontName="Helvetica",
        fontSize=T_LABEL,
        leading=LEADING_SMALL,
        textColor=MID,
        spaceAfter=6 * mm,
    )
    s["section_label"] = ParagraphStyle(
        "section_label",
        fontName="Helvetica-Bold",
        fontSize=T_LABEL,
        leading=LEADING_SMALL,
        textColor=MID,
        spaceBefore=5 * mm,
        spaceAfter=1 * mm,
        textTransform="uppercase",
        letterSpacing=0.8,
    )
    s["phase_heading"] = ParagraphStyle(
        "phase_heading",
        fontName="Helvetica-Bold",
        fontSize=T_TITLE,
        leading=LEADING_TITLE,
        textColor=INK,
        spaceBefore=4 * mm,
        spaceAfter=2 * mm,
    )
    s["sub_heading"] = ParagraphStyle(
        "sub_heading",
        fontName="Helvetica-Bold",
        fontSize=T_BODY,
        leading=LEADING_BODY,
        textColor=INK,
        spaceBefore=3 * mm,
        spaceAfter=1 * mm,
    )
    s["prompt_label"] = ParagraphStyle(
        "prompt_label",
        fontName="Helvetica-Bold",
        fontSize=T_SMALL,
        leading=LEADING_SMALL,
        textColor=INK,
        spaceBefore=3 * mm,
        spaceAfter=1.5 * mm,
    )
    s["body"] = ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=T_BODY,
        leading=LEADING_BODY,
        textColor=INK,
        spaceAfter=2 * mm,
    )
    s["body_note"] = ParagraphStyle(
        "body_note",
        fontName="Helvetica-Oblique",
        fontSize=T_SMALL,
        leading=LEADING_SMALL,
        textColor=MID,
        spaceAfter=2 * mm,
    )
    s["small"] = ParagraphStyle(
        "small",
        fontName="Helvetica",
        fontSize=T_SMALL,
        leading=LEADING_SMALL,
        textColor=MID,
        spaceAfter=1.5 * mm,
    )
    s["micro"] = ParagraphStyle(
        "micro",
        fontName="Helvetica",
        fontSize=T_MICRO,
        leading=LEADING_MICRO,
        textColor=LIGHT,
    )
    s["table_header"] = ParagraphStyle(
        "table_header",
        fontName="Helvetica-Bold",
        fontSize=T_SMALL,
        leading=LEADING_SMALL,
        textColor=INK,
    )
    s["table_cell"] = ParagraphStyle(
        "table_cell",
        fontName="Helvetica",
        fontSize=T_SMALL,
        leading=LEADING_SMALL,
        textColor=INK,
    )
    s["quote"] = ParagraphStyle(
        "quote",
        fontName="Helvetica-BoldOblique",
        fontSize=T_BODY,
        leading=LEADING_BODY,
        textColor=INK,
        leftIndent=5 * mm,
        spaceBefore=2 * mm,
        spaceAfter=2 * mm,
    )
    s["reference_heading"] = ParagraphStyle(
        "reference_heading",
        fontName="Helvetica-Bold",
        fontSize=T_BODY,
        leading=LEADING_BODY,
        textColor=INK,
        spaceBefore=4 * mm,
        spaceAfter=1 * mm,
    )
    s["footer"] = ParagraphStyle(
        "footer",
        fontName="Helvetica",
        fontSize=T_MICRO,
        leading=LEADING_MICRO,
        textColor=LIGHT,
        alignment=TA_CENTER,
    )

    return s


# ─── Reusable components ──────────────────────────────────────────────────────

def rule(width=None, thickness=0.5, color=RULE, space_before=1*mm, space_after=1*mm):
    return HRFlowable(
        width=width or "100%",
        thickness=thickness,
        color=color,
        spaceAfter=space_after,
        spaceBefore=space_before,
        lineCap="round",
    )

def write_lines(n=3, width=None):
    """Returns n blank write-in line rows as a Table."""
    w = width or BODY_W
    rows = []
    for _ in range(n):
        rows.append([""])
    t = Table(rows, colWidths=[w])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), FIELD_BG),
        ("LINEBELOW",     (0, 0), (-1, -1), 0.5, RULE),
        ("LEFTPADDING",   (0, 0), (-1, -1), 3),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 3),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    return t

def inline_field(label, width=None):
    """Single-line labelled field."""
    w = width or BODY_W
    t = Table([[label, ""]], colWidths=[w * 0.35, w * 0.65])
    t.setStyle(TableStyle([
        ("FONTNAME",      (0, 0), (0, 0), "Helvetica-Bold"),
        ("FONTNAME",      (1, 0), (1, 0), "Helvetica"),
        ("FONTSIZE",      (0, 0), (-1, -1), T_SMALL),
        ("LEADING",       (0, 0), (-1, -1), LEADING_SMALL),
        ("TEXTCOLOR",     (0, 0), (0, 0), INK),
        ("TEXTCOLOR",     (1, 0), (1, 0), MID),
        ("LINEBELOW",     (1, 0), (1, 0), 0.5, INK),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
        ("TOPPADDING",    (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("VALIGN",        (0, 0), (-1, -1), "BOTTOM"),
    ]))
    return t

def grid_table(headers, row_count, col_widths=None):
    """Structured table with headers and empty data rows for writing."""
    col_widths = col_widths or [BODY_W / len(headers)] * len(headers)
    header_row = [Paragraph(h, make_styles()["table_header"]) for h in headers]
    data_rows = [[""] * len(headers) for _ in range(row_count)]
    data = [header_row] + data_rows
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), INK),
        ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
        ("BACKGROUND",    (0, 1), (-1, -1), FIELD_BG),
        ("GRID",          (0, 0), (-1, -1), 0.4, RULE),
        ("LINEBELOW",     (0, 1), (-1, -1), 0.5, RULE),
        ("LEFTPADDING",   (0, 0), (-1, -1), 4),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
        ("TOPPADDING",    (0, 0), (-1, 0), 4),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
        ("TOPPADDING",    (0, 1), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 2),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), T_SMALL),
        ("LEADING",       (0, 0), (-1, -1), LEADING_SMALL),
    ]))
    return t

def section_divider(styles):
    return [rule(thickness=0.5, color=RULE, space_before=3*mm, space_after=3*mm)]

def phase_header(number, title, styles):
    """Phase header block with a number tag and title."""
    label = Paragraph(f"PHASE {number}", styles["section_label"])
    heading = Paragraph(title, styles["phase_heading"])
    return [label, heading, rule(thickness=1, color=INK, space_before=0, space_after=3*mm)]


# ─── Page template (header/footer) ────────────────────────────────────────────

class WorkbookTemplate(SimpleDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        self._page_num = 0

    def handle_pageBegin(self):
        self._page_num += 1
        super().handle_pageBegin()

    def afterPage(self):
        c = self.canv
        # Footer left: workbook title
        c.setFont("Helvetica", T_MICRO)
        c.setFillColor(LIGHT)
        c.drawString(
            MARGIN_LEFT,
            MARGIN_BOTTOM - 4 * mm,
            "Participant Workbook — Designing Learning as a Cross-Functional Activity System"
        )
        # Footer right: page number
        c.drawRightString(
            PAGE_W - MARGIN_RIGHT,
            MARGIN_BOTTOM - 4 * mm,
            f"{self.page}"
        )
        # Footer rule
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        c.line(MARGIN_LEFT, MARGIN_BOTTOM - 1.5 * mm, PAGE_W - MARGIN_RIGHT, MARGIN_BOTTOM - 1.5 * mm)


# ─── Content builders ─────────────────────────────────────────────────────────

def build_cover(styles):
    elems = []
    elems.append(Spacer(1, 20 * mm))
    elems.append(Paragraph("Participant Workbook", styles["display"]))
    elems.append(Paragraph(
        "Designing Learning as a Cross-Functional Activity System",
        styles["subtitle"]
    ))
    elems.append(rule(thickness=1.5, color=INK, space_before=2*mm, space_after=8*mm))

    # Identity fields
    for label in ["Name", "Role", "Date"]:
        elems.append(inline_field(f"{label}:"))
        elems.append(Spacer(1, 3 * mm))

    elems.append(Spacer(1, 10 * mm))
    elems.append(rule(thickness=0.5, color=RULE))
    elems.append(Spacer(1, 4 * mm))

    # How to use
    elems.append(Paragraph("How to use this workbook", styles["sub_heading"]))
    elems.append(Paragraph(
        "This workbook is yours. Write in it. The prompts are structured to build on each other, "
        "so work through them in order and bring the workbook to the 30-day follow-up session.",
        styles["body"]
    ))
    elems.append(Paragraph(
        "You will be asked to write before discussion in almost every phase. That sequencing is "
        "deliberate: individual thinking before group conversation produces better ideas and reduces "
        "the pull toward the most confident voice in the room.",
        styles["body"]
    ))

    elems.append(Spacer(1, 6 * mm))
    elems.append(rule(thickness=0.5, color=RULE))
    elems.append(Spacer(1, 4 * mm))

    # Glossary
    elems.append(Paragraph("Key terms", styles["sub_heading"]))
    elems.append(Paragraph(
        "Review these terms before the workshop. We will use them consistently throughout the session.",
        styles["small"]
    ))
    elems.append(Spacer(1, 2 * mm))

    glossary_data = [
        [Paragraph("Term", styles["table_header"]), Paragraph("Definition", styles["table_header"])],
        [Paragraph("Schema", styles["table_cell"]),
         Paragraph("Organised knowledge structures in long-term memory", styles["table_cell"])],
        [Paragraph("Retrieval", styles["table_cell"]),
         Paragraph("Actively recalling information from memory — not re-reading it", styles["table_cell"])],
        [Paragraph("Cognitive load", styles["table_cell"]),
         Paragraph("The mental effort required during learning", styles["table_cell"])],
        [Paragraph("Extraneous load", styles["table_cell"]),
         Paragraph("Effort that does not contribute to schema formation", styles["table_cell"])],
        [Paragraph("Germane load", styles["table_cell"]),
         Paragraph("Effort that builds understanding", styles["table_cell"])],
        [Paragraph("Object of design", styles["table_cell"]),
         Paragraph("The shared cognitive outcome all roles are working toward", styles["table_cell"])],
        [Paragraph("Activity system", styles["table_cell"]),
         Paragraph("A social structure where multiple roles coordinate tools, rules and artefacts toward a shared outcome", styles["table_cell"])],
        [Paragraph("Durable capability", styles["table_cell"]),
         Paragraph("The ability to perform competently in real conditions, 6 to 12 months after a learning experience", styles["table_cell"])],
    ]
    col_w = [BODY_W * 0.28, BODY_W * 0.72]
    t = Table(glossary_data, colWidths=col_w)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), INK),
        ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
        ("BACKGROUND",    (0, 1), (-1, -1), FIELD_BG),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, FIELD_BG]),
        ("GRID",          (0, 0), (-1, -1), 0.4, RULE),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    elems.append(t)

    return elems


def build_phase1(styles):
    elems = []
    elems += phase_header("1", "Framing the Shared Object", styles)

    elems.append(Paragraph("Writing prompt 1A", styles["prompt_label"]))
    elems.append(Paragraph(
        "Define learning in one sentence. Write without looking at the glossary.",
        styles["body_note"]
    ))
    elems.append(write_lines(3))
    elems.append(Spacer(1, 4 * mm))

    elems.append(Paragraph("Writing prompt 1B", styles["prompt_label"]))
    elems.append(Paragraph(
        "How do you know when learning has happened?",
        styles["body_note"]
    ))
    elems.append(write_lines(3))
    elems.append(Spacer(1, 4 * mm))

    elems.append(rule(thickness=0.5, color=RULE, space_before=2*mm, space_after=3*mm))
    elems.append(Paragraph("The operational definition", styles["sub_heading"]))
    elems.append(Paragraph(
        "After the facilitator introduces it, write the definition here in your own words:",
        styles["body_note"]
    ))
    elems.append(write_lines(2))
    elems.append(Spacer(1, 4 * mm))

    elems.append(rule(thickness=0.5, color=RULE, space_before=2*mm, space_after=3*mm))
    elems.append(Paragraph("Writing prompt 1C", styles["prompt_label"]))
    elems.append(Paragraph(
        "Apply the definition to your current work.",
        styles["body_note"]
    ))

    elems.append(Paragraph(
        "What must learners be able to do 6 to 12 months after your module or programme, in real conditions?",
        styles["prompt_label"]
    ))
    elems.append(write_lines(3))
    elems.append(Spacer(1, 4 * mm))

    elems.append(Paragraph(
        "What cognitive change must occur for that to be possible?",
        styles["prompt_label"]
    ))
    elems.append(Paragraph(
        "What must change in their mental models, schemas or judgment?",
        styles["body_note"]
    ))
    elems.append(write_lines(3))

    return elems


def build_phase2(styles):
    elems = []
    elems += phase_header("2", "Learning Science Core", styles)

    elems.append(Paragraph("Recall task", styles["sub_heading"]))
    elems.append(Paragraph(
        "Without looking at your notes or the glossary, write the three learning science commitments from the pre-work.",
        styles["body_note"]
    ))
    elems.append(Spacer(1, 2 * mm))

    for n in ["1", "2", "3"]:
        elems.append(Paragraph(n + ".", styles["prompt_label"]))
        elems.append(write_lines(2))
        elems.append(Spacer(1, 2 * mm))

    elems.append(rule(thickness=0.5, color=RULE, space_before=3*mm, space_after=3*mm))
    elems.append(Paragraph("Role-based application", styles["sub_heading"]))
    elems.append(Paragraph("Work through these prompts with your role group.", styles["body_note"]))
    elems.append(Spacer(1, 2 * mm))

    prompts = [
        ("Where is retrieval structured in your typical design work?",
         "Name a specific artefact or moment."),
        ("Where might cognitive load be excessive?",
         "Name a specific place in a module, assessment or platform."),
        ("Where is thinking hidden?",
         "Where do learners perform activity without their reasoning being visible?"),
    ]
    for q, hint in prompts:
        elems.append(Paragraph(q, styles["prompt_label"]))
        elems.append(Paragraph(hint, styles["body_note"]))
        elems.append(write_lines(3))
        elems.append(Spacer(1, 3 * mm))

    elems.append(rule(thickness=0.5, color=RULE, space_before=2*mm, space_after=3*mm))
    elems.append(Paragraph("Worked example notes", styles["sub_heading"]))
    elems.append(Paragraph(
        "Use this space to note the misalignment the facilitator demonstrates.",
        styles["body_note"]
    ))
    elems.append(Spacer(1, 2 * mm))

    for label in ["Module outcome:", "Assessment:", "Misalignment:", "Why it impairs learning:"]:
        elems.append(Paragraph(label, styles["prompt_label"]))
        elems.append(write_lines(2))
        elems.append(Spacer(1, 2 * mm))

    return elems


def build_phase3(styles):
    elems = []
    elems += phase_header("3", "Role Mapping", styles)

    elems.append(Paragraph("Part A — Role clarification", styles["sub_heading"]))
    elems.append(Paragraph(
        "Work through the prompts for your role only.",
        styles["body_note"]
    ))
    elems.append(Spacer(1, 3 * mm))

    roles = [
        ("Curriculum Design", [
            ("Where does this module align with programme-level capability?", "What is the specific link?"),
            ("Where is knowledge reinforced over time in the programme?", "List two or three points."),
            ("How is sequencing designed to support transfer?", "What comes before and after this module, and why?"),
        ]),
        ("Learning or Experience Design", [
            ("What cognitive operations must learners practise?", "List them specifically — not just 'understand' or 'apply'."),
            ("Where is retrieval embedded in the design?", "Name the specific mechanism and timing."),
            ("How is reasoning externalised?", "Where must learners produce visible thinking, not just correct answers?"),
        ]),
        ("Multimedia Design", [
            ("What cognitive function does each major media element serve?", "List the elements and their functions."),
            ("Where does media reduce extraneous load?", "Where might it add it?"),
            ("How does representation support schema formation?", "Which concepts require visual or spatial representation?"),
        ]),
        ("Learning Technology", [
            ("What platform affordances enable retrieval, feedback and collaboration?", ""),
            ("Where does platform structure constrain pedagogy?", "What can the platform not do that the design requires?"),
            ("What analytics or data would inform iteration on this design?", ""),
        ]),
    ]

    for role_name, prompts in roles:
        elems.append(KeepTogether([
            rule(thickness=0.5, color=RULE, space_before=2*mm, space_after=2*mm),
            Paragraph(f"If your role is: {role_name}", styles["sub_heading"]),
        ]))
        for q, hint in prompts:
            elems.append(Paragraph(q, styles["prompt_label"]))
            if hint:
                elems.append(Paragraph(hint, styles["body_note"]))
            elems.append(write_lines(2))
            elems.append(Spacer(1, 2 * mm))

    elems.append(rule(thickness=0.5, color=RULE, space_before=3*mm, space_after=3*mm))
    elems.append(Paragraph("Part B — Cross-role perspective taking", styles["sub_heading"]))
    elems.append(Paragraph(
        "Pair with someone from a different role. One person describes a recent design decision. "
        "The other identifies which learning science commitment it serves — or violates.",
        styles["body_note"]
    ))
    elems.append(Spacer(1, 2 * mm))

    for label, hint in [
        ("Your partner's role:", ""),
        ("Their design decision:", ""),
        ("Which learning science commitment does it serve — or violate?", ""),
        ("Their observation about your decision:", ""),
    ]:
        elems.append(Paragraph(label, styles["prompt_label"]))
        if hint:
            elems.append(Paragraph(hint, styles["body_note"]))
        lines = 1 if "role" in label.lower() else 2
        elems.append(write_lines(lines))
        elems.append(Spacer(1, 2 * mm))

    return elems


def build_phase4(styles):
    elems = []
    elems += phase_header("4", "Cross-Role Diagnosis", styles)

    elems.append(Paragraph("Your team's artefact", styles["sub_heading"]))
    for label in ["Module or assessment name:", "Role that created it:", "Programme context (if known):"]:
        elems.append(Paragraph(label, styles["prompt_label"]))
        elems.append(write_lines(1))
        elems.append(Spacer(1, 2 * mm))

    elems.append(rule(thickness=0.5, color=RULE, space_before=3*mm, space_after=3*mm))
    elems.append(Paragraph("Stage 1 — Identify", styles["sub_heading"]))
    elems.append(Paragraph(
        "Work through these questions as a team. Write your team's answers here.",
        styles["body_note"]
    ))
    elems.append(Spacer(1, 2 * mm))

    stage1 = [
        ("1. What must learners remember?", ""),
        ("2. Where is retrieval structured?", ""),
        ("3. Where is thinking visible?", ""),
        ("4. Where is cognitive load unnecessary?", ""),
    ]
    for q, hint in stage1:
        elems.append(Paragraph(q, styles["prompt_label"]))
        elems.append(write_lines(2))
        elems.append(Spacer(1, 2 * mm))

    elems.append(rule(thickness=0.5, color=RULE, space_before=3*mm, space_after=3*mm))
    elems.append(Paragraph("Stage 2 — Diagnose misalignment", styles["sub_heading"]))
    elems.append(Spacer(1, 2 * mm))

    elems.append(Paragraph(
        "5. Where do role decisions contradict each other? List at least two.",
        styles["prompt_label"]
    ))
    elems.append(Spacer(1, 1 * mm))
    elems.append(grid_table(
        ["Contradiction", "Roles involved"],
        3,
        col_widths=[BODY_W * 0.65, BODY_W * 0.35]
    ))
    elems.append(Spacer(1, 4 * mm))

    elems.append(Paragraph(
        "6. Which contradiction most impairs learning, and why?",
        styles["prompt_label"]
    ))
    elems.append(write_lines(3))
    elems.append(Spacer(1, 3 * mm))
    elems.append(Paragraph(
        "This is your redesign focus for Phase 5.",
        styles["body_note"]
    ))

    return elems


def build_phase5(styles):
    elems = []
    elems += phase_header("5", "Collaborative Redesign", styles)

    elems.append(Paragraph("Learning Experience Redesign Map", styles["sub_heading"]))
    elems.append(Paragraph(
        "Complete each section as a team. If you cannot complete the Learning Science Justification "
        "section, the redesign is not yet grounded in science — return to it before the gallery walk.",
        styles["body_note"]
    ))
    elems.append(Spacer(1, 3 * mm))

    sections = [
        ("1", "Capability Object", [
            ("What must learners be able to do 6 to 12 months after this experience, in real conditions?", "", 3),
            ("What cognitive change is required?", "What must change in their schemas, judgment or mental models?", 2),
        ]),
        ("2", "Retrieval Points", None),
        ("3", "Visible Reasoning", [
            ("What prompts or tasks require learners to externalise their thinking?",
             "Not just produce a correct answer — show their reasoning.", 3),
        ]),
        ("4", "Load Reduction", [
            ("What extraneous elements were removed or simplified?", "", 2),
            ("What decisions were made to protect working memory capacity?", "", 2),
        ]),
        ("5", "Media Justification", None),
        ("6", "Platform Alignment", [
            ("How does the technology enable the design?", "Name specific affordances.", 2),
            ("What does the platform need to do that it currently cannot?",
             "Flag this as a change to advocate for.", 2),
        ]),
        ("7", "Connection to Programme", [
            ("How does this module contribute to programme-level capability?", "", 2),
            ("What must come before this module for it to work? What comes after?", "", 2),
        ]),
    ]

    for num, title, prompts in sections:
        elems.append(rule(thickness=0.5, color=RULE, space_before=3*mm, space_after=2*mm))
        elems.append(Paragraph(f"{num}. {title}", styles["sub_heading"]))

        if num == "2":
            elems.append(Paragraph(
                "Where and when is this knowledge retrieved after initial learning?",
                styles["body_note"]
            ))
            elems.append(Spacer(1, 1 * mm))
            elems.append(grid_table(
                ["Retrieval point", "Timing", "Mechanism"],
                3,
                col_widths=[BODY_W * 0.40, BODY_W * 0.25, BODY_W * 0.35]
            ))
        elif num == "5":
            elems.append(Paragraph(
                "For each significant media element, state its cognitive function.",
                styles["body_note"]
            ))
            elems.append(Spacer(1, 1 * mm))
            elems.append(grid_table(
                ["Media element", "Cognitive function it serves"],
                3,
                col_widths=[BODY_W * 0.35, BODY_W * 0.65]
            ))
            elems.append(Spacer(1, 2 * mm))
            elems.append(Paragraph("Is there a medium you removed? Why?", styles["prompt_label"]))
            elems.append(write_lines(2))
        else:
            if prompts:
                for q, hint, lines in prompts:
                    elems.append(Paragraph(q, styles["prompt_label"]))
                    if hint:
                        elems.append(Paragraph(hint, styles["body_note"]))
                    elems.append(write_lines(lines))
                    elems.append(Spacer(1, 2 * mm))

        elems.append(Spacer(1, 1 * mm))

    # Learning science justification
    elems.append(rule(thickness=1, color=INK, space_before=4*mm, space_after=3*mm))
    elems.append(Paragraph("Learning Science Justification", styles["sub_heading"]))
    elems.append(Paragraph(
        "Complete this section before the gallery walk. If you cannot answer these questions, "
        "the redesign is not yet grounded in learning science.",
        styles["body_note"]
    ))
    elems.append(Spacer(1, 2 * mm))

    lsj = [
        ("What memory structures are strengthened by this redesign?", ""),
        ("Where is retrieval embedded, and at what intervals?", ""),
        ("What cognitive load decisions were made?", "Name what was added, what was removed, and why."),
    ]
    for q, hint in lsj:
        elems.append(Paragraph(q, styles["prompt_label"]))
        if hint:
            elems.append(Paragraph(hint, styles["body_note"]))
        elems.append(write_lines(2))
        elems.append(Spacer(1, 2 * mm))

    return elems


def build_phase6(styles):
    elems = []
    elems += phase_header("6", "Cross-Team Critique", styles)

    elems.append(Paragraph(
        "Review at least two redesigns. Leave three sticky notes on each: "
        "green (strength), yellow (tension), blue (question).",
        styles["body_note"]
    ))
    elems.append(Spacer(1, 3 * mm))

    for team_n in ["1", "2"]:
        elems.append(rule(thickness=0.5, color=RULE, space_before=2*mm, space_after=2*mm))
        elems.append(Paragraph(f"Team {team_n}", styles["sub_heading"]))
        for label, color_note in [
            ("Strength", "green — aligns with learning science"),
            ("Tension", "yellow — may impair learning"),
            ("Clarification question", "blue — needs more explanation"),
        ]:
            elems.append(Paragraph(f"{label} ({color_note}):", styles["prompt_label"]))
            elems.append(write_lines(2))
            elems.append(Spacer(1, 2 * mm))

    elems.append(rule(thickness=0.5, color=RULE, space_before=3*mm, space_after=3*mm))
    elems.append(Paragraph("Feedback I received", styles["sub_heading"]))
    elems.append(Paragraph(
        "After the gallery walk, read the sticky notes on your team's map and record the most useful responses.",
        styles["body_note"]
    ))
    elems.append(Spacer(1, 2 * mm))

    for label in ["Most useful strength:", "Most useful tension:", "Most important question to resolve:"]:
        elems.append(Paragraph(label, styles["prompt_label"]))
        elems.append(write_lines(2))
        elems.append(Spacer(1, 2 * mm))

    return elems


def build_phase7(styles):
    elems = []
    elems += phase_header("7", "Collaboration Charter", styles)

    elems.append(Paragraph("Individual commitments", styles["sub_heading"]))
    elems.append(Paragraph(
        "Write each commitment before sharing with the group.",
        styles["body_note"]
    ))
    elems.append(Spacer(1, 2 * mm))

    commitments = [
        ("One decision I will no longer make alone:", "", 2),
        ("One role I need earlier in the design process:", "", 1),
        ("Why earlier involvement by that role would improve the learning outcome:", "", 2),
        ("One learning science principle I will use in future design discussions:", "", 1),
        ("One process change we will implement in the next design cycle:", "", 2),
    ]
    for label, hint, lines in commitments:
        elems.append(Paragraph(label, styles["prompt_label"]))
        if hint:
            elems.append(Paragraph(hint, styles["body_note"]))
        elems.append(write_lines(lines))
        elems.append(Spacer(1, 2 * mm))

    elems.append(rule(thickness=0.5, color=RULE, space_before=3*mm, space_after=3*mm))
    elems.append(Paragraph("30-day follow-up plan", styles["sub_heading"]))
    elems.append(Spacer(1, 1 * mm))

    for label in ["Follow-up session date:", "Who will attend:"]:
        elems.append(Paragraph(label, styles["prompt_label"]))
        elems.append(write_lines(1))
        elems.append(Spacer(1, 2 * mm))

    elems.append(Paragraph("What I will bring:", styles["prompt_label"]))
    for item in [
        "One decision I made differently since the workshop",
        "One place where collaboration improved",
        "One remaining misalignment that needs addressing",
    ]:
        elems.append(Paragraph(f"— {item}", styles["small"]))
    elems.append(Spacer(1, 2 * mm))

    elems.append(Paragraph("Notes on what I want to track between now and then:", styles["prompt_label"]))
    elems.append(write_lines(3))

    elems.append(rule(thickness=1, color=INK, space_before=5*mm, space_after=3*mm))
    elems.append(Paragraph("Closing retrieval task", styles["sub_heading"]))
    elems.append(Paragraph(
        "Without notes, write three things.",
        styles["body_note"]
    ))
    elems.append(Spacer(1, 2 * mm))

    for label in [
        "How I now define learning:",
        "One way my role mediates cognitive change:",
        "One collaboration commitment I am taking forward:",
    ]:
        elems.append(Paragraph(label, styles["prompt_label"]))
        elems.append(write_lines(2))
        elems.append(Spacer(1, 2 * mm))

    return elems


def build_reference(styles):
    elems = []
    elems.append(PageBreak())

    elems.append(Paragraph("REFERENCE", styles["section_label"]))
    elems.append(Paragraph("The Three Learning Science Commitments", styles["phase_heading"]))
    elems.append(rule(thickness=1, color=INK, space_before=0, space_after=4*mm))
    elems.append(Paragraph(
        "Use these commitments as your arbitration language when making design decisions.",
        styles["body_note"]
    ))
    elems.append(Spacer(1, 3 * mm))

    commitments = [
        (
            "1. Memory precedes complex thinking",
            "Higher-order cognitive operations require accessible knowledge structures in long-term memory. "
            "You cannot analyse, evaluate or create with knowledge you cannot recall.",
            "Sequence instruction so foundational knowledge is encoded and retrievable before learners are "
            "asked to apply it in complex ways."
        ),
        (
            "2. Retrieval strengthens memory",
            "Actively recalling information from memory strengthens the neural pathways that make future "
            "recall easier. Re-reading or re-watching does not produce the same effect.",
            "Build retrieval opportunities into the design with specific timing, mechanisms and spacing. "
            "Retrieval is not a test event — it is an instructional strategy."
        ),
        (
            "3. Cognitive load must be managed",
            "Working memory is limited. Extraneous cognitive load (effort not contributing to schema "
            "formation) reduces the capacity available for learning. Complexity and novelty must be "
            "introduced deliberately, not simultaneously.",
            "Remove presentation elements that do not serve the learning objective. Manage the number of "
            "new concepts introduced at once. Use worked examples before asking learners to solve problems independently."
        ),
    ]

    for title, body, implication in commitments:
        elems.append(rule(thickness=0.5, color=RULE, space_before=2*mm, space_after=2*mm))
        elems.append(Paragraph(title, styles["reference_heading"]))
        elems.append(Paragraph(body, styles["body"]))
        elems.append(Paragraph("Design implication: " + implication, styles["body_note"]))
        elems.append(Spacer(1, 2 * mm))

    elems.append(rule(thickness=1, color=INK, space_before=5*mm, space_after=4*mm))
    elems.append(Paragraph("Role Contributions to the Activity System", styles["phase_heading"]))
    elems.append(Paragraph(
        "Each role mediates learning differently. This table summarises how each contributes to durable learner capability.",
        styles["body_note"]
    ))
    elems.append(Spacer(1, 2 * mm))

    role_data = [
        [
            Paragraph("Role", styles["table_header"]),
            Paragraph("Primary contribution", styles["table_header"]),
            Paragraph("Key learning science responsibility", styles["table_header"]),
        ],
        [
            Paragraph("Curriculum Design", styles["table_cell"]),
            Paragraph("Programme-level sequencing and outcome coherence", styles["table_cell"]),
            Paragraph("Ensuring foundational knowledge precedes complex application across the programme", styles["table_cell"]),
        ],
        [
            Paragraph("Learning or Experience Design", styles["table_cell"]),
            Paragraph("Instructional strategy and cognitive engagement", styles["table_cell"]),
            Paragraph("Structuring retrieval, visible reasoning and appropriate challenge", styles["table_cell"]),
        ],
        [
            Paragraph("Multimedia Design", styles["table_cell"]),
            Paragraph("Cognitive representation through media", styles["table_cell"]),
            Paragraph("Reducing extraneous load and supporting schema formation through appropriate representation", styles["table_cell"]),
        ],
        [
            Paragraph("Learning Technology", styles["table_cell"]),
            Paragraph("Platform affordances for retrieval, feedback and collaboration", styles["table_cell"]),
            Paragraph("Ensuring the platform enables rather than constrains pedagogical intent", styles["table_cell"]),
        ],
    ]

    col_w = [BODY_W * 0.22, BODY_W * 0.30, BODY_W * 0.48]
    t = Table(role_data, colWidths=col_w)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), INK),
        ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, FIELD_BG]),
        ("GRID",          (0, 0), (-1, -1), 0.4, RULE),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    elems.append(t)

    elems.append(Spacer(1, 10 * mm))
    elems.append(rule(thickness=0.5, color=RULE))
    elems.append(Spacer(1, 3 * mm))
    elems.append(Paragraph(
        "Bring this workbook to the 30-day follow-up session.",
        styles["small"]
    ))

    return elems


# ─── Main ─────────────────────────────────────────────────────────────────────

def build_pdf(output_path):
    styles = make_styles()

    doc = WorkbookTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
    )

    story = []
    story += build_cover(styles)
    story.append(PageBreak())
    story += build_phase1(styles)
    story.append(PageBreak())
    story += build_phase2(styles)
    story.append(PageBreak())
    story += build_phase3(styles)
    story.append(PageBreak())
    story += build_phase4(styles)
    story.append(PageBreak())
    story += build_phase5(styles)
    story.append(PageBreak())
    story += build_phase6(styles)
    story.append(PageBreak())
    story += build_phase7(styles)
    story += build_reference(styles)

    doc.build(story)
    print(f"PDF written to: {output_path}")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "learner-handout.pdf")
    build_pdf(out)
