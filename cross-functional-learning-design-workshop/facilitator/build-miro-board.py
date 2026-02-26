#!/usr/bin/env python3
"""
Build the workshop Miro board from the miro-playbook.md specification.

Requires: MIRO_ACCESS_TOKEN in the environment (and optionally MIRO_TEAM_ID).
Install: pip install requests

Usage:
  export MIRO_ACCESS_TOKEN="your_token"
  python build-miro-board.py

Creates a new board with 9 zones (Landing + Phases 1–7 + Break), frames, prompts,
sticky note areas, and the Redesign Map template. After running, open the board
URL printed at the end; duplicate the Phase 5 Redesign Map template once per team
and add participant names to the Landing zone sticky notes.

See miro-playbook.md for facilitation and manual steps (timer, covering shapes,
lock/unlock, duplicate template per team).
"""

import os
import sys
import time

try:
    import requests
except ImportError:
    print("Install requests: pip install requests", file=sys.stderr)
    sys.exit(1)

# -----------------------------------------------------------------------------
# Config (edit before running if needed)
# -----------------------------------------------------------------------------
BOARD_NAME = "Designing Learning as a Cross-Functional Activity System — Workshop"
FRAME_WIDTH = 1600
FRAME_HEIGHT = 1400
FRAME_GAP = 200
# Sticky notes to pre-place for participants (facilitator renames in Miro)
NUM_PARTICIPANT_SLOTS = 16
# Teams for Phase 4/5 (each team gets a frame in Phase 4 and a Redesign Map in Phase 5)
NUM_TEAMS = 4
# Role colours per Miro API: light_yellow, yellow, orange, light_green, green, light_blue, blue, etc.
COLOR_CURRICULUM = "light_yellow"
COLOR_LEARNING_DESIGN = "light_blue"
COLOR_MULTIMEDIA = "light_green"
COLOR_LEARNING_TECH = "orange"
# Dark cover for reveals
FILL_DARK = "#111111"
FILL_LIGHT_ZONE = "#f5f5f5"

BASE = "https://api.miro.com/v2"

# -----------------------------------------------------------------------------
# API helpers
# -----------------------------------------------------------------------------
def get_token():
    t = os.environ.get("MIRO_ACCESS_TOKEN", "").strip()
    if not t:
        print("Set MIRO_ACCESS_TOKEN. See https://developers.miro.com/docs/getting-started", file=sys.stderr)
        sys.exit(1)
    return t


def headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def create_board(token):
    body = {"name": BOARD_NAME[:60], "description": "135-minute cross-functional learning design workshop. See facilitator miro-playbook."}
    team_id = os.environ.get("MIRO_TEAM_ID", "").strip()
    if team_id:
        body["teamId"] = team_id
    r = requests.post(f"{BASE}/boards", json=body, headers=headers(token), timeout=30)
    r.raise_for_status()
    data = r.json()
    return data["id"]


def create_frame(token, board_id, title, x, y, width=FRAME_WIDTH, height=FRAME_HEIGHT, fill_color=None):
    body = {
        "data": {"title": title[:6000], "format": "custom", "type": "freeform"},
        "position": {"x": x, "y": y},
        "geometry": {"width": width, "height": height},
    }
    if fill_color:
        body["style"] = {"fillColor": fill_color}
    r = requests.post(f"{BASE}/boards/{board_id}/frames", json=body, headers=headers(token), timeout=30)
    r.raise_for_status()
    return r.json()["id"]


def create_text(token, board_id, content, x, y, parent_id=None, width=400, font_size=14, color="#1a1a1a", fill_color=None):
    pos = {"x": x, "y": y}
    if parent_id:
        pos["relativeTo"] = "parent_top_left"
    body = {
        "data": {"content": content[:65000]},
        "position": pos,
        "geometry": {"width": width},
        "style": {"fontSize": str(font_size), "color": color},
    }
    if fill_color:
        body["style"]["fillColor"] = fill_color
        body["style"]["fillOpacity"] = "1.0"
    if parent_id:
        body["parent"] = {"id": str(parent_id)}
    r = requests.post(f"{BASE}/boards/{board_id}/texts", json=body, headers=headers(token), timeout=30)
    r.raise_for_status()
    return r.json()["id"]


def create_sticky(token, board_id, content, x, y, parent_id=None, fill_color="light_yellow", width=200):
    pos = {"x": x, "y": y}
    if parent_id:
        pos["relativeTo"] = "parent_top_left"
    body = {
        "data": {"content": content[:65000], "shape": "rectangle"},
        "position": pos,
        "geometry": {"width": width},
        "style": {"fillColor": fill_color},
    }
    if parent_id:
        body["parent"] = {"id": str(parent_id)}
    r = requests.post(f"{BASE}/boards/{board_id}/sticky_notes", json=body, headers=headers(token), timeout=30)
    r.raise_for_status()
    return r.json()["id"]


