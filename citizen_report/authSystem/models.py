from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, email, username, password, is_staff, is_superuser, department, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an email address')

        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username = username,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            department=department,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password, **extra_fields):
        user = self._create_user(
            email,
            username,
            password,
            **extra_fields
        )
        user.is_staff = False
        user.is_superuser = False
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        user = self._create_user(
            email,
            username,
            password,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    department = models.CharField(max_length=254, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()


    def __str__(self) -> str:
        return f'{self.username}'
