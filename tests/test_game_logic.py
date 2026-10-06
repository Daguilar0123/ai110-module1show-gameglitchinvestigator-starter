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

def test_guess_too_low_one_digit_vs_two_digit():
    # 9 < 80 numerically (but "9" > "80" alphabetically)
    assert check_guess(9, 80) == "Too Low"

def test_check_guess_does_not_fall_back_to_string_compare():
    # The old code caught the TypeError from int-vs-str and compared alphabetically,
    # silently answering "Too High" for check_guess(9, "80"). A str secret must fail loudly.
    import pytest
    with pytest.raises(TypeError):
        check_guess(9, "80")

def test_win_score_first_guess():
    from logic_utils import update_score
    assert update_score(0, "Win", 1) == 90

def test_too_high_score_flat_penalty():
    from logic_utils import update_score
    assert update_score(0, "Too High", 2) == -5
    assert update_score(0, "Too High", 3) == -5

def test_hard_range_at_least_as_wide_as_normal():
    from logic_utils import get_range_for_difficulty
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")
    assert (hard_high - hard_low) >= (normal_high - normal_low)

def test_attempt_limit_per_difficulty():
    # Hard keeps fewer attempts than Normal; the range test above covers the other axis
    from logic_utils import get_attempt_limit
    assert get_attempt_limit("Easy") == 6
    assert get_attempt_limit("Normal") == 8
    assert get_attempt_limit("Hard") == 5
