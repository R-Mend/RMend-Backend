from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from django.contrib.gis.geos import GEOSGeometry

from rmend_authorities.models import Authority
from .models import User, EmployeeRequest


# Create your tests here.
class UserTest(APITestCase):
    """Tests the users get, create, and update routes"""

    def setUp(self):
        """Sets up the test user, token, and client for the test cases"""
        self.test_user = User.objects.create_user('test@example.com', 'testpassword', 'testname')
        self.token = Token.objects.create(user=self.test_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.user_url = '/api/users/me'
        self.create_url = '/api/users/'

    def test_get_user(self):
        """Ensues we can get a users information"""
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.test_user.username)
        self.assertEqual(response.data['email'], self.test_user.email)
        self.assertEqual(response.data['phone_number'], self.test_user.phone_number)
        self.assertEqual(response.data['auth_code'], self.test_user.auth_code)

    def test_update_user(self):
        """Ensue we can update the users updatable infromation"""
        data = {
            'email': 'test@example.com',
            'username': 'newtestname',
            'phone_number': '1234567890',
            'auth_code': '123456'
        }

        response = self.client.put(self.user_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['phone_number'], data['phone_number'])
        self.assertEqual(response.data['auth_code'], data['auth_code'])

    def test_create_user(self):
        """Ensure that we can create a new user and a valid token is created with it"""
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
        """Ensure user is not created for password lengths less than 8."""
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
        """Ensure user is not created with no password"""
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
        """Ensure user is not created with a username that's too long"""
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
        """Ensure user is not created without a username"""
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
        """Ensure user is not created with an email that is already taken"""
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
        """Ensure user us not created with an invalid email"""
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
        """Ensure user is not created without an email"""
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
        """Ensure a user us not created with an emial that's too long"""
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
    """Tests the users authentication and permissions"""

    def setUp(self):
        """Sets up the test user, token, and client for the test cases"""
        self.test_user = User.objects.create_user('test@example.com', 'testpassword', 'testname')
        self.token = Token.objects.create(user=self.test_user)
        self.login_url = '/api/token/login'
        self.logout_url = '/api/token/logout'

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_login_user(self):
        """Ensure users can login"""
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
        """Ensure users can logout"""
        request = self.client.post(self.logout_url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.count(), 0)


class EmployeeRequestTests(APITestCase):
    """Test employee requests routes"""

    def setUp(self):
        """Sets up needed models, tokens, and client for test cases"""
        report_area = GEOSGeometry('POLYGON ((-86.62170408951287 36.57142381906437, \
            -86.19049071065865 36.56039392897386, -85.92956541772644 36.92135192347484, \
            -86.20697020284396 37.08804885508249, -86.5530395387336 37.09681224924606,  \
            -86.82495115978935 36.97183824650084, -86.77551268323343 36.69485093715447, \
            -86.62170408951287 36.57142381906437))')
        self.test_authority = Authority.objects.create(
            name='Test Authority', authority_type='test', address='testaddress',
            phone_number='1234567890', email='test@email.com', website_url='',
            report_range=report_area)

        self.test_user = User.objects.create_user('test@example.com', 'testpassword', 'testname')
        self.token = Token.objects.create(user=self.test_user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.create_url = '/api/users/me/employee-requests/create'

    def test_create_employee_request(self):
        """Ensure we can create a new employee request"""
        data = {'authority_auth_code': self.test_authority.auth_code}
        request = self.client.post(self.create_url, data=data, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmployeeRequest.objects.count(), 1)

    def test_create_duplicate_employee_request(self):
        """Ensure an employee requests is not created with the same user and authority"""
        EmployeeRequest.objects.create(authority=self.test_authority, user=self.test_user)
        data = {'authority_auth_code': self.test_authority.auth_code}
        request = self.client.post(self.create_url, data=data, format='json')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(EmployeeRequest.objects.count(), 1)


class AdminEmployeeRequestTests(APITestCase):
    """Tests the employee request delete route"""

    def setUp(self):
        """Sets up needed models, tokens, and client for test cases"""
        report_area = GEOSGeometry('POLYGON ((-86.62170408951287 36.57142381906437, \
            -86.19049071065865 36.56039392897386, -85.92956541772644 36.92135192347484, \
            -86.20697020284396 37.08804885508249, -86.5530395387336 37.09681224924606,  \
            -86.82495115978935 36.97183824650084, -86.77551268323343 36.69485093715447, \
            -86.62170408951287 36.57142381906437))')
        self.test_authority = Authority.objects.create(
            name='Test Authority', authority_type='test', address='testaddress',
            phone_number='1234567890', email='test@email.com', website_url='',
            report_range=report_area)

        self.test_user = User.objects.create_user('test@example.com', 'testpassword', 'testname')
        self.token = Token.objects.create(user=self.test_user)
        self.test_user.authority = self.test_authority
        self.test_user.save()

        self.test_user2 = User.objects.create_user(
            'test2@example.com', 'test2password', 'test2name')

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_delete_employee_request(self):
        """Ensure we can delete employee requests"""
        employee_request = EmployeeRequest.objects.create(
            authority=self.test_authority, user=self.test_user)
        request = self.client.delete(
            f'/api/authority/{self.test_authority.id}/employee-requests/{employee_request.id}/delete',
            data={'is_accepted': False},
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(EmployeeRequest.objects.count(), 0)

    def test_delete_accepted_employee_request(self):
        """Ensure we can delete employee request when they are accepted"""
        employee_request = EmployeeRequest.objects.create(
            authority=self.test_authority, user=self.test_user2)
        request = self.client.delete(
            f'/api/authority/{self.test_authority.id}/employee-requests/{employee_request.id}/delete',
            data={'is_accepted': True},
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(EmployeeRequest.objects.count(), 0)
        self.assertEqual(self.test_user.authority, self.test_authority)


class AdminEmployeeRequestPermissionTests(APITestCase):
    """Test the admin only permissions for employee request"""

    def setUp(self):
        """Sets up needed models, tokens, and client for test cases"""
        report_area = GEOSGeometry('POLYGON ((-86.62170408951287 36.57142381906437, \
            -86.19049071065865 36.56039392897386, -85.92956541772644 36.92135192347484, \
            -86.20697020284396 37.08804885508249, -86.5530395387336 37.09681224924606,  \
            -86.82495115978935 36.97183824650084, -86.77551268323343 36.69485093715447, \
            -86.62170408951287 36.57142381906437))')
        self.test_authority = Authority.objects.create(
            name='Test Authority', authority_type='test', address='testaddress',
            phone_number='1234567890', email='test@email.com', website_url='',
            report_range=report_area)

        self.test_user = User.objects.create_user('test@example.com', 'testpassword', 'testname')
        self.token = Token.objects.create(user=self.test_user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.create_url = '/api/users/employee/request'

    def test_delete_employee_request_without_permission(self):
        """Ensure employee requests can not be created without admin access the to authority"""
        employee_request = EmployeeRequest.objects.create(
            authority=self.test_authority, user=self.test_user)
        request = self.client.delete(
            f'/api/authority/{self.test_authority.id}/employee-requests/{employee_request.id}/delete',
            data={'is_accepted': False},
            format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(EmployeeRequest.objects.count(), 1)
