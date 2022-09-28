from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import UserModel
from .serializers import UserModelSerializer
from rest_framework import generics

def test_email(request):

    send_mail('Subject here',
    'Here is the message.',
    'ulsuproject@outlook.com',
    ['to@example.com'],
    fail_silently=False,)
    return HttpResponse("email was sent")



class UserModelListCreate(generics.ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer

