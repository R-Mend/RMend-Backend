from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import UserManager
from rmend_authorities.models import Authority
import re


class User(AbstractUser):
    first_name = None
    last_name = None

    email = models.EmailField(_('email address'), unique=True,)
    username = models.CharField(max_length=100, blank=False, null=False,)
    phone_number = models.CharField(max_length=20, default='', blank=True)
    auth_code = models.CharField(max_length=100, default='', blank=True)

    authority = models.ForeignKey(Authority, on_delete=models.SET_NULL, null=True, blank=True,
         related_name='admin_users')
    is_admin = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False,)
    is_deleted = models.BooleanField(_('is deleted'), default=False,)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number', 'auth_code']
    objects = UserManager()

    def __str__(self):
        return self.email

    @classmethod
    def is_email_taken(cls, email):
        try:
            cls.objects.get(email=email)
            return True
        except User.DoesNotExist:
            return False

    @classmethod
    def get_temporary_username(cls, email):
        username = email.split('@')[0]
        temp_username = cls.sanitise_username(username)
        return temp_username

    @classmethod
    def sanitise_username(cls, username):
        return re.sub('[^a-zA-Z]', '', username)

    def update_username(self, username):
        check_username_not_taken(user=self, username=username)
        self.username = username
        self.save()

    def update_password(self, password):
        self.set_password(password)
        self._reset_auth_token()
        self.save()
