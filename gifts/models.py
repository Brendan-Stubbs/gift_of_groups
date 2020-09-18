from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.db.models import Count, Sum
from django.dispatch import receiver
from django.utils import timezone
from django.utils.crypto import get_random_string
from gifts.utils import datehelper, group_helper, sendgrid_helper


class ProfilePic(models.Model):
    image = models.URLField()
    is_premium = models.BooleanField(default=False)


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
    has_made_donation = models.BooleanField(default=False)
    profile_pic = models.ForeignKey(ProfilePic, on_delete=models.SET_NULL, null=True, blank=True)

    def get_profile_pic(self):
        if self.profile_pic:
            return self.profile_pic.image
        return "https://giftly-groups.s3.us-east-2.amazonaws.com/no-avatar.jpg"

    def get_groups(self):
        return GiftGroup.objects.filter(user=self)

    def get_next_birthday(self):
        if self.birth_date:
            return datehelper.get_next_birthday(self)

    def are_bank_details_complete(self):
        return bool(self.bank_account_number) and bool(self.bank_name)

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
    icon = models.CharField(max_length=30, default="fas fa-users", choices=group_helper.ICON_CHOICES)

    def get_all_comments(self):
        return GroupComment.objects.filter(group=self).order_by('-created_at')

    def create_invitation(self, inviter, invitee_email):
        if not GiftGroupInvitation.objects.filter(gift_group=self, invitee=invitee_email, status=GiftGroupInvitation.STATUS_PENDING).exists() and not invitee in self.users.all():
            invite = GiftGroupInvitation.objects.create(gift_group=self, invitee_email=invitee_email, inviter=inviter)
            sendgrid_helper.send_invite_email(invite)

    def get_group_gifts_for_user(self, user):
        '''Returns all active gifts for the group, excluding the one's pertaining to user'''
        group_gifts = ContributorGiftRelation.objects.filter(gift__gift_group=self, gift__is_complete=False, contributor=user).exclude(gift__receiver=user)
        return [x.gift for x in group_gifts]

    def create_gift_relation_for_group(self, user):
        active_gifts = Gift.objects.filter(gift_group=self, is_complete=False).exclude(receiver=user)
        for gift in active_gifts:
            if not ContributorGiftRelation.objects.filter(contributor=user, gift=gift).exists():
                ContributorGiftRelation.objects.create(contributor=user, gift=gift)

    def create_upcoming_gifts(self):
        '''Creates any upcoming gifts and returns the amount create as an integer'''
        gifts_created = 0
        birthdays_in_scope = datehelper.get_upcoming_birthdays(self)
        for user in birthdays_in_scope:
            if not Gift.objects.filter(gift_group=self, receiver=user, wrap_up_date=user.profile.get_next_birthday()).exists():
                Gift.objects.create(gift_group=self, receiver=user, wrap_up_date=user.profile.get_next_birthday())
                gifts_created += 1
        return gifts_created

    def manage_user_change(sender, instance, action, pk_set, **kwargs):
        ids = list(pk_set)
        changed_users = User.objects.filter(pk__in=ids)
        if action == 'post_add':
            for user in changed_users:
                instance.create_gift_relation_for_group(user)
        # elif action == 'post_remove':
        #     instance.remove_gift_relation_for_group(user)

    def get_all_members_next_birthday(self):
        members = self.users.all()
        birthdays = {}
        for member in members:
            next_birthday = member.profile.get_next_birthday()
            if next_birthday:
                member_name = "{} {}".format(member.first_name, member.last_name)
                if next_birthday in birthdays:
                    birthdays[next_birthday].append(member_name)
                else:
                    birthdays[next_birthday] = [member_name]
        return birthdays


    def save(self, *args, **kwargs):
        if not self.pk:
            super(GiftGroup, self).save(*args, **kwargs)
            GroupInvitationLink.objects.create(group=self)
        else:
            super(GiftGroup, self).save(*args, **kwargs)
        

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


m2m_changed.connect(GiftGroup.manage_user_change,
                    sender=GiftGroup.users.through)


