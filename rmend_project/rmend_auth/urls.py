from django.urls import path

from .views import UserCreateView, UserLoginView, UserLogoutView, UserView


app_name = 'rmend_auth'

urlpatterns = [
    path('users/', UserCreateView.as_view()),
    path('users/me', UserView.as_view()),
    path('token/login', UserLoginView.as_view()),
    path('token/logout', UserLogoutView.as_view())
]