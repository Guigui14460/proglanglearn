from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
# from django.core.exceptions import ValidationError
# from django.core.validators import RegexValidator, FileExtensionValidator, MinLengthValidator, MaxLengthValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .fields import StringListField


class User(AbstractUser):
    REQUIRED_FIELDS = ['email']


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            verbose_name=_("Nom du tag"))

    class Meta:
        verbose_name = _("Tag")

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            verbose_name=_("Nom du langage de programmation"))

    class Meta:
        verbose_name = _("Langage")

    def __str__(self):
        return self.name


class ProfileQuerySet(models.QuerySet):
    def dev_profile_shown(self):
        return self.filter(is_dev=True)

    def student_profile_shown(self):
        return self.filter(is_student=True)


class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def full_profile_shown(self):
        return (self.get_queryset().dev_profile_shown() | self.get_queryset().student_profile_shown()).distinct()


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("Utilisateur associé"))
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
    languages_learnt = models.ManyToManyField(Language, verbose_name=_(
        "Compétences (langages ou framework)"), blank=True)
    strike = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("Signalement"))
    email_confirmed = models.BooleanField(
        default=False, verbose_name=_("Addresse e-mail confirmée"))
    # Advanced options
    level = models.PositiveSmallIntegerField(
        default=1, verbose_name=_("Niveau"))
    level_experience = models.PositiveIntegerField(
        default=0, verbose_name=_("Expérience acquise"))
    favorite_articles = StringListField(
        verbose_name=_("Articles favoris"), default='', null=True, blank=True)
    favorite_subjects = StringListField(verbose_name=_(
        "Sujets marqués comme favoris"), default='', null=True, blank=True)
    tutorial_finished = StringListField(verbose_name=_(
        "Tutoriels marqués comme terminé"), default='', blank=True, null=True)
    # Developer options
    github_username = models.CharField(max_length=100,
                                       blank=True, null=True, verbose_name=_("Nom d'utilisateur/Email Github"))
    links = models.TextField(blank=True, null=True)

    objects = ProfileManager()

    class Meta:
        ordering = ['user', 'level']
        verbose_name = _("Profil")

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        try:
            profile = Profile.objects.get(user__id=self.id)
            if profile.image != self.image and profile.image.url != '/media/user_pictures/default.png':
                profile.image.delete()
            if profile.strike >= 3:
                print("Banni")
                # TODO : Banir la personne lorsqu'il a 3 strike
        except:
            pass
        super(Profile, self).save(*args, **kwargs)


@receiver(post_delete, sender=Profile)
def submission_user_delete(sender, instance, **kwargs):
    if instance.image.url != '/media/user_pictures/default.png':
        instance.image.delete(save=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if kwargs.get('created', True) and not kwargs.get('raw', False):
        Profile.objects.get_or_create(user=instance)


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    school = models.CharField(max_length=50, verbose_name=_("Nom de l'école"))
    degree = models.CharField(max_length=50, verbose_name=_("Diplôme"))
    entry_date = models.DateField(verbose_name=_("Date d'entrée"))
    exit_date = models.DateField(verbose_name=_(
        "Date de sortie"))

    class Meta:
        verbose_name = _("Éducation")

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

    class Meta:
        verbose_name = _("Expérience")

    def __str__(self):
        return f"{self.profile.user.username} - {self.entreprise}"