class GroupInvitationLink(models.Model):
    group = models.OneToOneField(GiftGroup, on_delete=models.CASCADE)
    code = models.CharField(max_length=32, unique=True)

    def create_unique_code(self):
        random_code = get_random_string(32)
        while GroupInvitationLink.objects.filter(code=random_code).exists():
            random_code = get_random_string(32)
        return random_code

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = self.create_unique_code()
        super(GroupInvitationLink, self).save(*args, **kwargs)


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
        sendgrid_helper.send_gift_creation_mail(self)

    def get_total_pledged_amount(self):
        pledged_total = ContributorGiftRelation.objects.filter(gift=self).aggregate(Sum('contribution'))['contribution__sum']
        return pledged_total if pledged_total else 0

    def get_total_contribution_amount(self):
        contribution_total = ContributorGiftRelation.objects.filter(gift=self, payment_has_cleared=True).aggregate(Sum('contribution'))['contribution__sum']
        return contribution_total if contribution_total else 0

    def get_total_pledged_percentage(self):
        if self.chosen_gift:
            return (self.get_total_pledged_amount() / self.chosen_gift.price) * 100
        return 0

    def get_total_contribution_percentage(self):
        if self.chosen_gift:
            return (self.get_total_contribution_amount() / self.chosen_gift.price) * 100
        return 0

    def save(self, *args, **kwargs):
        self.wrap_up_date = self.receiver.profile.get_next_birthday()
        super(Gift, self).save(*args, **kwargs)

    def get_all_gift_suggestions_with_vote_info(self, user):
        gift_ideas = GiftIdea.objects.filter(gift=self).annotate(vote_count=Count('votes')).order_by('-vote_count')
        for idea in gift_ideas:
            idea.user_has_voted = user in idea.votes.all()
        return gift_ideas

    def get_all_contributors(self):
        gift_relations = ContributorGiftRelation.objects.filter(gift=self)
        return [x.contributor for x in gift_relations]

    def get_all_comments(self):
        return GiftComment.objects.filter(gift=self).order_by('-created_at')

    def get_contributor_count(self):
        return len(ContributorGiftRelation.objects.filter(gift=self, participation_status="approved"))

    def get_confirmed_payment_count(self):
        return len(ContributorGiftRelation.objects.filter(gift=self, has_made_payment=True))

    def __unicode__(self):
        return "{} {} : {}".format(self.receiver.first_name, self.receiver.last_name, self.wrap_up_date.strftime("%d %b"))

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
    PARICIPATION_CHOICES = (
        ("approved", "Yes, I will be contributing!"),
        ("rejected", "No, I am sitting this one out."),
    )

    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    contribution = models.FloatField(default=0)
    has_made_payment = models.BooleanField(default=False)
    payment_has_cleared = models.BooleanField(default=False)
    participation_status = models.CharField(max_length=15, null=True, blank=True, choices=PARICIPATION_CHOICES, default=None)

    def save(self, *args, **kwargs):
        if self.contributor != self.gift.receiver:
            super(ContributorGiftRelation, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{} - {}".format(self.contributor, self.gift)

    def __str__(self):
        return self.__unicode__()


class GiftComment(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    content = models.TextField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{} commented on {}'s gift".format(self.poster.first_name, self.gift.receiver.first_name)

    def __str__(self):
        return self.__unicode__()


@receiver(post_save, sender=GiftComment)
def create_gift_notification(sender, instance, created, **kwargs):
    if created:
        gift_relations = ContributorGiftRelation.objects.filter(gift=instance.gift).exclude(participation_status='rejected').exclude(contributor=instance.poster)
        for relation in gift_relations:
            GiftCommentNotification.objects.create(user=relation.contributor, comment=instance)


class GroupComment(models.Model):
    group = models.ForeignKey(GiftGroup, on_delete=models.CASCADE)
    content = models.TextField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{} commented in {}".format(self.poster.first_name, self.group.name)

    def __str__(self):
        return self.__unicode__()


@receiver(post_save, sender=GroupComment)
def create_group_notification(sender, instance, created, **kwargs):
    if created:
        group_members = instance.group.users.all().exclude(id=instance.poster.id)
        for member in group_members:
            GroupCommentNotification.objects.create(user=member, comment=instance)


class GiftCommentNotification(models.Model):
    comment = models.ForeignKey(GiftComment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    def get_url_type(self):
        return "gift"


class GroupCommentNotification(models.Model):
    comment = models.ForeignKey(GroupComment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    def get_url_type(self):
        return "group"


class Donation(models.Model):
    ORIGIN_CHOICES = (
        ("patreon", "Patreon"),
        ("buy_me_a_coffee", "Buy Me a Coffee"),
    )
    email = models.EmailField(max_length=100, null=True, blank=True)
    origin = models.CharField(max_length=30, null=True, blank=True, choices=ORIGIN_CHOICES)
    amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
