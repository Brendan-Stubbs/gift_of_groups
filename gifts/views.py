from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.models import User

from .forms import GiftGroupForm, Profile, GiftGroupInvitationForm
from gifts.models import GiftGroup, GiftGroupInvitation


class Index(generic.View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "gifts/index.html", context)


class ViewGroups(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("index")  # TODO Change to something apropriate
        user = request.user
        groups = GiftGroup.objects.filter(users=user)
        for group in groups:
            group.members_total = len(group.users.all())
            group.user_is_admin = user in group.admins.all()
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
            instance.admins.add(request.user)
            instance.users.add(request.user)
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
        user = request.user
        group = GiftGroup.objects.get(id=self.kwargs["id"])
        if not user in group.admins.all():
            return  # TODO add appropriate redirect

        form = GiftGroupForm(instance=group)
        context = {"form": form}
        return render(request, "gifts/edit_group.html", context)

    def post(self, request, *args, **kwargs):
        if not GiftGroup.objects.filter(id=self.kwargs["id"]).exists():
            return  # TODO add approprite redirect
        user = request.user
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
        user = request.user
        group = GiftGroup.objects.get(id=self.kwargs["id"])
        if not user in group.users.all():
            return  # TODO appropriate redirect
        members = group.users.all()
        for member in members:
            member.is_admin = member in group.admins.all()
        user_is_admin = user in group.admins.all()
        invitation_form = GiftGroupInvitationForm()

        context = {
            "members": members,
            "user_is_admin": user_is_admin,
            "group": group,
            "invitation_form": invitation_form,
        }
        return render(request, "gifts/view_individual_group.html", context)


    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("register")
        user = request.user
        group = GiftGroup.objects.get(id=self.kwargs["id"])
        if not user in group.users.all():
            return redirect("view_groups")
        invitation_form = GiftGroupInvitationForm(request.POST)
        # TODO simplify this validation
        if invitation_form.is_valid():
            instance = invitation_form.save(commit=False)
            instance.gift_group = group
            instance.inviter = user
            instance.status = GiftGroupInvitation.STATUS_PENDING
            if not GiftGroupInvitation.objects.filter(invitee_email=instance.invitee_email, gift_group=group, status=1) and not GiftGroup.objects.filter(id=group.id, users__email=instance.invitee_email).exists():
                instance.save()

        return redirect("view_individual_group", group.id)


class GrantAdminAccess(generic.View):
    def get(self, request, *args, **kwargs):
        if (
            not request.user.is_authenticated
            or not GiftGroup.objects.filter(id=self.kwargs["group_id"]).exists()
            or not User.objects.filter(id=self.kwargs["profile_id"]).exists()
        ):
            return  # TODO appropriate redirect
        user = request.user
        group = GiftGroup.objects.get(id=self.kwargs["group_id"])
        selected_user = User.objects.get(id=self.kwargs["profile_id"])
        if not user in group.admins.all():
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


class LeaveGiftGroup(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return #TODO appropriate redirect
        if not GiftGroup.objects.filter(id=self.kwargs['id']):
            return # TODO appropriate redirect
        gift_group = GiftGroup.objects.get(id=self.kwargs['id'])
        gift_group.users.remove(request.user)
        gift_group.admins.remove(request.user)
        gift_group.save()
        return redirect("view_groups")



# TODO consider changing Reject Invite to an ajax function. Maybe just on rejection
