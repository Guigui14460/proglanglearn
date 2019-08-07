from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import DeleteView, DetailView, ListView, RedirectView, UpdateView, View

from main.forms import CommentModelForm
from main.mixins import NavbarSearchMixin
from main.models import Comment, Language, Tag
from main.signals import comment_signal
from .forms import ArticleModelForm, ArticleUpdateModelForm
from .mixins import ArticleObjectMixin, UserCanModifyArticle
from .models import Article


class ArticleListView(NavbarSearchMixin, ListView):
    queryset = Article.objects.get_published_articles()
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activate'] = 'article-list'
        context['last_articles'] = Article.objects.get_last_articles(3)
        context['tags_used'] = self.get_most_used_tags()
        return context

    def get_most_used_tags(self):
        languages = [lang for lang in Language.objects.all()
                     if lang.article.all().count() > 0]
        tags = [tag for tag in Tag.objects.all() if tag.article.all().count() > 0]
        items = languages + tags
        items.sort(key=lambda item: item.article.all().count(), reverse=True)
        return items[:5]


class ArticleCreateView(LoginRequiredMixin, NavbarSearchMixin, View):
    template_name = 'articles/article_create.html'
    success_message = _("Article ajouté avec succès")
    error_message = _(
        "Un problème est survenu ! Réessayez plus tard et si le problème persiste, contactez l'administration")

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ArticleModelForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = self.request.user
            article.last_modification = timezone.now()
            article.save()
            for language in form.cleaned_data['languages']:
                article.languages.add(language)
            for tag in form.cleaned_data['tags']:
                article.tags.add(tag)
            messages.success(request, self.success_message)
            return redirect('articles:detail', article_slug=article.slug)
        messages.error(request, self.error_message)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = {**kwargs}
        context['type'] = 'add'
        context['form'] = ArticleModelForm()
        context['activate'] = 'article-create'
        return context


class ArticleDetailView(ArticleObjectMixin, NavbarSearchMixin, DetailView):
    def get(self, request, *args, **kwargs):
        article = self.get_object()
        self.object = article
        article.views = F('views') + 1
        article.save()
        return super(ArticleDetailView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentModelForm(request.POST or None)
        if form.is_valid() and request.user.is_authenticated:
            content = form.cleaned_data['content']
            parent_id = request.POST.get('parent_id')
            instance = self.object
            if parent_id:
                instance = Comment.objects.get(id=parent_id)
            comment_signal.send(instance.__class__,
                                instance=instance, request=request)
        if request.is_ajax():
            context = self.get_context_data(**kwargs)
            context['form'] = form
            html = render_to_string(
                'main/comments.html', context, request=request)
            return JsonResponse({'html': html, 'comments_count': context['parent_comments'].count()})
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentModelForm()
        instance = self.get_object()
        c_type = ContentType.objects.get_for_model(instance)
        context['parent_comments'] = Comment.objects.filter(
            content_type=c_type, object_id=instance.id, reported=False).order_by('timestamp')
        context['article_in_favorite'] = self.article_in_favorite()
        context['last_articles'] = Article.objects.get_last_articles(3)
        context['tags_used'] = self.get_most_used_tags()
        return context

    def article_in_favorite(self):
        user = self.request.user
        tuto = self.object
        if not user.is_authenticated:
            return False
        liste_article = user.profile.favorite_articles.all()
        return tuto in liste_article

    def get_most_used_tags(self):
        languages = [lang for lang in Language.objects.all()
                     if lang.article.all().count() > 0]
        tags = [tag for tag in Tag.objects.all() if tag.article.all().count() > 0]
        items = languages + tags
        items.sort(key=lambda item: item.article.all().count(), reverse=True)
        return items[:5]


class ArticleUpdateView(LoginRequiredMixin, ArticleObjectMixin, UserCanModifyArticle, SuccessMessageMixin, NavbarSearchMixin, UpdateView):
    template_name = 'articles/article_create.html'
    form_class = ArticleUpdateModelForm
    success_message = _("Article modifié avec succès")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'modify'
        return context

    def get_success_url(self):
        slug = self.kwargs.get('article_slug')
        return reverse('articles:detail', kwargs={'article_slug': slug})


class ArticleDeleteView(LoginRequiredMixin, ArticleObjectMixin, SuccessMessageMixin, NavbarSearchMixin, DeleteView):
    success_message = _("Article supprimé avec succès")
    success_url = reverse_lazy('articles:list')


class ArticleFavoriteToggleRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Article, slug=kwargs.get('article_slug'))
        user = self.request.user
        if user.is_authenticated:
            if obj in user.profile.favorite_articles.all():
                user.profile.favorite_articles.remove(obj)
            else:
                user.profile.favorite_articles.add(obj)
        return obj.get_absolute_url()
