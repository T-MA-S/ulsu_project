from django.urls import path
from .views import *
from django.contrib import admin

urlpatterns = [
    path('', views.sign, name='sign_in')
]