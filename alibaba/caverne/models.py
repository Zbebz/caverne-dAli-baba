from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
# Create your models here.

class User(AbstractUser):
    username = models.CharField(blank=False, null=False)
    ecole = models.CharField(blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    pass

