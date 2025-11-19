from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from .models import ESIM

class CustomAdminSite(admin.AdminSite):
    site_header = "ESIM Yönetim Paneli"
    site_title = "ESIM Admin"
    index_title = "Yönetim Paneli"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path("", self.admin_view(self.dashboard_view), name="index"),
        ]
        return custom + urls

    def dashboard_view(self, request):
        # ESIM modeline göre sayımlar
        active_count = ESIM.objects.filter(is_active=True).count()
        passive_count = ESIM.objects.filter(is_active=False).count()
        blocked_count = 0  # Bu modelde blocked yok

        context = {
            **self.each_context(request),
            "active_count": active_count,
            "passive_count": passive_count,
            "blocked_count": blocked_count,
        }

        return TemplateResponse(request, "admin/index.html", context)

custom_admin_site = CustomAdminSite(name="custom_admin")

# Model kaydı
custom_admin_site.register(ESIM)
