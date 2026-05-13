from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth_app.api.permissions import IsCustomerUserOrAdmin, IsStaffMember, IsBusinessUserOrAdmin
from orders_app.api.permissions import IsContractedOrStaff
from orders_app.api.serializers import OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer
from orders_app.models import Order
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, DestroyModelMixin


# Create your views here.
class OrderListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUserOrAdmin()]
        return [IsAuthenticated()]

class OrderUpdateDestroyView(
    UpdateModelMixin,
    DestroyModelMixin,
    GenericAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsContractedOrStaff()]
        return [IsStaffMember()]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = OrderStatusUpdateSerializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OrderSerializer(instance).data)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)