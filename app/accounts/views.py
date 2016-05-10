import simplejson
import logging
import json
import datetime
import hashlib
import random
import os
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import Http404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from rest_framework import status, views
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from collections import OrderedDict

from app.accounts.models import Account
from app.accounts.serializers import SignupSerializer, LoginSerializer
from app.accounts.helpers import verification_email
from django.shortcuts import redirect

log = logging.getLogger(__name__)


def register(request):
    """
    View for user registration.
    :param request:
    :return:
    """
    return render(request, 'accounts/register.html')


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_user(request):
    """
    Creates user after the successful validation
    and returns serialized object of user.
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SignupSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors,\
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            user = serializer.save()
            output_serializer = SignupSerializer(user)
            # create_artist_profile(user)
            verify_email(user)
            return Response({
                    'status': 'Created',
                    'message': 'Verification email has been sent to your email. Please verify your account.'
                }, status=status.HTTP_201_CREATED)


def login(request):
    """
    View for user login.
    :param request:
    :return:
    """
    return render(request, 'accounts/login.html')


@api_view(['POST'])
@permission_classes((AllowAny,))
def login_user(request):
    """
    Login the current user, after authenticating the credentials.
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        email = data.get('email', None)
        password = data.get('password', None)
        account = authenticate(email=email, password=password)

        if account is not None:

            if not account.is_email_verified:
                return Response({
                    'status': 'Unverified',
                    'message': 'This account is not verified.'
                }, status=status.HTTP_401_UNAUTHORIZED)

            if not account.is_active:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)

            auth_login(request, account)
            serialized = LoginSerializer(account)
            return Response(serialized.data, status=status.HTTP_200_OK)

        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


def confirm_email(request, key):
    try:
        user = Account.objects.get(activation_key=key)
    except Account.DoesNotExist:
        return render(request, 'accounts/invalid_reset_url.html')

    if (user.key_expires + datetime.timedelta(days=2)) < timezone.now():
        return render(request, 'accounts/confirm_expired.html')

    user.is_email_verified = 1
    user.is_active = True
    user.save()
    email_subject = 'Welcome to commonproject!'
    message = render_to_string('email/email_verified.html', {'user': user})
    msg = EmailMultiAlternatives(subject=email_subject, body=message,
                                 from_email="admin@commonproject.com", to=[user.email])
    msg.attach_alternative(message, "text/html")
    msg.send()
    response = msg.mandrill_response[0]
    return redirect('/accounts/email-verified/')


def reset_password(request):
    """
    View for Resetting password.
    :param request:
    :return:
    """
    return render(request, 'accounts/reset_password.html')


def verify_email(request):
    """
    View for Resetting password.
    :param request:
    :return:
    """
    return render(request, 'accounts/verify_email.html')


@api_view(['POST'])
@permission_classes((AllowAny,))
def send_verification_email(request):
    data = JSONParser().parse(request)
    email = data['email']
    try:
        user = Account.objects.get(email=email)
        verification_email(user)

        return Response({'status': 'success',
                   'message': 'Verification Email is sent to your email.'})
    except Account.DoesNotExist:
        return Response({'status': 'error',
                   'message': 'Email id is not registered. Please enter the valid email id.'})


def email_verified(request):
    """
    View for Resetting password.
    :param request:
    :return:
    """
    return render(request, 'accounts/email_verified.html')


def forgot_password(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        email = data.get('email', None)
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha1(email+salt).hexdigest()
        try:
            # user = User.objects.get(email=email)
            user=Account.objects.get(email=email)
            log.info(user)
        except user.DoesNotExist:
            request.session['error1']="Email Id Doesn't exist"
        user.reset_password_key = activation_key
        user.save()

        email_subject = 'Reset Password.'
        activation_url = "{1}/accounts/update_password/{0}".format(activation_key, os.environ.get('HOST_NAME'))

        rendertxt = render_to_string('email/reset_password.html', {'user': user, 'activation_url': activation_url})
        msg = EmailMultiAlternatives(subject=email_subject, body=rendertxt,
                                     from_email="admin@commonproject.com", to=[email])
        msg.attach_alternative(rendertxt, "text/html")
        msg.send()
        response = msg.mandrill_response[0]
        mandrill_status = response['status']
        return redirect('/accounts/forget_pwd/')


def update_new_password(request,key):
    result=""
    if 'error1' in request.session:
       result=request.session.get('error1')
    if 'error2' in request.session:
       result=request.session.get('error2')
    elif 'error1' not in request.session:
       result="Please Enter Properly"
    return render(request, 'accounts/update_password.html', {'result':result,'key':key})


def update_password_new(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        # if form.is_valid():
        password = data.get('password',None)
        confirm_password = data.get('confirm_password',None)
        key = data.get('key')
        log.info(key)
        if password != confirm_password:
            request.session['error1']= "passwords doesn't match"

        try:
            user = Account.objects.get(reset_password_key=key)
        except user.DoesNotExist:
            request.session['error1']="Invalid URL"

        if user is not None:
            user.set_password(password)
            user.reset_password_key = ''
            user.save()
            email_subject = 'Password changed for your commonproject account!'
            message = render_to_string('email/password_changed.html')
            msg = EmailMultiAlternatives(subject=email_subject, body=message,
                                         from_email="admin@commonproject.com", to=[user.email])
            msg.attach_alternative(message, "text/html")
            msg.send()
            request.session['error1']="password updated successfully"
            return redirect('/accounts/login/')

        else:
            request.session['error1']="password is not valid "