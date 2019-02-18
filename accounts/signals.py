from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from .models import UserProfile
from django.dispatch import receiver


@receiver(post_save, sender=AbstractUser)
def create_user(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=AbstractUser)
def save_user(sender, instance, **kwargs):
    instance.UserProfile.save()
