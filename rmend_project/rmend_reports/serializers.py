from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from .models import Report
from rmend_authorities.serializers import AuthorityModelSerializer, AuthorityIssueTypeSerializer


class AdminReportSeralizer(gis_serializers.GeoFeatureModelSerializer):
    report_type = AuthorityIssueTypeSerializer(read_only=True)

    class Meta:
        model = Report
        geo_field = "location"
        id_field = False # we don't want to return id field in the response
        fields = ("location", 'authority', 'details', 'date_created', 'report_type', 'nearest_address',
                    'sender_email', 'sender_name', 'sender_phone', 'priority', 'state')

        def create(self, validated_data):
            return Report.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.priority = validated_data.get('priority', instance.priority)
            instance.state = validated_data.get('state', instance.state)
            instance.save()
            return instance


class ReportSeralizer(gis_serializers.GeoFeatureModelSerializer):
    authority = serializers.StringRelatedField(read_only=True)
    report_type = AuthorityIssueTypeSerializer(read_only=True)

    class Meta:
        model = Report
        geo_field = "location"
        id_field = False # we don't want to return id field in the response
        fields = ("location", 'authority', 'details', 'date_created', 'report_type', 'nearest_address', 
                    'state')