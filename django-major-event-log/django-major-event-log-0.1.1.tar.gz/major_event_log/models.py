"""Model definition.

The Event class defines all the data required in order to create a
major PREMIS event.
"""
import uuid

from django.db import models
from django.core.urlresolvers import reverse


class Event(models.Model):
    SUCCESS = 'http://purl.org/NET/UNTL/vocabularies/eventOutcomes/#success'
    FAILURE = 'http://purl.org/NET/UNTL/vocabularies/eventOutcomes/#failure'
    OUTCOME_CHOICES = (
        (SUCCESS, 'Success'),
        (FAILURE, 'Failure'),
    )
    # Unique identifier for each event. Primary key.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    detail = models.TextField()
    outcome = models.CharField(max_length='80',
                               choices=OUTCOME_CHOICES)
    outcome_detail = models.TextField()
    # Date of the event, NOT the date of entry.
    date = models.DateTimeField()
    entry_created = models.DateTimeField(auto_now_add=True)
    entry_modified = models.DateTimeField(auto_now=True)
    # The contact_name attribute will be used as the reporting agent.
    contact_name = models.CharField(max_length=100,
                                    help_text='Appears as the Reporting Agent')
    contact_email = models.EmailField()

    def get_absolute_url(self):
        return(reverse('major-event-log:event_details', args=[self.id]))

    def is_success(self):
        return self.outcome == self.SUCCESS

    class Meta:
        ordering = ['date']

    def __unicode__(self):
        return self.title
