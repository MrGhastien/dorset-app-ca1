import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


# Fields inside these classes tells Django how the database should be organised
# E.g. each User has a unique nickname, a full name and a register date.

class UserManager(BaseUserManager):
    def newUser(self, nickname, name, password=None, email=None, registerDate=timezone.now(), **extraFields):
        nickname = str.lower(nickname)

        user = self.model(nickname=nickname, email=email, name=name, registerDate=registerDate, **extraFields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, nickname, name, password=None, email=None, registerDate=timezone.now(), **extraFields):
        extraFields.setdefault("is_superuser", False)
        extraFields.setdefault("isAdmin", False)
        return self.newUser(nickname, name, password, email, registerDate, **extraFields)

    def create_superuser(self, nickname, name, password=None, email=None, registerDate=timezone.now(), **extraFields):
        extraFields.setdefault("is_superuser", True)
        extraFields.setdefault("isAdmin", True)

        if extraFields.get("is_superuser") is not True:
            raise ValueError("A superuser must have \'is_superuser\' set to true.")
        if extraFields.get("isAdmin") is not True:
            raise ValueError("A superuser must have \'isAdmin\' set to true.")

        return self.newUser(nickname, name, password, email, registerDate, **extraFields)


class User(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField("email address", blank=True)
    registerDate = models.DateTimeField('Registration date', default=timezone.now)

    isAdmin = models.BooleanField("is admin", default=False)

    objects = UserManager()

    USERNAME_FIELD = 'nickname'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return "@" + self.nickname

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return "@" + self.nickname

    @property
    def is_staff(self):
        """Is this user a member of staff ?"""
        return self.isAdmin


class SSHKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.TextField(max_length=500, null=False)
    title = models.CharField(max_length=200, null=False)
    addDate = models.DateTimeField('date added')
    permissions = models.PositiveSmallIntegerField()

    # All permissions are stored in a single integer
    # Each bit of the integer represents a permission. A bit set to one represents 'true' / 'yes'.
    # bit 0 -> Read
    # bit 1 -> Write

    def __str__(self) -> str:
        return self.title

    def isRecent(self) -> bool:
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.addDate <= now
