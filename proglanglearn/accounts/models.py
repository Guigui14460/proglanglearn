from itertools import chain

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField
from tinymce.models import HTMLField

from articles.models import Article
from courses.models import Course, Tutorial
from forum.models import Subject
from main.models import Language, Tag
from .managers import ProfileManager
from .utils import get_user_type


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
    strike = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("signalement"))
    email_confirmed = models.BooleanField(
        default=False, verbose_name=_("addresse e-mail confirmée"))
    email_notification = models.BooleanField(
        default=True, verbose_name=_("notification par email"))
    # Advanced options
    profile_reported = models.BooleanField(default=False)
    level = models.PositiveSmallIntegerField(
        default=1, verbose_name=_("niveau"))
    level_experience = models.PositiveIntegerField(
        default=0, verbose_name=_("expérience acquise"))
    favorite_articles = models.ManyToManyField(Article,
                                               verbose_name=_("articles favoris"), blank=True, related_name='article_favorite')
    favorite_subjects = models.ManyToManyField(Subject, verbose_name=_(
        "sujets marqués comme favoris"), blank=True)
    tutorial_finished = models.ManyToManyField(Tutorial, verbose_name=_(
        "tutoriels marqués comme terminé"), blank=True, related_name='tutorial_finished')
    favorite_tutorials = models.ManyToManyField(Tutorial, verbose_name=_(
        "tutoriels favoris"), blank=True, related_name='tutorial_favorite')
    # Developer options
    github_username = models.CharField(max_length=100,
                                       blank=True, null=True, verbose_name=_("nom d'utilisateur Github"))
    links = models.TextField(blank=True, null=True, default=";;;;;",
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

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'user_id': self.user.id})

    def get_user_profile_type(self):
        return get_user_type(self.level)

    @property
    def get_last_experience_or_education(self):
        all_ = list(chain(self.educations.all(), self.experiences.all()))
        all_.sort(key=lambda x: x.entry_date)
        try:
            try:
                return f"{all_[0].degree} - {all_[0].school}"
            except:
                return f"{all_[0].employment} - {all_[0].entreprise}"
        except IndexError:
            return _("Aucune école ou expérience renseignée")


def submission_user_delete(sender, instance, **kwargs):
    from analytics.models import UserExperienceJournal
    if instance.image.url != '/media/user_pictures/default.png':
        instance.image.delete(save=False)
    qs = UserExperienceJournal.objects.filter(user=instance.user)
    if qs.exists():
        for q in qs:
            q.delete()


def create_user_profile(sender, instance, created, **kwargs):
    from analytics.models import UserExperienceJournal
    if kwargs.get('created', True) and not kwargs.get('raw', False):
        Profile.objects.get_or_create(user=instance)
    if created:
        UserExperienceJournal.objects.create(
            user=instance,
            experience=instance.profile.level_experience
        )


post_delete.connect(submission_user_delete, sender=Profile)
post_save.connect(create_user_profile, sender=User)


class Education(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='educations', verbose_name=_("profile associé"))
    school = models.CharField(max_length=50, verbose_name=_("nom de l'école"))
    degree = models.CharField(max_length=50, verbose_name=_("diplôme obtenu"))
    entry_date = models.DateField(verbose_name=_("date d'entrée dans l'école"))
    exit_date = models.DateField(verbose_name=_(
        "date de sortie de l'école"), null=True, blank=True)

    class Meta:
        ordering = ['entry_date']
        verbose_name = _("éducation")
        verbose_name_plural = _("éducations")

    def __str__(self):
        return f"{self.profile.user.username} - {self.school}"


class Experience(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='experiences', verbose_name=_("profile associé"))
    entreprise = models.CharField(
        max_length=50, verbose_name=_("nom de l'entreprise"))
    employment = models.CharField(
        max_length=100, verbose_name=_("type de l'emploi"))
    description = HTMLField(verbose_name=_("description de l'emploi"))
    entry_date = models.DateField(
        verbose_name=_("date d'arrivée dans l'entreprise"))
    exit_date = models.DateField(verbose_name=_(
        "date de sortie de l'entreprise"), null=True, blank=True)

    class Meta:
        ordering = ['entry_date']
        verbose_name = _("expérience")
        verbose_name_plural = _("expériences")

    def __str__(self):
        return f"{self.profile.user.username} - {self.entreprise}"


class ProfileReport(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='reports', verbose_name=_("profil reporté"))
    timestamp = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(verbose_name=_("vérifié"), default=False)
    to_strike = models.BooleanField(default=False, verbose_name=_("à striker"))
    striked = models.BooleanField(verbose_name=_("striké"), default=False)

    class Meta:
        verbose_name = _("signalement de profil")
        verbose_name_plural = _("signalements de profil")

    def __str__(self):
        return f"{self.profile.user.username}"
