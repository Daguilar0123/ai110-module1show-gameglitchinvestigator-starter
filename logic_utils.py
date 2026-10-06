# Single source of truth for per-difficulty behavior. Hard ties Normal's range
# and allows fewer attempts, so it is at least as hard on both axes.
DIFFICULTY_SETTINGS = {
    "Easy": {"range": (1, 20), "attempts": 6},
    "Normal": {"range": (1, 100), "attempts": 8},
    "Hard": {"range": (1, 100), "attempts": 5},
}
DEFAULT_DIFFICULTY = "Normal"


def _settings_for(difficulty: str):
    """Look up a difficulty's settings, falling back to Normal if unknown."""
    return DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS[DEFAULT_DIFFICULTY])


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    return _settings_for(difficulty)["range"]


def get_attempt_limit(difficulty: str):
    """Return the number of attempts allowed for a given difficulty."""
    return _settings_for(difficulty)["attempts"]


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome string.

    outcome: "Win", "Too High" (guess > secret), or "Too Low" (guess < secret)

    Both arguments must be ints. Display text for each outcome lives in the UI.
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    attempt_number is the guess count including the current guess (1 on the
    first guess). A win pays 100 - 10 * attempt_number, floored at 10; any
    wrong guess costs a flat 5.
    """
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
