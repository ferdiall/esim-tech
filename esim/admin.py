from django.contrib import admin
from django.utils.html import format_html
from .models import ESIM, Order

@admin.register(ESIM)
class ESIMAdmin(admin.ModelAdmin):
    list_display = ('ICCID', 'phone_number', 'colored_status', 'assigned_to', 'created_at')
    search_fields = ('ICCID', 'phone_number')
    list_filter = ('is_active',)

    def colored_status(self, obj):
        color = 'green' if obj.is_active else 'red'
        return format_html(f'<b style="color:{color}">{ "Aktif" if obj.is_active else "Pasif" }</b>')
    colored_status.short_description = 'Durum'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'esim', 'colored_status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'esim__ICCID')

    def colored_status(self, obj):
        colors = {'pending': 'orange', 'completed': 'green', 'canceled': 'red'}
        return format_html(f'<b style="color:{colors[obj.status]}">{obj.get_status_display()}</b>')
    colored_status.short_description = 'Durum'
