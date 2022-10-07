from django.urls import path
from .views import *
from django.contrib import admin


urlpatterns = [
    path('register/', signup, name='sign_up'),
    path('login/', login, name='login'),
    path('', home, name='home')

]

