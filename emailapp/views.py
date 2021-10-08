from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets

from .models import UserProfile

import pyotp
from django.core.mail import send_mail

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


def send_otp_mail(otp, username):
    send_mail(
        'MainStreamMedia using SparkPost with Django',
        f'The otp code is {otp}, this code will expire in 40 seconds',
        'django-sparkpost@sparkpostbox.com',
        [username],
        fail_silently=False,
    )


@api_view(['GET', 'POST'])
def createUser(request):
    getTOTP()
    otp = totp.now()

    if request.method == 'POST':
        try:
            user = UserProfile.objects.get(
                username=request.data['username'], password=request.data['password']
            )

            user.otp = otp
            user.save()
            send_otp_mail(otp=otp, username=request.data['username'])
            return Response(
                {
                    'username': user.username,
                    'otp': user.otp
                }
            )
        except ObjectDoesNotExist:
            new_user = UserProfile.objects.create(
                username=request.data['username'], password=request.data['password']
            )
            new_user.otp = otp;
            new_user.save()
            send_otp_mail(otp=otp, username=new_user.username)
            return Response(
                {
                    'message': 'user created successfully',
                    'username': new_user.username,
                    'password': new_user.password,
                    'otp': new_user.otp,
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
