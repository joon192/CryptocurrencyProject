from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as AbstractUserManager

# Create your models here.
class UserManager(AbstractUserManager):
    pass

class User(AbstractUser):
    objects = UserManager()
