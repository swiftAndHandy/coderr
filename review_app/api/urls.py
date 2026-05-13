from django.urls import path

from review_app.api.views import ReviewListCreateView

urlpatterns = [
    path('reviews/', ReviewListCreateView.as_view()),
]