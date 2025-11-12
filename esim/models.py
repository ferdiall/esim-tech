from django.db import models
from django.contrib.auth.models import User

class ESIM(models.Model):
    ICCID = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ICCID} ({'Aktif' if self.is_active else 'Pasif'})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('completed', 'Tamamlandı'),
        ('canceled', 'İptal Edildi'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    esim = models.ForeignKey(ESIM, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sipariş #{self.id} - {self.status}"
