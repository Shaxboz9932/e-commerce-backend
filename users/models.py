from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **kwargs):
        if username is None:
            raise TypeError("User da foydalanuvchi nomi bo'lishi kerak")
        if email is None:
            raise TypeError("User da email bo'lishi kerak")
        if password is None:
            raise TypeError("User da parol bo'lishi kerak")

        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        if password is None:
            raise TypeError("SuperUser da parol bo'lishi kerak")

        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):

    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)

    username = models.CharField(max_length=200, db_index=True, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=200)

    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return f"{self.name}"

    @property
    def name(self):
        return f"{self.last_name} {self.first_name}"


