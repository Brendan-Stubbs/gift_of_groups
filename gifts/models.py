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
    users = models.ManyToManyField(User)
    admins = models.ManyToManyField(User, related_name="admin")
    created_at = models.DateField(auto_now_add=True)
    standard_user_can_invite = models.BooleanField(default=False)

    def create_invitation(self, inviter, invitee_email):
        if not GiftGroupInvitation.objects.filter(gift_group=self, invitee=invitee_email, status=GiftGroupInvitation.STATUS_PENDING).exists() and not invitee in self.users.all():
            GiftGroupInvitation.objects.create(gift_group=self, invitee_email=invitee_email, inviter=inviter)
            # TODO trigger an email here

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class GiftGroupInvitation(models.Model):
    STATUS_PENDING = 1
    STATUS_ACCEPTED = 2
    STATUS_REJECTED = 3

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_REJECTED, "Rejected"),
    )

    gift_group = models.ForeignKey(GiftGroup, on_delete=models.CASCADE)
    inviter = models.ForeignKey(User, on_delete=models.CASCADE)
    invitee_email = models.CharField(max_length=50)
    status = models.IntegerField(default=1, choices=STATUS_CHOICES)

    def accepted(self):
        if not User.objects.filter(email=self.invitee_email).exists():
            return
        invitee = User.objects.get(email=self.invitee_email)
        self.gift_group.users.add(invitee)
        self.status = self.STATUS_ACCEPTED
        self.save()

    def rejected(self):
        self.status = self.STATUS_REJECTED
        self.save()


class Gift(models.Model):
    gift_group = models.ForeignKey(GiftGroup, null=True, on_delete=models.SET_NULL)
    receiver = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    item_title = models.CharField(max_length=100)
    item_description = models.TextField(blank=True)
    item_url = models.URLField(null=True, blank=True)
    target_amount = models.FloatField(default=0)


class ContributorGiftRelation(models.Model):
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    contribution = models.FloatField(default = 0)
    has_made_payment = models.BooleanField(default=True)
    payment_has_cleared = models.BooleanField(default=True)

    # TODO change title, description, url to a gift idea foreign key
