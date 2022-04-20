from django.core.mail import send_mail
import random
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from .models import User


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

def send_otp_via_email(email, code):
    try:
        subject = 'Your account verification email'
        message = f'Your otp is {code}'
        email_from = settings.EMAIL_HOST
        send_mail(subject,message, email_from, [email])
        return True
    except Exception as e:
        return False