from django.urls import path, include
from .views import getOTP
from rest_framework import routers
from emailapp import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('otp/', views.getOTP),
    path('user/', views.createUser),
    path('verify_otp/', views.verifyOTP),
]
