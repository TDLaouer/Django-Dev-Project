from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
import django.utils.timezone
# Create your models here.

class UserProfile(AbstractUser):
    description = models.CharField(max_length=1023, default='')
    city = models.CharField(max_length=50, default='')
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, default=django.utils.timezone.now)
    country = models.CharField(max_length=50, default='')
    gender = models.CharField(max_length=2, default='')
    profession = models.CharField(max_length=50, default='')
    avatar = models.ImageField(default='default.jpg', upload_to='avatars')

    def __str__(self):
        return self.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile=UserProfile.objects.create(user=kwargs['instance'])
