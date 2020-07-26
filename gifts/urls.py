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
    path("reject_invite/<int:id>/", views.RejectGiftGroupInvitation.as_view(), name="reject_invite"),
    path("leave_group/<int:id>/", views.LeaveGiftGroup.as_view(), name="leave_group"),
    path("gift/<int:id>", views.ViewGift.as_view(), name="view_gift"),
    path("claim_captain/<int:id>", views.ClaimGiftCaptaincy.as_view(), name="claim_captain"),
]
