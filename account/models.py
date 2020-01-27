from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone


# Create your models here.
class User(AbstractUser):
    balance = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0,
    )
    inviter_id = models.IntegerField(default=1)

    def __str__(self):
        return self.username


class InviteCode(models.Model):
    text = models.CharField(max_length=20,unique=True)
    times = models.IntegerField(default=1)
    days = models.IntegerField(default=30)
    create_at = models.DateTimeField(auto_now_add=True)

    user_id = models.IntegerField(default=1)

    def __str__(self):
        return self.text


class ResetCode(models.Model):
    email = models.CharField(max_length=256)
    code = models.CharField(max_length=5)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
