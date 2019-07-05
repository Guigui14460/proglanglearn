from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from tinymce.models import HTMLField

from accounts.models import Language, Tag, Profile

User = get_user_model()

DIFFICULTY_CHOICES = (
    ('B', _('Débutant')),
    ('I', _('Intermédiaire')),
    ('E', _('Expert'))
)


class CourseQuerySet(models.QuerySet):
    def last_courses(self, number):
        return self.published_courses()[number:]

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
        User, on_delete=models.SET_NULL, null=True, verbose_name=_("Auteur"), related_name='course')
    title = models.CharField(max_length=150, verbose_name=_("Titre du cours"))
    thumbnail = models.ImageField(
        upload_to='course_thumbnail/', verbose_name=_("Vignette du cours"))
    languages = models.ManyToManyField(
        Language, verbose_name=_("Langages de programmation"))
    tags = models.ManyToManyField(
        Tag, verbose_name=_("Tags"), blank=True)
    difficulty = models.CharField(
        max_length=1, choices=DIFFICULTY_CHOICES, verbose_name=_("Difficulté du cours"))
    content_introduction = HTMLField(
        verbose_name=_("Contenu d'introduction au cours"))
    pdf = models.FileField(upload_to="pdf_course/",
                           verbose_name=_("Version PDF du cours"), blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    published_date = models.DateField(
        verbose_name=_("Date de publication"))
    old_price = models.DecimalField(default=0, verbose_name=_(
        "Prix (ou ancien prix si nouveau)"), decimal_places=2, max_digits=6)
    new_price = models.DecimalField(verbose_name=_(
        "Nouveau prix"), null=True, blank=True, decimal_places=2, max_digits=6)
    students = models.ManyToManyField(Profile, verbose_name=_(
        "Étudiants enrollés"), blank=True)

    objects = CourseManager()

    class Meta:
        ordering = ['-published_date', 'title']
        verbose_name = _("Cours")
        verbose_name_plural = _("Cours")

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
        return reverse('courses:detail', kwargs={'id': self.id})

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


@receiver(post_delete, sender=Course)
def submission_course_delete(sender, instance, **kwargs):
    if instance.thumbnail != None:
        instance.thumbnail.delete(save=False)


class Tutorial(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name=_("Cours rattaché"), related_name='tutorial')
    title = models.CharField(
        max_length=100, verbose_name=_("Title du tutoriel"))
    content = HTMLField(verbose_name=_("Contenu du tutoriel"))
    resources = models.FileField(verbose_name=_(
        "Ressources à déposer"), upload_to='resources/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['zip', 'rar', 'tar.gz'])])
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
        return self.title

    def get_absolute_url(self):
        return reverse('courses:tutorial-detail', kwargs={'course_id': self.course.id, 'tutorial_id': self.id})

    def get_favorite_url(self):
        return reverse('courses:tutorial-favorite', kwargs={'course_id': self.course.id, 'tutorial_id': self.id})


class TutorialCommentQuerySet(models.QuerySet):
    def all_parent_comments(self):
        return self.filter(parent=None).order_by('posted_date')

    def tutorial_parent_comments(self, tutorial):
        return self.filter(tutorial=tutorial, parent=None).order_by('posted_date')

    def children_comments(self, parent):
        return self.filter(parent=parent).order_by('posted_date')


class TutorialCommentManager(models.Manager):
    def get_queryset(self):
        return TutorialCommentQuerySet(self.model, using=self._db)

    def all_parent_comments(self):
        return self.get_queryset().all_parent_comments()

    def tutorial_parent_comments(self, tutorial):
        return self.get_queryset().tutorial_parent_comments(tutorial)


class TutorialComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)

    objects = TutorialCommentManager()

    class Meta:
        ordering = ['-posted_date']
        verbose_name = _("Commentaire de tutoriel")
        verbose_name_plural = _("Commentaires de tutoriel")

    def __str__(self):
        if self.parent is None:
            return f"Comment by {self.user} : {self.content[:20]}"
        else:
            return f"Reply by {self.user} : {self.content[:20]}"

    def children(self):
        return TutorialComment.objects.filter(parent=self).order_by('posted_date')
    
    @property
    def is_parent(self):
        if self.parent == None:
            return False
        return True
