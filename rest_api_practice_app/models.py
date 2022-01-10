from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=60)  # charfield for small amounts of text
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True, max_length=500)

    def __str__(self):
        return self.title

