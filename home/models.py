
from django.db import models
from accounts.models import UserProfile
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50, default='')
    text = models.CharField(max_length=65535)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.CharField(max_length=65535)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
