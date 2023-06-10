from django.db.models.signals import post_save, post_delete
from .models import User, Profile


def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )


def update_user(sender, instance, created, **kwargs):
    if not created:
        profile = instance
        user = profile.user

        user.first_name = profile.name
        user.email = profile.email
        user.username = profile.username
        user.save()


def delete_user(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(create_profile, sender=User)
post_save.connect(update_user, sender=Profile)
post_delete.connect(delete_user, sender=Profile)
