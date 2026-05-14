from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.api.serializers import RegistrationSerializer


# Create your views here.
class RegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        data = dict(serializer.data)
        data['token'] = token.key
        data['user_id'] = user.id

        return Response(data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username') #TODO: add .lower() after code review
        user = authenticate(username=username, password=request.data.get('password'))
        if not user:
            return Response({'message': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)

        data = {
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'user_id': user.id,
        }
        return Response(data, status=status.HTTP_200_OK)