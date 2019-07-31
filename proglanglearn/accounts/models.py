from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

from articles.models import Article
from courses.models import Course, Tutorial
from main.models import Language, Tag
from .fields import StringListField
from .managers import ProfileManager


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("utilisateur associé"), related_name='profile')
    is_dev = models.BooleanField(
        default=False, verbose_name=_("est un développeur"))
    is_student = models.BooleanField(
        default=False, verbose_name=_("est un étudiant en informatique"))
    is_teacher = models.BooleanField(
        default=False, verbose_name=_("est un formateur"))
    image = models.ImageField(upload_to='user_pictures/',
                              default='user_pictures/default.png', verbose_name=_("image de profil"), validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])])
    country = CountryField(verbose_name=_('pays'))
    biography = models.TextField(max_length=1500,
                                 blank=True, null=True, verbose_name=_("biographie"))
    languages_learnt = models.ManyToManyField(Language, verbose_name=_(
        "langages maîtrisés"), blank=True)
    tag_learnt = models.ManyToManyField(Tag, verbose_name=_(
        "compétences apprises"), blank=True)
    strike = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("signalement"))
    email_confirmed = models.BooleanField(
        default=False, verbose_name=_("addresse e-mail confirmée"))
    # Advanced options
    level = models.PositiveSmallIntegerField(
        default=1, verbose_name=_("niveau"))
    level_experience = models.PositiveIntegerField(
        default=0, verbose_name=_("expérience acquise"))
    favorite_articles = models.ManyToManyField(Article,
                                               verbose_name=_("articles favoris"), blank=True, related_name='article_favorite')
    favorite_subjects = StringListField(verbose_name=_(
        "sujets marqués comme favoris"), default='', null=True, blank=True)
    tutorial_finished = models.ManyToManyField(Tutorial, verbose_name=_(
        "tutoriels marqués comme terminé"), blank=True, related_name='tutorial_finished')
    favorite_tutorials = models.ManyToManyField(Tutorial, verbose_name=_(
        "tutoriels favoris"), blank=True, related_name='tutorial_favorite')
    # Developer options
    github_username = models.CharField(max_length=100,
                                       blank=True, null=True, verbose_name=_("nom d'utilisateur/email Github"))
    links = models.TextField(blank=True, null=True,
                             verbose_name=_("liens vers les médias sociaux"))

    objects = ProfileManager()

    class Meta:
        ordering = ['-level', '-level_experience']
        verbose_name = _("profil")

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        try:
            profile = Profile.objects.get(user__id=self.id)
            if profile.image != self.image and profile.image.url != '/media/user_pictures/default.png':
                profile.image.delete()
        except:
            pass
        super(Profile, self).save(*args, **kwargs)


def submission_user_delete(sender, instance, **kwargs):
    if instance.image.url != '/media/user_pictures/default.png':
        instance.image.delete(save=False)


def create_user_profile(sender, instance, created, **kwargs):
    if kwargs.get('created', True) and not kwargs.get('raw', False):
        Profile.objects.get_or_create(user=instance)


post_delete.connect(submission_user_delete, sender=Profile)
post_save.connect(create_user_profile, sender=User)


class Education(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name=_("profile associé"))
    school = models.CharField(max_length=50, verbose_name=_("nom de l'école"))
    degree = models.CharField(max_length=50, verbose_name=_("diplôme"))
    entry_date = models.DateField(verbose_name=_("date d'entrée"))
    exit_date = models.DateField(verbose_name=_("date de sortie"))

    class Meta:
        verbose_name = _("éducation")

    def __str__(self):
        return f"{self.profile.user.username} - {self.school}"


class Experience(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name=_("profile associé"))
    entreprise = models.CharField(
        max_length=50, verbose_name=_("nom de l'entreprise"))
    employment = models.CharField(
        max_length=250, verbose_name=_("type d'emploi"))
    entry_date = models.DateField(verbose_name=_("date d'entrée"))
    exit_date = models.DateField(verbose_name=_(
        "date de sortie"))

    class Meta:
        verbose_name = _("expérience")

    def __str__(self):
        return f"{self.profile.user.username} - {self.entreprise}"
