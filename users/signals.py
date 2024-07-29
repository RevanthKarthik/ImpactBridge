from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import ProfilePersonal,kyc,Userdefine,NGOdetail

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfilePersonal.objects.create(user=instance)
        kyc.objects.create(user=instance)
        Userdefine.objects.create(user=instance)
        NGOdetail.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profilepersonal.save()
    instance.userdefine.save()
    instance.ngodetail.save()
    instance.kyc.save()
