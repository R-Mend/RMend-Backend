from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.gis.geos import GEOSGeometry
from rest_framework.authtoken.models import Token

from .models import Authority, AuthorityIssueType, AuthorityIssueTypeGroup, BaseIssueTypeGroup, BaseIssueType
from rmend_auth.models import User


# Create your tests here.
class IssueGroupTest(APITestCase):
    def setUp(self):
        report_area = GEOSGeometry('POLYGON ((-86.62170408951287 36.57142381906437, -86.19049071065865 36.56039392897386, -85.92956541772644 36.92135192347484, -86.20697020284396 37.08804885508249, -86.5530395387336 37.09681224924606, -86.82495115978935 36.97183824650084, -86.77551268323343 36.69485093715447, -86.62170408951287 36.57142381906437))')
        self.test_authority = Authority.objects.create(name='Test Authority', authority_type='test', 
            address='testaddress', phone_number='1234567890', email='test@email.com', website_url='', 
            report_range=report_area)

        self.test_base_issue_type_group = BaseIssueTypeGroup.objects.create(name='TestGroup')
        self.test_base_issue_type = BaseIssueType.objects.create(name='TestType', 
            issue_group=self.test_base_issue_type_group)

        self.test_issue_type_group = AuthorityIssueTypeGroup.objects.create(name='DupeTestGroup', 
            authority=self.test_authority)
        self.test_issue_type = AuthorityIssueType.objects.create(name='DupeTest ype', 
            issue_group=self.test_issue_type_group)

    def test_get_issue_type_groups(self):
        data = {'location': (-86.19049071065865, 36.56039392897386)}
        response = self.client.post('/api/issue-groups/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['issue_groups']), 1)


class AuthorityTest(APITestCase):
    def setUp(self):

        report_area = GEOSGeometry('POLYGON ((-86.62170408951287 36.57142381906437, -86.19049071065865 36.56039392897386, -85.92956541772644 36.92135192347484, -86.20697020284396 37.08804885508249, -86.5530395387336 37.09681224924606, -86.82495115978935 36.97183824650084, -86.77551268323343 36.69485093715447, -86.62170408951287 36.57142381906437))')
        self.test_authority = Authority.objects.create(name='Test Authority', authority_type='test', 
            address='testaddress', phone_number='1234567890', email='test@email.com', website_url='', 
            report_range=report_area)

        self.test_base_issue_type_group = BaseIssueTypeGroup.objects.create(name='TestGroup')
        self.test_base_issue_type = BaseIssueType.objects.create(name='TestType', issue_group=self.test_base_issue_type_group)

        self.test_issue_type_group = AuthorityIssueTypeGroup.objects.create(name='DupeTestGroup', 
            authority=self.test_authority)
        self.test_issue_type = AuthorityIssueType.objects.create(name='DupeTestType', 
            issue_group=self.test_issue_type_group)
        
        self.test_user = User.objects.create_user('test@example.com', 'testpassword', 'testname')
        self.token = Token.objects.create(user=self.test_user)
        self.test_user.authority = self.test_authority
        self.test_user.save()

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_issue_type_groups(self):
        response = self.client.get(f'/api/authority/{self.test_authority.id}/issue-groups')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['issue_groups']), 1)

    def test_create_issue_type_group(self):
        data = { 'group_name': self.test_base_issue_type_group.name }
        response = self.client.post(f'/api/authority/{self.test_authority.id}/issue-groups/create', 
            data, format='json')
        self.assertEqual(AuthorityIssueTypeGroup.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_issue_type_group_with_no_group_name(self):
        data = { 'group_name': '' }
        response = self.client.post(f'/api/authority/{self.test_authority.id}/issue-groups/create', 
            data, format='json')
        self.assertEqual(AuthorityIssueTypeGroup.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_issue_type_group(self):
        data = { 'group_name': self.test_issue_type_group.name }
        response = self.client.post(f'/api/authority/{self.test_authority.id}/issue-groups/create', 
            data, format='json')
        self.assertEqual(AuthorityIssueTypeGroup.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_issue_type_group(self):
        data = { 'group_name': self.test_issue_type_group.name }
        response = self.client.delete(f'/api/authority/{self.test_authority.id}/issue-groups/delete', 
            data, format='json')
        self.assertEqual(AuthorityIssueTypeGroup.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_issue_type(self):
        AuthorityIssueTypeGroup.objects.create(name=self.test_base_issue_type_group, authority=self.test_authority)
        data = {'issue_group_name': self.test_base_issue_type_group.name, 'type_name': self.test_base_issue_type.name}
        response = self.client.post(f'/api/authority/{self.test_authority.id}/issue-types/create', data, format='json')
        self.assertEqual(AuthorityIssueType.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_issue_type_with_no_type_name(self):
        AuthorityIssueTypeGroup.objects.create(name=self.test_base_issue_type_group, authority=self.test_authority)
        data = {'issue_group_name': self.test_issue_type_group.name, 'type_name': ''}
        response = self.client.post(f'/api/authority/{self.test_authority.id}/issue-types/create', 
            data, format='json')
        self.assertEqual(AuthorityIssueType.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_issue_type(self):
        AuthorityIssueTypeGroup.objects.create(name=self.test_base_issue_type_group, authority=self.test_authority)
        data = {'issue_group_name': self.test_issue_type_group.name, 'type_name': self.test_issue_type.name}
        response = self.client.post(f'/api/authority/{self.test_authority.id}/issue-types/create', 
            data, format='json')
        self.assertEqual(AuthorityIssueType.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_issue_type(self):
        data = {'type_name': self.test_issue_type.name}
        response = self.client.delete(f'/api/authority/{self.test_authority.id}/issue-types/delete', 
            data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(AuthorityIssueType.objects.count(), 0)

        

class AuthorityPermissionsTest(APITestCase):
    def setUp(self):

        report_area = GEOSGeometry('POLYGON ((-86.62170408951287 36.57142381906437, -86.19049071065865 36.56039392897386, -85.92956541772644 36.92135192347484, -86.20697020284396 37.08804885508249, -86.5530395387336 37.09681224924606, -86.82495115978935 36.97183824650084, -86.77551268323343 36.69485093715447, -86.62170408951287 36.57142381906437))')
        self.test_authority = Authority.objects.create(name='Test Authority', authority_type='test', 
            address='testaddress', phone_number='1234567890', email='test@email.com', website_url='', 
            report_range=report_area)

        self.test_base_issue_type_group = BaseIssueTypeGroup.objects.create(name='TestGroup')
        self.test_base_issue_type = BaseIssueType.objects.create(name='TestType', 
            issue_group=self.test_base_issue_type_group)

        self.test_issue_type_group = AuthorityIssueTypeGroup.objects.create(name='DupeTestGroup', 
            authority=self.test_authority)
        self.test_issue_type = AuthorityIssueType.objects.create(name='DupeTestType', 
            issue_group=self.test_issue_type_group)

    def test_create_issue_type_group_without_admin_access(self):
        data = { 'group_name': self.test_base_issue_type.name }
        response = self.client.post(f'/api/authority/{self.test_authority.id}/issue-groups/create', 
            data, format='json')
        self.assertEqual(AuthorityIssueTypeGroup.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_issue_type_group_without_admin_access(self):
        data = { 'group_name': self.test_issue_type_group.name }
        response = self.client.delete(f'/api/authority/{self.test_authority.id}/issue-groups/delete', 
            data, format='json')
        self.assertEqual(AuthorityIssueTypeGroup.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_issue_type_without_admin_access(self):
        data = {'issue_group_name': self.test_base_issue_type_group.name, 'type_name': self.test_base_issue_type.name}
        response = self.client.post(f'/api/authority/{self.test_authority.id}/issue-types/create', 
            data, format='json')
        self.assertEqual(AuthorityIssueType.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_issue_type_without_admin_access(self):
        data = {'type_name': 'Dupe Test Type'}
        response = self.client.delete(f'/api/authority/{self.test_authority.id}/issue-types/delete', 
            data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(AuthorityIssueType.objects.count(), 1)