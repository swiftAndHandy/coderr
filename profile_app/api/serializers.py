from rest_framework import serializers

from profile_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for business and customer profiles.
    The email field lives on the User model and is handled separately
    in update() and injected back in to_representation().
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    type = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(required=False)

    class Meta:
        model = Profile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type',
            'email',
            'created_at'
        ]

    def update(self, instance, validated_data):
        email = validated_data.pop('email', None)
        if email:
            instance.user.email = email
            instance.user.save()
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['email'] = instance.user.email
        return data