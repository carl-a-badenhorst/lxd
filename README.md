# LXD Agent

Learning Experience Design AI driven by AGENT.md. The agent designs human-centered learning experiences across corporate L&D, higher education, product learning and leadership development.

Open this project in Cursor; the agent follows AGENT.md and applies the LXD identity, design philosophy and response format (including the required "Where next?" section) in every conversation.

## Project structure

| Path | Purpose |
|------|---------|
| `AGENT.md`, `NAMING.md` | Agent behaviour and naming conventions |
| `docs/` | Design rationale, learning objectives and other project docs |
| `cross-functional-learning-design-workshop/` | Workshop "Designing Learning as a Cross-Functional Activity System" |
| `…/workshop-outline.md` | Workshop agenda, objectives and phase detail |
| `…/facilitator/` | Facilitator guide, run-of-show, Miro/FigJam playbooks, visual-design-specs, build-miro-board script |
| `…/participant/` | Learner handout, redesign map template, pre-work primer, glossary, 30-day follow-up, build-handout script |
| `…/slides/` | Workshop slides (PDF/PPTX), build scripts, slide-image-prompts |
| `…/assets/images/` | Workshop images (e.g. slide art); generated assets are gitignored |
| `…/assets/media/` | Audio/video assets; generated assets are gitignored |

See NAMING.md for standard file names in each folder.

---

**Workshop slides (PowerPoint):** From the repo root, run `pip install -r cross-functional-learning-design-workshop/slides/requirements.txt` then `python cross-functional-learning-design-workshop/slides/build-pptx.py` to generate `workshop-slides.pptx`.

**Workshop Miro board:** From the repo root, run `pip install requests` then set `MIRO_ACCESS_TOKEN` and run `python cross-functional-learning-design-workshop/facilitator/build-miro-board.py` to create the workshop board via the Miro API. See `cross-functional-learning-design-workshop/facilitator/miro-playbook.md` (section “Building the board with the script”) for token setup and next steps.
