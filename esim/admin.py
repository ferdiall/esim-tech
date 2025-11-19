from django.contrib import admin
from django.utils.html import format_html
from .models import ESIM, Order

class CustomAdminSite(admin.AdminSite):
    class Media:
        css = {
            'all': ('admin/css/admin_custom.css',)
        }

admin.site = CustomAdminSite()

@admin.register(ESIM)
class ESIMAdmin(admin.ModelAdmin):
    list_display = ('ICCID', 'phone_number', 'colored_status', 'assigned_to', 'created_at')
    search_fields = ('ICCID', 'phone_number')
    list_filter = ('is_active',)

    class Media:
        css = {
            'all': ('admin/css/admin_custom.css',)
        }

    def colored_status(self, obj):
        color = 'green' if obj.is_active else 'red'
        return format_html(f'<b style="color:{color}">{ "Aktif" if obj.is_active else "Pasif" }</b>')
    colored_status.short_description = 'Durum'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    search_fields = ('user__username', 'esim__ICCID')

    class Media:
        css = {
            'all': ('admin/css/admin_custom.css',)
        }

    def colored_status(self, obj):
        colors = {'pending': 'orange', 'completed': 'green', 'canceled': 'red'}
        return format_html(f'<b style="color:{colors[obj.status]}">{obj.get_status_display()}</b>')
    colored_status.short_description = 'Durum'

    from django.utils.html import format_html
from django.contrib import admin
from .models import SimCard

@admin.register(SimCard)
class SimCardAdmin(admin.ModelAdmin):
    list_display = ("id", "phone_number", "status_colored", "created_at")

    def status_colored(self, obj):
        colors = {
            "active": "green",
            "pending": "orange",
            "blocked": "red",
            "expired": "gray"
        }

        color = colors.get(obj.status, "blue")

        return format_html(
            '<span class="status-badge" style="background:{};">{}</span>',
            color,
            obj.status.capitalize()
        )

    status_colored.short_description = "Status"

from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from .models import SimCard

class CustomAdminSite(admin.AdminSite):
    site_header = "ESIM Yönetim Paneli"
    site_title = "ESIM Admin"
    index_title = "Yönetim Paneli"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path("", self.admin_view(self.dashboard_view))
        ]
        return custom + urls

    def dashboard_view(self, request):
        active_count = SimCard.objects.filter(status="active").count()
        passive_count = SimCard.objects.filter(status="passive").count()
        blocked_count = SimCard.objects.filter(status="blocked").count()

        context = dict(
            self.each_context(request),
            active_count=active_count,
            passive_count=passive_count,
            blocked_count=blocked_count,
        )
        return TemplateResponse(request, "admin/index.html", context)

custom_admin_site = CustomAdminSite(name="custom_admin")
admin.site = custom_admin_site

# Model kaydı
admin.site.register(SimCard)
