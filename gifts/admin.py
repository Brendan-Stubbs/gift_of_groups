from django.contrib import admin
from .models import GiftGroup, Profile, GiftGroupInvitation, Gift, GiftIdea, ContributorGiftRelation, GiftComment, GroupComment, GiftCommentNotification, GroupInvitationLink, GiftInvitationLink

admin.site.register(GiftGroup)
admin.site.register(Profile)
admin.site.register(GiftGroupInvitation)
admin.site.register(Gift)
admin.site.register(GiftIdea)
admin.site.register(ContributorGiftRelation)
admin.site.register(GiftComment)
admin.site.register(GroupComment)
admin.site.register(GiftCommentNotification)
admin.site.register(GroupInvitationLink)
admin.site.register(GiftInvitationLink)
