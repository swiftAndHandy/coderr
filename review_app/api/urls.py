from django.urls import path

from review_app.api.views import ReviewListCreateView, ReviewUpdateDestroyView

urlpatterns = [
    path('reviews/', ReviewListCreateView.as_view()),
    path('reviews/<int:pk>/', ReviewUpdateDestroyView.as_view()),
]