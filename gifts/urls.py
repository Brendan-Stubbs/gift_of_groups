from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("new_group/", views.CreateGroup.as_view(), name="new_group"),
    path("groups", views.ViewGroups.as_view(), name="view_groups"),
    path("edit_group/<int:id>/", views.EditGroup.as_view(), name="edit_group"),
    path(
        "groups/<int:id>/",
        views.ViewIndividualGroup.as_view(),
        name="view_individual_group",
    ),
    path(
        "group_grant_admin/<int:group_id>/<int:profile_id>/",
        views.GrantAdminAccess.as_view(),
        name="group_grant_admin",
    ),
]
