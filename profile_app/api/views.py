from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from profile_app.api.permissions import IsOwnerOrAdmin
from profile_app.api.serializers import ProfileSerializer
from profile_app.models import Profile


# Create your views here.
class ProfileDetailView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        obj = get_object_or_404(Profile, user_id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsOwnerOrAdmin()]

class BusinessProfileListView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(type="business")

class CustomerProfileListView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(type="customer")