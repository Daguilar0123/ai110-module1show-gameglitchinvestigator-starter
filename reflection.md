# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

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

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Open the sidebar and compare "Normal" vs. "Hard" (no guess needed) | Hard should be at least as hard as Normal on every axis (same-or-narrower range, same-or-fewer attempts) | Hard shows a *smaller* range (1–50) than Normal (1–100) despite fewer attempts (5 vs. 8) — its range is actually easier to search | None — renders normally, no error |
| Normal mode, secret was 35, guessed 50 (higher than the secret) | Hint should say "Go LOWER" | Hint said "Go HIGHER" — and kept saying it on every subsequent guess climbing toward 100, until the attempts ran out | None — no error, just the wrong text |
| Easy mode (range should be 1–20); Developer Debug Info checked at attempt 3 | Secret should always be between 1 and 20 while Easy is selected | Secret was 96 — outside the stated range | None — no error, just an out-of-range value with nothing flagging it |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
