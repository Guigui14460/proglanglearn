from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path

from allauth.account.views import confirm_email
from filebrowser.sites import site
from rest_framework.authtoken.views import obtain_auth_token

from .adminsite import admin_site
from .router import router
from .sitemaps import ArticleSitemap, CourseSitemap, TutorialSitemap, StaticViewSitemap
from .social_rest_auth import FacebookLogin, GithubLogin, GoogleLogin, TwitterLogin


site.directory = 'uploads/'

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': {'static': StaticViewSitemap, 'articles': ArticleSitemap, 'courses': CourseSitemap, 'tutorials': TutorialSitemap}},
         name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('main.urls')),
    path('accounts/', include('accounts.allauth_urls')),
    path('accounts/', include('accounts.urls')),
    path('articles/', include('articles.urls')),
    path('courses/', include('courses.urls')),
    path('forum/', include('forum.urls')),
    path('polls/', include('polls.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', obtain_auth_token, name='obtain-token'),
    path('rest-auth/', include('rest_auth.urls')),
    re_path(r"^rest-auth/registration/account-confirm-email/(?P<key>[\s\d\w().+-_',:&]+)/$", confirm_email,
            name="account_confirm_email"),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # path('rest-auth/facebook/', FacebookLogin.as_view(), name='facebook_login'),
    # path('rest-auth/github/', GithubLogin.as_view(), name='github_login'),
    # path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    # path('rest-auth/twitter/', TwitterLogin.as_view(), name='twitter_login'),
    path('admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
