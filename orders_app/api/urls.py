from django.urls import path

from orders_app.api.views import OrderListCreateAPIView, OrderUpdateDestroyView

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view()),
    path('orders/<int:pk>/', OrderUpdateDestroyView.as_view()),
]