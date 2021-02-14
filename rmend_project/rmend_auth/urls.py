from django.urls import path

from .views import (UserCreateView, UserLoginView, UserLogoutView, UserView,
CreateEmployeeRequestView, AdminDeleteEmployeeRequestView)


app_name = 'rmend_auth'

urlpatterns = [
    path('users/', UserCreateView.as_view()),
    path('users/me', UserView.as_view()),
    path('users/employee/request', CreateEmployeeRequestView.as_view()),
    path('token/login', UserLoginView.as_view()),
    path('token/logout', UserLogoutView.as_view()),
    path('authority/<int:authority_id>/employee/requests/<int:employee_request_id>/delete', 
      AdminDeleteEmployeeRequestView.as_view())
]