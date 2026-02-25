# Naming Conventions

This file defines naming conventions for this project. The agent and contributors must follow it when creating or renaming files, folders, branches, commits, tags, and assets.

---

## 1. General format

- Use **lowercase** for file and folder names. Exception: root-level identity files that are conventionally uppercase (e.g. `README.md`, `AGENT.md`) may keep that form.
- Use a **hyphen** (`-`) to separate words. Examples: `workshop-outline.md`, `learning-objectives.pdf`, `facilitator-guide.md`.
- Do **not** use spaces or underscores for word separation in file or folder names. For branch names, use the format in **Branch naming** (slash and hyphens, no underscores).
- Apply this rule everywhere unless a section below overrides it (e.g. semantic version numbers, git tags).

---

## 2. Standard file names by folder

Use these standard names so the agent and contributors know what to create or expect in each place. All names use lowercase and hyphens unless listed otherwise.

| Folder | Standard file names |
|--------|---------------------|
| Repo root | `README.md`, `AGENT.md`, `NAMING.md`, `LICENSE` (if used) |
| Workshop or learning-design folder (e.g. `workshop-name/`) | `workshop-outline.md` at root; see workshop subfolders below |
| Workshop subfolder `facilitator/` | `facilitator-guide.md`, `run-of-show.md` |
| Workshop subfolder `participant/` | `learner-handout.md`, `learner-handout.pdf`, `build-handout.py` |
| Workshop subfolder `slides/` | `workshop-slides.pdf`, `build-slides.py` |
| `docs/` | `design-rationale.md`, `learning-objectives.md`, and other doc types as needed (lowercase, hyphenated) |
| Assets | See **Asset naming** below. Main subfolders: `assets/images/`, `assets/media/` |

Add new standard names to this table as the project grows. Keep the same format: lowercase, hyphens.

---

## 3. Semantic versioning

- Follow [Semantic Versioning 2.0.0](https://semver.org/): **MAJOR.MINOR.PATCH**.
- **Format:** `X.Y.Z` (e.g. `1.0.0`, `2.1.3`). Do not include a "v" prefix in the version number itself; the "v" is for git tags (see below).
- **When to bump:**
  - **MAJOR:** incompatible changes (e.g. breaking changes to structure or behaviour).
  - **MINOR:** backward-compatible new capability (e.g. new workshop, new section).
  - **PATCH:** backward-compatible fixes (e.g. typos, clarifications, small corrections).

---

## 4. Git tags

- Use a **"v" prefix** for version tags: `vMAJOR.MINOR.PATCH`.
- **Examples:** `v1.0.0`, `v2.1.3`.
- Tag at releases or milestones. Do not move or overwrite tags after they have been used for a release.

---

## 5. Branch naming

- **Format:** `type/short-description`. Use lowercase. Use a **slash** between type and description. Use **hyphens** between words in the description.
- **Types:** `feature/`, `fix/`, `docs/`, `chore/`. Use others only if agreed (e.g. `refactor/`).
- **Examples:**
  - `feature/workshop-prework-video`
  - `fix/outline-typos`
  - `docs/naming-reference`
  - `chore/update-deps`
- Keep the short description concise. No spaces.

---

## 6. Commit messages

- **Format:** One short imperative summary line (50 characters or fewer when practical). Optional body after a blank line for detail.
- **Style:**
  - Imperative mood: "Add" not "Added", "Fix" not "Fixed".
  - Lowercase after the first word in the summary line (or use sentence case consistently).
  - No period at the end of the summary line.
- **Example:** `Add naming convention reference for the agent`
- **Optional (Conventional Commits):** Use a type prefix for consistency: `type(scope): message`. Common types: `feat`, `fix`, `docs`, `chore`. Example: `docs: add NAMING.md and naming-conventions rule`.

---

## 7. Asset naming

- **General:** Lowercase. Hyphens between words. No spaces. Include the correct file extension.
- **Images:** `section-or-topic-descriptor.extension` (e.g. `stage2-commitments-slide.png`, `workshop-hero.jpg`).
- **Media (audio/video):** Same rule (e.g. `intro-learning-commitments.mp4`, `feedback-example.wav`).
- Place images under `assets/images/` and other media under `assets/media/` unless the project defines a different structure. Add standard names to the **Standard file names by folder** table if needed.
