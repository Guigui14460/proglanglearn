from django.core.exceptions import ImproperlyConfigured, MultipleObjectsReturned, ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy

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
        except ObjectDoesNotExist:
            sitting = self.new_sitting(user, quiz)
        except MultipleObjectsReturned:
            sitting = self.filter(user=user, quiz=quiz, complete=False)[0]
        return sitting
