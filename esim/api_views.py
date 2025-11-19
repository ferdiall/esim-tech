from rest_framework import viewsets
from .models import ESIM, Order
from .serializers import ESIMSerializer, OrderSerializer

class ESIMViewSet(viewsets.ModelViewSet):
    queryset = ESIM.objects.all()
    serializer_class = ESIMSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
