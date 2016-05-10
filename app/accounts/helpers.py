import hashlib
import logging
import random
import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

log = logging.getLogger(__name__)


def verification_email(user):

    email = user.email

    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(email+salt).hexdigest()

    user.activation_key = activation_key
    user.key_expires = timezone.now()
    user.save()

    email_subject = 'Activate your Creathives account.'
    activation_url = "{1}/accounts/confirm-email/{0}".format(activation_key, os.environ.get('HOST_NAME'))

    render = render_to_string('email/verify_email.html', {'user': user, 'activation_url': activation_url})
    msg = EmailMultiAlternatives(subject=email_subject, body=render,
                                 from_email="admin@creathives.com", to=[email])
    msg.attach_alternative(render, "text/html")
    msg.send()
    response = msg.mandrill_response[0]
    mandrill_status = response['status']
    return mandrill_status