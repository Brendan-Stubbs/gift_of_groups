from django.urls import path
from . import views
from gift_of_groups import local_settings

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("about", views.About.as_view(), name="about"),
    path("edit_profile", views.EditProfile.as_view(), name="edit_profile"),
    path("new_group/", views.CreateGroup.as_view(), name="new_group"),
    path("groups", views.ViewGroups.as_view(), name="view_groups"),
    path("gifts", views.ViewAllGifts.as_view(), name="view_all_gifts"),
    path("edit_group/<int:id>/", views.EditGroup.as_view(), name="edit_group"),
    path("groups/<int:id>/", views.ViewIndividualGroup.as_view(), name="view_individual_group"),
    path("group_grant_admin/<int:group_id>/<int:user_id>/", views.GrantAdminAccess.as_view(), name="group_grant_admin"),
    path("accept_invite/<int:id>/", views.AcceptGiftGroupInvitation.as_view(), name="accept_invite"),
    path("group_invitation_link/<str:code>", views.AcceptGroupInvitationLink.as_view(), name="invitation_link"),
    path("gift_invitation_link/<str:code>", views.AcceptGiftInvitationLink.as_view(), name="gift_invitation_link"),
    path("calendar", views.MasterCalendar.as_view(), name="master_calendar"),
    path("leave_group/<int:id>/", views.LeaveGiftGroup.as_view(), name="leave_group"),
    path("gift/<int:id>", views.ViewGift.as_view(), name="view_gift"),
    path("claim_captain/<int:id>", views.ClaimGiftCaptaincy.as_view(), name="claim_captain"),
    path("create_onceoff_gift", views.CreateOnceOffGift.as_view(), name="create_once_off_gift"),
    path("happy-birthday/<str:code>/", views.ViewBirthdayCard.as_view(), name="view_birthday_card"),

    path("set_gift/<int:gift_id>", views.SetGift.as_view(), name="set_gift"),
    path("mark_gift_complete/<int:id>/", views.MarkGiftComplete.as_view(), name="mark_gift_complete"),

    path("reject_invite/<int:id>/", views.RejectGiftGroupInvitation.as_view(), name="reject_invite"),
    path("ajax/vote_for_gift/<int:id>/", views.VoteForGift.as_view(), name="vote_for_gift"),
    path("ajax/add_gift_suggestion/", views.SuggestIdea.as_view(), name="suggest_gift_idea"),
    path("ajax/update_user_gift_relation/", views.UpdateUserGiftRelation.as_view(), name="update_user_gift_relation"),
    path("ajax/post_gift_comment/<int:gift_id>/", views.PostGiftComment.as_view(), name="post_gift_comment"),
    path("ajax/post_group_comment/<int:group_id>/", views.PostGroupComment.as_view(), name="post_group_comment"),
    path("ajax/captain_confirm_payment/<int:relation_id>/", views.CaptainConfirmPayment.as_view(), name="captain_confirm_payment"),
    path("ajax/update_email_notifications/<int:relation_id>/", views.UpdateEmailNotifications.as_view(), name="update_email_notifications"),
    path("ajax/get_idea_form/<int:gift_idea_id>", views.getIdeaForm.as_view(), name='get_idea_form'),
    path("ajax/update_idea/<int:idea_id>", views.UpdateIdea.as_view(), name="update_idea"),
    path("ajax/get_relation_form/<int:relation_id>", views.GetUserGiftRelationForm.as_view(), name="get_relation_form"),
    path("ajax/captain_update_relation/<int:relation_id>", views.CaptainUpdateRelationForm.as_view(), name="captain_update_relation"),
    path("ajax/generate_card/<int:gift_id>/", views.GenerateCard.as_view(), name="generate_card"),

    path("ajax/mark_notifications_read/", views.MarkNotificationsRead.as_view(), name="mark_notfications_read"),
    path("ajax/get_comments/<int:gift_id>/", views.GetComments.as_view(), name="get_comments"),
    path("ajax/get_group_comments/<int:group_id>/", views.GetGroupComments.as_view(), name="get_group_comments"),

    path("ajax/refresh_gifts/<int:id>/", views.RefreshGifts.as_view(), name="refresh_gifts"),
    path("ajax/invite_to_gift/<int:id>/", views.InviteToGift.as_view(), name="invite_to_gift"),
    path("ajax/update_profile_pic/<int:id>", views.UpdateProfilePic.as_view(), name="update_profile_pic"),

    path("webhook/donatemesomecoffee/", views.WebhookBuyMeACoffee.as_view(), name="webhook_buy_coffee"),
    path("webhook/supportthegiftlyonpatreon/", views.WebhookPatreon.as_view(), name="webhook_patreon"),
]
