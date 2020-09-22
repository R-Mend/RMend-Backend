from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import UserManager
import uuid


class User(AbstractUser):
    first_name = None
    last_name = None

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_('email address'), unique=True,)
    is_email_verified = models.BooleanField(default=False,)
    is_deleted = models.BooleanField(_('is deleted'), default=False,)
    username = models.CharField(max_length=100, blank=False, null=False,)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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

    def update_username(self, username):
        check_username_not_taken(user=self, username=username)
        self.username = username
        self.save()

    def update_password(self, password):
        self.set_password(password)
        self._reset_auth_token()
        self.save()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayName = models.CharField(max_length=100, default='', blank=True)
    phoneNumber = models.CharField(max_length=20, default='', blank=True)
    authCode = models.CharField(max_length=100, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    def __repr__(self):
        return '<UserProfile %s>' % self.user.username

    def __str__(self):
        return self.user.username
