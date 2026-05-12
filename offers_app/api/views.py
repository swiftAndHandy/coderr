from django.db.models import Min
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

from auth_app.api.permissions import IsBusinessUserOrAdmin
from offers_app.api.pagination import OfferListPagination
from offers_app.api.serializers import OfferSerializer, OfferListSerializer, OfferDetailSerializer
from offers_app.models import Offer, OfferDetail
from profile_app.api.permissions import IsOwnerOrAdmin


# Create your views here.
class OfferDetailsView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OfferDetailSerializer

    def get_object(self):
        return get_object_or_404(OfferDetail, pk=self.kwargs['pk'])



class OfferRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsOwnerOrAdmin()]

class OfferListCreateView(ListCreateAPIView):
    queryset = Offer.objects.all()
    pagination_class = OfferListPagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferSerializer
        return OfferListSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsBusinessUserOrAdmin()]
        return [AllowAny()]

    def get_queryset(self):
        offers = Offer.objects.annotate(min_price=Min("offerdetail__price"))
        creator_id = self.request.query_params.get("creator_id")
        min_price = self.request.query_params.get("min_price")
        max_delivery_time = self.request.query_params.get("max_delivery_time")

        if creator_id:
            offers = offers.filter(user=creator_id)
        if min_price:
            offers = offers.filter(offerdetail__price__gte=min_price)
        if max_delivery_time:
            offers = offers.filter(offerdetail__delivery_time_in_days__lte=max_delivery_time)

        return offers