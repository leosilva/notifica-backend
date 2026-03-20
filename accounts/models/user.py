from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager


class User(AbstractBaseUser):
    class Meta:
        app_label = 'accounts'


    username = models.CharField(max_length=14, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
