from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import F
from django.template.loader import render_to_string

from gifts.utils import group_helper, sendgrid_helper
from .forms import GiftGroupForm, Profile, GiftGroupInvitationForm, ProfileForm, GiftIdeaForm, GiftIdea, GiftManagementUserForm, GiftCommentForm, GroupCommentForm
from gifts.models import GiftGroup, GiftGroupInvitation, Gift, ContributorGiftRelation, GiftCommentNotification, Donation, Profile, ProfilePic, GroupCommentNotification, GroupInvitationLink
import json


class Index(generic.View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "gifts/index.html", context)


class EditProfile(generic.View):
    free_pics = ProfilePic.objects.filter(is_premium=False)
    premium_pics = ProfilePic.objects.filter(is_premium=True)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        form = ProfileForm(instance=request.user.profile)
        context = {
            "form": form,
            "page_name": "edit_profile",
            "free_pics": self.free_pics,
            "premium_pics": self.premium_pics
        }
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
        context = {
            "form": form,
            "page_name": "edit_profile",
            "free_pics": self.free_pics,
            "premium_pics": self.premium_pics
        }
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
        icons = [x[0] for x in group_helper.ICON_CHOICES]
        selected_icon = "fas fa-users"
        context = {"form": form, "icons": icons,
                   "selected_icon": selected_icon}
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
        icons = [x[0] for x in group_helper.ICON_CHOICES]
        selected_icon = "fas fa-users"
        context = {"form": form, "icons": icons,
                   "selected_icon": selected_icon}
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
        icons = [x[0] for x in group_helper.ICON_CHOICES]
        context = {"form": form, "group": group, "icons": icons}
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
        icons = [x[0] for x in group_helper.ICON_CHOICES]
        context = {"form": form, "group": group, "icons": icons}
        return render(request, "gifts/edit_group.html", context)


