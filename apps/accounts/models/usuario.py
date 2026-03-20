from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager


class Usuario(AbstractBaseUser):
    class Meta:
        app_label = 'accounts'
    

    class Cargo(models.TextChoices):
        ALUNO = ('aluno', 'Aluno')
        SERVIDOR = ('servidor', 'Servidor')
        ADMINISTRADOR = ('admin', 'Admin')


    matricula = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)

    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255)

    cargo = models.CharField(max_length=8, choices=Cargo.choices)

    objects = UserManager()
    USERNAME_FIELD = 'matricula'

    @property
    def is_authorized(self):
        return self.cargo != self.Cargo.ALUNO
