from django.contrib import admin
from django.urls import path,include
from . import views


app_name = 'users'

urlpatterns = [
    path('',include('dj_rest_auth.urls')),
    # path('registration/',include('dj_rest_auth.registration.urls')),
    path('register/',views.UserRegistrationView.as_view(),name='register'),
    path('verify/',views.VerifyView.as_view(),name='verify'),
]