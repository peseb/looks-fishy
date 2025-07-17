from colorama import Fore, Style
from helper.color_condition_result import color_condition_result
from helper.get_condition_summary_text import get_condition_summary_text


def test_get_condition_summary_text_bad():
    condition = 0
    result = get_condition_summary_text(condition)
    result = color_condition_result(condition, result)
    assert result == f"{Fore.RED}Bad{Style.RESET_ALL}"


def test_get_condition_summary_text_decent():
    condition = 1.5
    result = get_condition_summary_text(condition)
    result = color_condition_result(condition, result)

    assert result == f"{Fore.YELLOW}Decent{Style.RESET_ALL}"


def test_get_condition_summary_text_good():
    condition = 2.5
    result = get_condition_summary_text(condition)
    result = color_condition_result(condition, result)

    assert result == f"{Fore.LIGHTGREEN_EX}Good{Style.RESET_ALL}"


def test_get_condition_summary_text_excellent():
    condition = 5.5
    result = get_condition_summary_text(condition)
    result = color_condition_result(condition, result)

    assert result == f"{Fore.GREEN}Excellent{Style.RESET_ALL}"
