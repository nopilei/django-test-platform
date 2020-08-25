from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class TestUser(AbstractUser):
    date_of_birth = models.DateField(default=timezone.now, verbose_name='Дата рождения')
    description = models.TextField(verbose_name='Описание', blank=True)
    photo = models.ImageField(verbose_name='Фото', blank=True,
                              null=True, upload_to='images',
                              default='images/default_profile.png')
