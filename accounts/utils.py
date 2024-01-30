from datetime import timedelta
from django.core.mail import EmailMessage
import datetime
import pytz


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            to=[data["to_email"]],
        )
        email.send()


def current_time():
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

    