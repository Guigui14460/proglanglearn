from django.contrib.auth.models import User
from django.core.validators import RegexValidator, FileExtensionValidator, MinLengthValidator, MaxLengthValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("Utilisateur associé"), unique=True)
    is_dev = models.BooleanField(
        default=False, verbose_name=_("Est un développeur"))
    is_teacher = models.BooleanField(
        default=False, verbose_name=_("Est un formateur"))
    image = models.ImageField(upload_to='user_pictures/',
                              default='user_pictures/default.png', verbose_name=_("Image de profil"))
    country = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        try:
            profile = Profile.objects.get(user__id=self.id)
            if profile.image != self.image:
                profile.image.delete()
        except:
            pass
        super(Profile, self).save(*args, **kwargs)


@receiver(post_delete, sender=Profile)
def submission_user_delete(sender, instance, **kwargs):
    instance.image.delete(save=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if kwargs.get('created', True) and not kwargs.get('raw', False):
        Profile.objects.create(user=instance)
