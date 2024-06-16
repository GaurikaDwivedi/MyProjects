from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255, unique = True)
    password = models.CharField(max_length = 255)
    # django also creates a "username" field , it is required for abstract user. But we can override it by saying it's None.
    username = None
    # django usually logs in by username & password. But we want to login with email & password
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []