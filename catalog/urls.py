from django.urls import path
from .views import *


urlpatterns = [
    path('register/', signup, name='sign_up'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', home, name='home'),
    path('forgot_password/', forgotpassword, name='forgot_password'),
    path('restore_password/<str:access_code>', restore_password, name='restore_password'),
]

