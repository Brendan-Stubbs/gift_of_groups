from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from gifts.models import GiftGroup, Gift, Profile
from datetime import datetime, timedelta
import operator
from django.db.models import Q
from functools import reduce


def birthdays_within(days):
    now = datetime.now()
    then = now + timedelta(days)

    monthdays = [(now.month, now.day)]
    while now <= then:
        monthdays.append((now.month, now.day))
        now += timedelta(days=1)

    monthdays = (dict(zip(("profile__birth_date__month", "profile__birth_date__day"), t))
                 for t in monthdays)

    query = reduce(operator.or_, (Q(**d) for d in monthdays))
    return User.objects.filter(query)


def run():
    groups = GiftGroup.objects.all()
    for group in groups:
        birthdays_in_scope = birthdays_within(group.days_to_notify)
        for user in birthdays_in_scope:
            if not Gift.objects.filter(gift_group=group, receiver=user, wrap_up_date=user.profile.get_next_birthday()).exists():
                Gift.objects.create(gift_group=group, receiver=user, wrap_up_date=user.profile.get_next_birthday())


class Command(BaseCommand):

    def handle(self, *args, **options):
        help = 'Create gifts from birthdays, taking into consideration the notice period set on groups "python manage.py create_gifts_from_birthdays"'
        run()