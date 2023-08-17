from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from blog.models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print("Creating profile for user:", instance.username)
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print("Saving profile for user:", instance.username)
    instance.profile.save()
