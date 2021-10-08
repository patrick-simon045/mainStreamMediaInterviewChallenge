from django.core.exceptions import ObjectDoesNotExist
from pyotp.totp import TOTP
from rest_framework.authentication import SessionAuthentication
from rest_framework import serializers
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
import json

from .models import UserProfile

import pyotp
import time
from django.core.mail import EmailMessage, send_mail
from django.conf import settings

from django import forms


class EmailForm(forms.Form):
    recipient = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


# making totp global
secret = ''
totp = pyotp.TOTP(pyotp.random_base32())


def getTOTP():
    global secret
    secret = pyotp.random_base32()
    global totp
    totp = pyotp.TOTP(secret, interval=40)


def verifyTOTP(otp):
    res = totp.verify(otp)
    return res


@api_view()
def getOTP(request):
    getTOTP()
    otp = totp.now()

    return Response({"otp": otp})


@api_view(['GET', 'POST'])
def createUser(request):

    getTOTP()
    otp = totp.now()

    if request.method == 'POST':
        user = UserProfile.objects.get(
            username=request.data['username'], password=request.data['password']
        )

        user.otp = otp
        user.save()

        # send otp email to recipient email
        #
        #
        email = EmailMessage(
            'OPT CODE',
            f'The otp code is {otp}, this code will expire in 40 seconds',
            settings.EMAIL_HOST_USER,
            ['devtest047@gmail.com'],
            headers={'Message-ID': '45215487'},
        )
        email.send()
        #
        #

        return Response(
            {
                'username': user.username,
                'otp': user.otp
            }
        )


@api_view(['POST'])
def verifyOTP(request):
    otp = request.data['otp']
    username = request.data['username']

    try:
        UserProfile.objects.get(username=username, otp=otp)
        res = totp.verify(otp)
        print(res)

        if res:
            return Response(
                {
                    'message': 'we have a match',
                }
            )
        else:
            return Response(
                {
                    'message': 'otp expired',
                }
            )

    except ObjectDoesNotExist:
        return Response(
            {
                'message': 'object does not exist',
            }
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'otp', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
