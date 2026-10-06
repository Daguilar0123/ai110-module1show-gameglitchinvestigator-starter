# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The [OLD] Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [✅] Describe the game's purpose.
- [✅] Detail which bugs you found.
- [✅] Explain what fixes you applied.

## 📸 Demo Walkthrough

**Describe your fixed game in numbered steps so a reader can follow along without watching a video:**

1. Start a new game on Normal difficulty (range 1 to 100, 8 attempts allowed). The secret is 98.
2. Guess 50 — the game returns "Go Higher!" (too low). Score: -5. Attempts used: 1.
3. Guess 75 — "Go Higher!" again. Score: -10. Attempts used: 2.
4. Guess 87 — "Go Higher!". Score: -15. Attempts used: 3.
5. Guess 97 — "Go Higher!". Score: -20. Attempts used: 4.
6. Guess 98 — "🎉 Correct!" The game displays "You won! The secret was 98. Final score: 30," confirming the score updated correctly on every guess and the game ended properly on the correct answer.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
================================ test session starts ================================
platform darwin -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0 -- .venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/danielaguilar/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.15.1
collected 9 items

tests/test_game_logic.py::test_winning_guess PASSED                           [ 11%]
tests/test_game_logic.py::test_guess_too_high PASSED                          [ 22%]
tests/test_game_logic.py::test_guess_too_low PASSED                           [ 33%]
tests/test_game_logic.py::test_guess_too_low_one_digit_vs_two_digit PASSED    [ 44%]
tests/test_game_logic.py::test_check_guess_does_not_fall_back_to_string_compare PASSED [ 55%]
tests/test_game_logic.py::test_win_score_first_guess PASSED                   [ 66%]
tests/test_game_logic.py::test_too_high_score_flat_penalty PASSED             [ 77%]
tests/test_game_logic.py::test_hard_range_at_least_as_wide_as_normal PASSED   [ 88%]
tests/test_game_logic.py::test_attempt_limit_per_difficulty PASSED            [100%]

================================= 9 passed in 0.03s =================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
