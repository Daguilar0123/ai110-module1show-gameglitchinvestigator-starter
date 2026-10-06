# 💭 Reflection: Game Glitch Investigator

**Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.**

## 1. What was broken when you started?

**What did the game look like the first time you ran it?**
**List at least two concrete bugs you noticed at the start (for example: "the hints were backwards").**

The first time I ran the game, it looked normal. Nothing jumped out as off or wrong, at first. It looks like a working Streamlit number-guessing app. Components include: a difficulty selector in the sidebar, a guess box, and hint feedback after each submission. Nothing looked broken on the surface. I found the bugs by actually playing the app first, before reading any code at all:

1. The difficulty settings don't make sense — Hard has a *smaller* number range
   (1–50) than Normal (1–100) despite being the harder difficulty, even though it
   also gives fewer attempts (5 vs. 8).
2. The hints point the wrong direction. Guessing higher than the secret told me to
   go *higher* (should be lower), and vice versa — consistently, every guess.
3. The secret number itself sometimes falls outside the range the selected
   difficulty promises — I saw a secret of 96 while playing on Easy, which should
   only draw from 1–20.

**Bug Reproduction Log**

**Document at least 3 bugs you found. Add rows as needed.**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Open the sidebar and compare "Normal" vs. "Hard" (no guess needed) | Hard should be at least as hard as Normal on every axis (same-or-narrower range, same-or-fewer attempts) | Hard shows a *smaller* range (1–50) than Normal (1–100) despite fewer attempts (5 vs. 8) — its range is actually easier to search | None — renders normally, no error |
| Normal mode, secret was 35, guessed 50 (higher than the secret) | Hint should say "Go LOWER" | Hint said "Go HIGHER" — and kept saying it on every subsequent guess climbing toward 100, until the attempts ran out | None — no error, just the wrong text |
| Easy mode (range should be 1–20); Developer Debug Info checked at attempt 3 | Secret should always be between 1 and 20 while Easy is selected | Secret was 96 — outside the stated range | None — no error, just an out-of-range value with nothing flagging it |

---

## 2. How did you use AI as a teammate?

**Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?**

I used only Claude Code on this project. CLAUDE.md was used to write the general rules for the project, and I collaborated with Claude to create and refine it — important things like how I would work with worktrees were included in that document. The main structure is explained in CLAUDE.md, but overall, I started with one session to set up the project. Then we worked out a plan for identifying the bugs, labeled them, and made plans to give instructions to four separate sessions that would each start their own worktree. From there, I coordinated with the coordinator (or orchestrator) session, going back and forth as each bug got fixed, then tested, then merged.

**Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).**

The session fixing the difficulty-settings bug suggested merging two separate pieces of code — one function that handled the number range for each difficulty, and a separate dictionary that handled attempt counts — into one combined dictionary called `DIFFICULTY_SETTINGS`. That made sense to me: the bug existed in the first place because those two things were tracked separately and could drift out of sync, which is exactly what had happened (Hard had a smaller range than Normal even though it's supposed to be the harder difficulty). Keeping both values together for each difficulty means that kind of mismatch can't happen again. I confirmed it worked two ways: two new pytest tests passed, and I played the game live on each difficulty and checked that the range, the attempts allowed, and the guess-prompt text all matched up correctly.

**Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.**

The session that worked on the difficulty settings initially recommended raising Hard's attempts from 5 to 6, on top of widening its range, so it would keep roughly the same overall difficulty the game already had. I pushed back and said that didn't make sense, because the difficulty it was trying to preserve was measured on the broken game — backwards hints, wrong attempt counts, secrets outside the range — so there wasn't a real baseline worth protecting. I kept Hard's attempts at 5, which matches what the assignment brief called correct from the start, and I verified that this was still a fair level of difficulty by checking the math myself: with perfect play, the number of secrets you can find in k guesses works out to 2^k − 1, which confirmed 5 attempts already gives Hard a real, deliberate challenge without needing any extra adjustment.

---

## 3. Debugging and testing your fixes

**How did you decide whether a bug was really fixed?**

I tested it using pytest, then I did a live test run, going through the numbered checklist my orchestrator session created for me.

**Describe at least one test you ran (manual or using pytest) and what it showed you about your code.**

```
def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"
```
This test checked that the "Too Low" hint fired when it was supposed to fire. First it sets a variable named result with the result of check_guess(40,50). `def check_guess(guess, secret):` This means that the `guess=40` and the `secret=50`. Then assert checked if after running `check_guess(40,50)` the answer was "Too Low". If it was, it passed. If it was not, it failed.

**Did AI help you design or understand any tests? How?**

Yes. The test I was originally given for the hint-direction bug was check_guess(9, 80) == "Too Low", but the session working on that bug pointed out that this test doesn't actually prove the fix works — two plain numbers never trigger the part of the code that was actually broken, so the test would pass whether the bug existed or not. It replaced that test with one that calls check_guess(9, "80") (a string this time) and checks that it raises a TypeError, since the fixed code is supposed to fail loudly instead of silently comparing things the wrong way. Seeing pytest pass on the new version and fail on the old one made it click for me: a good test has to actually exercise the broken code path, not just produce the right-looking answer by coincidence.

---

## 4. What did you learn about Streamlit and state?

**How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?**

The Streamlit session state is the part of the app's memory that sticks around between actions, even though Streamlit actually reruns the entire script from top to bottom every time I do something — click a button, type a guess, change the difficulty dropdown. Without session state, every one of those actions would reset the whole app, like refreshing the page from scratch. It's what lets things like the current secret number, my score, and how many attempts I've used stick around across all those reruns instead of disappearing. I used to think winning, losing, or switching difficulty "started a new session," but that's not quite right — the session is really tied to having the page open in my browser. What those actions actually do is explicitly reset specific pieces of session state through code written for those buttons, not because Streamlit automatically wipes anything. That distinction is actually how I found a real bug: the "New Game" button wasn't resetting everything it should have — the score and status were getting left behind — which only made sense once I understood that session state only changes when the code tells it to.

---

## 5. Looking ahead: your developer habits

**What is one habit or strategy from this project that you want to reuse in future labs or projects?**
  **This could be a testing habit, a prompting strategy, or a way you used Git.**

Plan Mode, and planning the bug fixes before actually fixing, has done so much to help me understand the code I'm looking at. Using a new chat for each bugfix is a great idea too. I'll also use worktrees going forward, and have one chat set up the project before I start making changes to code — making sure that session becomes the orchestrator or coordinator that sets up CLAUDE.md and keeps the spec updated regularly as the project changes.

**What is one thing you would do differently next time you work with AI on a coding task?**

I will start a lot sooner. I am doing better with time management now that I am using AI agents to regularly check my emails and plan my days.

**In one or two sentences, describe how this project changed the way you think about AI generated code.**

It increased my confidence in AI's ability to generate good code, as long as I take the steps to be diligent, plan, verify, and use pytest — which is another thing I learned along the way. I learned that live tests exercise the whole running app, which matters for testing the full experience, while pytest or any test I write can hone in on one specific function and test it directly.
