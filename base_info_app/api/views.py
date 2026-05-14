from django.db.models import Avg
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import Offer
from profile_app.models import Profile
from review_app.models import Review


# Create your views here.
class PlatformInformation(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        return Response({
            'review_count': Review.objects.count(),
            'average_rating': round(Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0, 1),
            'business_profile_count': Profile.objects.filter(type='business').count(),
            'offer_count': Offer.objects.count()
        })