from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class Authority(models.Model):
    name = models.CharField(max_length=100, unique=True)
    report_range = models.PolygonField()
    authority_type = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(_('email address'))
    website_url = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def is_name_taken(cls, name):
        try:
            cls.objects.get(name=name)
            return True
        except Authority.DoesNotExist:
            return False

    def update_name(self, name):
        if is_name_taken(name):
            return
        self.name = name
        self.save()

    def update_type(self, authority_type):
        self.authority_type = authority_type
        self.save()

    def update_address(self, address):
        self.address = address
        self.save()

    def update_phone(self, phone_number):
        self.phone_number = phone_number
        self.save()

    def update_email(self, email):
        self.email = email
        self.save()
    
    def update_website(self, website_url):
        self.website_url = website_url

    
class AuthorityIssueGroup(models.Model):
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def is_name_taken(cls, name):
        try:
            cls.objects.get(name=name)
            return True
        except Authority.DoesNotExist:
            return False

    def update_name(self, name):
        if is_name_taken(name):
            return
        self.name = name
        self.save()

class AuthorityIssue(models.Model):
    issue_group = models.ForeignKey(AuthorityIssueGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

    @classmethod
    def is_name_taken(cls, name):
        try:
            cls.objects.get(name=name)
            return True
        except Authority.DoesNotExist:
            return False

    def update_name(self, name):
        if is_name_taken(name):
            return
        self.name = name
        self.save()

