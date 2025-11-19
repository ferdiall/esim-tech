from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.contrib.auth.models import User
from .models import ESIM
from .models import ESIM, Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "colored_status", "esim", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("id", "user__username")

    def colored_status(self, obj):
        if obj.status == "pending":
            color = "#facc15"  # sarı
            label = "Beklemede"
        elif obj.status == "completed":
            color = "#22c55e"  # yeşil
            label = "Tamamlandı"
        else:
            color = "#ef4444"  # kırmızı
            label = "İptal Edildi"

        return format_html(
            '<span style="color: white; background:{}; padding:4px 10px; border-radius:6px;">{}</span>',
            color, label
        )

    colored_status.short_description = "Durum"


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
from django.utils.html import format_html

class ESIMAdmin(admin.ModelAdmin):
    list_display = ("ICCID", "colored_status", "assigned_to", "created_at")
    list_filter = ("is_active", "assigned_to")
    search_fields = ("ICCID", "phone_number")

    def colored_status(self, obj):
        if obj.is_active:
            color = "#22c55e"  # yeşil
            label = "Aktif"
        else:
            color = "#3b82f6"  # mavi
            label = "Pasif"

        return format_html(
            '<span style="color: white; background:{}; padding:4px 10px; border-radius:6px;">{}</span>',
            color,
            label,
        )

    colored_status.short_description = "Durum"


# modelleri kaydet
custom_admin_site.register(ESIM, ESIMAdmin)
custom_admin_site.register(Order, OrderAdmin)