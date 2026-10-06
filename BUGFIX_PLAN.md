# Bugfix Plan — Game Glitch Investigator

## Total bug count

**8** `# FIXME: Logic breaks here` comments in `app.py`, mapping to **4 distinct
bugs** — two locations each, causally coupled (fixing one location without the
other leaves the bug half-fixed). Each bug gets ONE worktree/session, not one per
FIXME comment. **→ Open 4 terminals.** Testing is a separate 5th session, run only
after all 4 merge — not counted in the 4.

## Prerequisite — commit before creating any worktree (DONE)

`git worktree add` branches off a commit, not your working tree, so the FIXME
markers and this plan file needed to be committed before any worktree would see
them. Resolved: `app.py` and `BUGFIX_PLAN.md` are committed to `main`.
`ai_interactions.md` and `reflection.md` did not need to be committed for this —
none of the four bug prompts read or reference them.

## How this runs

1. ~~Commit the current changes to `main`.~~ Done.
2. Open 4 terminals, each starting a fresh Claude Code session **in this repo's
   root** (not inside a worktree yet — creating the worktree is each session's own
   first step, per its prompt below).
3. Once all 4 sessions are visible, each gets sent its prompt simultaneously.
4. Each session reads the real code first and sanity-checks the diagnosis and
   proposed fix below against its own read of the files — if it agrees, it executes
   the plan as written; if it finds a better approach by general best-practice
   standards, it uses that instead, but says why before writing any code. The point
   of the prompt is to save it from re-diagnosing from zero, not to be followed
   blindly.
5. Each session pauses for review at every major step (after the move+fix, again
   after the import update) — you can Undo/Discard in your editor and redirect it
   with a more specific instruction if something looks wrong, before it continues.
6. Each session adds ONE small, targeted pytest test for the exact bug it fixed
   (not a rewrite of the existing suite), and gives you the exact command to run it
   yourself.
7. Each session gives you the exact `streamlit run` command, on its own dedicated
   port, so all 4 can run live side-by-side without port collisions.

## Overview

| Bug | FIXME locations | Branch | Worktree path | Port |
|---|---|---|---|---|
| A — Difficulty settings duplicated | `get_range_for_difficulty`, `attempt_limit_map` | `bugfix/difficulty-settings` | `../ggi-difficulty-settings` | 8511 |
| B — Hint direction / check_guess | `check_guess`, the even-attempt `str(secret)` coercion | `bugfix/hint-direction` | `../ggi-hint-direction` | 8512 |
| C — Scoring logic | `update_score`, the `attempts = 1` seed line | `bugfix/scoring-logic` | `../ggi-scoring-logic` | 8513 |
| D — Secret out of range | the initial `secret` guard, New Game's `random.randint(1, 100)` | `bugfix/secret-range` | `../ggi-secret-range` | 8514 |

**Pytest commands you'll be given by each session (reference now, for your own
terminal).** The assignment's own instructions say to "confirm that your new
test passes along with the existing starter tests" — that means running the
whole file, not filtering to just the new test name, so all four use the same
unfiltered command:
```
Bug A: .venv/bin/python -m pytest tests/test_game_logic.py -v
Bug B: .venv/bin/python -m pytest tests/test_game_logic.py -v
Bug C: .venv/bin/python -m pytest tests/test_game_logic.py -v
Bug D: .venv/bin/python -m pytest tests/test_game_logic.py -v   (only meaningful if a test was actually added — see Bug D below)
```

