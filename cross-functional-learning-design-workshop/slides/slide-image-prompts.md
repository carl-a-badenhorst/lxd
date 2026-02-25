# Slide Image Prompts

Image recommendations and AI generation prompts for the workshop slide deck.

---

## How to use this document

The deck has seven image slots: cover (slide 1), five phase headers (slides 3, 9, 18, 22, 27) and the close (slide 36). For each slot this document gives a design rationale, placement note and two prompts — one photorealistic, one abstract or editorial.

Generate at 1920 x 1080 px minimum. The deck is monochrome; desaturate images on import if they compete with the type.

---

## Global style guidance

- **Tone:** Quiet, documentary, intelligent. No stock staging, no people smiling at camera, no generic teamwork.
- **Content:** Real work environments, physical materials (paper, notebooks, sticky notes), people in focused thought — never posed.
- **In every prompt:** 16:9 or 4:3 as noted; natural or diffused light; muted, slightly desaturated, cool-to-neutral colour; no legible text or logos; photorealistic unless using the abstract variant.

---

## Slide 1 — Cover

**Slot:** Left column, ~60% width. Right column is white type.

**Rationale:** Sets the register: rigour and focused collaboration, not energy or celebration.

**Placement:** Full-bleed left. Compositional weight toward the right edge (toward the type).

**Prompt A — photorealistic:**

A wide-angle shot of a large work table covered with printed documents, sticky notes and handwritten diagrams. Several people seated around it, leaning in, studying the materials. Hands visible — pointing, annotating, moving objects. No faces prominent. Dim natural light from a window to the left. Muted, slightly desaturated colour. Quiet, concentrated, collaborative. No laptops. No one looking at camera. 35mm lens. 16:9. No legible text in frame.

**Prompt B — abstract:**

Close overhead shot of a wooden work table. On the surface: printed A4 sheets with diagrams (no legible content), three colours of sticky notes in loose clusters, a pencil, a ruled notebook open to a blank page. Arrangement organised but clearly in use. Cool diffused natural light. Detailed. 16:9.

---

## Slide 3 — Phase 1: Framing the Shared Object

**Slot:** Right column, ~38% width, vertically centred.

**Rationale:** Phase 1 disrupts assumptions. Image = moment before clarity: ambiguity, divergence, initial thinking.

**Prompt A — photorealistic:**

Close-up of a person's hands writing in a blank notebook on a desk. Pen mid-stroke. Writing not legible — angle shows the act of writing, not the content. Small pool of warm desk-lamp light on the page. Rest of frame slightly out of focus. Quiet, intimate. 4:3. No text visible. Natural, unmanicured hands.

**Prompt B — abstract:**

Four different sticky-note clusters on a whiteboard, each a different muted colour (sage, terracotta, slate, cream), each with illegible handwritten text. Four distinct clusters — four perspectives not yet connected. Overhead. Cool diffused light. Minimal. 16:9.

---

## Slide 9 — Phase 2: Learning Science Core

**Slot:** Right column, ~38% width, vertically centred.

**Rationale:** Scientific grounding. Avoid literal brain imagery. Use a material metaphor: structures built, organised or strengthened.

**Prompt A — photorealistic:**

Macro of the internal cross-section of wood — annual rings as concentric arcs, grain in layered parallel lines. Rich, organised texture. Warm neutral tones. Shallow depth of field, centre sharp, edges soft. Natural wood tones. 4:3. No text.

**Prompt B — abstract:**

Close-up of a hand-drawn diagram on grid paper: three concentric circles, illegible labels, small arrows connecting them. Diagram looks mid-construction — a schema being built. Pencil at edge of paper. Overhead. Warm desk light. No legible text. 4:3.

---

## Slide 18 — Phase 3: Role Mapping

**Slot:** Right column, ~38% width, vertically centred.

**Rationale:** Role contributions made legible. Multiple perspectives converging on a shared object — not teamwork, but distinct contributors oriented to a common centre.

**Prompt A — photorealistic:**

