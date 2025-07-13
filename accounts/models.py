from django.db import models
from django.contrib.auth.models import AbstractUser

# clase personalizada y extendida de user
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username