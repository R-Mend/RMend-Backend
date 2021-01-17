from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.gis.geos import GEOSGeometry

from .models import Report
from rmend_auth.models import User
from rmend_authorities.models import Authority, AuthorityIssueTypeGroup, AuthorityIssueType

# Create your tests here.
class ReportTest(APITestCase):
    def setUp(self):
        report_area = GEOSGeometry('POLYGON ((-86.62170408951287 36.57142381906437, -86.19049071065865 36.56039392897386, -85.92956541772644 36.92135192347484, -86.20697020284396 37.08804885508249, -86.5530395387336 37.09681224924606, -86.82495115978935 36.97183824650084, -86.77551268323343 36.69485093715447, -86.62170408951287 36.57142381906437))')
        self.test_authority = Authority.objects.create(name='Test Authority', authority_type='test', 
            address='testaddress', phone_number='1234567890', email='test@email.com', website_url='', 
            report_range=report_area)

        self.test_issue_type_group = AuthorityIssueTypeGroup.objects.create(name='Test Group', 
            authority=self.test_authority)
        self.test_issue_type = AuthorityIssueType.objects.create(name='Test Type', 
            issue_group=self.test_issue_type_group)

        test_point = GEOSGeometry('POINT(-86.19049071065865 36.56039392897386)')
        self.test_report = Report.objects.create(authority=self.test_authority, report_type=self.test_issue_type, 
            details='', nearest_address='', sender_email='test@email.com', location=test_point)

        test_point = GEOSGeometry('POINT(-86.19049071065865 36.56039392897386)')
        self.test_report_2 = Report.objects.create(authority=self.test_authority, report_type=self.test_issue_type, 
            details='', nearest_address='', sender_email='test@email.com', location=test_point)
        
    def test_get_reports(self):
        data = {'longitude': '-86.19049071065865', 'latitude': '36.56039392897386'}
        response = self.client.get('/api/reports/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 2)

    def test_create_report(self):
        data = {
            'report_type': self.test_issue_type.pk,
            'location': ('-86.62170408951287', '36.57142381906437'),
            'details': 'Test test test test test test',
            'nearest_address': '505 Test Road, Test, TY',
            'sender_email': 'test@email.com',
            'sender_name': 'TestName'
        }
        
        response = self.client.post('/api/reports/create', data=data, format='json')
        self.assertEqual(Report.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_report_outside_report_range(self):
        data = {
            'report_type': self.test_issue_type.pk,
            'location': ('-100.62170408951287', '36.57142381906437'),
            'details': 'Test test test test test test',
            'nearest_address': '505 Test Road, Test, TY',
            'sender_email': 'test@email.com',
            'sender_name': 'TestName'
        }
        
        response = self.client.post('/api/reports/create', data=data, format='json')
        self.assertEqual(Report.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_report_with_no_details(self):
        data = {
            'report_type': self.test_issue_type.pk,
            'location': ('-86.62170408951287', '36.57142381906437'),
            'nearest_address': '505 Test Road, Test, TY',
            'sender_email': 'test@email.com',
            'sender_name': 'TestName'
        }
        
        response = self.client.post('/api/reports/create', data=data, format='json')
        self.assertEqual(Report.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_report_with_no_details(self):
        data = {
            'report_type': self.test_issue_type.pk,
            'location': ('-86.62170408951287', '36.57142381906437'),
            'details': 'Test test test test test test',
            'sender_email': 'test@email.com',
            'sender_name': 'TestName'
        }
        
        response = self.client.post('/api/reports/create', data=data, format='json')
        self.assertEqual(Report.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_report_with_no_report_type(self):
        data = {
            'report_type': '',
            'location': ('-86.62170408951287', '36.57142381906437'),
            'details': 'Test test test test test test',
            'nearest_address': '505 Test Road, Test, TY',
            'sender_email': 'test@email.com',
            'sender_name': 'TestName'
        }

        response = self.client.post('/api/reports/create', data=data, format='json')
        self.assertEqual(Report.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_report_with_no_location(self):
        data = {
            'report_type': self.test_issue_type.pk,
            'location': '',
            'details': 'Test test test test test test',
            'nearest_address': '505 Test Road, Test, TY',
            'sender_email': 'test@email.com',
            'sender_name': 'TestName'
        }

        response = self.client.post('/api/reports/create', data=data, format='json')
        self.assertEqual(Report.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_report_with_no_sender_email(self):
        data = {
            'report_type': self.test_issue_type.pk,
            'location': ('-86.62170408951287', '36.57142381906437'),
            'details': 'Test test test test test test',
            'nearest_address': '505 Test Road, Test, TY',
            'sender_email': '',
            'sender_name': 'TestName'
        }

        response = self.client.post('/api/reports/create', data=data, format='json')
        self.assertEqual(Report.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_report_with_no_sender_name(self):
        data = {
            'report_type': self.test_issue_type.pk,
            'location': ('-86.62170408951287', '36.57142381906437'),
            'details': 'Test test test test test test',
            'nearest_address': '505 Test Road, Test, TY',
            'sender_email': 'test@email.com',
            'sender_name': ''
        }

        response = self.client.post('/api/reports/create', data=data, format='json')
        self.assertEqual(Report.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AdminReportTest(APITestCase):
    def setUp(self):
        report_area = GEOSGeometry('POLYGON ((-86.62170408951287 36.57142381906437, -86.19049071065865 36.56039392897386, -85.92956541772644 36.92135192347484, -86.20697020284396 37.08804885508249, -86.5530395387336 37.09681224924606, -86.82495115978935 36.97183824650084, -86.77551268323343 36.69485093715447, -86.62170408951287 36.57142381906437))')
        self.test_authority = Authority.objects.create(name='Test Authority', authority_type='test', 
            address='testaddress', phone_number='1234567890', email='test@email.com', website_url='', 
            report_range=report_area)

        self.test_issue_type_group = AuthorityIssueTypeGroup.objects.create(name='Test Group', 
            authority=self.test_authority)
        self.test_issue_type = AuthorityIssueType.objects.create(name='Test Type', 
            issue_group=self.test_issue_type_group)

        test_point = GEOSGeometry('POINT(-86.19049071065865 36.56039392897386)')
        self.test_report = Report.objects.create(authority=self.test_authority, report_type=self.test_issue_type, 
            details='', nearest_address='', sender_email='test@email.com', location=test_point)

        self.test_user = User.objects.create_user('test@example.com', 'testpassword', 'testname')
        self.token = Token.objects.create(user=self.test_user)
        self.test_user.authority = self.test_authority
        self.test_user.save()

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_admin_reports(self):
        data = {'longitude': '-86.19049071065865', 'latitude': '36.56039392897386'}
        response = self.client.get(f'/api/authority/{self.test_authority.id}/reports/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 1)

    def test_update_report(self):
        data = {
            'priority': True,
            'state': 2
        }
        
        response = self.client.put(f'/api/authority/{self.test_authority.id}/reports/{self.test_report.id}/update', 
            data=data, format='json')
        self.assertEqual(Report.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_report = Report.objects.get(id=self.test_report.id)
        self.assertEqual(new_report.priority, data['priority'])
        self.assertEqual(new_report.state, data['state'])

    def test_update_report_with_read_only_fields(self):
        data = {
            'details': 'sadadfasdfasdf',
            'nearest_address': 'sdfsDfSDfsdfSDf',
            'priority': True,
            'state': 2
        }
        
        response = self.client.put(f'/api/authority/{self.test_authority.id}/reports/{self.test_report.id}/update', 
            data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_report = Report.objects.get(id=self.test_report.id)
        self.assertEqual(new_report.priority, data['priority'])
        self.assertEqual(new_report.state, data['state'])
        self.assertNotEqual(new_report.details, data['details'])
        self.assertNotEqual(new_report.nearest_address, data['nearest_address'])

    def test_delete_report(self):
        response = self.client.delete(f'/api/authority/{self.test_authority.id}/reports/{self.test_report.id}/delete', 
            format='json')

        self.assertEqual(Report.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AdminReportPermissionsTest(APITestCase):
    def setUp(self):
        report_area = GEOSGeometry('POLYGON ((-86.62170408951287 36.57142381906437, -86.19049071065865 36.56039392897386, -85.92956541772644 36.92135192347484, -86.20697020284396 37.08804885508249, -86.5530395387336 37.09681224924606, -86.82495115978935 36.97183824650084, -86.77551268323343 36.69485093715447, -86.62170408951287 36.57142381906437))')
        self.test_authority = Authority.objects.create(name='Test Authority', authority_type='test', 
            address='testaddress', phone_number='1234567890', email='test@email.com', website_url='', 
            report_range=report_area)

        self.test_issue_type_group = AuthorityIssueTypeGroup.objects.create(name='Test Group', 
            authority=self.test_authority)
        self.test_issue_type = AuthorityIssueType.objects.create(name='Test Type', 
            issue_group=self.test_issue_type_group)

        test_point = GEOSGeometry('POINT(-86.19049071065865 36.56039392897386)')
        self.test_report = Report.objects.create(authority=self.test_authority, report_type=self.test_issue_type, 
            details='', nearest_address='', sender_email='test@email.com', location=test_point)

    def test_get_admin_reports_without_admin_access(self):
        data = {'longitude': '-86.19049071065865', 'latitude': '36.56039392897386'}
        response = self.client.get(f'/api/authority/{self.test_authority.id}/reports/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_report_without_admin_access(self):
        data = {
            'priority': True,
            'state': 2
        }
        
        response = self.client.put(f'/api/authority/{self.test_authority.id}/reports/{self.test_report.id}/update', 
            data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        new_report = Report.objects.get(id=self.test_report.id)
        self.assertNotEqual(new_report.priority, data['priority'])
        self.assertNotEqual(new_report.state, data['state'])

    def test_delete_report_without_admin_access(self):
        response = self.client.delete(f'/api/authority/{self.test_authority.id}/reports/{self.test_report.id}/delete', 
            format='json')
        self.assertEqual(Report.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


