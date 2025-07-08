
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def ensure_user_profile(sender, instance, created, **kwargs):
    """
    Make sure every User has exactly one Profile,
    and sync the email into it if set.
    """
    # this will fetch the existing profile or create it if missing
    profile, _ = Profile.objects.get_or_create(user=instance)

    # if the User has an email, and it differs from Profile.email, update it
    if instance.email and profile.email != instance.email:
        profile.email = instance.email
        profile.save()