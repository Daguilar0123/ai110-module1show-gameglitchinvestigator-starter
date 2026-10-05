# CLAUDE.md

## Setup
This project's `.venv` is `uv`-managed, pinned to Python 3.13 — the system
`python3` is 3.12. This isn't arbitrary: the standard `python3 -m venv .venv`
would silently build a 3.12 venv with no warning, so `uv` was adopted so
`.python-version` pins 3.13 inside the repo itself (DR10, 2026-09-22). A side
effect of that choice: a uv venv has no `pip` module. **Never run plain
`pip install`** here — it silently falls through to the global 3.12 `pip` and
"succeeds" while installing into the wrong interpreter entirely.

```bash
uv venv && uv pip install -r requirements.txt
```

**Failure signatures:**
- `ModuleNotFoundError` for a package you just "successfully" installed → bare
  `pip` was used; it installed into the global 3.12 environment instead.
- `python -m pip` → `No module named pip` → this is *expected and correct* in a
  uv venv — it's the loud failure the policy is designed to produce. Use
  `uv pip`; don't install `pip` into this venv to make the error go away.

Before any install: confirm `.venv` exists and `.venv/bin/python --version`
prints `3.13.x`.

## Commands
```bash
.venv/bin/python -m pytest -v             # run tests
.venv/bin/python -m streamlit run app.py  # run the app
```

## Architecture
- `app.py` — the Streamlit UI. Some game logic may still live here inline,
  duplicated with stubs in `logic_utils.py`, as part of an in-progress refactor
  exercise. This is deliberate scaffolding for a debugging assignment, not
  leftover cruft — don't "clean up" the duplication without checking context
  first.
- `logic_utils.py` — the refactor target: pure functions with no Streamlit
  dependency, unit-testable directly with pytest.
- `tests/test_game_logic.py` — imports from `logic_utils.py` only.

## Required deliverables
- `README.md` — project overview, demo walkthrough, and (if applicable) test output.
- `reflection.md` — bug reproduction logs and the AI-collaboration reflection.
- `tests/test_game_logic.py` — the automated tests.
- `ai_interactions.md` — **only required if a stretch challenge was attempted**
  (documents AI prompts, agent workflow, linting evidence, or a model
  comparison). Note: this repo is currently also using it as a general
  debugging/interaction log beyond that stated scope — see the note at the top
  of that file.
- `test_results.txt` (optional) — generated via `pytest > test_results.txt`.

## Workflow: parallel bugfixing with worktrees
When there are multiple independent-ish defects to fix at once, prefer one
Claude Code session per defect over fixing sequentially in one session or
letting multiple sessions share a working tree:
- Each session creates its own `git worktree` + branch as its first action —
  never share one working tree across sessions.
- Each session reads the real code before trusting any prescribed diagnosis, and
  sanity-checks it against what it actually finds rather than following it
  blindly — a prescribed plan is a starting point to save re-diagnosis time, not
  a script to execute unquestioned.
- Each session pauses for human review at major checkpoints (after moving/fixing
  logic, again after wiring up imports) before committing.
- Coordinate via a written plan file (read one if it exists before touching
  `app.py`/`logic_utils.py`), not live inter-session messaging — session-to-
  session visibility isn't reliable in this harness.

## Git commits
Never run `git commit` directly — always present the exact `git add`/`git
commit` commands for Danny to run himself, with a well-written message for
each. Group commits by shared topic rather than defaulting to one file per
commit: batch changes that tell the same story into a single commit, and split
unrelated changes into separate commits even within the same file.

## Gotchas
- `app.py`/`logic_utils.py` duplication may be intentional mid-refactor
  scaffolding, not a mistake — check for an active bugfix/refactor plan file
  before consolidating it yourself.
