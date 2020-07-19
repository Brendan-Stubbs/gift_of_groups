from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


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

    def get_group_gifts_for_user(self, user):
        '''Returns all active gifts for the group, excluding the one's pertaining to user'''
        return Gift.objects.filter(gift_group=self, is_complete=False).exclude(receiver=user)

    def create_gift_relation_for_group(self,user):
        active_gifts = Gift.objects.filter(gift_group=self, is_complete=False).exclude(receiver=user)
        for gift in active_gifts:
            if not ContributorGiftRelation.objects.filter(contributor=user, gift=gift).exists():
                ContributorGiftRelation.objects.create(contributor=user, gift=gift)
    

    def manage_user_change(sender, instance, action, pk_set, **kwargs):
        ids = list(pk_set)
        changed_users = User.objects.filter(pk__in=ids)
        if action == 'post_add':
            for user in changed_users:
                instance.create_gift_relation_for_group(user)
        # elif action == 'post_remove':
        #     instance.remove_gift_relation_for_group(user)


    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

m2m_changed.connect(GiftGroup.manage_user_change, sender=GiftGroup.users.through)


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
    gift_group = models.ForeignKey(GiftGroup, null=True, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    wrap_up_date = models.DateField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    chosen_gift = models.ForeignKey('GiftIdea', null=True, blank=True, on_delete=models.SET_NULL, related_name="chosen_gift")

    def create_contributor_relationship_for_group(self):
        contributors = self.gift_group.users.all().exclude(id=self.receiver.id)
        for contributor in contributors:
            ContributorGiftRelation.objects.create(contributor=contributor, gift=self)

    def save(self, *args, **kwargs):
        self.wrap_up_date = self.receiver.profile.birth_date #TODO defend against Null value
        super(Gift, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{}'s gift : {}".format(self.receiver, self.wrap_up_date.strftime("%d %b"))

    def __str__(self):
        return self.__unicode__()

@receiver(post_save, sender=Gift)
def populate_gift_relations(sender, instance, created, **kwargs):
    if created:
        instance.create_contributor_relationship_for_group()


class GiftIdea(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    description = models.TextField(blank=True)
    url = models.URLField(null=True, blank=True)
    price = models.FloatField()

    def __unicode__(self):
        return "{} for {}".format(self.title, self.gift)

    def __str__(self):
        return self.__unicode__()


class ContributorGiftRelation(models.Model):
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    contribution = models.FloatField(default = 0)
    has_made_payment = models.BooleanField(default=False)
    payment_has_cleared = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.contributor != self.gift.receiver:
            super(ContributorGiftRelation, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{} - {}".format(self.contributor, self.gift)

    def __str__(self):
        return self.__unicode__()