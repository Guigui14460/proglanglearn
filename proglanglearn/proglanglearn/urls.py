from django.conf import settings, urls as conf_urls
from django.contrib import admin
from django.urls import path, include

from accounts.views import (
    error_403,
    error_404,
    error_500
)

urlpatterns = [
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
]

conf_urls.handler403 = error_403
conf_urls.handler404 = error_404
conf_urls.handler500 = error_500

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
