import datetime

from django.db import models
from django.utils import timezone


# Fields inside these classes tells Django how the database should be organised
# E.g. each User has an unique nickname, a full name and a register date.
class User(models.Model):
    nickname = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    registerDate = models.DateTimeField('Registration date', default=timezone.now)

    def __str__(self):
        return "@" + self.nickname


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
