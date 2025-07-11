from datetime import datetime


def is_data_for_date(timeserie_date: str, date: datetime):
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    parsed_date = datetime.strptime(timeserie_date, date_format)
    return parsed_date.date() == date.date()
