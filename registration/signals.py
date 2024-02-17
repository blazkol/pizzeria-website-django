from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import UserDetails

@receiver(post_save, sender=User)
def create_or_save_userdetails(sender, instance, created, **kwargs):
    if created:
        UserDetails.objects.create(user=instance)
    instance.userdetails.save()