from django.contrib.auth.models import AbstractUser
from django.db import models

from mailing_service.models import NULLABLE


# Create your models here.
class User(AbstractUser):

    username = None
    email = models.EmailField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to='users/avatar', **NULLABLE)
    phone = models.CharField(max_length=35, **NULLABLE)
    country = models.CharField(max_length=30, **NULLABLE)
    birthday = models.DateField(verbose_name='дата рождения', **NULLABLE)

    token = models.CharField(max_length=30, **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
