from rest_framework import serializers

from profile_app.models import Profile
from review_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Read-Only serializer for the review model.
    """
    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at',
        ]

class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Creates a review. Validates that the target is a business user
    and that the reviewer has not already reviewed them.
    The reviewer is set from the request context, not the request body.
    """
    class Meta:
        model = Review
        fields = ['business_user', 'rating', 'description']

    def validate(self, attrs):
        reviewer = self.context['request'].user
        business_user = attrs.get('business_user')
        if not Profile.objects.filter(user=business_user, type='business').exists():
            raise serializers.ValidationError(f'{business_user} is not a business user.')
        duplicate = Review.objects.filter(reviewer=reviewer, business_user=business_user).exists()
        if duplicate:
            raise serializers.ValidationError(f'reviewer {reviewer} already reviewed {business_user}')
        return attrs

    def create(self, validated_data):
        return Review.objects.create(
            reviewer=self.context['request'].user,
            **validated_data
        )

class ReviewUpdateSerializer(serializers.ModelSerializer):
    """
    Restricts PATCH updated to rating and description.
    """
    class Meta:
        model = Review
        fields = ['rating', 'description']