def create_shape(token, board_id, x, y, width, height, parent_id=None, fill_color="#ffffff", content=""):
    pos = {"x": x, "y": y}
    if parent_id:
        pos["relativeTo"] = "parent_top_left"
    body = {
        "data": {"shape": "rectangle", "content": content},
        "position": pos,
        "geometry": {"width": width, "height": height},
        "style": {"fillColor": fill_color},
    }
    if parent_id:
        body["parent"] = {"id": str(parent_id)}
    r = requests.post(f"{BASE}/boards/{board_id}/shapes", json=body, headers=headers(token), timeout=30)
    r.raise_for_status()
    return r.json()["id"]


def _rate_limit():
    time.sleep(0.15)


# -----------------------------------------------------------------------------
# Zone builders (position relative to frame top-left)
# -----------------------------------------------------------------------------
def build_landing(token, board_id, frame_id):
    create_text(token, board_id, "Designing Learning as a Cross-Functional Activity System", 80, 40, frame_id, width=800, font_size=24)
    create_text(token, board_id, "Facilitator: [Your name]\nDate: [Session date]", 80, 120, frame_id, width=400, font_size=12)
    create_text(token, board_id, "Zoom out to see the full board. We will move left to right through the phases. Start here and wait for the facilitator.", 80, 220, frame_id, width=700, font_size=12)
    create_text(token, board_id, "Find your name below (colour = your role). Click your note to confirm you can edit.", 80, 320, frame_id, width=600, font_size=12)
    # Participant name sticky notes (mix of role colours)
    colors = [COLOR_CURRICULUM, COLOR_LEARNING_DESIGN, COLOR_MULTIMEDIA, COLOR_LEARNING_TECH]
    for i in range(NUM_PARTICIPANT_SLOTS):
        row, col = divmod(i, 4)
        create_sticky(token, board_id, "Name", 100 + col * 220, 400 + row * 120, frame_id, fill_color=colors[i % 4], width=200)
        _rate_limit()


def build_phase1(token, board_id, frame_id):
    create_text(token, board_id, "Phase 1 — Framing the Shared Object", 80, 30, frame_id, width=600, font_size=18)
    create_text(token, board_id, "Define learning in one sentence.", 80, 80, frame_id, width=500, font_size=16)
    for i in range(min(8, NUM_PARTICIPANT_SLOTS)):
        row, col = divmod(i, 4)
        create_sticky(token, board_id, "", 80 + col * 220, 140 + row * 110, frame_id, fill_color="light_yellow", width=200)
        _rate_limit()
    create_text(token, board_id, "How do you know when learning has happened?", 80, 480, frame_id, width=500, font_size=16)
    for i in range(min(8, NUM_PARTICIPANT_SLOTS)):
        row, col = divmod(i, 4)
        create_sticky(token, board_id, "", 80 + col * 220, 540 + row * 110, frame_id, fill_color="light_yellow", width=200)
        _rate_limit()
    # Definition (covered — create dark shape on top; facilitator deletes to reveal)
    create_text(token, board_id, "Learning is durable change in knowledge structures that enables future participation and performance.", 80, 920, frame_id, width=500, font_size=14)
    create_shape(token, board_id, 70, 900, 520, 80, frame_id, fill_color=FILL_DARK)
    create_text(token, board_id, "Durable — Not fleeting. Visible months later.\nKnowledge structures — Organised schemas in long-term memory.\nEnables future — The test is what learners can do later.", 620, 900, frame_id, width=400, font_size=12)
    create_text(token, board_id, "1. What must learners be able to do 6–12 months from now, in real conditions?", 80, 1020, frame_id, width=700, font_size=12)
    create_text(token, board_id, "2. What cognitive change must occur for that to be possible?", 80, 1100, frame_id, width=700, font_size=12)
    for i in range(4):
        create_sticky(token, board_id, "", 80 + (i % 4) * 220, 1180, frame_id, fill_color="light_yellow", width=200)
        _rate_limit()


