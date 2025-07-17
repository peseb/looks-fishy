def get_condition_summary_text(fishing_condition: float) -> str:
    if fishing_condition < 1:
        return "Bad"
    elif fishing_condition < 2:
        return "Decent"
    elif fishing_condition < 3:
        return "Good"

    return "Excellent"
