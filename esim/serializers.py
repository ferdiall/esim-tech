from rest_framework import serializers
from .models import ESIM, Order

class ESIMSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESIM
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'