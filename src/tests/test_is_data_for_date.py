from datetime import datetime
from helper.is_data_for_date import is_data_for_date


def test_same_date():
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    date = datetime.strptime("2025-7-15T17:00:00Z", date_format)

    assert is_data_for_date("2025-7-15T17:00:00Z", date)


def test_same_date_different_hour():
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    date = datetime.strptime("2025-7-15T17:00:00Z", date_format)

    assert is_data_for_date("2025-7-15T21:00:00Z", date)


def test_different_date():
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    date = datetime.strptime("2025-7-15T17:00:00Z", date_format)

    assert not is_data_for_date("2025-7-16T17:00:00Z", date)
