from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Boards(models.Model):
    data = models.TextField(
        default='{"boards":[{"name":"Untitled Board","id":"b0","settings":{"theme":null},"cards":[],"identifier":0}],'
                '"settings":{"userName":"User","dataPersistence":true},"currentBoard":0,"identifier":1}')


class UserModel(AbstractUser):
    username = None  # удаление первичного ключа из родительской модели AbstractUser

    email = models.EmailField('Email', unique=True)

    boards = models.ForeignKey(Boards, on_delete=models.CASCADE, null=True)

    username = models.TextField("username")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class RestorelinkModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            expired_date__gte=timezone.now() - timezone.timedelta(hours=24)
        )


class RestorelinkModel(models.Model):
    url = models.CharField(max_length=128, null=True)
    expired_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)

    objects = RestorelinkModelManager()

    class Meta:
        verbose_name = "Ссылка для восстановления"
        verbose_name_plural = "Ссылки для восстановления"

    def __str__(self):
        return f'{self.url}'



class RegisterlinkModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            expired_date__gte=timezone.now() - timezone.timedelta(hours=24)
        )


class RegisterlinkModel(models.Model):
    url = models.CharField(max_length=128, null=True)
    expired_date = models.DateTimeField(auto_now_add=True)

    email = models.EmailField('Email')
    username = models.TextField()
    password = models.TextField()


    objects = RegisterlinkModelManager()

    class Meta:
        verbose_name = "Ссылка для регистрации"
        verbose_name_plural = "Ссылки для регистрации"

    def __str__(self):
        return f'{self.url}'