def build_phase2(token, board_id, frame_id):
    create_text(token, board_id, "Phase 2 — Learning Science Core", 80, 30, frame_id, width=600, font_size=18)
    create_shape(token, board_id, 0, 0, FRAME_WIDTH, 320, frame_id, fill_color=FILL_DARK)
    create_text(token, board_id, "Close your notes. Write the three commitments from memory.", 80, 100, frame_id, width=600, font_size=16, color="#ffffff")
    for i in range(min(8, NUM_PARTICIPANT_SLOTS)):
        row, col = divmod(i, 4)
        create_sticky(token, board_id, "", 80 + col * 220, 180 + row * 100, frame_id, fill_color="light_yellow", width=200)
        _rate_limit()
    # Three commitment cards (covered)
    for i, (title, body) in enumerate([
        ("Memory precedes complex thinking", "You cannot think critically about what you don't remember. Schema must be built before application."),
        ("Retrieval strengthens memory", "Actively recalling information strengthens retention. Retrieval practice must be embedded."),
        ("Cognitive load must be managed", "Working memory is limited. Simplify; remove elements that do not serve cognition."),
    ]):
        cx = 120 + i * 480
        create_shape(token, board_id, cx, 420, 400, 180, frame_id, fill_color="#ffffff")
        create_text(token, board_id, title, cx + 20, 440, frame_id, width=360, font_size=14)
        create_text(token, board_id, body, cx + 20, 500, frame_id, width=360, font_size=11)
        create_shape(token, board_id, cx, 418, 404, 184, frame_id, fill_color=FILL_DARK)
        _rate_limit()
    # Worked example
    create_text(token, board_id, "Module outcome: Evaluate ethical frameworks", 80, 680, frame_id, width=400, font_size=12)
    create_text(token, board_id, "Assessment: Multiple-choice quiz on definitions", 500, 680, frame_id, width=400, font_size=12)
    create_text(token, board_id, "What is the misalignment?", 80, 740, frame_id, width=400, font_size=12)
    for i in range(4):
        create_sticky(token, board_id, "", 80 + i * 220, 780, frame_id, fill_color="light_yellow", width=200)
        _rate_limit()
    create_text(token, board_id, "Diagnosis: Outcome demands evaluation (higher-order); assessment only tests recognition. Commitment violated: Memory precedes complex thinking.", 80, 920, frame_id, width=900, font_size=11)
    create_shape(token, board_id, 70, 900, 920, 60, frame_id, fill_color=FILL_DARK)
    # Role columns
    roles = [
        ("Curriculum Design", COLOR_CURRICULUM, "Alignment? Reinforcement over time? Sequencing for transfer?"),
        ("Learning / Experience Design", COLOR_LEARNING_DESIGN, "Cognitive operations? Retrieval? Visible reasoning?"),
        ("Multimedia Design", COLOR_MULTIMEDIA, "Cognitive function of media? Load? Schema support?"),
        ("Learning Technology", COLOR_LEARNING_TECH, "Affordances? Constraints? Analytics?"),
    ]
    for i, (name, color, prompts) in enumerate(roles):
        cx = 80 + i * 380
        create_text(token, board_id, name, cx, 1020, frame_id, width=340, font_size=12)
        create_text(token, board_id, prompts, cx, 1060, frame_id, width=340, font_size=10)
        for j in range(2):
            create_sticky(token, board_id, "", cx + j * 180, 1160, frame_id, fill_color=color, width=160)
            _rate_limit()


