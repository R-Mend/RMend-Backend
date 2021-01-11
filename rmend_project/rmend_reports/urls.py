from django.urls import path
from .views import AdminReportView, ReportView


app_name = "rmend_reports"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('reports/', ReportView.as_view()),
    path('reports-admin/', AdminReportView.as_view())
]