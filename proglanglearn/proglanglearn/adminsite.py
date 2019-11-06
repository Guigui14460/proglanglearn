from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _


class MyAdminSite(AdminSite):
    site_header = _("Administration de ProgLangLearn")
    site_title = _("Site d'administration de ProgLangLearn")
    empty_value_display = _("---")


admin_site = MyAdminSite(name='admin')
