from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.db.models import Count, Sum
from django.dispatch import receiver
from django.utils import timezone
from gifts.utils import datehelper


class Profile(models.Model):
    ACCOUNT_TYPE_CHOICES = (
        ("Cheque", "Cheque"),
        ("Savings", "Savings"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    bank_account_name = models.CharField(max_length=50, null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    bank_account_number = models.CharField(max_length=30, null=True, blank=True)
    bank_account_type = models.CharField(max_length=20, null=True, blank=True, choices=ACCOUNT_TYPE_CHOICES)
    bank_branch_number = models.CharField(max_length=15, null=True, blank=True)
    bank_branch_name = models.CharField(max_length=50, null=True, blank=True)


    def get_groups(self):
        return GiftGroup.objects.filter(user=self)

    def get_next_birthday(self):
        return datehelper.get_next_birthday(self)

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
    days_to_notify = models.IntegerField(default=14)


    def create_invitation(self, inviter, invitee_email):
        if not GiftGroupInvitation.objects.filter(gift_group=self, invitee=invitee_email, status=GiftGroupInvitation.STATUS_PENDING).exists() and not invitee in self.users.all():
            GiftGroupInvitation.objects.create(gift_group=self, invitee_email=invitee_email, inviter=inviter)
            # TODO trigger an email here

    def get_group_gifts_for_user(self, user):
        '''Returns all active gifts for the group, excluding the one's pertaining to user'''
        group_gifts = ContributorGiftRelation.objects.filter(gift__gift_group=self, gift__is_complete=False, contributor=user).exclude(gift__receiver=user)
        return [x.gift for x in group_gifts]

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
    captain = models.ForeignKey(User, null=True, blank=True, related_name="group_captain", on_delete=models.SET_NULL)
    receiver = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    wrap_up_date = models.DateField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    chosen_gift = models.ForeignKey('GiftIdea', null=True, blank=True, on_delete=models.SET_NULL, related_name="chosen_gift")

    def create_contributor_relationship_for_group(self):
        contributors = self.gift_group.users.all().exclude(id=self.receiver.id)
        for contributor in contributors:
            ContributorGiftRelation.objects.create(contributor=contributor, gift=self)

    def get_total_pledged_amount(self):
        return ContributorGiftRelation.objects.filter(gift=self).aggregate(Sum('contribution'))['contribution__sum']

    def get_total_contribution_amount(self):
        return ContributorGiftRelation.objects.filter(gift=self, payment_has_cleared=True).aggregate(Sum('contribution'))['contribution__sum']

    def save(self, *args, **kwargs):
        self.wrap_up_date = self.receiver.get_next_birthday()
        super(Gift, self).save(*args, **kwargs)

    def get_all_gift_suggestions_with_vote_info(self, user):
        gift_ideas = GiftIdea.objects.filter(gift=self).annotate(vote_count=Count('votes')).order_by('-vote_count')
        for idea in gift_ideas:
            idea.user_has_voted = user in idea.votes.all()
        return gift_ideas

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
    suggested_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    votes = models.ManyToManyField(User, related_name="votes")

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