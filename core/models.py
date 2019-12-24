from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

#User = get_user_model()


class User(AbstractUser):
    repo_count = models.IntegerField(blank=True, null=True)


class Repo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deep_link = models.CharField(max_length=100)
    relative_dir = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    creation_date = models.DateField(default=date.today)
    is_test = models.BooleanField(default=False)


class Doc(models.Model):
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    deep_link = models.CharField(max_length=100)
    meta_data = models.CharField(max_length=2048)
    body = models.CharField(max_length=2048)


class Note(models.Model):
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    path = models.CharField(max_length=100)
    format = models.CharField(max_length=100)
