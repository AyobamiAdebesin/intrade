from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
  """ 
  Custom user model.
  This class extends the default user model provided by Django.
  """
  email = models.EmailField(unique=True)