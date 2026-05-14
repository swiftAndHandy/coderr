from django.contrib.auth.models import User
from rest_framework import serializers

from profile_app.models import Profile


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=['customer', 'business'], write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'repeated_password', 'type')

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError('Passwords must match')
        data.pop('repeated_password')
        data['username'] = data['username'] #TODO: Add .lower after Code Review
        data['email'] = data['email'].lower()
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        type = validated_data.pop('type')
        user = User.objects.create_user(password=password, **validated_data)
        Profile.objects.create(user=user, type=type)
        return user