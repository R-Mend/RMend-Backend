from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from rmend_authorities.models import Authority
from .managers import UserManager


class User(AbstractUser):
    """
    Custom user model where email is the unique identifiers
    for authentication instead of usernames.
    """
    first_name = None
    last_name = None

    email = models.EmailField(_('email address'), unique=True,)
    username = models.CharField(max_length=100, blank=False, null=False,)
    phone_number = models.CharField(max_length=20, default='', blank=True)
    auth_code = models.CharField(max_length=100, default='', blank=True)

    authority = models.ForeignKey(
        Authority, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='admin_users', editable=True
    )
    is_admin = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False,)
    is_deleted = models.BooleanField(_('is deleted'), default=False,)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number', 'auth_code']
    objects = UserManager()

    def __str__(self):
        return self.email

    def update_username(self, username):
        """Updates and saves the users username"""
        self.username = username
        self.save()

    def update_password(self, password):
        """Updates and saves users password and resets users auth token"""
        self.set_password(password)
        self._reset_auth_token()
        self.save()

class EmployeeRequest(models.Model):
    """
    Employee request model for allowing users to request to be
    an employee to an authority
    """
    authority = models.ForeignKey(
        Authority, related_name='employee_requests',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, related_name='employee_requests', on_delete=models.CASCADE)
