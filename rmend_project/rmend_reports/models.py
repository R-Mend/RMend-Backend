from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class Report(models.Model):
    """
    Model for managin reports properites like 
    location, type, authority, priority, state
    """
    authority = models.ForeignKey('rmend_authorities.Authority', on_delete=models.CASCADE)
    report_type = models.ForeignKey('rmend_authorities.AuthorityIssueType', null=True, on_delete=models.SET_NULL)
    location = models.PointField()
    details = models.TextField(blank=True, editable=False)
    nearest_address = models.TextField(blank=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    sender_email = models.EmailField(_('email address'), editable=False)
    sender_name = models.CharField(max_length=100, editable=False)
    sender_phone = models.CharField(max_length=100, blank=True, editable=False)

    priority = models.BooleanField(default=False)

    class Status(models.IntegerChoices):
        """Choice field for keeping the reports current status"""
        REPORTED = 1, _('Reported')
        REVIEWING = 2, _('Reviewing')
        COMPLETED = 3, _('Completed')
    state = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.REPORTED
    )

    def __str__(self):
        """String representation fo a report object"""
        return f'{self.sender_email} - {self.date_created}'

    def update_state(self, state):
        """Updates the state of the report"""
        if state in (x[0] for x in self.Status.choices):
            self.state = state
            self.save()
            return True
        return False
            
    def toggle_priority(self):
        """Toggles the reports priority to true or false"""
        self.priority = not self.priority
        self.save()
