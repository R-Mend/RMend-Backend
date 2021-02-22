import uuid

from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


def get_readable_uid():
    """Gets a readable unique id for authorites auth code"""
    return str(uuid.uuid4())[0:8]

class Authority(models.Model):
    """
    Model for managing authorities' properties like name,
    report range, location, auth code, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    report_range = models.PolygonField()
    authority_type = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(_('email address'))
    website_url = models.CharField(max_length=250, blank=True)
    auth_code = models.CharField(default=get_readable_uid, max_length=8,
      unique=True, null=False, blank=False)

    def __str__(self):
        return self.name

    @classmethod
    def is_name_taken(cls, name):
        """Checks if the given name is already used by another authoritiy"""
        try:
            cls.objects.get(name=name)
            return True
        except Authority.DoesNotExist:
            return False

    def update_name(self, name):
        """Updates and saves the authority's name"""
        if self.is_name_taken(name):
            return
        self.name = name
        self.save()

    def update_type(self, authority_type):
        """Updates and saves the authority's type"""
        self.authority_type = authority_type
        self.save()

    def update_address(self, address):
        """Updates and saves the authority's address"""
        self.address = address
        self.save()

    def update_phone(self, phone_number):
        """Update and saves the authority's phone number"""
        self.phone_number = phone_number
        self.save()

    def update_email(self, email):
        """Updates and saves that authority's email"""
        self.email = email
        self.save()

    def update_website(self, website_url):
        """Updates and saves the authority's website url"""
        self.website_url = website_url


class AuthorityIssueTypeGroup(models.Model):
    """Model for Authoryties' issue groups"""
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE,
      related_name='issue_groups')
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class AuthorityIssueType(models.Model):
    """Model for Authorities' issue types"""
    issue_group = models.ForeignKey(AuthorityIssueTypeGroup,
      related_name='issue_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BaseIssueTypeGroup(models.Model):
    """Model for base issue groups for authories to add to their issue groups"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BaseIssueType(models.Model):
    """Model for base issue groups for authories to add to their issue types"""
    issue_group = models.ForeignKey(BaseIssueTypeGroup,
      related_name='issue_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
