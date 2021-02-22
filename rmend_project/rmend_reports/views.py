from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.gis.measure import D # Distance
from django.contrib.gis.geos import Point

from rmend_authorities.models import Authority, AuthorityIssueType
from .serializers import AdminReportSeralizer, ReportGetSeralizer, ReportCreateSerializer
from .permissions import IsAuthorityAdmin
from .models import Report


class ReportView(APIView):
    """API view for getting reports based on a given location"""
    permission_classes = [AllowAny]

    def get(self, request):
        """Gets a list of report 10 miles from the given location"""
        # Verify the required data is given
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        if not latitude or not longitude:
            return missing_requred_data_error('latitude' if not latitude else 'longitude')

        # Get all reports from 5 miles from the users location
        pnt = Point(float(longitude), float(latitude))
        reports = Report.objects.filter(location__distance_lte=(pnt, D(mi=10)))

        # Serialize and return the found reports
        serializer = ReportGetSeralizer(reports, many=True)
        return Response(dict(serializer.data))

class ReportCreateView(APIView):
    """API view for creating reports"""
    # TODO: Determin if report creation will required authenticatied users or not
    permission_classes = [AllowAny]

    def post(self, request):
        """Creates a new report with the given report information"""
        # Verify that the required data is given
        required_data = set(['report_type', 'location', 'sender_email', 'sender_name'])
        for key in required_data:
            if key not in request.data or not request.data[key]:
                return missing_requred_data_error(key)

        # Verify that the issue group and thus authority exist
        try:
            issue_type = AuthorityIssueType.objects.get(id=request.data['report_type'])
        except AuthorityIssueType.DoesNotExist:
            return data_does_not_exist_error('Issue Type', request.data['report_type'])
        request.data['report_type'] = issue_type.id
        request.data['authority'] = issue_type.issue_group.authority.id

        # Verify that the location is in range of current authorities
        pnt = Point(float(request.data['location'][0]), float(request.data['location'][1]))
        if len(Authority.objects.filter(report_range__touches=pnt)) == 0:
            return out_of_range_error()
        request.data['location'] = pnt

        # Save the report if the given data is valid
        serializer = ReportCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        # Return a successfull responce message
        return Response({'success': f'Report {issue_type.name} created successfully'})

class AdminReportView(APIView):
    """API view for admin users to get admin level info on reports"""
    permission_classes = [IsAuthenticated, IsAuthorityAdmin]

    def get(self, request, *args, **kwargs):
        """Gets a list of reports with an authority of the admin user"""
        # Verify the required data is given
        authority_id = kwargs.get('authority_id')
        if not authority_id:
            return missing_requred_data_error('authority_id')

        # Get all the reports from the requested authority
        reports = Report.objects.filter(authority=authority_id)

        # Verify that the user is part of the requested authority
        self.check_object_permissions(request, reports[0])

        serializer = AdminReportSeralizer(reports, many=True)
        return Response(serializer.data)

class AdminReportUpdateView(APIView):
    """API view for admins to update reports"""
    permission_classes = [IsAuthenticated, IsAuthorityAdmin]

    def put(self, request, authority_id, report_id):
        """Updates the requested report with the given information"""
        # Verify that the required data is given
        if not authority_id or not report_id:
            return missing_requred_data_error('authority_id' if not authority_id else 'report_id')

        # Verify that the report requested to update exist, return an error if not
        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return data_does_not_exist_error('Report', report.id)

        # Verify that the user is an admin of the reports authority
        self.check_object_permissions(request, report)

        # Save the report if the data given is valid
        serializer = AdminReportSeralizer(report, request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            report_saved = serializer.save()

        # Return a successfull responce message
        return Response({'success': f'Report {report_saved.report_type.name} updated successfully'})

class AdminReportDeleteView(APIView):
    """API view for admin to delete reports"""
    permission_classes = [IsAuthenticated, IsAuthorityAdmin]

    def delete(self, request, authority_id, report_id):
        """Deltes the requested report if the users is an admin of the reports authority"""
        # Verify that the required data is given
        if not authority_id or not report_id:
            return missing_requred_data_error('authority_id' if not authority_id else 'report_id')

        # Get the report to delete and throw an error if it doesn't exist
        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return data_does_not_exist_error('Report', report_id)

        # Verify that the user is an admin of the reports authority
        self.check_object_permissions(request, report)

        # Delete the report matching the given id and return a successful response
        report.delete()
        return Response({'success': f'Report {report.report_type.name} delete successfully'})


# Error helper functions
def out_of_range_error():
    """Returns an response error for when a reports location is out of range"""
    return Response(
        {'detial': 'Sorry. The report you\'re trying to create is out of R.Mends report range'},
        status=status.HTTP_400_BAD_REQUEST)

def missing_requred_data_error(data):
    """Returns a response error for when required data for a model is missing"""
    return Response({'detial': f'Missing required data {data}'},
                status=status.HTTP_400_BAD_REQUEST)

def data_does_not_exist_error(data_type, data):
    """Returns a response error for when requested data does not exist"""
    return Response({'detial': f'{data_type} {data} does not exist'},
                status=status.HTTP_400_BAD_REQUEST)

def field_provided_is_not_editable_error(data):
    """Return an response error for when trying to update a field that is non-editable"""
    return Response({'detial': f'{data} is not editable'}, status=status.HTTP_400_BAD_REQUEST)
