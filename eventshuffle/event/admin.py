# Django library imports
from django.contrib import admin

# Local application imports
from .models import Event


class EventAdmin(admin.ModelAdmin):

    fields = ['name']
    list_display = ['name']

admin.site.register(Event, EventAdmin)