def build_phase3(token, board_id, frame_id):
    create_text(token, board_id, "Phase 3 — Role Mapping", 80, 30, frame_id, width=600, font_size=18)
    roles = [
        ("Curriculum Design", COLOR_CURRICULUM, "How does this module align with programme capability? Where is knowledge reinforced? Sequencing for transfer?"),
        ("Learning / Experience Design", COLOR_LEARNING_DESIGN, "What cognitive operations must learners practice? Where is retrieval? Visible reasoning?"),
        ("Multimedia Design", COLOR_MULTIMEDIA, "What cognitive function does each media element serve? Load? Schema support?"),
        ("Learning Technology", COLOR_LEARNING_TECH, "What affordances enable retrieval, feedback, collaboration? Where does platform constrain pedagogy? Analytics?"),
    ]
    for i, (name, color, prompts) in enumerate(roles):
        cx = 80 + i * 380
        create_text(token, board_id, name, cx, 80, frame_id, width=340, font_size=12)
        create_text(token, board_id, prompts, cx, 120, frame_id, width=340, font_size=10)
        for r in range(3):
            create_sticky(token, board_id, "", cx + (r % 2) * 180, 220 + r * 100, frame_id, fill_color=color, width=160)
            _rate_limit()
    create_text(token, board_id, "Cross-role pairing: Their decision → Which commitment does it serve or violate?", 80, 580, frame_id, width=800, font_size=12)
    create_text(token, board_id, "Decision", 80, 620, frame_id, width=200, font_size=10)
    create_text(token, board_id, "Commitment", 300, 620, frame_id, width=200, font_size=10)
    for i in range(6):
        create_sticky(token, board_id, "", 80 + (i % 2) * 220, 660 + (i // 2) * 100, frame_id, fill_color="light_yellow", width=200)
        _rate_limit()


def build_phase4(token, board_id, frame_id):
    create_text(token, board_id, "Phase 4 — Cross-Role Diagnosis", 80, 30, frame_id, width=600, font_size=18)
    for t in range(NUM_TEAMS):
        ty = 80 + t * 320
        create_text(token, board_id, f"Team {t + 1}", 80, ty, frame_id, width=200, font_size=14)
        create_text(token, board_id, "Your artefact: paste a screenshot or add a link below", 80, ty + 40, frame_id, width=500, font_size=10)
        create_sticky(token, board_id, "", 80, ty + 80, frame_id, fill_color="light_yellow", width=400)
        _rate_limit()
        create_text(token, board_id, "Stage 1 — What must learners remember? Where is retrieval? Where is thinking visible? Where is load unnecessary?", 80, ty + 200, frame_id, width=900, font_size=10)
        create_text(token, board_id, "Stage 2 — Where do role decisions contradict? Which contradiction most impairs learning? → This is your redesign focus for Phase 5.", 80, ty + 260, frame_id, width=900, font_size=10)
        create_sticky(token, board_id, "", 80, ty + 290, frame_id, fill_color="light_yellow", width=400)
        _rate_limit()
    # Fallback artefact
    create_text(token, board_id, "Sample artefact (use if your team has none): Programme: Apply risk frameworks. Module: 45-min video lecture. Assessment: Scenario reflection 2 weeks later. Media: Dense slides, no retrieval. Platform: LMS video + text.", 80, 80 + NUM_TEAMS * 320, frame_id, width=1000, font_size=10)


def build_break_zone(token, board_id, frame_id):
    create_shape(token, board_id, 0, 0, FRAME_WIDTH, 300, frame_id, fill_color=FILL_DARK)
    create_text(token, board_id, "Break — 10 minutes", 80, 100, frame_id, width=400, font_size=24, color="#ffffff")
    create_text(token, board_id, "When you return: identify the one misalignment most blocking learning. That is your redesign focus. One misalignment. Not all of them.", 80, 380, frame_id, width=800, font_size=12)


def build_phase5_template(token, board_id, frame_id, team_label=""):
    """Single Redesign Map template (duplicate in Miro once per team)."""
    create_text(token, board_id, f"Phase 5 — Collaborative Redesign {team_label}".strip(), 80, 30, frame_id, width=700, font_size=18)
    sections = [
        ("1. Capability Object", "What must learners do 6–12 months later? What cognitive change is required?"),
        ("2. Retrieval Points", "Where and when is knowledge retrieved after initial learning?"),
        ("3. Visible Reasoning", "What prompts require learners to externalise thinking?"),
        ("4. Load Reduction", "What extraneous elements were removed or simplified?"),
        ("5. Media Justification", "What cognitive function does each medium serve?"),
        ("6. Platform Alignment", "How does technology enable the design? What must the platform do that it currently cannot?"),
        ("7. Connection to Programme", "How does this module contribute to programme-level capability?"),
    ]
    y = 80
    for title, prompt in sections:
        create_text(token, board_id, title, 80, y, frame_id, width=500, font_size=12)
        create_text(token, board_id, prompt, 80, y + 28, frame_id, width=900, font_size=10)
        create_sticky(token, board_id, "", 80, y + 50, frame_id, fill_color="light_yellow", width=400)
        _rate_limit()
        y += 140
    create_text(token, board_id, "Learning Science Justification", 80, y, frame_id, width=400, font_size=12)
    create_text(token, board_id, "Memory structures strengthened:\nRetrieval embedded at:\nCognitive load decisions:", 80, y + 30, frame_id, width=700, font_size=10)
    create_sticky(token, board_id, "", 80, y + 90, frame_id, fill_color="light_yellow", width=500)
    _rate_limit()


def build_phase5(token, board_id, frame_id):
    # One template; facilitator duplicates per team (see playbook)
    build_phase5_template(token, board_id, frame_id, team_label="(Template — duplicate per team)")


def build_phase6(token, board_id, frame_id):
    create_text(token, board_id, "Phase 6 — Cross-Team Critique (Gallery Walk)", 80, 30, frame_id, width=700, font_size=18)
    create_text(token, board_id, "Review at least two other teams' Redesign Maps. For each map add:", 80, 80, frame_id, width=800, font_size=12)
    create_text(token, board_id, "Green — Strength: What aligns with learning science? Name the commitment.", 80, 120, frame_id, width=400, font_size=10)
    create_text(token, board_id, "Yellow — Tension: Where might the design impair learning? Name the commitment.", 500, 120, frame_id, width=400, font_size=10)
    create_text(token, board_id, "Blue — Clarification question: What needs more explanation?", 80, 160, frame_id, width=400, font_size=10)
    for i in range(12):
        row, col = divmod(i, 3)
        color = ["light_green", "light_yellow", "light_blue"][col]
        create_sticky(token, board_id, "", 80 + col * 220, 200 + row * 110, frame_id, fill_color=color, width=200)
        _rate_limit()


def build_phase7(token, board_id, frame_id):
    create_text(token, board_id, "Phase 7 — Collaboration Charter & Closing", 80, 30, frame_id, width=700, font_size=18)
    prompts = [
        "One decision I will no longer make alone",
        "One role I need earlier in the design process",
        "One learning science principle I will use in future discussions",
        "One process change we will implement in the next design cycle",
    ]
    for i, p in enumerate(prompts):
        create_text(token, board_id, p, 80, 80 + i * 100, frame_id, width=600, font_size=12)
        for j in range(4):
            create_sticky(token, board_id, "", 80 + j * 220, 120 + i * 100, frame_id, fill_color=[COLOR_CURRICULUM, COLOR_LEARNING_DESIGN, COLOR_MULTIMEDIA, COLOR_LEARNING_TECH][j % 4], width=200)
            _rate_limit()
    create_text(token, board_id, "30-day follow-up: One decision you made differently; one place collaboration improved; one remaining misalignment. Note date and calendar link below.", 80, 520, frame_id, width=800, font_size=10)
    create_text(token, board_id, "No notes. Write three things: (1) How you now define learning. (2) One way your role mediates cognitive change. (3) One collaboration commitment you are taking forward.", 80, 620, frame_id, width=800, font_size=12)
    create_shape(token, board_id, 0, 600, FRAME_WIDTH, 320, frame_id, fill_color=FILL_DARK)
    create_text(token, board_id, "No notes. Write three things.", 80, 680, frame_id, width=600, font_size=18, color="#ffffff")
    create_text(token, board_id, "1. How you now define learning\n2. One way your role mediates cognitive change\n3. One collaboration commitment you are taking forward", 80, 740, frame_id, width=700, font_size=12, color="#e0e0e0")
    for i in range(min(8, NUM_PARTICIPANT_SLOTS)):
        row, col = divmod(i, 4)
        create_sticky(token, board_id, "", 80 + col * 220, 860 + row * 100, frame_id, fill_color="light_yellow", width=200)
        _rate_limit()


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main():
    token = get_token()
    print("Creating board...")
    board_id = create_board(token)
    _rate_limit()
    # Frame centers left to right; origin board center (0,0)
    step = FRAME_WIDTH + FRAME_GAP
    start_x = -4 * step  # 9 frames: -4,-3,-2,-1,0,1,2,3,4
    zones = [
        ("Landing Zone", build_landing),
        ("Phase 1 — Framing the Shared Object", build_phase1),
        ("Phase 2 — Learning Science Core", build_phase2),
        ("Phase 3 — Role Mapping", build_phase3),
        ("Phase 4 — Cross-Role Diagnosis", build_phase4),
        ("Break", build_break_zone),
        ("Phase 5 — Collaborative Redesign", build_phase5),
        ("Phase 6 — Cross-Team Critique", build_phase6),
        ("Phase 7 — Collaboration Charter", build_phase7),
    ]
    frame_ids = []
    for i, (title, builder) in enumerate(zones):
        x = start_x + i * step
        fill = FILL_LIGHT_ZONE
        if "Break" in title:
            fill = FILL_DARK
        fid = create_frame(token, board_id, title, x, 0, fill_color=fill)
        frame_ids.append((title, fid))
        _rate_limit()
        builder(token, board_id, fid)
        print(f"  Built: {title}")

    # Board view URL (open in browser)
    view_url = f"https://miro.com/app/board/{board_id}/"
    print("")
    print("Board created successfully.")
    print("Open:", view_url)
    print("")
    print("Next steps (see miro-playbook.md):")
    print("  1. Duplicate the Phase 5 Redesign Map template once per team and label each copy.")
    print("  2. Add participant names to Landing zone sticky notes (or leave placeholders).")
    print("  3. Add Timer widget in Phase 2 (Insert > Apps > Timer).")
    print("  4. Lock zone headers, prompts, and cover shapes; unlock cover shapes when revealing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
