from django.db import models
from django.conf import settings

#clase personalizada del tablero
class Board(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_boards', on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='boards', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name