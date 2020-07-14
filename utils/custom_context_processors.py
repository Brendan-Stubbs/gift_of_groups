from gifts.models import GiftGroupInvitation


def check_invitations(request):
    if not request.user.is_authenticated:
        group_invitations = None
    else:
        group_invitations = GiftGroupInvitation.objects.filter(
            invitee_email=request.user.email, status=GiftGroupInvitation.STATUS_PENDING
        )
    return {"gift_group_invitations": group_invitations}
