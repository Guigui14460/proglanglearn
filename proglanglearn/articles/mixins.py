from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _

from .models import Article


class ArticleObjectMixin(object):
    model = Article

    def get_object(self):
        article_slug = self.kwargs.get('article_slug')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, slug=article_slug)
        return obj


class UserCanModifyArticle(UserPassesTestMixin):
    permission_denied_message = _(
        "Vous n'avez pas l'autorisation de modifier cet article")

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            article = self.get_object()
            if article is not None:
                messages.error(self.request, self.permission_denied_message)
                return redirect('articles:list')
            messages.info(self.request, _(
                "L'article auquel vous essayez d'accéder n'existe pas, ou plus, ou est actuellement inaccessible"))
            return Http404
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

    def test_func(self):
        user = self.request.user
        article = self.get_object()
        return user.is_staff or article.author == user
