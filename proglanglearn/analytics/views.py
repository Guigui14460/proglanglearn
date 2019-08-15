from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse
from django.utils.translation import ngettext, gettext as _
from django.views.generic import TemplateView

from accounts.models import Profile
from accounts.utils import get_exp_limit, check_level
from articles.models import Article
from billing.models import Order
from courses.models import Course
from forum.models import Subject
from main.mixins import NavbarSearchMixin
from main.models import CommentReport
from .utils import get_recent_user_exp_journal


class DashboardView(LoginRequiredMixin, NavbarSearchMixin, TemplateView):
    template_name = 'analytics/dashboard.html'

    def get(self, request, *args, **kwargs):
        check_level(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'dashboard'
        context['activate'] = 'dashboard'
        level = self.request.user.profile.level
        user_exp = self.request.user.profile.level_experience
        context['level'] = level
        exp_limit_level = get_exp_limit(level)
        context['level_experience'] = f"{user_exp}/{exp_limit_level}"
        context['level_percent'] = f"{round(user_exp / exp_limit_level * 100)}"
        context['label'], context['data'] = get_recent_user_exp_journal(
            self.request.user)
        context['strike'] = ngettext(
            'Vous avez %(count)d signalement. Cliquez <a href="%(url)s" title="Les signalements">ici</a> pour en savoir plus sur nos conditions liés aux signalements.',
            'Vous avez %(count)d signalements. Cliquez <a href="%(url)s" title="Les signalements">ici</a> pour en savoir plus sur nos conditions liés aux signalements.',
            self.request.user.profile.strike) % {'count': self.request.user.profile.strike, 'url': reverse('main:terms')}
        return context


class RankingView(LoginRequiredMixin, NavbarSearchMixin, TemplateView):
    template_name = 'analytics/ranking.html'

    def get(self, request, *args, **kwargs):
        check_level(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'ranking'
        context['activate'] = 'ranking'
        context['all_user'] = Profile.objects.all()
        return context


class FavoriteTutorialView(LoginRequiredMixin, NavbarSearchMixin, TemplateView):
    template_name = 'analytics/my_favorite.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'my_favorite_tutorials'
        context['activate'] = 'my_favorite_tutorials'
        context['data'] = self.course_tutorial()
        return context

    def course_tutorial(self):
        data = {}
        for obj in self.request.user.profile.favorite_tutorials.all():
            if obj.course.title in data:
                data[obj.course.title].append(obj)
            else:
                data[obj.course.title] = [obj]
        return data


class FavoriteArticleView(LoginRequiredMixin, NavbarSearchMixin, TemplateView):
    template_name = 'analytics/my_favorite.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'my_favorite_articles'
        context['activate'] = 'my_favorite_articles'
        context['data'] = self.request.user.profile.favorite_articles.all()
        return context


class FavoriteSubjectView(LoginRequiredMixin, NavbarSearchMixin, TemplateView):
    template_name = 'analytics/my_favorite.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'my_favorite_subjects'
        context['activate'] = 'my_favorite_subjects'
        context['data'] = self.request.user.profile.favorite_subjects.all()
        return context


class OrderListView(LoginRequiredMixin, NavbarSearchMixin, TemplateView):
    template_name = 'analytics/my_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'my_orders'
        context['activate'] = 'my_orders'
        data = Order.objects.filter(user=self.request.user, ordered=True)
        context['data'] = data if data.exists() else None
        return context


class MyCommentReportListView(LoginRequiredMixin, NavbarSearchMixin, TemplateView):
    template_name = 'analytics/my_comment_reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'my_comment_report'
        context['activate'] = 'my_comment_report'
        data = CommentReport.objects.filter(alerter=self.request.user)
        context['data'] = data if data.exists() else None
        return context


class MyCoursesListView(LoginRequiredMixin, NavbarSearchMixin, TemplateView):
    template_name = 'analytics/my_.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'my_courses'
        context['activate'] = 'my_courses'
        data = [course for course in Course.objects.all(
        ) if course.user_is_student_of_course(self.request.user)]
        context['data'] = data if data != [] else None
        context['data2'] = [course.get_student_percentage_finished(
            self.request.user) for course in data]
        return context


class MyArticlesListView(LoginRequiredMixin, NavbarSearchMixin, TemplateView):
    template_name = 'analytics/my_.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'my_articles'
        context['activate'] = 'my_articles'
        data = Article.objects.filter(author=self.request.user)
        context['data'] = data if data.exists() else None
        return context


class MySubjectsListView(LoginRequiredMixin, NavbarSearchMixin, TemplateView):
    template_name = 'analytics/my_.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'my_subjects'
        context['activate'] = 'my_subjects'
        data = Subject.objects.filter(user=self.request.user)
        context['data'] = data if data.exists() else None
        return context
