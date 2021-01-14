from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'phone_number', 'auth_code')

    def create(self, validated_data):
        if 'username' not in validated_data:
            validated_data['username'] = User.get_temporary_username(validated_data['email'])

        user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'], 
            username=validated_data['username'])
        return user