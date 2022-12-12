from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import UserModel
from .serializers import UserModelSerializer
from rest_framework import generics
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.generic import TemplateView
from django.views.generic import FormView
from .forms import *
from .models import *

import hashlib
import random
import string


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
    return ('{}restore_password/{}'.format(request.build_absolute_uri('/'), the_string))


def generate_register_link(request, email, username, pass1):
    the_string = randomString()
    RegisterlinkModel.objects.create(url=the_string, email=email, username=username, password=pass1)
    return ('{}accept_register/{}'.format(request.build_absolute_uri('/'), the_string))


def test_email(request):
    send_mail('Subject here',
              'Here is the message.',
              'ulsuproject@outlook.com',
              ['to@example.com'],
              fail_silently=False, )
    return HttpResponse("email was sent")


class UserModelListCreate(generics.ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer


def home(request):
    if request.user.is_authenticated:
        context = {
            "user_email": request.user.email
        }
        return render(request, "catalog/index.html", context=context)
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

            link = generate_register_link(request, email, username, pass1)

            send_mail(
                "Confirm Your Account",
                'Перейдите по ссылке, чтобы подтвердить учётную запись ' + link,
                'ulsuproject@outlook.com',
                [email],
            )

            return HttpResponse("Проверьте почту, мы отправили вам ссылку для подтверждения учётной записи")



    else:
        form = UserRegisterForm()

    context = {
        "form": form,
    }
    return render(request, "catalog/sign_up.html", context=context)


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

            else:
                error = "Неверный логин или пароль"
                context = {
                    "form": form,
                    "error": error
                }
                return render(request, "catalog/sign_in.html", context=context)


    else:
        form = UserLoginForm()
    context = {
        "form": form,
        "error": "",
    }
    return render(request, "catalog/sign_in.html", context=context)


def forgotpassword(request):
    if request.method == 'POST':
        form = GetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            link = generate_restore_link(request, email)

            send_mail(
                "Restore your password",
                'Перейдите по ссылке, чтобы восстановить пароль ' + link,
                'ulsuproject@outlook.com',
                [email],
            )

            return HttpResponse("Проверьте почту, мы отправили вам ссылку для восстановления")
    else:

        form = GetEmailForm()
    return render(request, 'catalog/forgot_password.html', {'form': form})


def get_user_data(request, email):
    if request.method == "GET":
        current_user = UserModel.objects.get(email=email)
        return HttpResponse(current_user.boards.data)


def post_user_data(request, email):
    if request.method == "POST":
        data = request.POST
        current_user = UserModel.objects.get(email=email)
        current_user.boards.data = data['content']
        current_user.boards.save()

        return HttpResponse("")


def restore_password(request, access_code):
    if RestorelinkModel.objects.filter(url=access_code).exists():
        if request.method == 'POST':
            form = RestorePasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password1']
                current_user = UserModel.objects.get(
                    id=RestorelinkModel.objects.get(url=access_code).user.id)
                current_user.set_password(password)
                current_user.save()
                RestorelinkModel.objects.filter(url=access_code).delete()
                return redirect('login')
        else:

            form = RestorePasswordForm()

        return render(request, 'catalog/restore_password.html', {'form': form})

    else:
        return HttpResponse("Bad or Expired link")


def accept_register(request, access_code):
    if RegisterlinkModel.objects.filter(url=access_code).exists():
        current_link = RegisterlinkModel.objects.get(url=access_code)
        email = current_link.email
        username = current_link.username
        pass1 = current_link.password
        user = UserModel(email=email, username=username)
        user.set_password(pass1)
        board = Boards()
        board.save()
        user.boards = board
        user.save()
        return HttpResponse('Учетнаяа запись успешно подтверждена')

    else:
        return HttpResponse("Bad or Expired link")


def user_logout(request):
    logout(request)
    return redirect('home')
