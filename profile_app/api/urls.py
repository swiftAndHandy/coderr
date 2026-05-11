from django.urls import path

from profile_app.api.views import ProfileDetailView

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    ]