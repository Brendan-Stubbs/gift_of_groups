# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
from gift_of_groups import local_settings
from django.template.loader import render_to_string
from gift_of_groups.settings import DOMAIN_NAME, ACTIVATE_EMAIL_ON_ENVIRONMENT, DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.utils.html import strip_tags

domain = DOMAIN_NAME

def send_mail_helper(from_email, to_emails, subject, html_content, fail_silently=True):
    if isinstance(to_emails, str):
        to_emails = [to_emails]
    plain_message = strip_tags(html_content)
    if ACTIVATE_EMAIL_ON_ENVIRONMENT:
        send_mail(
            subject,
            plain_message,
            from_email,
            to_emails,
            html_message=html_content,
            fail_silently=fail_silently,
        )


def send_invite_email(invitation):
    send_mail_helper(
        from_email=DEFAULT_FROM_EMAIL,
        to_emails=invitation.invitee_email,
        subject = "{} {} has invited you to join {}".format(invitation.inviter.first_name, invitation.inviter.last_name, invitation.gift_group.name),
        html_content = render_to_string("gifts/email_templates/invitation_mail.html", {"invitation":invitation, "domain":domain}),
    )

def send_invite_mail_existing_user(invitation):
    send_mail_helper(
        from_email=DEFAULT_FROM_EMAIL,
        to_emails=invitation.invitee_email,
        subject = "{} {} has invited you to join {}".format(invitation.inviter.first_name, invitation.inviter.last_name, invitation.gift_group.name),
        html_content = render_to_string("gifts/email_templates/invitation_mail_existing_user.html", {"invitation":invitation, "domain":domain}),
    )

def send_gift_creation_mail(gift):
    all_emails = [x.email for x in gift.get_all_participants()]
    send_mail_helper(
        from_email=DEFAULT_FROM_EMAIL,
        to_emails=all_emails,
        subject = "{}'s birthday is approaching".format(gift.receiver.first_name),
        html_content = render_to_string("gifts/email_templates/gift_created_mail.html", {"gift":gift, "domain":domain}),
    )

def send_json_mail(subject, error):
    send_mail_helper(
        from_email=DEFAULT_FROM_EMAIL,
        to_emails="stubbsbrendan@gmail.com",
        subject = subject,
        html_content = "<p>{}</p>".format(error)
    )