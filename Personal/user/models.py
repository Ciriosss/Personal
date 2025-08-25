from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class Profile(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)