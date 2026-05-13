from django.urls import path

from orders_app.api.views import OrderListCreateAPIView

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view()),
]