class ViewAllGifts(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        user = request.user
        gift_relations = ContributorGiftRelation.objects.filter(
            contributor=user).exclude(gift__receiver=user)
        active_gifts = [x.gift for x in gift_relations.filter(
            gift__is_complete=False)]
        complete_gifts = [
            x.gift for x in gift_relations.filter(gift__is_complete=True)]
        context = {
            "active_gifts": active_gifts,
            "complete_gifts": complete_gifts,
        }
        return render(request, "gifts/view_all_gifts.html", context)


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
        group_gifts_component = render_to_string(
            "gifts/components/group_gift_collection.html", {"active_gifts": active_gifts})
        comment_form = GroupCommentForm()

        context = {
            "members": members,
            "user_is_admin": user_is_admin,
            "group": group,
            "invitation_form": invitation_form,
            "active_gifts": active_gifts,
            "group_gifts_component": group_gifts_component,
            "comment_form": comment_form,
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
            if (not GiftGroupInvitation.objects.filter(invitee_email=instance.invitee_email, gift_group=group, status=1)
                    and not GiftGroup.objects.filter(id=group.id, users__email=instance.invitee_email).exists()):
                instance.save()
                # Move the below into the model
                if User.objects.filter(email=instance.invitee_email).exists():
                    sendgrid_helper.send_invite_mail_existing_user(instance)
                else:
                    sendgrid_helper.send_invite_email(instance)

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
            or not User.objects.filter(id=self.kwargs["user_id"]).exists()
        ):
            return redirect("groups")
        user = request.user
        group = GiftGroup.objects.get(id=self.kwargs["group_id"])
        selected_user = User.objects.get(id=self.kwargs["user_id"])
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


class AcceptGroupInvitationLink(generic.View):
    def get(self, request, *args, **kwargs):
        print("get request")
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        user = request.user
        try:
            invite_link = GroupInvitationLink.objects.get(code=self.kwargs['code'])
            group = invite_link.group
            if not user in group.users.all():
                group.users.add(user)
            return redirect('view_individual_group', group.id)
        except Exception as e:
            return redirect('index')


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
            return redirect('view_groups')
        gift = Gift.objects.get(pk=self.kwargs["id"])
        if not ContributorGiftRelation.objects.filter(contributor=user, gift=gift).exists():
            return redirect('view_groups')
        gift_relations = ContributorGiftRelation.objects.filter(gift=gift)
        members = [x.contributor for x in gift_relations]
        gift_ideas = gift.get_all_gift_suggestions_with_vote_info(user)
        total_pledged = gift.get_total_pledged_amount()
        total_contributed = gift.get_total_contribution_amount
        gift_idea_form = GiftIdeaForm()
        user_gift_relation = gift_relations.get(contributor=user)
        gift_relation_form = GiftManagementUserForm(
            instance=user_gift_relation)
        birthday_has_passed = timezone.now().date() > gift.wrap_up_date
        comment_form = GiftCommentForm()
        captain_management_component = render_to_string(
            "gifts/components/captain_gift_management.html", {"gift_relations": gift_relations})

        context = {
            "gift": gift,
            "members": members,
            "captain": gift.captain,
            "gift_idea_form": gift_idea_form,
            "gift_relation_form": gift_relation_form,
            "gift_ideas": gift_ideas,
            "total_pledged": total_pledged,
            "total_contributed": total_contributed,
            "user": user,
            "user_gift_relation": user_gift_relation, # TODO Use this to hide the mark complete button
            "birthday_has_passed": birthday_has_passed,
            "comment_form": comment_form,
            "captain_management_component": captain_management_component,
        }
        return render(request, "gifts/view_gift.html", context)


class ClaimGiftCaptaincy(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        if not Gift.objects.filter(pk=self.kwargs["id"]).exists():
            return redirect('view_groups')
        gift = Gift.objects.get(pk=self.kwargs["id"])
        if request.user in gift.gift_group.users.all() and not gift.captain:
            gift.captain = request.user
            gift.save()
        return redirect("view_gift", gift.id)


class VoteForGift(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            response = JsonResponse({"error": "You are not logged in"})
            response.status_code = 403
            return response
        if not GiftIdea.objects.filter(pk=self.kwargs["id"]).exists():
            return redirect('view_groups')
        idea = GiftIdea.objects.get(pk=self.kwargs["id"])
        if ContributorGiftRelation.objects.filter(gift=idea.gift, contributor=request.user).exists():
            idea.votes.add(request.user)
            idea.save()
        total_votes = len(idea.votes.all())
        return JsonResponse({"total_votes": total_votes})


class SuggestIdea(generic.View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            response = JsonResponse(
                {"message": "Please make sure you are logged in"})
            response.status_code = 403
            return response

        try:
            user = User.objects.get(pk=request.POST.get('user_id'))
            gift = Gift.objects.get(pk=request.POST.get('gift_id'))
            ContributorGiftRelation.objects.get(
                contributor__pk=user.pk, gift__pk=gift.pk)
            gift_idea_form = GiftIdeaForm(request.POST)

            if gift_idea_form.is_valid():
                instance = gift_idea_form.save(commit=False)
                instance.gift = gift
                instance.suggested_by = user
                instance.save()

                gift_ideas = gift.get_all_gift_suggestions_with_vote_info(user)
                gift_suggestion_component = render_to_string(
                    "gifts/components/gift_suggestions_component.html", {"gift_ideas": gift_ideas})

                response = JsonResponse({
                    "title": instance.title,
                    "description": instance.description,
                    "id": instance.pk,
                    "price": instance.price,
                    "gift_suggestion_component": gift_suggestion_component,
                    "message": "Suggestion submitted succesfully",
                })
                return response

        except Exception as e:
            print(e)
            response = JsonResponse(
                {"message": "There was an error submitting your idea"})
            response.status_code = 403
            return response


class SetGift(generic.View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        user = request.user
        if not Gift.objects.filter(pk=self.kwargs["gift_id"]).exists():
            return redirect('view_groups')
        gift = Gift.objects.get(pk=self.kwargs["gift_id"])
        idea_id = request.POST.get('idea_id')
        if user == gift.captain and idea_id:
            if GiftIdea.objects.filter(gift=gift, pk=idea_id).exists():
                idea = GiftIdea.objects.get(pk=idea_id)
                gift.chosen_gift = idea
                gift.save()
        return redirect("view_gift", gift.pk)


class MarkGiftComplete(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/?next=%s' % request.path)
        self.kwargs.get("id")
        if Gift.objects.filter(id=self.kwargs.get("id")).exists():
            gift = Gift.objects.get(id=self.kwargs.get("id"))
            gift.is_complete = True
            gift.save()
            return redirect("view_individual_group", gift.gift_group.id)
        return redirect("view_groups")


class UpdateUserGiftRelation(generic.View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=403)
        try:
            gift_relation = ContributorGiftRelation.objects.get(
                pk=request.POST.get('gift_relation_id'))
            form = GiftManagementUserForm(request.POST, instance=gift_relation)
            if form.is_valid():
                instance = form.save()
            context = {
                "gift": gift_relation.gift,
            }
            gift_progress_component = render_to_string(
                "gifts/components/gift_progress_component.html", context)
            return JsonResponse({"gift_progress_component": gift_progress_component})
        except Exception as e:
            print(e)
            return JsonResponse({}, status=403)


class PostGiftComment(generic.View):
    def post(self, request, *args, **kwargs):
        try:
            gift = Gift.objects.get(pk=request.POST.get('gift_id'))
            if not request.user.is_authenticated or not ContributorGiftRelation.objects.filter(gift=gift, contributor=request.user).exists():
                return JsonResponse({}, status=403)
        except Exception as e:
            print(e)
            return JsonResponse({}, status=403)

        comment_form = GiftCommentForm(request.POST)
        instance = comment_form.save(commit=False)
        instance.poster = request.user
        instance.gift = gift
        instance.save()

        comments_component = render_to_string(
            "gifts/components/gift-comments.html", {"gift": gift})
        # comments = gift.get_all_comments().values("id", "content", "created_at", first_name=F("poster__first_name"), last_name=F("poster__last_name")).order_by('created_at')
        return JsonResponse({"comments_component": comments_component})


class GetComments(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not ContributorGiftRelation.objects.filter(gift__id=self.kwargs.get("gift_id"), contributor=request.user).exists():
            return JsonResponse(status=403)
        gift = Gift.objects.get(pk=self.kwargs.get("gift_id"))
        comments_component = render_to_string(
            "gifts/components/gift-comments.html", {"gift": gift})
        return JsonResponse({"comments_component": comments_component})


class PostGroupComment(generic.View):
    def post(self, request, *args, **kwargs):
        try:
            group = GiftGroup.objects.get(pk=request.POST.get('group_id'))
            if not request.user.is_authenticated or not request.user in group.users.all():
                return JsonResponse({}, status=403)
        except Exception as e:
            print(e)
            return JsonResponse({}, status=403)

        comment_form = GroupCommentForm(request.POST)
        instance = comment_form.save(commit=False)
        instance.poster = request.user
        instance.group = group
        instance.save()

        comments_component = render_to_string(
            "gifts/components/group-comments.html", {"group": group})
        return JsonResponse({"comments_component": comments_component})


class GetGroupComments(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user in GiftGroup.objects.get(id=self.kwargs.get("group_id")).users.all():
            return JsonResponse(status=403)
        group = GiftGroup.objects.get(pk=self.kwargs.get("group_id"))
        comments_component = render_to_string(
            "gifts/components/group-comments.html", {"group": group})
        return JsonResponse({"comments_component": comments_component})


class MarkNotificationsRead(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=403)
        notifications = list(GiftCommentNotification.objects.filter(
            user=request.user, read=False))
        notifications += list(GroupCommentNotification.objects.filter(
            user=request.user, read=False))
        for notfication in notifications:
            notfication.read = True
            notfication.save()
        return JsonResponse({})


class RefreshGifts(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=403)
        try:
            group = GiftGroup.objects.get(pk=self.kwargs.get("id"))
            group.create_upcoming_gifts()
            active_gifts = group.get_group_gifts_for_user(request.user)
            group_gifts_component = render_to_string(
                "gifts/components/group_gift_collection.html", {"active_gifts": active_gifts})
            return JsonResponse({"group_gifts_component": group_gifts_component})
        except Exception as e:
            print(e)
            return JsonResponse({}, status=403)


class InviteToGift(generic.View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=403)
        try:
            gift = Gift.objects.get(pk=self.kwargs.get("id"))
            if not User.objects.filter(email=self.kwargs.get("email")).exists():
                message = "There is no account linked to this address"
                return JsonResponse({"message": message})
            user = User.objects.get(email=self.kwargs.get("email"))
            if ContributorGiftRelation.objects.filter(gift=gift, user=user).exists():
                message = "This user is already part of the group"
                return JsonResponse({"message": message})
            gift.group.create_gift_relation_for_group(user)
            message = "Succesfully added {} {} to group".format(
                user.first_name, user.last_name)
            return JsonResponse({"message": message})
        except:
            return JsonResponse({}, status=403)


class UpdateProfilePic(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            try:
                profile_pic = ProfilePic.objects.get(pk=self.kwargs["id"])
                if profile_pic.is_premium and not user.has_made_donation:
                    pass
                else:
                    user.profile.profile_pic = profile_pic
                    user.profile.save()
                    return JsonResponse({"new_image": profile_pic.image})
            except:
                pass
        return JsonResponse({}, status=403)


@method_decorator(csrf_exempt, name="dispatch")
class WebhookBuyMeACoffee(generic.View):

    def post(self, request, *args, **kwargs):
        try:
            data = request.body.decode("utf-8")
            js = json.loads(data)["response"]
            email = js.get("supporter_email")
            amount = float(js.get("total_amount"))
            origin = "buy_me_a_coffee"
            Donation.objects.create(email=email, amount=amount, origin=origin)
            if Profile.objects.filter(user__email=email).exists():
                profile = Profile.objects.get(user__email=email)
                profile.has_made_donation = True
                profile.save()
        except:
            pass

        return HttpResponse("")


@method_decorator(csrf_exempt, name="dispatch")
class WebhookPatreon(generic.View):
    def post(self, request, *args, **kwargs):
        try:
            data = request.body.decode("utf-8")
            js = json.loads(data)
            sendgrid_helper.send_json_mail("Patreon JSON Response", str(js))
            email = js["included"][1]["attributes"]["email"]
            amount = js["data"]["attributes"]["campaign_lifetime_support_cents"] / 100.0
            origin = "patreon"

            if Donation.objects.filter(email=email, origin=origin).exists():
                donation = Donation.objects.get(email=email, origin=origin)
                donation.amount = amount
                donation.save()
            else:
                Donation.objects.create(email=email, amount=amount, origin=origin)

            if Profile.objects.filter(user__email=email).exists():
                profile = Profile.objects.get(user__email=email)
                profile.has_made_donation = True
                profile.save()
        except Exception as e:
            sendgrid_helper.send_json_mail("error with patreon", str(e))
        return HttpResponse("")

# TODO Create a Once Off Gift

# Maybe
# TODO Captain must be able to change pledged values
# TODO set up social auth (Google + Facebook)