import pyotp
import time
from django.core.mail import EmailMessage, send_mail
from django.conf import settings


def getTOTP():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=5)
    return totp


def verifyTOTP(totp, otp):
    res = totp.verify(otp)
    return res


totp = getTOTP()
otp = totp.now()

# settings.configure()

# send_mail(
#     'OTP code email',
#     f'the otp code is {otp}',
#     'pksimon007@gmail.com',
#     ['patricksimon045@gmail.com'],
# )

# email = EmailMessage(
#     'Hello',
#     'Body goes here',
#     settings.EMAIL_HOST_USER,
#     ['patricksimon045@gmail.com'],
#     headers={'Message-ID': '45215487'},
# )
# email.send()


isVerified = verifyTOTP(totp, otp)
print(otp)
print(isVerified)

time.sleep(6)

isVerified = verifyTOTP(totp, otp)
print(otp)
print(isVerified)
