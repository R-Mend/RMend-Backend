from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from rmend_authorities.serializers import AuthorityModelSerializer, AuthorityIssueTypeSerializer
from .models import Report


class AdminReportSeralizer(gis_serializers.GeoFeatureModelSerializer):
    """Rest framework model for serializing reports information for admin users"""
    report_type = AuthorityIssueTypeSerializer(read_only=True)

    class Meta:
        model = Report
        geo_field = 'location'
        fields = ('location', 'authority', 'details', 'date_created', 'report_type', 'nearest_address',
                    'sender_email', 'sender_name', 'sender_phone', 'priority', 'state')

    def update(self, instance, validated_data):
        instance.priority = validated_data.get('priority', instance.priority)
        instance.state = validated_data.get('state', instance.state)
        instance.save()
        return instance

class ReportGetSeralizer(gis_serializers.GeoFeatureModelSerializer):
    """Rest framework model for serializing list of reports for general users"""
    authority = serializers.StringRelatedField(read_only=True)
    report_type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Report
        geo_field = "location"
        fields = ("location", 'authority', 'details', 'date_created', 'report_type', 'nearest_address',
                    'state')

class ReportCreateSerializer(gis_serializers.GeoFeatureModelSerializer):
    """Rest frameork model for serializing reports for creation by general users"""
    class Meta:
        model = Report
        geo_field = "location"
        fields = ("location", 'authority', 'details', 'date_created', 'report_type', 'nearest_address',
                    'state', 'sender_email', 'sender_name', 'sender_phone')

    def create(self, validated_data):
        return Report.objects.create(**validated_data)
