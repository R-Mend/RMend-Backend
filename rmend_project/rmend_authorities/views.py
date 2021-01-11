from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.contrib.gis.geos import Point

from .models import Authority, AuthorityIssueType, AuthorityIssueTypeGroup, BaseIssueTypeGroup, BaseIssueType
from .serializers import AuthoritySerializer, AuthorityIssueTypeGroupSerializer, AuthorityIssueTypeSerializer


# Create your views here.
def AuthorityManagerLoginView(request):
    # Render the login view for RMends authority management console
    return 'Authority Manager Login View'

class IssueTypeGroupView(APIView):
    def get(self, request):
        required_data = {
            'latitude': request.data.get('latatude'),
            'longitude': request.data.get('longitude')
        }
        for data in required_data:
            if required_data[data] is None:
                return Response({'detail': f'Missing required data \'{data}\''}, 
                    status=status.HTTP_406_NOT_ACCEPTABLE)

        pnt = Point(required_data["longitude"], required_data["latitude"])
        issue_type_groups = AuthorityIssueTypeGroup.objects.filter(authority__report_range__contains=pnt)

        serializer = AuthorityIssueTypeGroupSerializer(issue_type_groups, many=True)

class AuthorityIssueTypeGroupView(APIView):
    def get(self, request):
        authority_name = request.data.get('authority_name')
        if authority_name is None:
            return Response({'detial': f'Missing required data \'authority_name\''},
                status=status.HTTP_406_NOT_ACCEPTABLE)
        
        try:
            authority = Authority.objects.get(name='Barren County Road Department')
        except Authority.DoesNotExist:
            return Response({'detial': f'Authority {authority_name} does not exist'},
                status=status.HTTP_404_NOT_FOUND)

        issue_groups = AuthorityIssueTypeGroup.objects.filter(authority=authority.id)
        serializer = AuthorityIssueTypeGroupSerializer(issue_groups, many=True)
        
        return Response({'issue_groups': serializer.data})
    
    def delete(self, request):
        '''Remove a issue type group from the authorities issue type groups'''
        # Verify that all the required info is given
        required_data = {
            'authority_name': request.data.get('authority_name'), 
            'group_name': request.data.get('group_name')
        }
        for data in required_data:
            if required_data[data] is None:
                return Response({'detail': f'Missing required data \'{data}\''},
                    status=status.HTTP_406_NOT_ACCEPTABLE)

        # TODO: Verify user is an admin for the issue type group's authority, return an error if not

        # Verify that the issue type group exist, return an error if not
        try:
            issue_group = AuthorityIssueTypeGroup.objects.get(name=required_data['group_name'], 
                authority__name=required_data['authority_name'])
        except AuthorityIssueTypeGroup.DoesNotExist:
            return Response({'detail': 'The issue group you\'re trying to delete does not exist. \
                Please try refreshing the page and if the group is still showing, contact R.Mend.'},
                status=status.HTTP_404_NOT_FOUND)
        
        # Delete the issue type group
        issue_group.delete()

        # Return a successfull response
        return Response({'success': f'Issue Type Group {issue_group.name} deleted successfully'})

    def post(self, request):
        '''Add a new copy of a issue type group to the authorites issue type groups'''
        # Verify that all the required info is given
        required_data = {
            'authority_name': request.data.get('authority_name'), 
            'group_name': request.data.get('group_name')
        }
        for data in required_data:
            if required_data[data] is None:
                return Response({'detail': f'Missing required data \'{data}\''},
                    status=status.HTTP_406_NOT_ACCEPTABLE)

        # Get the requested authority to add a new group too
        authority = Authority.objects.get(name=required_data['authority_name'])

        # TODO: Verify user is an admin for the issue type group's authority, return an error if not

        # Get the base issue type group to copy into the authorities issue type groups  
        try:
            base_issue_group = BaseIssueTypeGroup.objects.get(name=required_data['group_name'])
        except BaseIssueTypeGroup.DoesNotExist:
            return Response({'detail': 'The issue group you\'re trying to add is not an avalable option'},
                status=status.HTTP_404_NOT_FOUND)

        # Verify that the issue type group doesn't already exist, return an error if so
        issue_group, created = AuthorityIssueTypeGroup.objects.get_or_create(authority=authority, 
            name=required_data['group_name'])
        if not created:
            return Response({'detail': f'Issue Type Group \'{issue_group.name}\' already exist'},
                status=status.HTTP_406_NOT_ACCEPTABLE)
        
        # Return a successfull response
        return Response({'success': f'Issue Group {new_issue_group.name} created successfully'})


class AuthorityIssueTypeView(APIView):
    def delete(self, request):
         # Verify that all the required info is given
        issue_type_name = request.data.get('issue_type_name')
        if issue_type_name is None:
            return Response({'detail': f'Missing required data \'issue_type_name\''},
                status=status.HTTP_406_NOT_ACCEPTABLE)

        # TODO: Verify user is an admin for the issue type group's authority, return an error if not

        # Verify that the issue type exist, return an error if not
        try:
            issue_type = AuthorityIssueType.objects.get(name=issue_type_name)
        except AuthorityIssueType.DoesNotExist:
            return Response({'detail': f'Issue Type {issue_type_name} does not exist'},
                status=status.HTTP_404_NOT_FOUND)

        # Delete the issue type
        issue_type.delete()

        # Return a successfull response
        return Response({'success': f'Issue Type {issue_type.name} deleted successfully'})
    
    def post(self, request):
        # Verify that all the required info is given
        required_data = {
            'issue_group': request.data.get('issue_group'), 
            'type_name': request.data.get('type_name')
        }
        for data in required_data:
            if required_data[data] is None:
                return Response({'detail': f'Missing required data \'{data}\''},
                    status=status.HTTP_406_NOT_ACCEPTABLE)

        # Get the requested issue type group to add a new issue type to
        try:
            issue_group = AuthorityIssueTypeGroup.objects.get(name=required_data['issue_group'])
        except AuthorityIssueTypeGroup.DoesNotExist:
            return Response({'detail': f'Issue Type Group {required_data["issue_group"]} does not exist \
                in your authority'}, status=status.HTTP_404_NOT_FOUND)

        # TODO: Verify user is an admin for the issue type group's authority, return an error if not

        # Get the base issue type group to copy into the authorities issue type groups  
        try:
            base_issue_type = BaseIssueType.objects.get(name=required_data['type_name'])
        except BaseIssueType.DoesNotExist:
            return Response({'detail': 'The issue type you\'re trying to add in not an option'},
                status=status.HTTP_404_NOT_FOUND)

        # Verify that the issue type doesn't already exist, return an error if so
        issue_type, created = AuthorityIssueType.objects.get_or_create(issue_group=issue_group, name=base_issue_type.name)
        if not created:
            return Response({'detail': f'Issue Type \'{issue_type.name}\' already exist'},
                status=status.HTTP_406_NOT_ACCEPTABLE)

        #  Add the new issue group to the authority
        return Response({'success': f'Issue Type {issue_type.name} created successfully'})

    