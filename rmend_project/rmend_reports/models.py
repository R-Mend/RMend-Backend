from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class Report(models.Model):
    authority = models.ForeignKey('rmend_authorities.Authority', on_delete=models.CASCADE)
    report_type = models.ForeignKey('rmend_authorities.AuthorityIssueType', null=True, on_delete=models.SET_NULL)
    location = models.PointField()
    details = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    nearest_address = models.TextField(blank=True, null=True)

    sender_email = models.EmailField(_('email address'))
    sender_name = models.CharField(max_length=100)
    sender_phone = models.CharField(max_length=100, blank=True, null=True)

    priority = models.BooleanField(default=False)

    class Status(models.IntegerChoices):
        REPORTED = 1, _('Reported')
        REVIEWING = 2, _('Reviewing')
        COMPLETED = 3, _('Completed')
    state = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.REPORTED
    )

    def __str__(self):
        return f'{self.sender_email} - {self.date_created}'

    def update_state(self, state):
        if state in (x[0] for x in self.Status.choices):
            self.state = state
            self.save()
            return True
        return False
            
    def toggle_priority(self):
        self.priority = not self.priority
        self.save()
