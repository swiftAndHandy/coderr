from django.db.models import Q
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from auth_app.api.permissions import IsCustomerUserOrAdmin
from orders_app.api.serializers import OrderListSerializer, OrderCreateSerializer
from orders_app.models import Order


# Create your views here.
class OrderListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderListSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUserOrAdmin()]
        return [IsAuthenticated()]