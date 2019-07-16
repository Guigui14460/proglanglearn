from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from .models import Course, Tutorial


class UserCanViewTutorial(UserPassesTestMixin):
    permission_denied_message = _(
        "Vous n'avez pas accès à ce tutoriel. Veuillez vous enroller dans le cours")

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            tutorial = self.get_object()
            if tutorial is not None:
                course = tutorial.course
                messages.error(self.request, self.permission_denied_message)
                return redirect('courses:detail', slug=course.slug)
            messages.info(self.request, _(
                "Le tutoriel ou le cours auquel vous essayez d'accéder n'existe pas ou plus ou est inaccessible"))
            return Http404
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

    def test_func(self):
        user = self.request.user
        tutorial = self.get_object()
        if tutorial is not None:
            course = tutorial.course
            return user in course.students.all() or user == course.author or user.is_staff
        return False

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserCanAddCourse(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_staff or user.profile.is_teacher


class UserCanModifyCourse(UserPassesTestMixin):
    permission_denied_message = _(
        "Vous n'avez pas l'autorisation de modifier ce cours")

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            course = self.get_object()
            if course is not None:
                messages.error(self.request, self.permission_denied_message)
                return redirect('courses:list')
            messages.info(self.request, _(
                "Le cours auquel vous essayez d'accéder n'existe pas ou plus ou est inaccessible"))
            return Http404
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

    def test_func(self):
        user = self.request.user
        course = self.get_object()
        return user.is_staff or course.author == user


class CourseObjectMixin(object):
    model = Course

    def get_object(self):
        slug = self.kwargs.get('slug')
        obj = None
        if slug is not None:
            obj = get_object_or_404(self.model, slug=slug)
        return obj


class TutorialObjectMixin(object):
    model = Tutorial
    parent_model = Course

    def get_object(self):
        slug = self.kwargs.get('tutorial_slug')
        obj = None
        if slug is not None:
            obj = get_object_or_404(self.model, slug=slug)
        return obj

    def get_other_tutorial(self):
        slug = self.kwargs.get('course_slug')
        obj = None
        if slug is not None:
            obj = get_object_or_404(self.parent_model, slug=slug)
            return obj.get_tutorials()
        return []
