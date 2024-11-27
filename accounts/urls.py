from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('sign-in/',views.signin),
    path('register/',views.register),
    # path('change-password/',views.changePassword),
    path('logout/',views.signOut),
]