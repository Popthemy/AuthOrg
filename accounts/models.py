from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomeBaseUserManager


# Create your models here.
class User(AbstractBaseUser):
    id = models.CharField(max_length=36, unique=True, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomeBaseUserManager()

    USERNAME_FIELD = 'email'  # email will be used in place of username to login
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


