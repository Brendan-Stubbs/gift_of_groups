from django.utils import timezone
import datetime
from functools import reduce
import operator
from django.db.models import Q
# from django.contrib.auth.models import User



def get_next_birthday(profile):
    now = datetime.datetime.now()
    birth_month = profile.birth_date.month
    birth_day = profile.birth_date.day
    if birth_month == 2 and birth_day == 29:
        birth_year = now.year if now.month < 2 else now.year+1
        birth_day = 28 if birth_year % 4 != 0 else birth_day
        return datetime.datetime(birth_year, birth_month, birth_day)
    if datetime.datetime(now.year, birth_month, birth_day).date() >= now.date():
        return datetime.datetime(now.year, birth_month, birth_day)
    return datetime.datetime(now.year+1, birth_month, birth_day)

def get_next_birthday_starting_beginning_of_current_month(profile):
  now = datetime.datetime.now()
  birth_month = profile.birth_date.month
  birth_day = profile.birth_date.day
  if birth_month == 2 and birth_day == 29:
      birth_year = now.year if now.month < 2 else now.year+1
      birth_day = 28 if birth_year % 4 != 0 else birth_day
      return datetime.datetime(now.year, birth_month, birth_day)
  
  year_to_return =  now.year if now.month == birth_month else now.year + 1
  # if datetime.datetime(now.year, birth_month, birth_day).date() >= now.date():
  #     return datetime.datetime(now.year, birth_month, birth_day)
  return datetime.datetime(year_to_return, birth_month, birth_day)


def get_upcoming_birthdays(group):
    now = datetime.datetime.now()
    then = now + datetime.timedelta(days=group.days_to_notify)

    monthdays = [(now.month, now.day)]
    while now <= then:
        monthdays.append((now.month, now.day))
        now += datetime.timedelta(days=1)

    monthdays = (dict(zip(("profile__birth_date__month", "profile__birth_date__day"), t))
                 for t in monthdays)

    query = reduce(operator.or_, (Q(**d) for d in monthdays))
    group_users = group.users.all()
    return group_users.filter(query)

def stringify_datetime_year_month_day(date):
    return "{}-{}-{}".format(date.year, date.month, date.day)