from django.urls import path

from base_info_app.api.views import PlatformInformation

urlpatterns = [
    path('base-info/', PlatformInformation.as_view()),
]