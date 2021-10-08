from django.contrib import admin
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'otp')


admin.site.register(UserProfile, UserProfileAdmin)
