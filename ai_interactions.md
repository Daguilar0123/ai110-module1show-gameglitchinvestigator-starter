# AI Interactions Log

> **Note on how this file is actually being used (2026-10-05):** the template
> originally put a "stretch features only" disclaimer at the very top, implying it
> scoped the whole file. In practice, the **Notes** section below has been used as a
> running interaction/debugging log for the entire investigation — not a stretch
> feature — per Danny's own explicit instruction on 2026-10-04 ("if there is not a
> notes section, just use the interaction log to tag a note"). So this file is being
> used for more than what its instructions describe. To fix the organization: Notes
> (the actively-used section) now comes first, and the original "stretch features
> only" disclaimer has been moved down to sit directly above the four template
> sections it actually describes, instead of sitting at the top looking like it
> covers everything below it.

---

## Notes

> A running log of our debugging interactions on this project, one exchange at a time. Items tagged `#note` are things Danny flagged to revisit or implement later. No dedicated notes section exists elsewhere in this repo's docs, so this lives here per his instruction (2026-10-04).

**#note — 2026-10-04 — Difficulty settings observed in sidebar**

| Difficulty | Range | Attempts allowed |
|---|---|---|
| Easy | 1 to 20 | 6 |
| Normal | 1 to 100 | 8 |
| Hard | 1 to 50 | 5 |

Danny's flag: "It's probably a bug that Normal is 1 to 100 but Hard is 1 to 50" — Hard has a *smaller* range than Normal despite being the harder difficulty. Noted for investigation, not yet root-caused.

**#note — 2026-10-04 ~8:40 PM — Playthrough: hint direction + sudden loss at secret=35**

Observed sequence (Normal difficulty, range 1–100, 8 attempts):
- Guessed 50 → told "Go HIGHER" — and this continued ("Go HIGHER") all the way up through guesses 75, 93, 96, 98, 99, even as the guesses approached 100 (the range max).
- On the final guess (100, 7th recorded attempt), the hint suddenly flipped to "📉 Go LOWER!" and the game ended: "Out of attempts! The secret was 35. Score: -5."
- Full history at that point: `[50, 75, 93, 96, 98, 99]`, Attempts: 7, Score: 0 going into the last guess.

Danny's own note: "I noticed that when I selected 50, which was the halfway point of 1 to 100, it said go higher. It said go higher all the way up to 100, which was the max. All of a sudden it said go lower and 'you lose' ... It then said the number was 35." He's investigating further — logged here as the raw example, not yet diagnosed.

Evidence (screenshots, `~/Desktop/Screenshots/`):
- `Screenshot 2026-10-04 at 8.39.58 PM.png` — zoomed debug panel + final "Go LOWER!" / "Out of attempts" state
- `Screenshot 2026-10-04 at 8.40.02 PM.png` — full page view of the same end state
- `Screenshot 2026-10-04 at 8.40.08 PM.png` — sidebar settings (Normal: range 1–100, attempts 8) alongside the same debug panel

Full debug-panel text (pasted by Danny):
```
Secret: 35
Attempts: 7
Score: 0
Difficulty: Normal
History: [50, 75, 93, 96, 98, 99]
Enter your guess: 100
📉 Go LOWER!
Out of attempts! The secret was 35. Score: -5
```

**#note — 2026-10-04 — Second run: Easy mode, secret looks out-of-range + hints still off**

Settings: Easy, range 1 to 20, attempts allowed 6.

| Attempt | Guess | Hint shown |
|---|---|---|
| 1 | 50 | "Go lower" |
| 2 | 10 | "Go Lower" |
| 3 | 10 | (not noted) |

Debug panel checked at attempt 3: Secret: 96, Attempts: 3, Score: -10, Difficulty: Easy, History: `[50, 10, 10]`.

Attempt 4: guess 15 → Attempts: 4, Score: -15, History: `[50, 10, 10, 15]`.

