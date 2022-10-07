from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserModel(AbstractUser):
    username = None #удаление первичного ключа из родительской модели AbstractUser

    email = models.EmailField('Email', unique=True)

    name = models.TextField("username")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"