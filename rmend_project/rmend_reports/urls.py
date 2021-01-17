from django.urls import path
from .views import AdminReportView, AdminReportUpdateView, AdminReportDeleteView
from .views import ReportView, ReportCreateView


app_name = "rmend_reports"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('reports/', ReportView.as_view()),
    path('reports/create', ReportCreateView.as_view()),
    path('authority/<int:authority_id>/reports/', AdminReportView.as_view()),
    path('authority/<int:authority_id>/reports/<int:report_id>/update', AdminReportUpdateView.as_view()),
    path('authority/<int:authority_id>/reports/<int:report_id>/delete', AdminReportDeleteView.as_view()),
]