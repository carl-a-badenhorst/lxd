# Miro Playbook
## Designing Learning as a Cross-Functional Activity System

---

## What this document covers

This playbook tells you how to design, set up and run the workshop Miro board. It covers board architecture (how to structure the space), phase-by-phase facilitation moves (what to do and say inside Miro), Miro feature guidance (which tools to use and when), and contingency responses for common technical problems.

Read this alongside the facilitator guide, which covers facilitation approach and scripted transitions. This playbook focuses on the digital environment, not the pedagogical content.

---

## When to use a Miro board

Use Miro as the primary collaboration surface when:

- The workshop is delivered fully remotely (participants are not in the same room)
- The workshop is hybrid (some participants in-room, some remote)
- The workshop is in-room and you want a persistent digital artefact that participants can access after the session

Do not use Miro as a replacement for the printed workbook when delivering in-room to a group that has limited digital fluency or unreliable device access. In that case, run the workshop with printed handouts and use a physical whiteboard for shared surfaces.

---

## Board architecture overview

The Miro board is divided into eight zones, one per phase plus a landing zone. Each zone is a clearly labelled section of the infinite canvas, arranged left to right in session order. Participants can see the full board and navigate freely, but the facilitator controls which zone is active using the Presentation mode or by directing attention with a named cursor.

```
[Landing] → [Phase 1] → [Phase 2] → [Phase 3] → [Phase 4] → [Break] → [Phase 5] → [Phase 6] → [Phase 7]
```

Each zone contains:
- A header frame with the phase number and title
- All activity surfaces for that phase (sticky note areas, templates, tables)
- Facilitation instructions visible only in the facilitator view (use a locked, low-opacity text note)

Total estimated board width: approximately 12,000 to 15,000 px at standard zoom.

---

## Setting up the board

### Timing

- **T minus 2 days:** Create the board and complete all zone setup.
- **T minus 1 day:** Duplicate the Redesign Map template once per team. Label each copy with the team name.
- **T minus 30 minutes:** Test the board with a co-facilitator or alone. Run through every zone and confirm all frames, sticky note areas and templates are correctly placed and accessible.
- **T minus 10 minutes:** Share the board link with participants. Do not share earlier — participants who enter the board before the workshop may displace items or read ahead.

### Access and permissions

Set board permissions to **Can edit** for all participants. Do not restrict to view-only: participants need to add sticky notes, write on the template and move items during activities.

If your organisation uses Miro's guest access, confirm participants can edit without a Miro account. Guest access works for sticky notes and basic shapes but may restrict some features (e.g. voting). Test this before the session.

Create a named **Facilitator** cursor so participants can track your position on the board. Go to your profile icon during the session and set your cursor name to "Facilitator."

### Frame settings

Create each zone as a **Miro Frame** (Insert > Frame, or press F). Frames lock the zone dimensions and allow you to navigate between zones instantly using the frame navigator in the left panel.

Label each frame clearly:
- Landing Zone
- Phase 1 — Framing the Shared Object
- Phase 2 — Learning Science Core
- Phase 3 — Role Mapping
- Phase 4 — Cross-Role Diagnosis
- Break
- Phase 5 — Collaborative Redesign
- Phase 6 — Cross-Team Critique
- Phase 7 — Collaboration Charter

