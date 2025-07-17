from datetime import datetime


def date_from_str(date_str: str):
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    return datetime.strptime(date_str, date_format)


def is_data_for_date(timeserie_date: str, date: datetime):
    parsed_date = date_from_str(timeserie_date)
    return parsed_date.date() == date.date()
