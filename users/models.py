from django.db import models

# Create your models here.

class User(models.Model):

    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username