Use a consistent background for each zone: light grey (#F5F5F5) for active work phases, dark (#111111) for the high-focus moments (Phase 2 recall task, closing retrieval task). This reinforces the visual rhythm of the session.

### Building the board with the script

A Python script in this folder builds the full board via the Miro REST API so you do not have to create frames and content by hand.

**Requirements:** Python 3, `requests` (`pip install requests`), and a Miro API access token.

**Getting a token:**
1. Go to [Miro Developer](https://developers.miro.com), sign in, and create an app (or use an existing one).
2. In the app settings, add the scope `boards:write` and copy a **Personal access token** (or use OAuth if you need team boards).
3. Set `MIRO_ACCESS_TOKEN` in your environment. Optionally set `MIRO_TEAM_ID` if you want the new board created in a specific team.

**Run the script:** From the `facilitator/` folder run:
```bash
export MIRO_ACCESS_TOKEN="your_token"
python build-miro-board.py
```
The script creates a new board, nine frames (Landing + Phases 1–7 + Break), and all zone content (prompts, sticky note areas, commitment cards, Redesign Map template, fallback artefact text, etc.). It prints the board URL when done.

**After the script:** Open the board and (1) duplicate the Phase 5 Redesign Map template once per team and label each copy, (2) add participant names to the Landing zone sticky notes or leave placeholders, (3) add the Timer widget in Phase 2 (Insert > Apps > Timer), (4) lock zone headers, prompts, and any cover shapes you will reveal during the session. The playbook’s zone-by-zone and pre-session checklist still apply.

---

## Zone-by-zone setup guide

---

### Landing Zone

**Purpose:** Orient participants when they first enter the board.

**Contents:**
- Workshop title: "Designing Learning as a Cross-Functional Activity System"
- Your name and the session date
- One line of instruction: "Zoom out to see the full board. We will move left to right through the phases. Start here and wait for the facilitator."
- A name label area: a sticky note with each participant's name already placed, colour-coded by role (see below). Ask participants to find their name as soon as they enter.

**Colour coding by role** (used throughout the board):
- Curriculum Design: yellow
- Learning or Experience Design: blue
- Multimedia Design: green
- Learning Technology: orange

Use this colour coding for all sticky notes added by role throughout the session. Brief participants on this before the workshop begins.

---

### Phase 1 Zone — Framing the Shared Object

**Contents:**

1. **Writing area 1A:** A large text box prompt — "Define learning in one sentence." Below it, a sticky note area with one sticky note per participant, pre-placed with each person's name in small text at the bottom. Participants type into their own sticky note.

2. **Writing area 1B:** Same structure — "How do you know when learning has happened?"

3. **Operational definition reveal:** A text box containing the definition, initially covered by a rectangle shape filled in dark (#111111) to obscure it. You remove the covering shape when you reveal the definition to the group.

   > Learning is durable change in knowledge structures that enables future participation and performance.

4. **Three key words:** Three text boxes arranged side by side: "Durable", "Knowledge structures", "Enables future." Each has a short description below it. Reveal these after you uncover the definition.

5. **Writing area 1C:** Two numbered prompts with sticky note areas:
   - "What must learners be able to do 6 to 12 months from now, in real conditions?"
   - "What cognitive change must occur for that to be possible?"

**Facilitator tip:** When asking participants to write 1A and 1B, move your cursor away from their sticky note area. Participants write more freely when they cannot see the facilitator watching their response.

---

### Phase 2 Zone — Learning Science Core

**Contents:**

1. **Recall task area:** Dark background (#111111). Large white text: "Close your notes. Write the three commitments from memory." A sticky note area with one note per participant, pre-named. No hints on screen.

2. **Commitments reveal:** Three side-by-side cards, covered until the reveal:
   - Card 1: "Memory precedes complex thinking" + body text + design implication
   - Card 2: "Retrieval strengthens memory" + body text + design implication
   - Card 3: "Cognitive load must be managed" + body text + design implication

   Cover each card with a dark rectangle. Uncover them one at a time as you reveal.

3. **Role-based application area:** Four columns, one per role, each with the role name as a header and its three prompts below. Sticky note area under each column.
   - Curriculum Design column: alignment, knowledge reinforcement over time, sequencing for transfer
   - Learning / Experience Design column: cognitive operations, retrieval, visible reasoning
   - Multimedia Design column: cognitive function, load, schema support
   - Learning Technology column: affordances, constraints, analytics

4. **Worked example area:** Two boxes side by side:
   - "Module outcome: Evaluate ethical frameworks"
   - "Assessment: Multiple-choice quiz on definitions"
   Below these: a sticky note area labelled "What is the misalignment?" — participants add their answer before you reveal the diagnosis.

5. **Diagnosis reveal:** A text card with the four-row diagnosis (outcome demands, assessment tests, gap, commitment violated), covered until you present it.

**Facilitator tip:** During the recall task, use a timer widget (Insert > Apps > Timer) set to 2 minutes and start it visibly. The visible timer externalises the constraint and removes the need to say "you have two minutes" repeatedly.

---

### Phase 3 Zone — Role Mapping

**Contents:**

1. **Role clarification area:** Four colour-coded columns, one per role. Each column contains the three prompts for that role. Sticky notes in the column's role colour.

   Use Miro's sticky note colour lock for this section: pre-place empty sticky notes in each column with the correct role colour so participants do not need to change colour manually.

2. **Cross-role pairing area:** A pairing grid. Rows are one role, columns are another. Use a simple table shape or a grid of boxes. Each pairing box contains two sticky note areas: one for "Their decision" and one for "Which commitment does it serve or violate?"

   Alternatively, if the group is large, use a simpler structure: two sticky note areas per pair labelled "Decision" and "Commitment."

**Facilitator tip:** Announce pairings verbally. In Miro, call out each pair by name ("Ali from Curriculum Design, pair with Sam from Learning Technology"). This is faster than building pairing logic into the board.

---

### Phase 4 Zone — Cross-Role Diagnosis

**Contents:**

1. **Team artefact drop zone:** One frame per team, labelled with the team name and colour-coded border. Each frame contains:
   - A sticky note area labelled "Your artefact: paste a screenshot or add a link below"
   - The Stage 1 and Stage 2 questions listed below the artefact area

2. **Stage 1 — Identify:** Four numbered question labels with a sticky note area below each:
   - What must learners remember?
   - Where is retrieval structured?
   - Where is thinking visible?
   - Where is cognitive load unnecessary?

3. **Stage 2 — Diagnose misalignment:** Two question labels with sticky note areas:
   - Where do role decisions contradict each other?
   - Which contradiction most impairs learning?

   Below the second question, a callout box: "This is your redesign focus for Phase 5."

**Facilitator tip:** Walk between team frames using the frame navigator on the left panel. When you visit a team's frame, use your named cursor to point to specific sticky notes and prompt them if they are being too general. Say: "Point to something specific in your artefact. What exact element?"

**Fallback artefact:** If a team arrives without a real artefact, a pre-built sample is in this zone, below the team frames. It contains:
- Programme outcome: "Apply risk frameworks to operational decisions"
- Module: 45-minute video lecture with narrated slides
- Assessment: Scenario-based reflection submitted 2 weeks later
- Media: Dense slide decks, no worked examples, no retrieval points
- Platform: LMS with video playback and text submission only

---

### Break Zone

**Contents:**

- A simple dark card: "Break — 10 minutes"
- Below it: "When you return: identify the one misalignment most blocking learning. That is your redesign focus. One misalignment. Not all of them."

**Facilitator tip:** During the break, navigate to each team's Phase 4 frame and read their Stage 2 sticky notes. Identify which teams have a clear diagnosis and which need prompting when they return. Prepare a brief verbal prompt for each team that is still too general.

---

### Phase 5 Zone — Collaborative Redesign

**Contents:**

1. **Redesign Map template:** One frame per team, each containing a copy of the Redesign Map template. Pre-duplicate this template for each team before the session (see setup timing above).

The template has seven labelled sections, each with a sticky note area and a prompt question:

| Section | Prompt |
|---------|--------|
| 1. Capability Object | What must learners do 6–12 months later? What cognitive change is required? |
| 2. Retrieval Points | Where and when is knowledge retrieved after initial learning? |
| 3. Visible Reasoning | What prompts require learners to externalise thinking? |
| 4. Load Reduction | What extraneous elements were removed or simplified? |
| 5. Media Justification | What cognitive function does each medium serve? |
| 6. Platform Alignment | How does technology enable the design? What does the platform need to do that it currently cannot? |
| 7. Connection to Programme | How does this module contribute to programme-level capability? |

Below all seven sections: a bordered box labelled **Learning Science Justification** with three prompt lines:
- Memory structures strengthened:
- Retrieval embedded at:
- Cognitive load decisions:

**Facilitator tip:** During Phase 5, use Miro's Follow mode (click a participant's avatar > Follow) to watch what a specific team is doing without interrupting them. Use this to monitor whether teams are completing the Learning Science Justification section. If they skip it, navigate to their frame and drop a sticky note saying "Complete this section before the gallery walk."

---

### Phase 6 Zone — Cross-Team Critique (Gallery Walk)

**Contents:**

1. **Gallery display area:** All team Redesign Maps are visible here. You can link to the Phase 5 frames or duplicate the completed maps into this zone for ease of navigation.

2. **Feedback sticky note areas:** Adjacent to each team's map, three labelled columns:
   - Green column: "Strength — What aligns with learning science? Name the commitment."
   - Yellow column: "Tension — Where might the design impair learning? Name the commitment."
   - Blue column: "Clarification question — What needs more explanation?"

   Pre-place empty sticky notes in each column in the correct colour. Participants drag a note, type their feedback and drop it in the column.

**Facilitator tip:** Use Miro's **Voting** feature to add a layer of prioritisation after the gallery walk (optional). Once all feedback notes are placed, open a voting session and ask each participant to vote on the one tension they think is most critical across all maps. Results surface common system-level issues worth raising in Phase 7.

**Facilitator tip:** If participants are writing vague feedback ("this is good" or "this seems unclear"), move your cursor to their note and type a prompt note next to it: "Which commitment does this connect to?" They will see your cursor and respond.

---

### Phase 7 Zone — Collaboration Charter

**Contents:**

1. **Individual commitments area:** Four prompt lines, each with a sticky note area:
   - One decision I will no longer make alone
   - One role I need earlier in the design process
   - One learning science principle I will use in future discussions
   - One process change we will implement in the next design cycle

   Each participant adds their own sticky note in their role colour.

2. **30-day follow-up card:** A static card with the three share-out prompts for the follow-up session:
   - One decision you made differently since the workshop
   - One place where collaboration improved
   - One remaining misalignment that needs addressing

   Below: space for participants to note the date and a link to the follow-up calendar invitation.

3. **Closing retrieval task area:** Dark background. Large text: "No notes. Write three things."
   - How you now define learning
   - One way your role mediates cognitive change
   - One collaboration commitment you are taking forward

   A sticky note area below for participants to type their responses.

**Facilitator tip:** After the closing retrieval task, leave this zone visible on screen for 60 seconds of silence before saying anything. The silence is part of the task.

---

## Miro feature reference

This section lists the features you will use most, with brief notes on when and how to use each.

### Frames

Use frames to define each zone and to navigate between them during the session. In the left panel, click a frame name to jump to it instantly. During Presentation mode, pressing the right arrow moves to the next frame.

Use frames to lock zone boundaries. If participants accidentally drag items out of a zone, the frame border makes it visually clear that something is out of place.

### Sticky notes

Use sticky notes (N on keyboard) for all participant writing. Set the default colour before each activity using the colour selector in the sticky note toolbar. During role-based activities, lock the note colour to the role colour.

Keep sticky notes short: one idea per note. If a participant writes a long paragraph, that is a signal to prompt them to split their thinking into two or three separate notes.

### Timer

Insert a timer (Insert > Apps > Timer) and place it in the top-right corner of each active zone. Start the timer when you give the instruction and let it run visibly. The timer reduces the number of verbal time checks you need to make.

Set the timer duration exactly as specified in the run of show. Do not round up — a 2-minute recall task must stay at 2 minutes for retrieval practice to function correctly.

### Cursor names

Name your cursor "Facilitator" at the start of the session. This allows you to point at elements on the board without using verbal directions like "look at the top left." Move your cursor deliberately to the element you want participants to focus on, then speak.

Ask participants to add their first name to their cursor. This makes it possible to identify who is editing what in real time, which is important during Phase 4 when teams work simultaneously.

### Presentation mode

Use Presentation mode (the play button in the bottom toolbar) when you want to direct all participants to the same frame simultaneously. In Presentation mode, all participants' views follow yours. Exit Presentation mode when you want participants to work independently or in teams.

Use Presentation mode for:
- Phase 1 definition reveal
- Phase 2 commitment reveal
- Phase 2 worked example reveal
- Phase 4 transition statement
- Phase 5 introduction of the redesign map
- Phase 7 closing retrieval task

Exit Presentation mode for all independent or team work activities.

### Follow mode

Use Follow mode (click a participant's avatar in the top right > Follow) to shadow a single participant's view without controlling it. Use this during Phase 4 and Phase 5 to monitor team work without interrupting.

### Voting

Use the Voting feature (right panel > Dot voting) optionally at the end of Phase 6 to surface the most critical tensions across all redesign maps. Set up: 3 votes per person, no self-voting. Run for 2 minutes. Results are visible immediately.

### Locking

Lock any element that should not be moved by participants (Lock in the right-click menu). Lock:
- All zone headers and labels
- All prompt text boxes
- The covering rectangles you will reveal during the session (unlock these yourself when it is time to reveal)
- The fallback sample artefact in Phase 4

Do not lock participant sticky note areas.

### Screen share fallback

If Miro becomes inaccessible mid-session, switch to the slides deck (workshop-slides.pdf or .pptx) and share your screen. The slides carry all activity prompts. Instruct participants to use a shared document (Google Docs, Microsoft Word) for collaborative writing until Miro is restored. Do not end the session for a Miro outage.

---

## Pre-session checklist

- [ ] Board created and all zones set up
- [ ] All frames labelled and navigable via the frame panel
- [ ] Covering rectangles placed over all reveal elements
- [ ] Redesign Map template duplicated once per team and labelled
- [ ] Sticky notes pre-placed in correct colours for role-based activities
- [ ] Timer widget placed in each active zone
- [ ] Cursor name set to "Facilitator"
- [ ] Fallback sample artefact placed in Phase 4 zone and locked
- [ ] Board link shared with participants (T minus 10 min, not before)
- [ ] Board tested with a second device to confirm participant view matches facilitator view
- [ ] Screen share backup (slides deck) open and ready in a second window

---

## During-session quick reference

| Phase | Active Miro action | Feature |
|-------|--------------------|---------|
| Landing | Direct participants to name sticky notes | Sticky notes, named cursors |
| Phase 1 | Sticky note responses; reveal definition by deleting cover shape | Sticky notes, shape delete |
| Phase 2 | Timer for recall; uncover commitment cards one by one | Timer, shape delete |
| Phase 3 | Colour-coded sticky notes per role column | Sticky notes, colour lock |
| Phase 4 | Navigate team frames; point with cursor | Frame navigator, named cursor |
| Break | Read team diagnoses; prep prompts | Frame navigator |
| Phase 5 | Monitor with Follow mode; drop prompt notes if needed | Follow mode, sticky notes |
| Phase 6 | Gallery walk with colour-coded feedback; optional voting | Sticky notes, Voting |
| Phase 7 | Dark zone for retrieval task; 60 seconds silence | Presentation mode |

---

## After the session

### Saving the board

The Miro board is the persistent record of the session. After the workshop:

1. Export each team's Redesign Map as a PDF (right-click the frame > Export as PDF). Share with participants by email within 24 hours.
2. Take a full board screenshot (Export > Export image) for your records.
3. Lock the entire board to prevent post-session edits. Leave it accessible for participants to view.

### Sharing for the 30-day follow-up

Include the Miro board link in the post-session summary email. Ask participants to bring their Phase 7 commitment sticky note to the 30-day follow-up. They can screenshot it or return to the board to review it.

In the 30-day follow-up session, re-open the board and navigate to each team's Phase 4 and Phase 5 frames. Use these as reference points when participants share what has changed.

---

## Troubleshooting

| Problem | Response |
|---------|----------|
| Participant cannot access the board | Check access settings (edit vs view); resend the link; confirm they are using a supported browser (Chrome or Edge recommended) |
| Participant accidentally deletes a zone element | Use Ctrl+Z (undo) immediately; if caught too late, use the board activity log (right panel) to identify and restore the deleted item |
| Two participants editing the same sticky note | Ask one to create a new note; do not attempt to share a single note |
| Board is slow or lagging | Ask participants to reduce open browser tabs; zoom out to reduce the number of rendered elements on screen |
| Miro is inaccessible | Switch to screen-shared slides; use a shared document for participant writing; do not end the session |
| Participant is on mobile | Mobile access is limited in Miro; ask them to switch to a desktop or laptop; if unavailable, ask a co-facilitator to enter their contributions on their behalf |
| Team has no artefact to diagnose | Navigate to the fallback artefact in Phase 4 zone and share the link with the team |

---

## Design decisions and rationale

### Why Miro over FigJam

The workshop outline references FigJam as the default digital collaboration tool. Miro is a valid alternative for teams that already use it. The board architecture, template structure and facilitation moves in this playbook apply to either platform; feature names differ but the functions are equivalent.

If your organisation uses FigJam, apply this playbook's architecture and facilitation guidance directly and map the Miro features to their FigJam equivalents:
- Miro Frames = FigJam Sections
- Miro sticky notes = FigJam sticky notes
- Miro Presentation mode = FigJam Spotlight
- Miro Follow mode = FigJam Cursor Chat + manual navigation
- Miro Timer = FigJam Timer widget

### Why left-to-right board layout

The left-to-right sequence mirrors the cognitive progression of the workshop: from individual to collective, from diagnosis to redesign, from divergence to commitment. Participants who zoom out mid-session see the full arc of the work. This reinforces the sense that the session is going somewhere, not circling.

### Why colour-coded roles

Colour-coded sticky notes make role distribution visible at a glance during collaborative activities. When a team's Phase 4 sticky notes are all one colour, it is immediately clear that one role is dominating the diagnosis. The facilitator can intervene without having to ask who contributed what.

### Why covering rectangles for reveals

Revealing content progressively prevents participants from reading ahead and forming premature conclusions. The covering rectangle technique is low-friction: it requires no additional Miro features and works even with guest access. Remove the rectangle at the exact moment you want participants to see the content — not before.
