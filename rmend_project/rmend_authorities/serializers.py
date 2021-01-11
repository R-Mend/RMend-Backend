from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from .models import Authority, AuthorityIssueTypeGroup, AuthorityIssueType


class AuthoritySerializer(gis_serializers.GeoFeatureModelListSerializer):
    class Meta:
        model = Authority
        geo_field = 'report_range'
        id_field = False
        fields = ['name', 'report_range', 'authority_type', 'address', 'phone_number', 
                    'email', 'website_url']

# Needed for object serializers that refernce the authority model
class AuthorityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authority
        fields = ('name', 'report_range', 'authority_type', 'address', 'phone_number', 
                    'email', 'website_url')

class AuthorityIssueTypeGroupSerializer(serializers.ModelSerializer):
    authority = serializers.StringRelatedField(read_only=True)
    issue_types = serializers.SerializerMethodField('_get_types')

    class Meta:
        model = AuthorityIssueTypeGroup
        fields = ('name', 'authority', 'issue_types')

    def _get_types(self, obj):
        return [issue_type.name for issue_type in obj.issue_types.all()]

    def create(self, validated_data):
        return AuthorityIssueTypeGroup.objects.create(**validated_data)

class AuthorityIssueTypeSerializer(serializers.ModelSerializer):
    issue_group = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = AuthorityIssueType
        fields = ('name', 'issue_group')

    def create(self, validated_data):
        return AuthorityIssueType.objects.create(**validated_data)

class AuthorityIssueTypeSerializer(serializers.ModelSerializer):
    issue_group = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = AuthorityIssueType
        fields = ('name', 'issue_group')

    def create(self, validated_data):
        return AuthorityIssueType.objects.create(**validated_data)

        