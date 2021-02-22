from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from .models import Authority, AuthorityIssueTypeGroup, AuthorityIssueType


class AuthoritySerializer(gis_serializers.GeoFeatureModelListSerializer):
    """Rest framework gis serializer for Authority model"""
    employee_requests = serializers.SerializerMethodField('_get_employee_requests')
    
    class Meta:
        """Meta data for AuthoritySerializer class"""
        model = Authority
        geo_field = 'report_range'
        id_field = False
        fields = ['name', 'report_range', 'authority_type', 'address', 'phone_number',
                    'email', 'website_url', 'employee_requests']

    def _get_employee_requests(self, obj):
        """Gets the authorty's employee requests"""
        return obj.employee_requests.all()
                    


# Needed for object serializers that refernce the authority model
class AuthorityModelSerializer(serializers.ModelSerializer):
    """Rest framework model serializer for Authority model"""
    class Meta:
        """Meta data for AuthorityModelSerializer class"""
        model = Authority
        fields = ('name', 'report_range', 'authority_type', 'address', 'phone_number',
                    'email', 'website_url')


class AuthorityIssueTypeGroupSerializer(serializers.ModelSerializer):
    """Rest framework serializer for AuthorityIssueTypeGroup model"""
    authority = serializers.StringRelatedField(read_only=True)
    issue_types = serializers.SerializerMethodField('_get_types')

    class Meta:
        """Meta data for AuthorityIssueTypeGroupSerializer class"""
        model = AuthorityIssueTypeGroup
        fields = ('name', 'authority', 'issue_types')

    def _get_types(self, obj):
        """Gets the authority's issue types"""
        return [issue_type.name for issue_type in obj.issue_types.all()]


class AuthorityIssueTypeSerializer(serializers.ModelSerializer):
    """Rest framework serializer for the AuthorityIssueType model"""
    issue_group = serializers.StringRelatedField(read_only=True)
    class Meta:
        """Meta data for AuthorityIssueTypeSerializer class"""
        model = AuthorityIssueType
        fields = ('name', 'issue_group')
