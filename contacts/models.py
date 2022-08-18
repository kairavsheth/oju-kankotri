from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    pass


class Sender(models.Model):
    side = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Contact(models.Model):
    side = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    phone = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
