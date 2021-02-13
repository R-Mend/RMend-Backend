from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render, get_object_or_404
from django.contrib.gis.geos import Point

from .models import Authority, AuthorityIssueType, AuthorityIssueTypeGroup, BaseIssueTypeGroup, BaseIssueType
from .serializers import AuthoritySerializer, AuthorityIssueTypeGroupSerializer, AuthorityIssueTypeSerializer
from .permissions import IsAuthorityAdmin


# Create your views here.
class IssueTypeGroupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        location = request.data.get('location')
        if not location:
            return missing_requred_data_error('location')

        pnt = Point(location[0], location[1])
        issue_type_groups = AuthorityIssueTypeGroup.objects.filter(authority__report_range__touches=pnt)
        
        serializer = AuthorityIssueTypeGroupSerializer(issue_type_groups, many=True)
        return Response({'issue_groups': serializer.data})


class AuthorityIssueTypeGroupView(APIView):
    permission_classes = [IsAuthenticated, IsAuthorityAdmin]

    def get(self, request, *args, **kwargs):
        authority_id = kwargs.get('authority_id', '')
        if not authority_id:
            return missing_requred_data_error('authority_id')
        
        try:
            authority = Authority.objects.get(id=authority_id)
        except Authority.DoesNotExist:
            return data_does_not_exist_error('Authority', authority_id)

        self.check_object_permissions(request, authority)

        issue_groups = AuthorityIssueTypeGroup.objects.filter(authority=authority.id)
        serializer = AuthorityIssueTypeGroupSerializer(issue_groups, many=True)
        return Response({'issue_groups': serializer.data})

class AuthorityIssueTypeGroupCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAuthorityAdmin]

    def post(self, request, authority_id):
        '''Add a new copy of a issue type group to the authorites issue type groups'''
        # Verify that all the required info is given
        group_name = request.data.get('group_name')
        if not authority_id or not group_name:
            return missing_requred_data_error('authority_id' if not authority_id else 'group_name')

        # Get the requested authority to add a new group too or return error
        try:
            authority = Authority.objects.get(id=authority_id)
        except Authority.DoesNotExist:
            return not_authority_admin_error('Authority', authority_id)

        # Verify that the request user is an admin of the authority
        self.check_object_permissions(request, authority)

        # Get the base issue type group to copy into the authorities issue type groups  
        try:
            BaseIssueTypeGroup.objects.get(name=group_name)
        except BaseIssueTypeGroup.DoesNotExist:
            return data_does_not_exist_error('Issue Type Group', group_name)

        # Verify that the issue type group doesn't already exist, return an error if so
        issue_group, created = AuthorityIssueTypeGroup.objects.get_or_create(name=group_name, 
            authority=authority)
        if not created:
            return data_already_exist_error('Issue Type Group', issue_group.name)
        
        # Return a successfull response
        return Response({'success': f'Issue Group {issue_group.name} created successfully'})

class AuthorityIssueTypeGroupDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAuthorityAdmin]

    def delete(self, request, authority_id):
        '''Remove a issue type group from the authorities issue type groups'''
        group_name = request.data.get('group_name')
        if not authority_id or not group_name:
            return missing_requred_data_error('authority_id' if not authority_id else 'group_name')
        
        try:
            issue_group = AuthorityIssueTypeGroup.objects.get(name=group_name, authority__id=authority_id)
        except AuthorityIssueTypeGroup.DoesNotExist:
            return data_does_not_exist_error('Authority', authority_id)
        
        self.check_object_permissions(request, issue_group)
        
        issue_group.delete()
        return Response({'success': f'Issue Type Group {issue_group.name} deleted successfully'})

class AuthorityIssueTypeCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAuthorityAdmin]
    
    def post(self, request, authority_id):
        # Verify that all the required info is given
        issue_group_name = request.data.get('issue_group_name')
        type_name = request.data.get('type_name')
        if not issue_group_name or not type_name:
            return missing_requred_data_error('issue_group' if not issue_group_name else 'type_name')

        # Get the requested issue type group to add a new issue type to
        try:
            issue_group = AuthorityIssueTypeGroup.objects.get(name=issue_group_name, authority__id=authority_id)
        except AuthorityIssueTypeGroup.DoesNotExist:
            return data_does_not_exist_error('Issue Type Group', issue_group_name)

        # Verify that user has delete access to this groups authority
        self.check_object_permissions(request, issue_group)

        # Get the base issue type group to copy into the authorities issue type groups  
        try:
            base_issue_type = BaseIssueType.objects.get(name=type_name, issue_group__name=issue_group_name)
        except BaseIssueType.DoesNotExist:
            return data_does_not_exist_error('Issue Type', type_name)

        # Verify that the issue type doesn't already exist, return an error if so
        issue_type, created = AuthorityIssueType.objects.get_or_create(issue_group=issue_group, 
            name=base_issue_type.name)
        if not created:
            return data_already_exist_error('Issue Type', issue_type.name)

        #  Add the new issue group to the authority
        return Response({'success': f'Issue Type {issue_type.name} created successfully'})

class AuthorityIssueTypeDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAuthorityAdmin]

    def delete(self, request, authority_id):
         # Verify that all the required info is given
        type_name = request.data.get('type_name')
        if type_name is None:
            return missing_requred_data_error('type_name')

        # Verify that the issue type exist, return an error if not
        try:
            issue_type = AuthorityIssueType.objects.get(name=type_name, issue_group__authority=authority_id)
        except AuthorityIssueType.DoesNotExist:
            return data_does_not_exist_error('Issue Type', type_name)

        # Verify that user has delete access to this groups authority
        self.check_object_permissions(request, issue_type.issue_group)

        # Delete the issue type and return a successful response
        issue_type.delete()
        return Response({'success': f'Issue Type {issue_type.name} deleted successfully'})
    

# Error helper functions
def missing_requred_data_error(data):
    return Response({'detial': f'Missing required data {data}'},
                status=status.HTTP_400_BAD_REQUEST)

def data_does_not_exist_error(data_type, data):
    return Response({'detial': f'{data_type} {data} does not exist'},
                status=status.HTTP_400_BAD_REQUEST)

def data_already_exist_error(data_type, data):
    return Response({'detail': f'{data_type} {data} already exist'},
                status=status.HTTP_406_NOT_ACCEPTABLE)