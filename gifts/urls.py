from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("edit_profile", views.EditProfile.as_view(), name="edit_profile"),
    path("new_group/", views.CreateGroup.as_view(), name="new_group"),
    path("groups", views.ViewGroups.as_view(), name="view_groups"),
    path("edit_group/<int:id>/", views.EditGroup.as_view(), name="edit_group"),
    path("groups/<int:id>/", views.ViewIndividualGroup.as_view(), name="view_individual_group"),
    path("group_grant_admin/<int:group_id>/<int:user_id>/", views.GrantAdminAccess.as_view(), name="group_grant_admin"),
    path("accept_invite/<int:id>/", views.AcceptGiftGroupInvitation.as_view(), name="accept_invite"),
    path("leave_group/<int:id>/", views.LeaveGiftGroup.as_view(), name="leave_group"),
    path("gift/<int:id>", views.ViewGift.as_view(), name="view_gift"),
    path("claim_captain/<int:id>", views.ClaimGiftCaptaincy.as_view(), name="claim_captain"),

    path("set_gift/<int:gift_id>", views.SetGift.as_view(), name="set_gift"),
    path("mark_gift_complete/<int:id>/", views.MarkGiftComplete.as_view(), name="mark_gift_complete"),

    path("reject_invite/<int:id>/", views.RejectGiftGroupInvitation.as_view(), name="reject_invite"),
    path("ajax/vote_for_gift/<int:id>/", views.VoteForGift.as_view(), name="vote_for_gift"),
    path("ajax/add_gift_suggestion/", views.SuggestIdea.as_view(), name="suggest_gift_idea"),
    path("ajax/update_user_gift_relation/", views.UpdateUserGiftRelation.as_view(), name="update_user_gift_relation"),
    path("ajax/post_gift_comment/<int:gift_id>/", views.PostGiftComment.as_view(), name="post_gift_comment"),
    path("ajax/mark_notifications_read/", views.MarkNotificationsRead.as_view(), name="mark_notfications_read"),
    path("ajax/get_comments/<int:gift_id>/", views.GetComments.as_view(), name="get_comments"),
    path("ajax/refresh_gifts/<int:id>/", views.RefreshGifts.as_view(), name="refresh_gifts"),
    path("ajax/invite_to_gift/<int:id>/", views.InviteToGift.as_view(), name="invite_to_gift"),
]