from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	embedding = models.FileField(upload_to='embedding/', null=True)
