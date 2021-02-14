from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from .serializers import UserSerializer, EmployeeRequestSerializer
from .models import User, EmployeeRequest
from .permissions import IsAuthorityAdmin
from rmend_authorities.models import Authority


# Create your views here.
class UserView(APIView):
    """API View for for getting users infromation and updating users"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Gets the infromation of the user that sent the request"""
        user = User.objects.get(email=request.user.email)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        """Updates the user that sent the request with the request's updated information"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserCreateView(APIView):
    """API View for creating new users"""

    def post(self, request):
        """Creates a new user if all the required data is given an is valid"""
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
    """API VIew for logging users into the application"""

    def post(self, request):
        """Gives user an auth token if users email and password are correct"""
        user = authenticate(
            email=request.data.get('email'),
            password=request.data.get('password'))
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
    """Logs the user out of the application"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Deletes the users auth token, logging them out of the application"""
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response({'detail': 'The authcode you\'re trying to delete does not exist'})

        return Response({'success': f'User {request.user.username} successfully logged out'})

class CreateEmployeeRequestView(APIView):
    """API VIew for creating a new employee request"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Creates a new employee request from the request sender, to the requested authority"""
        authority_auth_code = request.data.get('authority_auth_code')
        if not authority_auth_code:
            return missing_requred_data_error('authority_auth_code')

        authority = Authority.objects.get(auth_code=authority_auth_code)
        employee_request, created = EmployeeRequest.objects.get_or_create(
            authority=authority, user=request.user)

        if not created:
            return Response({'deital': 'Pending request already sent to atuhroity'},
             status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'success': f'Successfully sent employee request to {employee_request.authority.name}'},
            status=status.HTTP_201_CREATED)

class AdminDeleteEmployeeRequestView(APIView):
    """API VIew for adins to delete and accept employee requests"""
    permission_classes = [IsAuthenticated, IsAuthorityAdmin]

    def delete(self, request, authority_id, employee_request_id):
        """Deletes the requested employee request and adds the users as an employee if accepted"""
        is_accepted = request.data.get('is_accepted')
        if is_accepted is None:
            return missing_requred_data_error('is_accepted')

        try:
            employee_request = EmployeeRequest.objects.get(id=employee_request_id)
        except EmployeeRequest.DoesNotExist:
            return data_does_not_exist_error('Employee Request,', employee_request_id)

        # Verify that the user is an admin of the requests authority
        self.check_object_permissions(request, employee_request)

        if is_accepted and employee_request.user.authority:
            return Response({'detail': 'User is already a part of an authority'},
                status=status.HTTP_400_BAD_REQUEST)

        if is_accepted:
            employee_request.user.authority = employee_request.authority
            employee_request.user.save()

        employee_request.delete()
        return Response({'success': 'Successfully delete employee request'})


def missing_requred_data_error(data):
    """Helper function for returning a missing data error"""
    return Response({'detial': f'Missing requested data: {data}'},
        status=status.HTTP_400_BAD_REQUEST)

def data_does_not_exist_error(data_type, data):
    """Helper function for returning a data does not exist error"""
    return Response({'detail': f'{data_type}, {data} does not exist'})
