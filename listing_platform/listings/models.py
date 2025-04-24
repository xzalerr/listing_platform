from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User

# Create your models here.

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = AutoSlugField(populate_from='title', unique=True)
    date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(default='database-error.jpg', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title
