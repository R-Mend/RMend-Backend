from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class Report(models.Model):
    authority = models.ForeignKey('rmend_authorities.Authority', on_delete=models.CASCADE)
    location = models.PointField(editable=False)
    detials = models.TextField(blank=True, null=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    report_type = models.CharField(max_length=100, editable=False)
    nearest_address = models.TextField(blank=True, null=True, editable=False)

    sender_email = models.EmailField(_('email address'), editable=False)
    sender_name = models.CharField(max_length=100, editable=False, editable=False)
    sender_phone = models.CharField(max_length=100, blank=True, null=True, editable=False)

    priority = models.BooleanField(default=False)

    class Status(models.TextChoices):
        REPORTED = 1, _('Reported')
        REVIEWING = 2, _('Reviewing')
        COMPLETED = 3, _('Completed')
    state = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.Reported
    )

    def update_state(self, state):
        if state in (x[0] for x in self.Status.choices):
            self.state = state
            self.save()
            return True
        return False
            
    def toggle_priority(self):
        self.priority = not self.priority
        self.save()
