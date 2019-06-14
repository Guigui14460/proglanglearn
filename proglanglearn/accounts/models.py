from django.contrib.auth.models import User
from django.core.validators import RegexValidator, FileExtensionValidator, MinLengthValidator, MaxLengthValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class StringListField(models.TextField):
    description = _(
        "Un champ pour enregistrer une liste en tant que chaîne de caractères")

    def get_db_prep_value(self, value, *args, **kwargs):
        if value is None:
            return None
        return ';'.join(value)

    def to_python(self, value):
        if value is None or isinstance(value, str):
            return []
        return value.split(';')

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    # def formfield(self, **kwargs):
    #     defaults = {'form_class': models.TextField}
    #     defaults.update(kwargs)
    #     return super(StringListField, self).formfield(**defaults)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("Utilisateur associé"), unique=True)
    is_dev = models.BooleanField(
        default=False, verbose_name=_("Est un développeur"))
    is_student = models.BooleanField(
        default=False, verbose_name=_("Est un étudiant en informatique"))
    is_teacher = models.BooleanField(
        default=False, verbose_name=_("Est un formateur"))
    image = models.ImageField(upload_to='user_pictures/',
                              default='user_pictures/default.png', verbose_name=_("Image de profil"))
    country = models.CharField(max_length=30)
    skills = StringListField(verbose_name=_(
        "Compétences"), default='', blank=True, null=True)
    strike = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("Signalement"))
    # Advanced options
    level = models.PositiveSmallIntegerField(
        default=1, verbose_name=_("Niveau"))
    experience = models.PositiveIntegerField(
        default=0, verbose_name=_("Expérience acquise"))
    favorite_articles = StringListField(
        verbose_name=_("Articles favoris"), default='', null=True, blank=True)
    favorite_subjects = StringListField(verbose_name=_(
        "Sujets marqués comme favoris"), default='', null=True, blank=True)
    # Developer options

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        try:
            profile = Profile.objects.get(user__id=self.id)
            if profile.image != self.image:
                profile.image.delete()
            if profile.strike >= 3:
                print("Banni")
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
