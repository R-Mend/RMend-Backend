from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import User


# Create your tests here.
class UserTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('test@example.com', 'testpassword', 'testname')
        self.token = Token.objects.create(user=self.test_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.user_url = '/api/users/me'

    def test_get_user(self):
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.test_user.username)
        self.assertEqual(response.data['email'], self.test_user.email)
        self.assertEqual(response.data['phone_number'], self.test_user.phone_number)
        self.assertEqual(response.data['auth_code'], self.test_user.auth_code)

    def test_update_user(self):
        data = {
            'email': 'test@example.com',
            'username': 'newtestname',
            'phone_number': '1234567890',
            'auth_code': '123456'
        }

        response = self.client.post(self.user_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['phone_number'], data['phone_number'])
        self.assertEqual(response.data['auth_code'], data['auth_code'])



class UserCreateTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('test@example.com', 'testpassword', 'testname')
        # URL for creating an account
        self.create_url = '/api/users/'

    def test_create_user(self):
        '''Ensure that we can create a new user and a valid token is created with it'''
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword',
            'phone_number': '1234567890',
            'auth_code': '31241243123'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)

        user = User.objects.latest('id')
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)

    def test_create_user_with_short_password(self):
        '''Ensure user is not created for password lengths less than 8.'''
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'some',
            'phone_number': '',
            'auth_code': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': '',
            'phone_number': '',
            'auth_code': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        data = {
            'username': 'foobar'*101,
            'email': 'foobar@example.com',
            'password': 'somepassword',
            'phone_number': '',
            'auth_code': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        data = {
            'username': '',
            'email': 'foobar@example.com',
            'password': 'somepassword',
            'phone_number': '',
            'auth_code': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_email(self):
        data = {
            'username': 'foobar',
            'email': 'test@example.com',
            'password': 'somepassword',
            'phone_number': '',
            'auth_code': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        data = {
            'username': 'foobar',
            'email': 'foobarexample',
            'password': 'somepassword',
            'phone_number': '',
            'auth_code': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_with_no_email(self):
        data = {
            'username': 'foobar',
            'email': '',
            'password': 'somepassword',
            'phone_number': '',
            'auth_code': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_to_long_phone_number(self):
        data = {
            'username': 'foobar',
            'email': '',
            'password': 'somepassword',
            'phone_number': '324123241234123412342',
            'auth_code': ''
        } 

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)


class UserAuthenticationTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('test@example.com', 'testpassword', 'testname')
        self.token = Token.objects.create(user=self.test_user)
        self.login_url = '/api/token/login'
        self.logout_url = '/api/token/logout'

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_login_user(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], self.token.key)
        self.assertEqual(response.data['user_name'], self.test_user.username)
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)

    def test_logout_user(self):
        request = self.client.post(self.logout_url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.count(), 0)