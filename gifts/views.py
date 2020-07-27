from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse

from .forms import GiftGroupForm, Profile, GiftGroupInvitationForm, ProfileForm, GiftIdeaForm
from gifts.models import GiftGroup, GiftGroupInvitation, Gift, ContributorGiftRelation


class Index(generic.View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "gifts/index.html", context)


class EditProfile(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        form = ProfileForm(instance=request.user.profile)
        context = {"form": form, "page_name": "edit_profile"}
        return render(request, "gifts/edit_profile.html", context)

    def post(self, request, *arg, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
        else:
            messages.warning(
                request, "There was an error saving your changes, please try again!")
        context = {"form": form, "page_name": "edit_profile"}
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
            return redirect("groups")
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
        active_gifts = group.get_group_gifts_for_user(user)

        context = {
            "members": members,
            "user_is_admin": user_is_admin,
            "group": group,
            "invitation_form": invitation_form,
            "active_gifts": active_gifts,
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
        # TODO simplify this validation Move into model save method
        if invitation_form.is_valid():
            instance = invitation_form.save(commit=False)
            instance.gift_group = group
            instance.inviter = user
            instance.status = GiftGroupInvitation.STATUS_PENDING
            if not GiftGroupInvitation.objects.filter(invitee_email=instance.invitee_email, gift_group=group, status=1) and not GiftGroup.objects.filter(id=group.id, users__email=instance.invitee_email).exists():
                instance.save()
                messages.success(request, "{} has been invited to the group".format(
                    instance.invitee_email))
            else:
                messages.warning(request, "{} has already been invited to this group".format(
                    instance.invitee_email))

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
            return  # TODO appropriate redirect
        invitation.accepted()
        return redirect("view_individual_group", invitation.gift_group.id)


class RejectGiftGroupInvitation(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            response = JsonResponse({"error": "You are not logged in"})
            return response
        if not GiftGroupInvitation.objects.filter(id=self.kwargs["id"]).exists():
            response = JsonResponse({"error": "This group doesn't exist"})
            response.status_code = 403
            return response
        invitation = GiftGroupInvitation.objects.get(id=self.kwargs["id"])
        if invitation.invitee_email != request.user.email:
            response = JsonResponse(
                {"error": "You are not authorised to reject this invitation"})
            response.status_code = 403
            return response
        invitation.rejected()
        return JsonResponse({"message": "Invitation Rejected"})


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


class ViewGift(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        user = request.user
        if not Gift.objects.filter(pk=self.kwargs["id"]).exists():
            redirect('view_groups')
        gift = Gift.objects.get(pk=self.kwargs["id"])
        if not ContributorGiftRelation.objects.filter(contributor=user, gift=gift).exists():
            redirect('view_groups')
        gift_relations = ContributorGiftRelation.objects.filter(gift=gift)
        members = [x.contributor for x in gift_relations]
        gift_idea_form = GiftIdeaForm()
        context = {
            "gift": gift,
            "members": members,
            "captain": gift.captain,
            "gift_idea_form": gift_idea_form,
        }
        return render(request, "gifts/view_gift.html", context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return ('/login/?next=%s' % request.path)
        user = request.user
        if not Gift.objects.filter(pk=self.kwargs["id"]).exists():
            redirect('view_groups')
        gift = Gift.objects.get(pk=self.kwargs["id"])
        if not ContributorGiftRelation.objects.filter(contributor=user, gift=gift).exists():
            redirect('view_groups')
        gift_relations = ContributorGiftRelation.objects.filter(gift=gift)
        members = [x.contributor for x in gift_relations]

        gift_idea_form = GiftIdeaForm(request.POST)
        if gift_idea_form.is_valid():
            instance = gift_idea_form.save(commit=False)
            instance.requested_by = user
            instance.gift = gift
            instance.save()
            messages.success(request, "Your suggestion was successful")
            return redirect("view_gift", gift.id)
        else:
            messages.warning(
                request, 'There was an error suggesting your gift')

        context = {
            "gift": gift,
            "members": members,
            "captain": gift.captain,
            "gift_idea_form": gift_idea_form,
        }
        return render(request, "gifts/view_gift.html", context)


class ClaimGiftCaptaincy(generic.View):
    def get(self, request, *args, **kwargs):
        print("Claiming")
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        if not Gift.objects.filter(pk=self.kwargs["id"]).exists():
            return redirect('view_groups')
        gift = Gift.objects.get(pk=self.kwargs["id"])
        if request.user in gift.gift_group.users.all() and not gift.captain:
            gift.captain = request.user
            gift.save()
        return redirect("view_gift", gift.id)


# Next Phases
# TODO handle post on gift suggestion form
# TODO Stop someone from becoming captain before they have given bank details
# TODO gifts
# TODO gift comments
# TODO notifications (ajax to mark as read)
# TODO functionality to invite non group members to a once off gift
