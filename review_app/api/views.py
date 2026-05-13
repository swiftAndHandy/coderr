# Create your views here.
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth_app.api.permissions import IsCustomerUserOrAdmin
from review_app.api.serializers import ReviewSerializer, ReviewCreateSerializer
from review_app.models import Review


class ReviewListCreateView(ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCustomerUserOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        reviews = Review.objects.all()
        business_user_id = self.request.query_params.get('business_user_id')
        reviewer_id = self.request.query_params.get('reviewer_id')

        if business_user_id:
            reviews = reviews.filter(business_user_id=business_user_id)
        if reviewer_id:
            reviews = reviews.filter(reviewer_id=reviewer_id)
        return reviews

    def post(self, request, *args, **kwargs):
        serializer = ReviewCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ReviewSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)