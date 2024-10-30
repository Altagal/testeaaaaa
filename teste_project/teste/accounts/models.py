from datetime import datetime
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None):
        if not email:
            raise ValueError('Usuario deve preencher o campo email')
        if not first_name:
            raise ValueError('Usuario deve preencher o campo Nome')
        if not last_name:
            raise ValueError('Usuario deve preencher o campo Sobrenome')

        user = self.model(
            email=email,
            first_name=first_name.title(),  # torna maiusculo os nomes
            last_name=last_name.title()  # torna maiusculo os sobrenomes
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(email=email, password=password, first_name=first_name,
                                last_name=last_name)

        user.username = None
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True

        user.save(using=self._db)

        return user


class Account(AbstractUser, BaseUserManager):
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)

    date_joined = models.DateTimeField(default=datetime.now)
    last_login = models.DateTimeField(default=datetime.now)

    is_active = models.BooleanField(default=False)  # ativação é feita só pelo superuser ou admin
    is_verified = models.BooleanField(default=False)  # verificação pelo email institucional

    # Campos nao ultilizados
    # is_staff = models.BooleanField(default=False)
    # is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Add List of fields which you want to be required

    objects = MyAccountManager()

    class Meta:
        # todas as permissoes do sistema serão alocadas aqui
        permissions = [
            ("can_manage_user", "Pode gerenciar Usuarios e Grupos"),
            ("can_test_things", "Pode testar essa coisa aqui"),
        ]

    def __str__(self):
        return self.email

    def set_status(self, status):
        self.is_active = status
