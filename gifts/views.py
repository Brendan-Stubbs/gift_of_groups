from django.shortcuts import render, redirect
from django.views import generic
from .forms import GiftGroupForm, Profile
from gifts.models import GiftGroup, GiftGroupInvitation


class Index(generic.View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "gifts/index.html", context)


class ViewGroups(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("index")  # TODO Change to something apropriate
        profile = request.user.profile
        groups = GiftGroup.objects.filter(users=profile)
        for group in groups:
            group.members_total = len(group.users.all())
            group.user_is_admin = profile in group.admins.all()
        page_name = "groups"
        context = {"groups": groups, "page_name": page_name}
        return render(request, "gifts/view_groups.html", context)


class CreateGroup(generic.View):
    def get(self, request, *arg, **kwargs):
        form = GiftGroupForm()
        context = {"form": form}
        return render(request, "gifts/create_group.html", context)

    def post(self, request, *args, **kwargs):
        form = GiftGroupForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.admins.add(request.user.profile)
            instance.users.add(request.user.profile)
            instance.save()
            return redirect("view_individual_group", instance.id)
        context = {"form": form}
        return render(request, "gifts/create_group.html", context)


class EditGroup(generic.View):
    def get(self, request, *args, **kwargs):
        if (
            not GiftGroup.objects.filter(id=self.kwargs["id"]).exists()
            or not request.user.is_authenticated
        ):
            return  # TODO add approprite redirect
        user = request.user.profile
        group = GiftGroup.objects.get(id=self.kwargs["id"])
        if not user in group.admins.all():
            return  # TODO add appropriate redirect

        form = GiftGroupForm(instance=group)
        context = {"form": form}
        return render(request, "gifts/edit_group.html", context)

    def post(self, request, *args, **kwargs):
        if not GiftGroup.objects.filter(id=self.kwargs["id"]).exists():
            return  # TODO add approprite redirect
        user = request.user.profile
        group = GiftGroup.objects.get(id=self.kwargs["id"])
        if not user in group.admins.all():
            return  # TODO add appropriate redirect

        form = GiftGroupForm(request.POST, instance=group)
        if form.is_valid():
            instance = form.save()
            return redirect("view_groups")
        context = {"form": form}
        return render(request, "gifts/edit_group.html", context)


class ViewIndividualGroup(generic.View):
    def get(self, request, *args, **kwargs):
        if (
            not GiftGroup.objects.filter(id=self.kwargs["id"]).exists()
            or not request.user.is_authenticated
        ):
            return  # TODO appropriate redirect
        profile = request.user.profile
        group = GiftGroup.objects.get(id=self.kwargs["id"])
        if not profile in group.users.all():
            return  # TODO appropriate redirect
        members = group.users.all()
        for member in members:
            member.is_admin = member in group.admins.all()
        user_is_admin = profile in group.admins.all()
        context = {
            "members": members,
            "user_is_admin": user_is_admin,
            "group": group,
        }
        return render(request, "gifts/view_individual_group.html", context)


class GrantAdminAccess(generic.View):
    def get(self, request, *args, **kwargs):
        if (
            not request.user.is_authenticated
            or not GiftGroup.objects.filter(id=self.kwargs["group_id"]).exists()
            or not Profile.objects.filter(id=self.kwargs["profile_id"]).exists()
        ):
            return  # TODO appropriate redirect
        profile = request.user.profile
        group = GiftGroup.objects.get(id=self.kwargs["group_id"])
        selected_user = Profile.objects.get(id=self.kwargs["profile_id"])
        if not profile in group.admins.all():
            return  # TODO appropriate redirect

        group.admins.add(selected_user)
        group.save()
        return redirect("view_individual_group", group.id)


class AcceptGiftGroupInvitation(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return # TODO appropriate redirect
        if not GiftGroupInvitation.objects.filter(id=self.kwargs["id"]):
            return #TODO appropriate redirect
        invitation = GiftGroupInvitation.objects.get(id=self.kwargs["id"])
        if invitation.invitee_email != request.user.email:
            return #TODO appropriate redirect
        invitation.accepted()
        return redirect("view_individual_group", invitation.gift_group.id)


class RejectGiftGroupInvitation(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return # TODO appropriate redirect
        if not GiftGroupInvitation.objects.filter(id=self.kwargs["id"]):
            return #TODO appropriate redirect
        invitation = GiftGroupInvitation.objects.get(id=self.kwargs["id"])
        if invitation.invitee_email != request.user.email:
            return #TODO appropriate redirect
        invitation.rejected()
        return redirect("index") #TODO Ajax instead?



# TODO Leave group
# TODO Create an invitation
# TODO Limit invitations to one per group
# TODO refactor user relationships to use user instead of profile
# TODO consider changing Reject Invite to an ajax function. Maybe just on rejection
