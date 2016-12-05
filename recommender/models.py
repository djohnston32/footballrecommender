from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Database model for storing user information.
# Username/password are in Django's user model by default
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pScore = models.IntegerField(default=10)
    pTime = models.IntegerField(default=10)
    pYardLine = models.IntegerField(default=5)
    pRank = models.IntegerField(default=5)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
