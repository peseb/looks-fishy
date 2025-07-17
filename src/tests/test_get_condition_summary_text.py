from helper.get_condition_summary_text import get_condition_summary_text


def test_get_condition_summary_text_bad():
    condition = 0
    result = get_condition_summary_text(condition)

    assert result == "Bad"


def test_get_condition_summary_text_decent():
    condition = 1.5
    result = get_condition_summary_text(condition)

    assert result == "Decent"


def test_get_condition_summary_text_good():
    condition = 2.5
    result = get_condition_summary_text(condition)

    assert result == "Good"


def test_get_condition_summary_text_excellent():
    condition = 5.5
    result = get_condition_summary_text(condition)

    assert result == "Excellent"
