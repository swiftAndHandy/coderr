from django.urls import path

from orders_app.api.views import OrderListCreateAPIView, OrderUpdateDestroyView, OrdersInProgressCountView

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view()),
    path('orders/<int:pk>/', OrderUpdateDestroyView.as_view()),
    path('order-count/<int:business_user_id>/', OrdersInProgressCountView.as_view()),
]