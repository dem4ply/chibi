import datetime


def today():
    return datetime.datetime.now( datetime.timezone.utc )
