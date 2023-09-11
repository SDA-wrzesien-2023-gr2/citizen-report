from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, email, username, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
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
            is_staff=False,
            is_superuser=False,
            **extra_fields
        )

        return user

    def create_superuser(self, email, username, password, **extra_fields):
        user = self._create_user(
            email,
            username,
            password,
            is_staff=True,
            is_superuser=True,
            department='SYS',
            **extra_fields
        )

        return user


class User(AbstractBaseUser, PermissionsMixin):
    DEPARTMENT_CHOICES = [
        ('APP', 'Applicant'),
        ('SYS', 'System supervisor'),
        ('RBR', 'Roads and bridges'),
        ('SWS', 'Sewer and waterworks'),
        ('POW', 'Power supply'),
        ('GAS', 'Gasworks'),
        ('TEL', 'Telecommunication'),
        ('GAR', 'Garbage disposal'),
        ('CTR', 'City transport'),
        ('HTH', 'Healthcare'),
        ('EDU', 'Education'),
        ('SAF', 'Public safety')
    ]
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    department = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES, default='APP'
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = UserManager()

    def __str__(self) -> str:
        return f'Email: {self.email} ' \
               f'Username: {self.username}'

    def get_absolute_url(self):
        return reverse('User',args=self.pk)
