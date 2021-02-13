from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from .serializers import UserSerializer, EmployeeRequestSerializer
from .models import User
from rmend_authorities.models import Authority


# Create your views here.
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(email=request.user.email)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)    


class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(ObtainAuthToken):
    def post(self, request):
        user = authenticate(email=request.data.get('email'), password=request.data.get('password'))
        if not user:
            return Response({'detial': 'Incorrect email or password. Please try agian.'},
                status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'user_name': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'auth_code': user.auth_code
        }, status=status.HTTP_200_OK)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response({'detail': 'The authcode you\'re trying to delete does not exist'})

        return Response({'success': f'User {request.user.username} deleted successfully'})