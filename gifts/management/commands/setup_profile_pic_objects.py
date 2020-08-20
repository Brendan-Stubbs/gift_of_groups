from django.core.management.base import BaseCommand, CommandError
from gifts.models import ProfilePic

free_pics = [
    "https://giftly-groups.s3.us-east-2.amazonaws.com/avatar1.png"
]

premium_pics = [

]

def create_profile_pics():
    total_created = 0
    for pic in free_pics:
        if not ProfilePic.objects.filter(image=pic):
            ProfilePic.objects.create(image=pic, is_premium=False)
            total_created += 1
    for pic in premium_pics:
        if not ProfilePic.objects.filter(image=pic):
            ProfilePic.objects.create(image=pic, is_premium=True)
            total_created += 1
    print("New objects created: {}".format(total_created))

def run():
    create_profile_pics()

class Command(BaseCommand):

    def handle(self, *args, **options):
        help = 'Create all profile pic objects "python manage.py setup_profile_pics"'
        run()
