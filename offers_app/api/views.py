from rest_framework import generics
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from auth_app.api.permissions import IsBusinessUserOrAdmin
from offers_app.api.serializers import OfferSerializer, OfferListSerializer
from offers_app.models import Offer
from profile_app.api.permissions import IsOwnerOrAdmin


# Create your views here.
class OfferDetailsView(RetrieveAPIView):
    def get_queryset(self):
        return Offer.objects.filter(id=self.kwargs['pk'])

class OfferRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsOwnerOrAdmin()]

class OfferListCreateView(ListCreateAPIView):
    queryset = Offer.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferSerializer
        return OfferListSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsBusinessUserOrAdmin()]
        return [AllowAny()]
