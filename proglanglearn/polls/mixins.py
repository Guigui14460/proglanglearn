from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from courses.models import Course
from .models import Quiz


class UserCanAnswerQuiz(UserPassesTestMixin):
    permission_denied_message = _(
        "Vous n'avez pas accès à ce quiz. Veuillez vous enroller dans le cours")

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            quiz = self.get_object()
            if quiz is not None:
                course = quiz.course
                messages.error(self.request, self.permission_denied_message)
                return redirect('courses:detail', slug=course.slug)
            messages.info(self.request, _(
                "Le tutoriel ou le cours auquel vous essayez d'accéder n'existe pas ou plus ou est inaccessible"))
            return Http404
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

    def test_func(self):
        user = self.request.user
        quiz = self.get_object()
        if quiz is not None:
            course = quiz.course
            return user in course.students.all() or user == course.author or user.is_staff
        return False

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class QuizObjectMixin(object):
    model = Quiz

    def get_object(self):
        course_slug = self.kwargs.get('course_slug')
        course = None
        if course_slug is not None:
            course = get_object_or_404(Course, slug=course_slug)
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        if obj.course == course:
            return obj
        messages.warning(self.request, _("Le quiz que vous essayez d'accéder n'appartient pas ou plus au cours"))
        return Http404
