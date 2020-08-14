from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from gifts.models import GiftGroup, Gift, Profile
from datetime import datetime, timedelta
import operator
from django.db.models import Q
from functools import reduce
from gifts.utils import datehelper

def mark_old_gifts_as_complete():
    expiry_date = datetime.now() - timedelta(days=25)
    old_gifts = Gift.objects.filter(wrap_up_date__lt=expiry_date)
    for gift in old_gifts:
        gift.is_complete = True
        gift.save()
    print("{} gifts marked as complete!".format(len(old_gifts)))


def create_gifts():
    gifts_created = 0
    groups = GiftGroup.objects.all()
    gifts_created = 0
    for group in groups:
        gifts_created += group.create_upcoming_gifts()
    print("Gifts created {}".format(gifts_created))


def run():
    mark_old_gifts_as_complete()
    create_gifts()


class Command(BaseCommand):

    def handle(self, *args, **options):
        help = 'Create gifts from birthdays, taking into consideration the notice period set on groups "python manage.py create_gifts_from_birthdays"'
        run()