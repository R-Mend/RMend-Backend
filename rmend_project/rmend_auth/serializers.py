from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User, EmployeeRequest
from rmend_authorities.models import Authority
from rmend_authorities.serializers import AuthorityModelSerializer


class UserSerializer(serializers.ModelSerializer):
    """Rest framework serializer for custom user model where password in write only"""
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'phone_number', 'auth_code')

    def create(self, validated_data):
        """
        Createsa a new user object when seralizer.save() is called
            Args:
                email (required): string of the new users email
                username (not-required): string of the users username
                password (required): string of the new users password
            Returns:
                User: the new custom user object with the given email, username, and password
        """
        if 'username' not in validated_data:
            validated_data['username'] = User.get_temporary_username(validated_data['email'])

        return User.objects.create_user(
            email=validated_data['email'], password=validated_data['password'], 
            username=validated_data['username'])

class EmployeeRequestSerializer(serializers.ModelSerializer):
    """Rest framework serializer  for the employee request model"""
    class Meta:
        model = EmployeeRequest
        fields = ('id', 'authority', 'user')

    def create(self, validated_data):
        """
        Creates a new employ request when serializer.save() is called
            Args:
                authority (required): the id of the authority the request is going to
                user (required): the is of the user the request is comming from
            Return:
                EmployeeRequest: a new employee request for the authority from the user
        """
        return EmployeeRequest.objects.create(**validated_data)