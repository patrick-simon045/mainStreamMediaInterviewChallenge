from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('otp/', views.getOTP),
    path('user/', views.createUser),
    path('verify_otp/', views.verifyOTP),
]
