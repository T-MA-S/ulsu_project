from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse

def test_email(request):
    send_mail('Subject here',
    'Here is the message.',
    'ulsuproject@outlook.com',
    ['to@example.com'],
    fail_silently=False,)
    return HttpResponse("email was sent")


def sign(request):
    return render(request, "catalog/sign_in.html")

