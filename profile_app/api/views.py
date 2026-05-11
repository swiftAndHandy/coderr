from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from profile_app.api.permissions import IsOwnerOrAdmin
from profile_app.api.serializers import ProfileSerializer
from profile_app.models import Profile


# Create your views here.
class ProfileDetailView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsOwnerOrAdmin()]

