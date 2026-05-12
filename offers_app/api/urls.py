from django.urls import path

from offers_app.api.views import OfferListCreateView, OfferRetrieveUpdateDestroyView, OfferDetailsView

urlpatterns = [
    path('offers/', OfferListCreateView.as_view()),
    path('offers/<int:pk>/', OfferRetrieveUpdateDestroyView.as_view()),
    path('offerdetails/<int:pk>/', OfferDetailsView.as_view(), name='offerdetails-list'),
]