Danny's observations (his words):
- "The secret must be the actual guess which is out of bounds from the beginning." — Secret shown as 96, which is outside the Easy range (1–20) it should have been drawn from. He wants to figure out why it's out of bounds.
- "The hints are not even accurate. They say go lower when they should say out of bounds and or go higher and vice versa."
- Ran out of attempts again on this run.

Not yet root-caused — his own investigation, same as the first run's note.

**#note — 2026-10-05 — to come back to: Streamlit's rerun model and session_state**

> `st.session_state` is the only thing that survives Streamlit's rerun-the-whole-script-on-every-click execution model. Nearly every "why does this variable do something weird" question in this codebase traces back to session_state.

Flagged by Danny to revisit later — the architectural key to understanding the state-related bugs in this app.

**#note to be implemented — 2026-10-05 — Difficulty figures: replace hardcoding with a shared dict**

> `get_range_for_difficulty`'s if/if/if chain should become a dict, same pattern as `attempt_limit_map`. Arguably the two should merge into one dict keyed by difficulty holding both range and attempt count, instead of two separate structures that can drift out of sync — which is what already happened between Normal and Hard.

Danny confirmed this is the fix he wants eventually applied (not just an observation).

**#note — 2026-10-05 — check_guess hint-direction diagnosis confirmed**

> `guess > secret` → outcome "Too High" → message "Go HIGHER!" is backwards. If your guess is higher than the secret, the next guess should go lower, not higher. Same inversion on the implicit `else` (reached whenever `guess <= secret`, since the exact-match case is handled above it).

Danny worked this out himself by reading the code; confirmed correct.

**#note — 2026-10-05 — update_score walkthrough**

> Win: `points = 100 - 10 * (attempt_number + 1)`, floored at 10, added to score. Too High: alternates +5/-5 by attempt parity. Too Low: always -5, flat. Anything else: unchanged.

Danny's own summary of this: "key-value pairs str-int where str is given or the parameter and the int is the value that is calculated with that formula" (his framing of `outcome: str` driving a computed `int` return — not literally a dict, but captures the input/output shape).

### Session summary — 2026-10-05 — Full bug catalog, before code revert

Danny decided to restart with one fresh chat session per bug, so the code fixes made
during this investigation session are being reverted (`git restore -- app.py logic_utils.py`).
This entry preserves everything learned before the revert — nothing from the
investigation is lost, only the code changes.

**Found by playing the app first, before reading any code:**
1. **Difficulty scaling is inconsistent.** Easy: 1–20, 6 attempts. Normal: 1–100, 8
   attempts. Hard: 1–50, 5 attempts. Hard has a *smaller* range than Normal despite
   being the harder difficulty — visible from the sidebar alone, no guess required.
2. **Hints point the wrong direction.** Guessing higher than the secret gets told to go
   *higher* (should be lower), and vice versa. Confirmed via the secret=35 / guess=50
   example logged above.
3. **The secret sometimes falls outside the selected difficulty's range.** Observed:
   secret=96 while in Easy mode (should be 1–20). Not yet confirmed which of two
   candidate mechanisms is responsible — flagged for its own investigation session:
   - `app.py`'s "New Game" button always draws `random.randint(1, 100)` regardless of
     the selected difficulty, instead of that difficulty's actual range.
   - Separately, switching the difficulty dropdown does *not* regenerate the secret at
     all (only first load and "New Game" do) — so a secret drawn under one difficulty
     can persist after switching to a narrower one.

**Found by reading the code, after the above:**
4. **Root cause of bug #2's deeper weirdness:** `app.py` converted the secret to a
   string on every even-numbered attempt before comparing it, which raises `TypeError`
   in Python when `>`/`<` compares an int to a str — caught by an `except TypeError`
   fallback that re-compared as strings (alphabetical order, not numeric), producing
   unpredictable results beyond just "backwards."
