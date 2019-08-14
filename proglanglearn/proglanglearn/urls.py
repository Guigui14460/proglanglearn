from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from filebrowser.sites import site

from .sitemaps import ArticleSitemap, CourseSitemap, TutorialSitemap, StaticViewSitemap


site.directory = 'uploads/'

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': {'static': StaticViewSitemap, 'articles': ArticleSitemap, 'courses': CourseSitemap, 'tutorials': TutorialSitemap}},
         name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('articles/', include('articles.urls')),
    path('courses/', include('courses.urls')),
    path('forum/', include('forum.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
