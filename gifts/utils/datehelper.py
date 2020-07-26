from django.utils import timezone
import datetime


def get_next_birthday(profile):
    now = datetime.datetime.now()
    birth_month = profile.birth_date.month
    birth_day = profile.birth_date.day
    if birth_month == 2 and birth_day == 29:
        birth_year = now.year if now.month < 2 else now.year+1
        birth_day = 28 if birth_year % 4 != 0 else birth_day
        return datetime.datetime(birth_year, birth_month, birth_day)
    if datetime.datetime(now.year, birth_month, birth_day) >= now:
        return datetime.datetime(now.year, birth_month, birth_day)
    return datetime.datetime(now.year+1, birth_month, birth_day)