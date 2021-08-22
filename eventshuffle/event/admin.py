# Django library imports
from django.contrib import admin

# Local application imports
from .models import Event, EventDate, EventDateVoter


class EventDateInline(admin.TabularInline):
    """
    The connecting event date model is added as an inline to
    a single event object in admin.
    """
    model = EventDate


class EventAdmin(admin.ModelAdmin):
    """
    The admin class for event model
    """
    fields = ['name']
    list_display = ['id', 'name']

    inlines = [EventDateInline]


class EventDateAdmin(admin.ModelAdmin):
    """
    The admin class for the connecting event date model
    """
    fields = ['event', 'date', 'voters']
    list_display = ['id', 'event', 'date']


class EventDateVoterAdmin(admin.ModelAdmin):
    """
    The admin class for event date voter model
    """
    fields = ['name']
    list_display = ['id', 'name']


admin.site.register(Event, EventAdmin)
admin.site.register(EventDate, EventDateAdmin)
admin.site.register(EventDateVoter, EventDateVoterAdmin)