**Streamlit commands (run from inside each bug's own worktree):**
```
Bug A: .venv/bin/python -m streamlit run app.py --server.port 8511
Bug B: .venv/bin/python -m streamlit run app.py --server.port 8512
Bug C: .venv/bin/python -m streamlit run app.py --server.port 8513
Bug D: .venv/bin/python -m streamlit run app.py --server.port 8514
```

---

## Bug A — Difficulty settings duplicated & inconsistent

**Status: COMMITTED as `c97c18e` on `bugfix/difficulty-settings` (2026-10-06).**
pytest (5 collected: 3 pre-existing failures are `check_guess`, unrelated to
this bug and expected until Bug B merges; both of this bug's own tests pass)
and the live check on port 8511 (sidebar range/attempts and the guess-prompt
text agree across Easy/Normal/Hard) both confirmed directly by Danny before
committing. Ready for the batched merge once B and C are also committed.

Session ran real win-rate modeling (verified independently: max
solvable secrets under perfect binary-search play with *k* guesses is exactly
2^k − 1 — for Hard's 5 attempts, 31, matching both the "Hard at 1–100" 31% figure
and "today's Hard at 1–50" 62% figure exactly) and found the original diagnosis
incomplete — range alone isn't the fairness picture once attempts are factored
in. Initial recommendation was Option B (range tied to Normal's, attempts 5→6),
but the session later reversed itself with a stronger argument: B's rationale was
"preserve today's ~62% difficulty," but that number is a ceiling measured on a
*broken* game (backwards hints, wrong attempt-seed, out-of-range secrets) — not a
baseline worth preserving. **Final decision: Hard = range (1, 100), attempts
stays at 5** (Option A) — matches what the original brief already called
correct, keeps this branch scoped to only the range bug actually diagnosed, and
defers attempt-count tuning to after B/C/D merge and the game is actually
playable (the new dict makes that a one-line change later). Also approved: a
symmetric `get_attempt_limit(difficulty)` helper, and folding in a fix for an
independently-found third bug — the guess-prompt text ("Guess a number between 1
and 100...") is hardcoded regardless of actual difficulty range.

**Prompt for a fresh session:**
```
You're working in the ai110-module1show-gameglitchinvestigator-starter repo — a
Streamlit number-guessing game deliberately shipped broken for a debugging
assignment.

Step 0 — set up your workspace:
1. From the repo root, create your own worktree and branch:
   git worktree add ../ggi-difficulty-settings -b bugfix/difficulty-settings
2. cd into ../ggi-difficulty-settings and set up the venv the way this project
   requires (it's a uv-managed project pinned to Python 3.13 — never plain pip):
   uv venv && uv pip install -r requirements.txt
3. All further work happens inside this worktree, not the original checkout.

Step 1 — get context, don't skip this:
Read app.py, logic_utils.py, and tests/test_game_logic.py in full before changing
anything. Find the two comments reading "# FIXME: Logic breaks here" that relate to
difficulty settings (above get_range_for_difficulty, and above attempt_limit_map).

Step 2 — sanity-check this plan before executing it:
Here's the diagnosis and proposed fix. Don't follow it blindly — you've now read
the real code, so confirm it's actually accurate, and decide if this is the best
approach or if you'd do it differently by general best-practice standards. If you
agree, execute as written. If not, do what you think is better, but explain why to
Danny before writing code.

Diagnosis: two separate structures define difficulty behavior —
get_range_for_difficulty() (an if/if/if chain) and attempt_limit_map (a dict). Hard
mode has range 1-50 (50 numbers to search) while Normal has range 1-100 (100
numbers), even though Hard is supposed to be the harder difficulty. Hard already
has fewer attempts (5 vs 8), which is correctly "harder," but its narrower range
makes it easier to search — the two settings disagree, and the two structures can
drift out of sync with each other because they're maintained independently (which
is exactly what happened).

Proposed multi-step fix:
1. Decide what Hard's range should be so it's consistently harder than Normal on
   both axes (e.g. widen it to be >= Normal's) — document your reasoning.
2. Move the logic into logic_utils.py as one consolidated dict, e.g.
   DIFFICULTY_SETTINGS = {"Easy": {"range": (1, 20), "attempts": 6}, "Normal":
   {...}, "Hard": {...}}, and implement get_range_for_difficulty to read from it
   (replacing its "raise NotImplementedError" stub).
3. Update the import in app.py: import get_range_for_difficulty (and the settings
   dict, if useful) from logic_utils, delete the inline duplicate function and the
   separate attempt_limit_map, and update both call sites.
4. Remove the two "# FIXME" comments once resolved.

STOP and show Danny the diff after step 2 (the logic_utils.py change) before
touching app.py — wait for explicit go-ahead. STOP again after step 3 before doing
anything else.

Step 3 — add one targeted test:
Add exactly this test to tests/test_game_logic.py (don't rewrite the existing
tests):
def test_hard_range_at_least_as_wide_as_normal():
    from logic_utils import get_range_for_difficulty
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")
    assert (hard_high - hard_low) >= (normal_high - normal_low)

Step 4 — give Danny these exact commands to run himself:
- Test (unfiltered, per the assignment's own instructions — confirms the new test passes alongside the existing suite, not in isolation): .venv/bin/python -m pytest tests/test_game_logic.py -v
- Live check: .venv/bin/python -m streamlit run app.py --server.port 8511

Constraints:
- Don't touch check_guess, update_score, parse_guess, or anything inside the "if
  submit:" block — other bugs, fixed in sibling worktrees in parallel.
- Don't edit ai_interactions.md or reflection.md.

Commit on this branch only after Danny confirms the diff and the test/live check
look right.
```

---

## Bug B — Hint direction / `check_guess`

**Status: COMMITTED as `22017a0` on `bugfix/hint-direction` (2026-10-06).** pytest
(5/5 passed — `check_guess` is actually implemented in this worktree, unlike A/C/D)
and the live check on port 8512 (hints point the correct direction on both odd
and even attempts) both confirmed directly by Danny before committing. Session
proactively flagged the two expected merge-conflict zones (the `app.py` import
block, the tail of `tests/test_game_logic.py`) — matches what's already
predicted in `HANDOFF.ahd.yaml`'s merge plan.

Earlier: session caught that the test prescribed below
(`test_check_guess_numeric_not_lexicographic`) doesn't actually test the bug —
passing two plain ints never reaches the `except TypeError` path at all, so it
would pass identically whether the bug existed or not. Approved replacement —
landed under renamed, clearer test names (confirmed 2026-10-06 by reading the
worktree's actual files directly, not just the self-report):
```python
def test_guess_too_low_one_digit_vs_two_digit():
    # 9 < 80 numerically (but "9" > "80" alphabetically) — kept as a basic-case check
    assert check_guess(9, 80) == "Too Low"

def test_check_guess_does_not_fall_back_to_string_compare():
    # The old code caught the TypeError from int-vs-str and compared alphabetically,
    # silently answering "Too High" for check_guess(9, "80"). A str secret must fail loudly.
    import pytest
    with pytest.raises(TypeError):
        check_guess(9, "80")
```
`app.py` diff also confirmed directly: import added, inline `check_guess` and the
even-attempt string coercion both removed, `OUTCOME_MESSAGES` lookup added with
the hint directions corrected ("Too High" → "Go LOWER!", "Too Low" → "Go
HIGHER!"). Since `check_guess` is actually implemented in this worktree (unlike
A/C/D), all 5 tests pass here, not just the 2 new ones. Command:
`.venv/bin/python -m pytest tests/test_game_logic.py -v`.

**Prompt for a fresh session:**
```
You're working in the ai110-module1show-gameglitchinvestigator-starter repo — a
Streamlit number-guessing game deliberately shipped broken for a debugging
assignment.

Step 0 — set up your workspace:
1. From the repo root: git worktree add ../ggi-hint-direction -b bugfix/hint-direction
2. cd into ../ggi-hint-direction: uv venv && uv pip install -r requirements.txt
3. All further work happens inside this worktree.

Step 1 — get context, don't skip this:
Read app.py, logic_utils.py, and tests/test_game_logic.py in full. Find the two
"# FIXME: Logic breaks here" comments relating to this: one above check_guess, one
inside the "if submit:" block right before check_guess is called.

Step 2 — sanity-check this plan before executing it:
Confirm this diagnosis against the real code, then either execute as written or do
better and explain why first.

Diagnosis: the hint message text is inverted ("guess > secret" returns "Too High"
with message "Go HIGHER!" — backwards; same inversion on the else branch).
Separately, app.py converts secret to a string on every even-numbered attempt
before calling check_guess, which raises TypeError on guess > secret (int vs str) —
caught by an except TypeError fallback that redoes the comparison alphabetically
instead of numerically (e.g. "9" > "80" is True alphabetically, though 9 < 80
numerically), producing extra-unpredictable results on even attempts specifically.
There's also a return-contract mismatch: tests/test_game_logic.py asserts
check_guess(50, 50) == "Win" (a bare string), but check_guess currently returns a
tuple.

Proposed multi-step fix:
1. Delete the even-attempt string coercion in app.py — always pass the real int
   st.session_state.secret.
2. Move check_guess to logic_utils.py, fixing the inverted direction, returning
   just the outcome string ("Win"/"Too High"/"Too Low"), and deleting the now-
   unreachable except TypeError block.
3. Update the import in app.py: import check_guess from logic_utils, delete the
   inline version, and add a small OUTCOME_MESSAGES lookup used only for display
   text, keyed by the outcome.

STOP and show Danny the diff after step 2 before touching app.py. STOP again after
step 3.

Step 3 — add one targeted test:
Add exactly this test (this specifically targets the string-comparison bug, not
just the basic direction, which the existing tests already cover):
def test_check_guess_numeric_not_lexicographic():
    from logic_utils import check_guess
    assert check_guess(9, 80) == "Too Low"

Step 4 — give Danny these exact commands:
- Tests: .venv/bin/python -m pytest tests/test_game_logic.py -v   (all 4 tests should pass now)
- Live check: .venv/bin/python -m streamlit run app.py --server.port 8512

Constraints:
- Don't touch get_range_for_difficulty, attempt_limit_map, update_score, or the
  attempts-seeding line — other bugs, fixed in sibling worktrees.
- Don't edit ai_interactions.md or reflection.md.

Commit only after Danny confirms the diff and the test/live check look right.
```

---

## Bug C — Scoring logic (`update_score` + attempts seed)

**Status: FULLY COMMITTED AND CLOSED OUT — two commits on `bugfix/scoring-logic`.**
`ed6a604` (2026-10-05): the original scoring fix — landed ahead of Danny's own
check (accepted per DR9, same precedent as Bug D/DR7), confirmed clean
afterward via Danny's own unfiltered pytest run and the port-8513 live check.
`7cc8b1f` (2026-10-06): fixes Issue 6 (New Game wasn't resetting
score/status/history — a genuine, severe, pre-existing bug found during the
live check, not caused by this branch). The session pushed back hard on the
coordinator's first proposed fix, empirically (scratch-clone merge tests, not
just argument), caught a factual error in the proposal, and the final plan
(DR11) reflects its own recommendation. Danny live-checked both the win and
loss paths before this commit. Also surfaced (separately, not fixed):
non-numeric input silently consumes an attempt, and the game-over check only
runs on valid guesses — tracked as **Issue 5**, confirmed as a real bug,
explicitly **not fixed** (Danny's call, due to time) — report only, no
worktree, no bundling with the parse_guess migration.

Independent verification inside the session was thorough: matched the
prescribed fix exactly, verified with real before/after numbers (a true
first-guess win paid 70 before the fix — seed bug and formula bug compounding
— 90 after). Implemented "Too High"/"Too Low" as one merged
`if outcome in ("Too High", "Too Low")` condition rather than two separate blocks
— functionally identical to what's prescribed below, just more compact.

**Prompt for a fresh session:**
```
You're working in the ai110-module1show-gameglitchinvestigator-starter repo — a
Streamlit number-guessing game deliberately shipped broken for a debugging
assignment.

Step 0 — set up your workspace:
1. From the repo root: git worktree add ../ggi-scoring-logic -b bugfix/scoring-logic
2. cd into ../ggi-scoring-logic: uv venv && uv pip install -r requirements.txt
3. All further work happens inside this worktree.

Step 1 — get context, don't skip this:
Read app.py, logic_utils.py, and tests/test_game_logic.py in full. Find the two
"# FIXME: Logic breaks here" comments: one above update_score, one above the
"st.session_state.attempts = 1" seed line.

Step 2 — sanity-check this plan before executing it:
Confirm against the real code, then either execute as written or do better and
explain why first.

Diagnosis: update_score's Win formula is "100 - 10 * (attempt_number + 1)", but
attempt_number is already the post-increment count when this runs, so the extra
"+1" double-counts, under-paying every win by 10 points. The "Too High" branch
alternates +5/-5 by attempt parity — rewarding a wrong guess half the time — while
"Too Low" is always a flat -5, an unexplained asymmetry (recommended fix: flatten
"Too High" to a flat -5 too, unless you have a specific reason to keep a quirk —
your call, document it). Separately, st.session_state.attempts seeds to 1 on first
load but resets to 0 via "New Game" — two different baselines for the same
counter, compounding the formula bug.

Proposed multi-step fix:
1. Fix the seed line to st.session_state.attempts = 0.
2. Move update_score to logic_utils.py: fix the Win formula to
   "100 - 10 * attempt_number" (keep the floor-at-10), flatten "Too High" to -5.
3. Update the import in app.py: import update_score from logic_utils, delete the
   inline version.

STOP and show Danny the diff after step 2 before touching app.py. STOP again after
step 3.

Step 3 — add targeted tests:
Add exactly these (two small tests, not a rewrite of the suite):
def test_win_score_first_guess():
    from logic_utils import update_score
    assert update_score(0, "Win", 1) == 90

def test_too_high_score_flat_penalty():
    from logic_utils import update_score
    assert update_score(0, "Too High", 2) == -5
    assert update_score(0, "Too High", 3) == -5

Step 4 — give Danny these exact commands:
- Tests (unfiltered, per the assignment's own instructions): .venv/bin/python -m pytest tests/test_game_logic.py -v
- Live check: .venv/bin/python -m streamlit run app.py --server.port 8513

Constraints:
- Don't touch check_guess, get_range_for_difficulty, attempt_limit_map, or the New
  Game button's secret-generation line — other bugs, fixed in sibling worktrees.
- Don't edit ai_interactions.md or reflection.md.

Commit only after Danny confirms the diff and the test/live check look right.
```

---

## Bug D — Secret can be out of range

**Status:** resolved empirically, not just reasoned about — used Streamlit's
`AppTest` harness to run real trials: 28/40 and 31/40 out-of-range before the fix
across the two candidate mechanisms respectively, confirming **both** were real
contributors (not just one). Fixed both with a single unified guard (tracks which
difficulty the current secret was drawn under, regenerates when it changes);
0/320 out-of-range after, across every difficulty with repeated switching.
Decided not to extract a pure `generate_secret()` into `logic_utils.py` (Bug A's
stub wasn't fixed yet in this worktree, so extracting would mean a third copy of
range data or depending on broken code, plus colliding with sibling worktrees
editing the same stub file) — approved. No pytest test written, as anticipated;
deferred to the testing session's `AppTest` approach. Also raised: should
switching difficulty mid-game reset the whole game state (attempts/score/status),
not just the secret? Recommended yes, to avoid landing in an incoherent state
(e.g. attempts already past the new difficulty's lower limit the instant you
switch).

Commit `c78016d` landed before the live check gate — Danny confirms (2026-10-05)
this was an accidental approval on his end, not a session process violation; the
session itself noted the ordering was off. Not reverting, since the diff was
already thoroughly empirically verified (28/40, 31/40 → 0/320 trial counts
above).

**Live check on port 8514: CONFIRMED (2026-10-06).** All 5 real scenarios
passed — difficulty switch regenerates the secret in-range for Easy/Normal/
Hard, New Game stays in-range across repeats, a mid-game switch to Hard resets
attempts/score/secret/history, and a same-difficulty rerun is a correct no-op.
Issue 6 (New Game not resetting status) is present here too, as expected —
this worktree never received Bug C's fix — but it's not a gate: it resolves
automatically once this branch and Bug C's merge together (already verified
clean via Bug C's own scratch-clone merge test). **This branch is ready for
the batched merge.**

**Prompt for a fresh session:**
```
You're working in the ai110-module1show-gameglitchinvestigator-starter repo — a
Streamlit number-guessing game deliberately shipped broken for a debugging
assignment. This one needs investigation, not just a known fix.

Step 0 — set up your workspace:
1. From the repo root: git worktree add ../ggi-secret-range -b bugfix/secret-range
2. cd into ../ggi-secret-range: uv venv && uv pip install -r requirements.txt
3. All further work happens inside this worktree.

Step 1 — get context, don't skip this:
Read app.py, logic_utils.py, and tests/test_game_logic.py in full. Find the two
"# FIXME: Logic breaks here" comments: one above the initial "secret" guard, one
inside the "if new_game:" block above its random.randint(1, 100) line.

Step 2 — sanity-check this plan before executing it:
Confirm against the real code, then either execute as written or do better and
explain why first — this bug specifically has an open question you need to resolve
yourself, not just apply a fix.

Diagnosis: the secret can land outside the selected difficulty's range (observed:
secret=96 while in Easy mode, range 1-20). Two candidate mechanisms, not yet
confirmed which is responsible:
1. The initial secret guard only runs once per session (first load) — switching
   the difficulty dropdown afterward doesn't regenerate the secret.
2. "New Game" always draws random.randint(1, 100), hardcoded, regardless of the
   selected difficulty's actual range.

Proposed steps:
1. Reproduce both paths yourself: (a) load the app, switch difficulty to Easy
   without clicking New Game, check the debug panel; (b) select Easy, click New
   Game, check the debug panel. Determine which (or both) actually produces an
   out-of-range secret.
2. Fix whichever you confirm: for #2, change random.randint(1, 100) to
   random.randint(low, high) (already computed above it). For #1, if switching
   difficulty alone is a real path to this bug, make switching the difficulty
   regenerate the secret within the new range (detect a difficulty change by
   comparing against the previously selected value in session_state).
3. If practical, extract secret-generation into a pure function in logic_utils.py,
   e.g. generate_secret(difficulty) calling get_range_for_difficulty internally —
   note get_range_for_difficulty may still be a stub if Bug A's branch hasn't
   merged yet; if so, inline the random.randint(low, high) logic directly instead,
   and leave deeper integration for after merges. This step is encouraged but
   optional — note your choice either way.

STOP and show Danny the diff after you've confirmed the mechanism and written the
fix, before going further. If you extract a logic_utils.py function, STOP again
after that.

Step 3 — add a targeted test, IF you extracted a pure function in step 2.3:
def test_generated_secret_within_easy_range():
    from logic_utils import generate_secret
    secret = generate_secret("Easy")
    assert 1 <= secret <= 20
If you did NOT extract a pure function (fix stayed inline in app.py only), skip
this — tell Danny plainly that this case isn't unit-testable with plain pytest as
written, and that the separate testing session will need Streamlit's AppTest
harness for it instead.

Step 4 — give Danny these exact commands:
- Test (only if you wrote it): .venv/bin/python -m pytest tests/test_game_logic.py::test_generated_secret_within_easy_range -v
- Live check: .venv/bin/python -m streamlit run app.py --server.port 8514

Constraints:
- Don't touch check_guess, update_score, get_range_for_difficulty, or
  attempt_limit_map — other bugs, fixed in sibling worktrees.
- Don't edit ai_interactions.md or reflection.md.

Commit only after Danny confirms the diff and live check. In your commit message,
state clearly which mechanism(s) you confirmed were actually responsible.
```

---

## Testing plan (NOT executed yet — session runs after A–D merge)

**What's missing:** each bug session above adds exactly one narrow test for its own
fix. Nothing covers `parse_guess` at all, and nothing broader than the single case
each session added for `update_score` / difficulty settings. Bug D's case may have
no pytest coverage at all if that fix stayed UI-only — this session is also where
that gets resolved, one way or another.

**Prompt for a fresh session (run only after Bugs A–D are merged to `main`):**
```
You're working in the ai110-module1show-gameglitchinvestigator-starter repo — a
Streamlit number-guessing game debugging assignment. Four separate bugfix branches
have been merged back into main by the time you start this session (difficulty
settings, hint direction / check_guess, scoring logic / update_score, and the
out-of-range secret bug) — confirm this by checking that logic_utils.py no longer
has any "raise NotImplementedError" stubs before you begin, and that
tests/test_game_logic.py now has the one narrow test each prior session added.

Read app.py, logic_utils.py, and the full current tests/test_game_logic.py before
making any changes.

Your task:
1. Add broader tests for update_score beyond the one case already there: the
   score floor never goes below 10 on a very-late win; a "Too Low" miss subtracts
   exactly 5 (mirroring the "Too High" test that already exists).
2. Add tests for parse_guess (nothing tests it yet): empty string, non-numeric
   input, a valid integer string, and a decimal string like "50.7".
3. Add a test for Easy and Hard's ranges specifically (not just the
   Hard-vs-Normal comparison that already exists) — confirm get_range_for_difficulty
   returns the exact expected (low, high) for all three difficulties.
4. For the out-of-range-secret bug: check whether a pure generate_secret()-style
   function exists in logic_utils.py. If yes and it already has a test, add one
   more for a different difficulty (e.g. Hard) to widen coverage. If no pure
   function exists (the fix stayed UI-only inside app.py's button handlers), you
   cannot test it with plain pytest — write a test using Streamlit's own test
   harness, streamlit.testing.v1.AppTest, to simulate selecting a difficulty and
   clicking "New Game," then assert at.session_state.secret is in range. Do not
   silently skip this case.
5. Run the full suite and report the final pass count.

Don't modify app.py or logic_utils.py beyond what's needed to make something
testable. Don't edit ai_interactions.md or reflection.md.

When done, report: how many tests exist now, whether all pass, and which of the
four original bug areas (if any) still lack coverage and why.
```
