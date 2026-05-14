from django.urls import path

from profile_app.api.views import ProfileDetailView, BusinessProfileListView, CustomerProfileListView

urlpatterns = [
    path('profiles/business/', BusinessProfileListView.as_view()),
    path('profiles/customer/', CustomerProfileListView.as_view()),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
]