Photo from directly above a round table. Four distinct working areas: each has a notebook, papers, pen, clearly different people not in frame. All four oriented toward a central shared printed diagram in the middle. Cool diffused light from above. Light wood or white table. No faces. No legible text. 4:3.

**Prompt B — abstract:**

Four clusters of objects on a flat white surface. Each cluster different: ruler and graph paper; colour swatches and stylus; keyboard and cable; notebook and printed sheet. Clusters point toward a common centre. Overhead. Desaturated, muted. 16:9.

---

## Slide 22 — Phase 4: Cross-Role Diagnosis

**Slot:** Right column, ~38% width, vertically centred.

**Rationale:** Analytical examination of real work. Scrutiny and close attention — not conflict. Looking carefully and finding what is wrong.

**Prompt A — photorealistic:**

Close-up of a person's hand with a red pen annotating a printed document. Document has text and a diagram (no legible content). Some words circled or underlined. Hand relaxed, analytical. Light desk. Slightly above, angled. Muted neutrals. Shallow depth of field. No face. No legible text. 4:3.

**Prompt B — abstract:**

Printed document flat on a table with three different-coloured sticky notes on different sections. Short illegible handwriting on each note. Some sections circled in pencil. Document clearly being examined. Cool overhead light. 4:3.

---

## Slide 27 — Phase 5: Collaborative Redesign

**Slot:** Right column, ~38% width, vertically centred.

**Rationale:** Generative phase — teams building something. Hands at work, materials in use. Productive and focused, not chaotic.

**Prompt A — photorealistic:**

Two or three pairs of hands working over a large printed template on a table. Blank sections being filled in with pen. Sticky notes being placed. One hand with pen, another pointing at a section. No faces — only arms and work surface. Warm, concentrated. Natural light. No legible text on template. 4:3.

**Prompt B — abstract:**

Overhead of a work surface in use: large white printed template with seven defined zones (labels illegible), each filled with sticky notes and handwritten annotations. Pencils, ruler, reference cards around it. Organised but in progress. Cool overhead light. 16:9.

---

## Slide 36 — Close

**Slot:** Left column, ~40% width. Right column is white type on dark.

**Rationale:** Moment after the workshop — forward movement, commitment, departure. Quieter and more personal than the cover.

**Prompt A — photorealistic:**

Wide-angle of a person at a window in an office or workspace, looking out. Holding a notebook. Still, slightly turned away from camera. Soft light through window, slightly overexposed. Background: whiteboard, table, chairs. Quiet, contemplative. Muted tones. 16:9. No face visible.

**Prompt B — abstract:**

Close-up of a completed notebook page with a numbered list of short handwritten commitments (illegible). Handwriting neat and deliberate. Pen resting diagonally on lower right. Warm desk lamp. Sense of something decided — a plan committed to. 4:3.

---

## Filenames and integration

Save generated images in `cross-functional-learning-design-workshop/assets/images/`:

| Slide | Filename |
|-------|----------|
| 1 — Cover | cover-workshop.jpg |
| 3 — Phase 1 | phase-1-framing.jpg |
| 9 — Phase 2 | phase-2-science.jpg |
| 18 — Phase 3 | phase-3-roles.jpg |
| 22 — Phase 4 | phase-4-diagnosis.jpg |
| 27 — Phase 5 | phase-5-redesign.jpg |
| 36 — Close | close-workshop.jpg |

To embed images in the deck, edit `build-slides.py`: replace each `image_slot()` call with `c.drawImage()` using the path to the image file. Regenerate with `python3 build-slides.py` from the `slides/` folder.

---

## Stock photography fallback

If not using AI generation, search for:

- **Cover:** workshop design table overhead hands documents
- **Phase 1:** writing notebook close-up pen hand
- **Phase 2:** wood grain macro texture OR pencil diagram grid paper
- **Phase 3:** overhead desk multiple work areas OR meeting table items
- **Phase 4:** annotating document pen close-up
- **Phase 5:** hands working template sticky notes
- **Close:** person window notebook office contemplative

Filter for natural light, no direct eye contact with camera, muted or desaturated palette.
