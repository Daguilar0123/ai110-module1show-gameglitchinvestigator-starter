from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_win_score_first_guess():
    from logic_utils import update_score
    assert update_score(0, "Win", 1) == 90

def test_too_high_score_flat_penalty():
    from logic_utils import update_score
    assert update_score(0, "Too High", 2) == -5
    assert update_score(0, "Too High", 3) == -5
