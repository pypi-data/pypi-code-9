from django.core.mail import get_connection
from postgun.message import MailGunMessage


def send_mail(subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, html_message=None, campaign=None,
              delivery_time=None, dkim=None, track=None,
              track_clicks=None, track_opens=None, custom_headers=None,
              cc=None, bcc=None, tags=None, reply_to=None):
    """
    Copied from the django send_mail function and uses the MailGunMessage
    class instead of the EmailMessage class.

    :param subject:
    :param message:
    :param from_email:
    :param recipient_list:
    :param fail_silently:
    :param auth_user: Ignored - kept for capability.
    :param auth_password: Ignored - kept for capability.
    :param connection: Ignored - kept for capability.
    :param html_message: string - HTML version of your message
    :param campaign:  string - Tag your email with a Mailgun Campaign.
    :param delivery_time:  string - 'Thu, 13 Oct 2011 18:02:00 GMT'
    :param dkim: Boolean -  Enables/disabled DKIM signatures on per-message basis
    :param track: Boolean -
    :param track_clicks: Boolean -
    :param track_opens:  Boolean -
    :param custom_headers: Dictionary - keys should be 'plain'.
    :param cc: List - email addresses to carbon copy
    :param bcc: List - email addresses to blind carbon copy
    :param tags: List - Maximum of 3 strings to tag the email with
    :param reply_to: string - Email address which to set to reply-to
    :return:
    """
    connection = connection or get_connection(username=auth_user,
                                              password=auth_password,
                                              fail_silently=fail_silently)
    mail = MailGunMessage(subject, message, from_email, recipient_list,
                          connection=connection, campaign=campaign,
                          delivery_time=delivery_time, dkim=dkim, track=track,
                          track_clicks=track_clicks, track_opens=track_opens,
                          custom_headers=custom_headers, cc=cc, bcc=bcc, tags=tags, reply_to=reply_to
    )
    if html_message:
        mail.attach_alternative(html_message, 'text/html')

    return mail.send()
