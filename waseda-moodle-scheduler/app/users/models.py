# https://github.com/django/django/blob/master/django/contrib/auth/models.py

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended User Model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
