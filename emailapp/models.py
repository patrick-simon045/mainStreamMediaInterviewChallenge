from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    otp = models.CharField(max_length=6, null=True)

    class Meta:
        unique_together = ['username', 'password']
