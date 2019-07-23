import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from tinymce.models import HTMLField


User = get_user_model()


class Quiz(models.Model):
    course = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=30, verbose_name=_("Titre"))
    description = HTMLField(verbose_name=_(
        "Description"), blank=True, null=True)
    random_order = models.BooleanField(default=True, verbose_name=_(
        "Ordre aléatoire ?"), help_text=_("Afficher aléatoirement les questions ?"))
    single_attempt = models.BooleanField(
        default=False, verbose_name=_("Un seul essai"))

    class Meta:
        verbose_name = _("quiz")
        verbose_name_plural = _("quiz")

    def __str__(self):
        return f"{self.title} -> {self.course.title}"
    
    def get_absolute_url(self):
        return reverse('courses:quizzes:detail', args=(self.course.slug, self.id))

    def get_question(self):
        return self.questions.all()

    @property
    def get_max_score(self):
        return self.get_question().count()
    
    @property
    def get_total_experience(self):
        exp = 0
        for question in self.questions.all():
            exp += question.experience
        return exp

    def order_question(self):
        if self.random_order:
            return self.get_question().order_by('?')
        return self.get_question()


class Question(models.Model):
    quiz = models.ManyToManyField(
        Quiz, verbose_name=_("Quiz"), related_name='questions')
    question_text = HTMLField(
        max_length=1000, verbose_name=_("Question"))
    explanation = HTMLField(blank=True, null=True,
                            max_length=2000, verbose_name=_("Explication"))
    random_answer_display = models.BooleanField(default=True, verbose_name=_(
        "Ordre aléatoire ?"), help_text=_("Afficher les réponses dans le désordre ?"))
    experience = models.PositiveSmallIntegerField(verbose_name=_("Expérience"), default=20)

    def __str__(self):
        return mark_safe(self.question_text)

    def check_if_correct(self, guess):
        answer = Answer.objects.get(id=guess)
        return answer.correct

    def order_answer(self, queryset):
        if self.random_answer_display:
            return queryset.order_by('?')
        return queryset

    def get_answer(self):
        return self.order_answer(self.answers.all())


class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name=_(
        "Question"), on_delete=models.CASCADE, related_name='answers')
    content = HTMLField(max_length=450, verbose_name=_(
        "Contenu"), help_text=_("Entrez la réponse que vous voulez afficher"))
    correct = models.BooleanField(default=False, verbose_name=_(
        "Correct"), help_text=_("Est-ce la bonne réponse ?"))

    def __str__(self):
        return mark_safe(self.content)

    class Meta:
        verbose_name = _("réponse")


class SittingManager(models.Manager):
    def new_sitting(self, user, quiz):
        question_set = quiz.order_question()
        question_set = [item.id for item in question_set]
        if len(question_set) == 0:
            raise ImproperlyConfigured(
                'Aucune question n\'a été reliée au quiz. Configurez les questions correctement')
        questions = ",".join(map(str, question_set)) + ","
        new_sitting = self.create(user=user,
                                  quiz=quiz,
                                  question_order=questions,
                                  question_list=questions,
                                  incorrect_questions="",
                                  current_score=0,
                                  complete=False,
                                  user_answers='{}')
        return new_sitting

    def user_sitting(self, user, quiz):
        if quiz.single_attempt is True and self.filter(user=user, quiz=quiz, complete=True).exists():
            return False
        try:
            sitting = self.get(user=user, quiz=quiz, complete=False)
        except Sitting.DoesNotExist:
            sitting = self.new_sitting(user, quiz)
        except Sitting.MultipleObjectsReturned:
            sitting = self.filter(user=user, quiz=quiz, complete=False)[0]
        return sitting


class Sitting(models.Model):
    user = models.ForeignKey(User, verbose_name=_(
        "Utilisateur"), on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, verbose_name=_(
        "Quiz"), on_delete=models.CASCADE)
    question_order = models.CharField(max_length=1024, verbose_name=_(
        "Ordre des questions"), validators=[validate_comma_separated_integer_list])
    question_list = models.CharField(max_length=1024, verbose_name=_(
        "Liste des questions"), validators=[validate_comma_separated_integer_list])
    incorrect_questions = models.CharField(max_length=1024, blank=True, verbose_name=_(
        "Questions incorrectes"), validators=[validate_comma_separated_integer_list])
    current_score = models.IntegerField(verbose_name=_("Score actuel"))
    complete = models.BooleanField(
        default=False, verbose_name=_("Terminé"))
    user_answers = models.TextField(
        blank=True, default='{}', verbose_name=_("Réponses de l'utilisateur"))
    start = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Commencement"))
    end = models.DateTimeField(null=True, blank=True, verbose_name=_("Fin"))

    objects = SittingManager()

    class Meta:
        verbose_name = _("séance")

    def get_first_question(self):
        if not self.question_list:
            return False
        first, _ = self.question_list.split(',', 1)
        question_id = int(first)
        return Question.objects.filter(id=question_id)

    def remove_first_question(self):
        if not self.question_list:
            return
        _, others = self.question_list.split(',', 1)
        self.question_list = others
        self.save()

    def add_to_score(self, points):
        self.current_score += int(points)
        self.save()

    @property
    def get_current_score(self):
        return self.current_score

    def _question_ids(self):
        return [int(n) for n in self.question_order.split(',') if n]

    @property
    def get_percent_correct(self):
        dividend = float(self.current_score)
        divisor = len(self._question_ids())
        if divisor < 1:
            return 0
        if dividend > divisor:
            return 100
        correct = int(round((dividend / divisor) * 100))
        if correct >= 1:
            return correct
        else:
            return 0

    def mark_quiz_complete(self):
        self.complete = True
        self.end = timezone.now()
        self.save()

    def add_incorrect_question(self, question):
        if len(self.incorrect_questions) > 0:
            self.incorrect_questions += ','
        self.incorrect_questions += str(question.id) + ","
        self.save()

    @property
    def get_incorrect_questions(self):
        return [int(q) for q in self.incorrect_questions.split(',') if q]

    def remove_incorrect_question(self, question):
        current = self.get_incorrect_questions
        current.remove(question.id)
        self.incorrect_questions = ','.join(map(str, current))
        self.add_to_score(1)
        self.save()

    def add_user_answer(self, question, guess):
        current = json.loads(self.user_answers)
        current[question.id] = guess
        self.user_answers = json.dumps(current)
        self.save()

    def get_questions(self, with_answers=False):
        question_ids = self._question_ids()
        questions = sorted(self.quiz.question_set.filter(
            id__in=question_ids), key=lambda q: question_ids.index(q.id))
        if with_answers:
            user_answers = json.loads(self.user_answers)
            for question in questions:
                question.user_answer = user_answers[str(question.id)]
        return questions

    @property
    def questions_with_user_answers(self):
        return {
            q: q.user_answer for q in self.get_questions(with_answers=True)
        }

    @property
    def get_max_score(self):
        return len(self._question_ids())

    def progress(self):
        answered = len(json.loads(self.user_answers))
        total = self.get_max_score
        return answered, total
