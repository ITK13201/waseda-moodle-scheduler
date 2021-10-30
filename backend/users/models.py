# https://github.com/django/django/blob/master/django/contrib/auth/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    """Extended User Model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
