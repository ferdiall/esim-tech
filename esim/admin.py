from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.contrib.auth.models import User
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
        # ESIM model verileri
        total_esim = ESIM.objects.count()
        active_count = ESIM.objects.filter(is_active=True).count()
        passive_count = ESIM.objects.filter(is_active=False).count()

        # kullanıcı sayısı
        total_users = User.objects.count()

        # Template'e göndereceğimiz veriler
        context = {
            **self.each_context(request),
            "total_esim": total_esim,
            "active_count": active_count,
            "passive_count": passive_count,
            "blocked_count": 0,  # Blokeli alan modelde yok
            "total_users": total_users,
        }

        return TemplateResponse(request, "admin/index.html", context)

# Custom admin site oluştur
custom_admin_site = CustomAdminSite(name="custom_admin")

# modelleri kaydet
custom_admin_site.register(ESIM)
