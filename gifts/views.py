from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import GiftGroupForm, Profile, GiftGroupInvitationForm, ProfileForm
from gifts.models import GiftGroup, GiftGroupInvitation


class Index(generic.View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "gifts/index.html", context)


class EditProfile(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        form = ProfileForm(instance=request.user.profile)
        context = {"form": form}
        return render(request, "gifts/edit_profile.html", context)


    def post(self, request, *arg, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
        else:
            messages.warning(request, "There was an error saving your changes, please try again!")
        context={"form":form}
        return render(request, "gifts/edit_profile.html", context)


class ViewGroups(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
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
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)

        form = GiftGroupForm()
        context = {"form": form}
        return render(request, "gifts/create_group.html", context)


    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)

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
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        if not GiftGroup.objects.filter(id=self.kwargs["id"]).exists():
            return  redirect("groups")
        user = request.user
        group = GiftGroup.objects.get(id=self.kwargs["id"])
        if not user in group.admins.all():
            return redirect("view_individual_group", group.id)

        form = GiftGroupForm(instance=group)
        context = {"form": form}
        return render(request, "gifts/edit_group.html", context)
        

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        if not GiftGroup.objects.filter(id=self.kwargs["id"]).exists():
            return redirect("groups")
        user = request.user
        group = GiftGroup.objects.get(id=self.kwargs["id"])
        if not user in group.admins.all():
            return redirect("view_individual_group", group.id)

        form = GiftGroupForm(request.POST, instance=group)
        if form.is_valid():
            instance = form.save()
            return redirect("view_groups")
        context = {"form": form}
        return render(request, "gifts/edit_group.html", context)


class ViewIndividualGroup(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        if not GiftGroup.objects.filter(id=self.kwargs["id"]).exists():
            return redirect("groups")
        user = request.user
        group = GiftGroup.objects.get(id=self.kwargs["id"])
        if not user in group.users.all():
            return redirect("groups")
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
            return redirect('/login/?next=%s' % request.path)
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
                messages.success(request, "{} has been invited to the group".format(instance.invitee_email))
            else:
                messages.warning(request, "{} has already been invited to this group".format(instance.invitee_email))

        return redirect("view_individual_group", group.id)


class GrantAdminAccess(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        if (
            not GiftGroup.objects.filter(id=self.kwargs["group_id"]).exists()
            or not User.objects.filter(id=self.kwargs["profile_id"]).exists()
        ):
            return redirect("groups")
        user = request.user
        group = GiftGroup.objects.get(id=self.kwargs["group_id"])
        selected_user = User.objects.get(id=self.kwargs["profile_id"])
        if user in group.admins.all():
            group.admins.add(selected_user)
            group.save()
        return redirect("view_individual_group", group.id)


class AcceptGiftGroupInvitation(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        if not GiftGroupInvitation.objects.filter(id=self.kwargs["id"]):
            return redirect("groups")
        invitation = GiftGroupInvitation.objects.get(id=self.kwargs["id"])
        if invitation.invitee_email != request.user.email:
            return #TODO appropriate redirect
        invitation.accepted()
        return redirect("view_individual_group", invitation.gift_group.id)


class RejectGiftGroupInvitation(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
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
            return redirect('/login/?next=%s' % request.path)
        if not GiftGroup.objects.filter(id=self.kwargs['id']):
            return redirect("groups")
        gift_group = GiftGroup.objects.get(id=self.kwargs['id'])
        gift_group.users.remove(request.user)
        gift_group.admins.remove(request.user)
        gift_group.save()
        return redirect("view_groups")



# TODO consider changing Reject Invite to an ajax function. Maybe just on rejection

# Next Phases
# TODO add birthdays to profile
# TODO gifts
# TODO gift comments
# TODO notifications (ajax to mark as read)
# TODO functionality to invite non group members to a once off gift

