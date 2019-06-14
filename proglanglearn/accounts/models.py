from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, FileExtensionValidator, MinLengthValidator, MaxLengthValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from courses.models import Tag
from .fields import StringListField

User = get_user_model()


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
    biography = models.TextField(max_length=1500,
                                 blank=True, null=True, verbose_name=_("Biographie"))
    skills = models.ManyToManyField(Tag, verbose_name=_(
        "Compétences"), blank=True)
    strike = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("Signalement"))
    # Advanced options
    level = models.PositiveSmallIntegerField(
        default=1, verbose_name=_("Niveau"))
    level_experience = models.PositiveIntegerField(
        default=0, verbose_name=_("Expérience acquise"))
    favorite_articles = StringListField(
        verbose_name=_("Articles favoris"), default='', null=True, blank=True)
    favorite_subjects = StringListField(verbose_name=_(
        "Sujets marqués comme favoris"), default='', null=True, blank=True)
    # Developer options
    github_username = models.CharField(max_length=100,
                                       blank=True, null=True, verbose_name=_("Nom d'utilisateur/Email Github"))
    links = models.TextField(blank=True, null=True)

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


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    school = models.CharField(max_length=50, verbose_name=_("Nom de l'école"))
    degree = models.CharField(max_length=50, verbose_name=_("Diplôme"))
    entry_date = models.DateField(verbose_name=_("Date d'entrée"))
    exit_date = models.DateField(verbose_name=_(
        "Date de sortie"))

    def __str__(self):
        return f"{self.profile.user.username} - {self.school}"


class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    entreprise = models.CharField(
        max_length=50, verbose_name=_("Nom de l'entreprise"))
    employment = models.CharField(
        max_length=250, verbose_name=_("Type d'emploi"))
    entry_date = models.DateField(verbose_name=_("Date d'entrée"))
    exit_date = models.DateField(verbose_name=_(
        "Date de sortie"))

    def __str__(self):
        return f"{self.profile.user.username} - {self.entreprise}"
