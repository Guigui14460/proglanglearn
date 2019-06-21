from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from accounts.models import Language, Tag

User = get_user_model()

DIFFICULTY_CHOICES = (
    ('B', _('Débutant')),
    ('I', _('Intermédiaire')),
    ('E', _('Expert'))
)


class CourseQuerySet(models.QuerySet):
    def last_courses(self, number):
        return self.published_courses()[number:]

    def student_enrolled(self):
        pass

    def published_courses(self):
        return self.filter(published_date__lte=timezone.now())


class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def get_last_courses(self, number):
        return self.get_queryset().last_courses(number)

    def get_published_courses(self):
        return self.get_queryset().published_courses()


class Course(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_("Auteur"), related_name='author')
    title = models.CharField(max_length=150, verbose_name=_("Titre du cours"))
    thumbnail = models.ImageField(
        upload_to='course_thumbnail/', verbose_name=_("Vignette du cours"))
    languages = models.ManyToManyField(
        Language, verbose_name=_("Langages de programmation"))
    tags = models.ManyToManyField(
        Tag, verbose_name=_("Tags"), blank=True)
    difficulty = models.CharField(
        max_length=1, choices=DIFFICULTY_CHOICES, verbose_name=_("Difficulté du cours"))
    content_introduction = RichTextUploadingField(
        verbose_name=_("Contenu d'introduction au cours"), null=True)
    pdf = models.FileField(upload_to="pdf_course/",
                           verbose_name=_("Version PDF du cours"), blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    published_date = models.DateField(
        verbose_name=_("Date de publication"))
    old_price = models.FloatField(default=0, verbose_name=_(
        "Prix (ou ancien prix si nouveau)"))
    new_price = models.FloatField(verbose_name=_(
        "Nouveau prix"), null=True, blank=True)

    objects = CourseManager()

    class Meta:
        ordering = ['-published_date', 'title']
        verbose_name = _("Cours")
        verbose_name_plural = _("Cours")

    def __str__(self):
        return f"{self.title} -- {self.author.username}"

    def save(self, *args, **kwargs):
        try:
            course = Course.objects.get(
                title=self.title, published_date=self.published_date)
            if course.thumbnail != self.thumbnail and course.thumbnail != None:
                course.thumbnail.delete(save=False)
        except:
            pass
        super(Course, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'id': self.id})

    def get_all_experience(self):
        exp = 0
        qs = self.get_sections()
        for section in qs:
            qs2 = Tutorial.objects.filter(section__id=section.id)
            for tut in qs2:
                exp += tut.experience
        return exp

    def get_all_downloadable_resources(self):
        tuts = self.get_tutorials()
        num = 0
        for sec, tut in tuts:
            if tut.resources is not None:
                num += 1
        return num

    def get_percentage_discount(self):
        try:
            discount = self.new_price / self.old_price
        except:
            discount = 1
        return int((1 - discount) * 100)

    def get_sections(self):
        return Section.objects.filter(course__id=self.id).order_by('id')

    def get_tutorials(self):
        tutorials = []
        for sec in self.get_sections():
            tutorials.append(
                (sec, Tutorial.objects.filter(section__id=sec.id)))
        return tutorials


@receiver(post_delete, sender=Course)
def submission_course_delete(sender, instance, **kwargs):
    if instance.thumbnail != None:
        instance.thumbnail.delete(save=False)


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL,
                               null=True, verbose_name=_("Cours attaché"))
    title = models.CharField(
        max_length=100, verbose_name=_("Titre de la section"))
    short_description = RichTextField(
        max_length=450, verbose_name=_("Courte description de la section"), blank=True, null=True)

    class Meta:
        ordering = ['title']
        verbose_name = _("Section de cours")
        verbose_name_plural = _("Sections de cours")

    def __str__(self):
        return f"{self.title} -- {self.course.title}"


class Tutorial(models.Model):
    section = models.ForeignKey(
        Section, on_delete=models.SET_NULL, null=True, verbose_name=_("Section"))
    title = models.CharField(
        max_length=100, verbose_name=_("Title du tutoriel"))
    content = RichTextUploadingField(verbose_name=_("Contenu du tutoriel"),
                                     config_name='blog', external_plugin_resources=[
        ('youtube', '/static/ckeditor/youtube/', 'plugin.js'),
        ('mathjax', '/static/ckeditor/mathjax/', 'plugin.js')
    ])
    resources = models.FileField(verbose_name=_(
        "Ressources à déposer"), upload_to='resources/', null=True, blank=True)
    experience = models.PositiveSmallIntegerField(
        verbose_name=_("Points d'expérience fournis"))
    published_date = models.DateTimeField(
        verbose_name=_("Date de publication"), null=True)
    views = models.BigIntegerField(verbose_name=_(
        "Nombre de vues"), blank=True, default=0)

    class Meta:
        ordering = ['title', 'experience']
        verbose_name = _("Tutoriel")
        verbose_name_plural = _("Tutoriels")

    def __str__(self):
        return f"{self.title} -- {self.section.title}"
