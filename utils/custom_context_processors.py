from gifts.models import GiftGroupInvitation, Gift, ContributorGiftRelation


def check_invitations(request):
    if not request.user.is_authenticated:
        group_invitations = None
    else:
        group_invitations = GiftGroupInvitation.objects.filter(
            invitee_email=request.user.email, status=GiftGroupInvitation.STATUS_PENDING
        )
    return {"gift_group_invitations": group_invitations}

def get_active_gifts(request):
    if request.user.is_authenticated:
        gift_relations = ContributorGiftRelation.objects.filter(contributor=request.user, gift__is_complete=False).exclude(participation_status="rejected").order_by('gift__wrap_up_date')
        active_gifts = [x.gift for x in gift_relations]
        return {"active_gifts":active_gifts}
    return {}