5. **`update_score`'s Win formula double-counts by one attempt** —
   `100 - 10 * (attempt_number + 1)` — because `attempt_number` is already the
   post-increment count when this runs.
6. **`update_score`'s "Too High" outcome alternates +5/-5 by attempt parity**, while
   "Too Low" is always a flat -5 — an unexplained asymmetry between two outcomes that
   are otherwise the same kind of mistake.
7. **`st.session_state.attempts` is seeded to `1` on first load** but reset to `0` by
   "New Game" — two different starting baselines for the same counter, compounding
   bug #5.
8. **Difficulty range and attempt-count are two separate, hand-maintained structures**
   (`get_range_for_difficulty`'s if-chain and a separate `attempt_limit_map` dict) that
   can drift out of sync — the structural root of bug #1.
9. **`logic_utils.py`'s four functions are still `NotImplementedError` stubs** — the
   real (buggy) implementations live duplicated inline in `app.py`.
10. **Return-contract mismatch:** `tests/test_game_logic.py` asserts
    `check_guess(50, 50) == "Win"` (a bare string), but the inline `check_guess` in
    `app.py` returns a `(outcome, message)` tuple.

**Adjacent, not yet confirmed as worth fixing:**
- The guess prompt text ("Guess a number between 1 and 100...") is hardcoded regardless
  of the actual difficulty range, inconsistent with the sidebar's correct caption.

**Testing gap:** only 3 pytest tests exist, all exercising `check_guess` only (Win / Too
High / Too Low). None exist for `parse_guess`, `update_score`, the difficulty settings,
or bug #3. Bug #3 isn't testable with plain pytest as-is, since it lives in a Streamlit
button handler / session_state, not a pure function — would need either refactoring
secret-generation into its own testable function, or Streamlit's `AppTest` harness.

**Status after this entry:** `app.py` and `logic_utils.py` reverted to their original
(broken, stub) state. This log and `reflection.md` are untouched by the revert.

### Session summary — 2026-10-05 — Four-worktree bugfix dispatch

Four fresh Claude sessions were started (all in the repo root on `main` initially),
each assigned one bug from `BUGFIX_PLAN.md` via a self-contained prompt instructing it
to create its own worktree, sanity-check the prescribed diagnosis against the real
code rather than follow it blindly, and stop for review at each major step. All four
did real independent verification rather than executing blindly:

- **Bug A (difficulty settings):** ran actual win-rate modeling under perfect play and
  found the original diagnosis incomplete — range alone isn't the fairness picture
  once attempts are factored in. Proposed Hard → range tied to Normal's, attempts 5→6,
  to preserve the existing difficulty curve. Independently found the same hardcoded
  "between 1 and 100" prompt-text bug Bug D's session also found.
- **Bug B (hint direction):** confirmed the diagnosis, but caught that the originally
  prescribed regression test (`check_guess(9, 80) == "Too Low"`) never actually
  exercised the buggy code path — it would pass identically whether the bug existed or
  not. Replaced it with a test asserting the old silent-fallback behavior is gone.
- **Bug C (scoring logic):** test-driven — wrote tests first, watched them fail against
  the stub, then fixed it, directly measuring the bug's compounding effect (a true
  first-guess win paid 70 instead of 90 before the fix).
- **Bug D (secret out of range):** used Streamlit's own `AppTest` harness to empirically
  confirm both candidate mechanisms were real contributors (28/40 and 31/40 trials
  out of range before the fix, 0/320 after), rather than guessing which one applied.
  Raised a genuine open question: should switching difficulty mid-game reset the whole
  game state, not just the secret? (Recommended: yes.)

All four are currently paused at a review checkpoint awaiting live confirmation before
committing.

---

> **Stretch features only.** Only fill in the sections below that apply to stretch
> features you attempted. If you did not attempt a stretch feature, leave its section
> blank or delete it. This file is not required for the core project.

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| | | | | |
| | | | | |
| | | | | |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
