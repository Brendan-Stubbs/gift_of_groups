from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from gift_of_groups import local_settings
from django.template.loader import render_to_string

try:
    SENDGRID_API_KEY = local_settings.SENDGRID_API_KEY
except:
    SENDGRID_API_KEY = None

def send_mail(message):
    if SENDGRID_API_KEY:
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
        except Exception as e:
            pass

def send_invite_email(invitation):
    message = Mail(
        from_email='giftlygroups@gmail.com',
        to_emails=invitation.invitee_email,
        subject = "{} {} has invited you to join {}".format(invitation.inviter.first_name, invitation.inviter.last_name, invitation.gift_group.name),
        html_content = render_to_string("gifts/email_templates/invitation_mail.html", {"invitation":invitation}),
    )
    send_mail(message)

def send_invite_mail_existing_user(invitation):
    message = Mail(
        from_email='giftlygroups@gmail.com',
        to_emails=invitation.invitee_email,
        subject = "{} {} has invited you to join {}".format(invitation.inviter.first_name, invitation.inviter.last_name, invitation.gift_group.name),
        html_content = render_to_string("gifts/email_templates/invitation_mail.html", {"invitation":invitation}),
    )
    send_mail(message)

def send_test_mail(e):
    message = Mail(
        from_email='giftlygroups@gmail.com',
        to_emails="stubbsbrendan@gmail.com",
        subject = "Testing some Sendgrid",
        html_content = "<p>{}</p>".format(e)
    )

    send_mail(message)