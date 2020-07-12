from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)

    def get_groups(self):
        return GiftGroup.objects.filter(user=self)

    def __unicode__(self):
        return self.user.email

    def __str__(self):
        return self.__unicode__()


class GiftGroup(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(Profile)
    admins = models.ManyToManyField(Profile, related_name="admin")
    created_at = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
