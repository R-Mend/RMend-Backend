from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.gis.measure import D # Distance
from django.contrib.gis.geos import Point

from .models import Report
from rmend_authorities.models import Authority
from .serializers import AdminReportSeralizer, ReportSeralizer


# Create your views here.
class ReportView(APIView):
    def get(self, request):
        # Verify the required data is given
        required_data = {
            'latitude': request.data.get('latitude'),
            'longitude': request.data.get('longitude')
        }
        for data in required_data:
            if required_data[data] is None:
                return Response({'detial': f'Missing required data \'{data}\''},
                    status=status.HTTP_406_NOT_ACCEPTABLE)

        # Get all reports from 5 miles from the users location 
        pnt = Point(required_data['longitude'], required_data['latitude'])
        reports = Report.objects.filter(location__distance_lte=(pnt, D(mi=5)))

        # Serialize and return the found reports
        serializer = ReportSeralizer(reports, many=True)
        return Response({'reports': serializer.data})

    def post(self, request):
        # Verify that the required data is given
        required_data = {
            'authority_name': request.data.get('authority_name'),
            'report': request.data.get('report')
        }
        for data in required_data:
            if required_data[data] is None:
                return Response({'detail': f'Missing required data \'{data}\''},
                    status=status.HTTP_406_NOT_ACCEPTABLE)

        # Verify that the authority requested to upload to exist, return an error if not
        try:
            Authority.objects.get(name=request.data.get('authority_name'))
        except Authority.DoesNotExist:
            return Response({'detial': f'Authority {required_data["authority_name"]} does not exist'},
                status=status.HTTP_404_NOT_FOUND)

        # Format data into a report object
        serializer = AdminReportSeralizer(data=required_data['report'])

        # Save the report if the data is valid
        if serializer.is_valid(raise_exception=True):
            report_saved = serializer.save()

        # Return a successfull responce message
        return Response({'success': f'Report {report_saved.report_type} created successfully'})


class AdminReportView(APIView):
    def get(self, request):
        # Verify the required data is given
        authority_id = request.data.get('authority_id')
        if authority_id is None:
            return Response({'detail': 'Missing required data \'authority_id\''},
                status=status.HTTP_406_NOT_ACCEPTABLE)

        # TODO: Verify that the user is part of the requested authority

        # Get all the reports from the requested authority
        reports = Report.objects.filter(authority=authority_id)

        serializer = AdminReportSeralizer(reports, many=True)
        return Response({"reports": serializer.data})

    def put(self, request):
        # Verify that the required data is given
        required_data = {
            'report_id': request.data.get('report_id'),
            'report': request.data.get('report')
        }
        for data in required_data:
            if required_data[data] is None:
                return Response({'detail': f'Missing required data \'{data}\''},
                    status=status.HTTP_406_NOT_ACCEPTABLE)

        # TODO: Verify that the user is an admin and that they're from the reports authority, 
        #   return error if either is false 

        # Verify that the report requested to update exist, return an error if not
        try:
            report = Report.objects.get(name=required_data['report_id'])
        except Report.DoesNotExist:
            return Response({'detail': 'The report you\'re trying to update does not exist'},
                status=status.HTTP_404_NOT_FOUND)

        # Format data into a report object
        serializer = AdminReportSeralizer(instance=report, data=required_data['report'], partial=True)

        # Save the report 
        if serializer.is_valid(raise_exception=True):
            report_saved = serializer.save()

        # Return a successfull responce message
        return Response({'success': f'Report {report_saved.report_type} updated successfully'})

    def delete(self, request):
        # Verify that the required data is given
        report_id = request.data.get('report_id')
        if report_id is None:
            return Response({'detail': f'Missing required data \'report_id\''},
                status=status.HTTP_406_NOT_ACCEPTABLE)

        # TODO: Authenticate that the user is an admin and that they're from the reports authority, 
        #   return error if either is false 

        # Get the report to delete and throw an error if it doesn't exist
        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return Response({'detail': f'Report {report_id} does not exist'},
                status=status.HTTP_404_NOT_FOUND)

        # Delete the report matching the given id
        report.delete()

        # Return a successfull responce message
        return Response({'success': f'Report {report.report_type} delete successfully'})