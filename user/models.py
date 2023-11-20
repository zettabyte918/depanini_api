from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from django.utils import timezone


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save()

        # generate token for new user
        Token.objects.create(user=user)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email, password=password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
        ("company", "Company"),
    )

    email = models.CharField(max_length=80)
    username = models.CharField(max_length=45, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username
    
class Employee(User):
    name = models.CharField(max_length=80)

    class Meta:
        verbose_name = "Employee"

    def save(self, *args, **kwargs):
        if not self.pk:  # If the object is being created for the first time
            self.role = "kap"
        super().save(*args, **kwargs)

class Employee(User):
    employee_count = models.CharField(max_length=80)

    class Meta:
        verbose_name = "Employee"

    def save(self, *args, **kwargs):
        if not self.pk:  # If the object is being created for the first time
            self.role = "kap"
        super().save(*args, **kwargs)