from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import FormView
from .forms import *
from .models import *


def test_email(request):
    send_mail('Subject here',
              'Here is the message.',
              'ulsuproject@outlook.com',
              ['to@example.com'],
              fail_silently=False, )
    return HttpResponse("email was sent")


def home(request):
    if request.user.is_authenticated:
        return render(request, "catalog/test.html")
    else:
        return redirect('login')


def login(request):
    return render(request, "catalog/sign_in.html")


def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            pass1 = form.cleaned_data['password1']
            pass2 = form.cleaned_data['password2']

            print(email, username, pass1, pass2)

            # здесь должен быть функционал добавления user'a

            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        "form": form,
    }
    return render(request, "catalog/sign_up.html", context=context)
