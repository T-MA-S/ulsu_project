from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic import FormView
from .forms import *
from .models import *

import hashlib
import random
import string



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

            user = UserModel(email=email, username=username, password=pass1)
            user.save()


            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        "form": form,
    }
    return render(request, "catalog/sign_up.html", context=context)


def login(request, exception = None):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            return redirect('home')
            if user is not None:
                form = login(request, user)
        else:
            messages.error(request, 'Введённые данные некорректны')

    else:

        form = UserLoginForm()
    context = {
        "forms": form,

    }
    return render(request, "catalog/sign_in.html", context=context)





def randomString(stringLength=10):
    letters = string.ascii_lowercase
    some_str = ''.join(random.choice(letters) for i in range(stringLength))
    hash_object = hashlib.sha256(str.encode(some_str))
    hex_dig = hash_object.hexdigest()

    return hex_dig

def generate_restore_link(request, email):
    user = UserModel.objects.get(email=email)
    the_string = randomString()
    RestorelinkModel.objects.create(url=the_string, user=user)
    return ('{}/restore_password/{}'.format(request.build_absolute_uri('/'), the_string))


def forgotpassword(request):
    if request.method == 'POST':
        form = GetEmailForm(request.POST)
        print(form.errors)
        if form.is_valid():
            email = form.cleaned_data['email']
            link = generate_restore_link(request, email)

            send_mail(
                "Restore your password",
                'Перейдите по ссылке, чтобы восстановить пароль ' + link,
                'ulsuproject@outlook.com',
                [email],
            )
            print(email)
            return HttpResponse("Проверьте почту, мы отправили вам ссылку для восстановления")
    else:

        form = GetEmailForm()
    return render(request, 'catalog/forgot_password.html', {'form': form})


