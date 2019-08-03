from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from tinymce.models import HTMLField

from main.models import Language, Tag
from main.utils import unique_slug_generator
from .managers import CourseManager, TutorialManager


User = settings.AUTH_USER_MODEL

DIFFICULTY_CHOICES = (
    ('B', _('Débutant')),
    ('I', _('Intermédiaire')),
    ('E', _('Expert'))
)


class Course(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_("auteur"), related_name='courses')
    title = models.CharField(max_length=150, verbose_name=_("titre du cours"))
    slug = models.SlugField(verbose_name=_(
        "URL d'accès"), blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to='course_thumbnail/', verbose_name=_("vignette/vidéo d'introduction"))
    languages = models.ManyToManyField(
        Language, verbose_name=_("langages utilisés"))
    tags = models.ManyToManyField(
        Tag, verbose_name=_("catégories"), blank=True)
    difficulty = models.CharField(
        max_length=1, choices=DIFFICULTY_CHOICES, verbose_name=_("difficulté"))
    content_introduction = HTMLField(
        verbose_name=_("contenu d'introduction"))
    pdf = models.FileField(upload_to="pdf_course/",
                           verbose_name=_("version PDF du cours"), blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    published_date = models.DateField(
        verbose_name=_("date de publication"))
    published = models.BooleanField(
        default=False, verbose_name=_("formation publiée"))
    email_send = models.BooleanField(
        default=False, verbose_name=_("email envoyé"))
    old_price = models.DecimalField(default=0, verbose_name=_(
        "prix (ou ancien prix si nouveau)"), decimal_places=2, max_digits=6)
    new_price = models.DecimalField(verbose_name=_(
        "nouveau prix"), null=True, blank=True, decimal_places=2, max_digits=6)
    students = models.ManyToManyField(User, verbose_name=_(
        "étudiants enrollés"), blank=True)

    objects = CourseManager()

    class Meta:
        ordering = ['-published_date', 'title']
        verbose_name = _("cours")
        verbose_name_plural = _("cours")

    def __str__(self):
        return f"{self.id} - {self.title} -> {self.author.username}"

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
        return reverse('courses:detail', kwargs={'slug': self.slug})

    def get_absolute_uri(self, request):
        return f"{settings.PROTOCOL}://{get_current_site(request)}{self.get_absolute_url()}"

    def get_remove_course_from_cart_url(self):
        return reverse('main:billing:remove-course', kwargs={'course_slug': self.slug})

    def get_student_percentage_finished(self, student):
        all_tutorials = self.get_tutorials()
        all_tutorials_count = all_tutorials.count()
        all_tutorials_student_and_course = student.tutorial_finished.filter(
            tutorials__in=all_tutorials)
        all_tutorials_student_and_course_count = all_tutorials_student_and_course.count()
        try:
            return int(round(all_tutorials_student_and_course_count / all_tutorials_count))
        except:
            raise ImproperlyConfigured(
                _("Aucun tutoriel n'est relié au cours ! Veuillez en relié au moins un pour obtenir un pourcentage"))
        return 0

    def get_all_experience(self):
        exp = 0
        qs = self.get_tutorials()
        for tut in qs:
            exp += tut.experience
        return exp

    def get_all_downloadable_resources(self):
        count = 0
        for tut in self.get_tutorials():
            if tut.resources.is_exists():
                count += 1
        return count

    def get_percentage_discount(self):
        try:
            discount = self.new_price / self.old_price
        except:
            discount = 1
        return int((1 - discount) * 100)

    def get_tutorials(self):
        return self.tutorial.all()


def submission_course_delete(sender, instance, **kwargs):
    if instance.thumbnail != None:
        instance.thumbnail.delete(save=False)


post_delete.connect(submission_course_delete, sender=Course)


def pre_save_course_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_course_receiver, sender=Course)


class Tutorial(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name=_("cours rattaché"), related_name='tutorial')
    slug = models.SlugField(verbose_name=_(
        "URL d'accès"), blank=True, null=True)
    title = models.CharField(
        max_length=100, verbose_name=_("titre du tutoriel"))
    content = HTMLField(verbose_name=_("contenu du tutoriel"))
    resources = models.FileField(verbose_name=_(
        "ressources à déposer"), upload_to='resources/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['zip', 'rar', 'tar.gz', 'tar'])])
    experience = models.PositiveSmallIntegerField(
        verbose_name=_("points d'expérience fournis"))
    published_date = models.DateTimeField(
        verbose_name=_("date de publication"), null=True)
    views = models.BigIntegerField(verbose_name=_(
        "nombre de vues"), blank=True, default=0)

    class Meta:
        ordering = ['-views', 'title', 'experience']
        verbose_name = _("tutoriel")
        verbose_name_plural = _("tutoriels")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:tutorial-detail', kwargs={'course_slug': self.course.slug, 'tutorial_slug': self.slug})

    def get_favorite_url(self):
        return reverse('courses:tutorial-favorite', kwargs={'course_slug': self.course.slug, 'tutorial_slug': self.slug})


def pre_save_tutorial_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_tutorial_receiver, sender=Tutorial)
