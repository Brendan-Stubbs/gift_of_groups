from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from gifts.models import GiftGroup, Gift, Profile



def run():
    # TODO take into consideration that the birthday is not the current year
    today = timezone.now()
    groups = GiftGroup.objects.all()
    for group in groups:
        notify_time = today + datetime.timedelta(days=group.days_to_notify)
        birthdays_in_scope = group.users.filter(profile__birth_date__gte=today, profile__birth_date__lte=notify_time)
        for user in birthdays_in_scope:
            if not Gift.objects.filter(gift_group=group, receiver=user, wrap_up_date=user.profile.birth_date).exists():
                Gift.objects.create(gift_group=group, receiver=user, wrap_up_date=user.profile.birth_date)



class Command(BaseCommand):

    def handle(self, *args, **options):
        help = 'Create gifts from birthdays, taking into consideration the notice period set on groups "python manage.py create_gifts_from_birthdays"'
        run()
