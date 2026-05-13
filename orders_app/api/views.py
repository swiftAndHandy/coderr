import profile

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, GenericAPIView, get_object_or_404
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.api.permissions import IsCustomerUserOrAdmin, IsStaffMember
from orders_app.api.permissions import IsContractedOrStaff
from orders_app.api.serializers import OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer
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
        return OrderSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUserOrAdmin()]
        return [IsAuthenticated()]

    def post(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OrderSerializer(serializer.instance).data)

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

class BaseOrderCountView(APIView):
    permission_classes = [IsAuthenticated]
    status = None
    response_name = 'order_count'

    def get(self, request, *args, **kwargs):
        business_user_id = kwargs.get('business_user_id')
        count = Order.objects.filter(business_user_id=business_user_id, status=self.status).count()
        print(count)
        if count == 0:
            get_object_or_404(User, id=business_user_id, profile__type='business')

        return Response({self.response_name: count})


class OrdersCompletedCountView(BaseOrderCountView):
    status = 'completed'
    response_name = 'completed_order_count'


class OrdersInProgressCountView(BaseOrderCountView):
    status = 'in_progress'