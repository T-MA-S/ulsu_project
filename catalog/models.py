from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserModel(AbstractUser):
    username = None #удаление первичного ключа из родительской модели AbstractUser

    email = models.EmailField('Email', unique=True)

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