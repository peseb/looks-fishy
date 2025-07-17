from colorama import Fore, Style


def color_condition_result(condition: float, condition_str: str) -> str:
    if condition < 1:
        return Fore.RED + condition_str + Style.RESET_ALL
    elif condition < 2:
        return Fore.YELLOW + condition_str + Style.RESET_ALL
    elif condition < 3:
        return Fore.LIGHTGREEN_EX + condition_str + Style.RESET_ALL

    return Fore.GREEN + condition_str + Style.RESET_ALL
