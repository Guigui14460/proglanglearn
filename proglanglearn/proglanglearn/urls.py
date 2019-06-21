from django.conf import settings, urls as conf_urls
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from main.views import (
    error_403,
    error_404,
    error_500
)

urlpatterns = [
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

conf_urls.handler403 = error_403
conf_urls.handler404 = error_404
conf_urls.handler500 = error_500

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
