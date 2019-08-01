from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from articles.models import Article
from courses.models import Course, Tutorial


class ArticleSitemap(Sitemap):
    def items(self):
        return Article.objects.get_published_articles()

    def lastmod(self, obj):
        return obj.last_modification


class CourseSitemap(Sitemap):
    def items(self):
        return Course.objects.get_published_courses()

    def lastmod(self, obj):
        return obj.published_date


class TutorialSitemap(Sitemap):
    def items(self):
        return Tutorial.objects.all()

    def lastmod(self, obj):
        return obj.published_date


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['main:index', 'main:about', 'main:contact', 'main:privacy', 'main:terms', 'main:search']

    def location(self, item):
        return reverse(item)
