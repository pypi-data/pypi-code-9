"""Setup the admin page so admins can view, make, and modify events."""
from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):
    # Display related fields in fieldsets.
    fieldsets = [
        ('Title info', {'fields': ['title', 'detail']}),
        ('Outcome info', {'fields': ['outcome', 'outcome_detail']}),
        ('Event date', {'fields': ['date']}),
        ('Contact info', {'fields': ['contact_name', 'contact_email']}),
    ]
    # Show the title, date, creation_date, and outcome in the event list.
    list_display = ('title', 'date', 'entry_created', 'outcome')
    # Allow an admin to filter events by the event date.
    list_filter = ['date', 'entry_created']
    # Allow an admin to search events by title.
    search_fields = ['title']


# Register the Event model on the admin page.
admin.site.register(Event, EventAdmin)
