# It is better to use Celery for sending emails.

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_notification_to_customers(customer_email, serial, model, version):
    """
    Send email to the customer, if the awaited robot appears.

    :param customer_email: address for sending email.
    :param serial: Robot.serial.
    :param model: Robot.model.
    :param version: Robot.version
    """
    html_message = render_to_string(
        "notification_email.html",
        {"model": model, "serial": serial, "version": version},
    )
    message = strip_tags(html_message)

    send_mail(
        subject=serial,
        message=message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[customer_email],
        fail_silently=True,
    )
