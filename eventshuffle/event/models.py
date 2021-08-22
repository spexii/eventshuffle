# Standard library imports
import uuid

# Django library imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    """
    The class for events
    """

    id = models.UUIDField(
        _("Unique id for the event"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        _("Event name"),
        max_length=255
    )

    def __str__(self):
        return f"{self.name} ({self.id})"

    def get_dates(self):
        """Gets event related dates

        Returns:
            list: All the suitable dates for the event
        """
        return [ed.date for ed in EventDate.objects.filter(event=self)]


class EventDateVoter(models.Model):
    """
    The class for event voters
    """

    id = models.UUIDField(
        _("Unique id for the event voter"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        _("Event voter name"),
        max_length=255
    )

    def __str__(self):
        return f"{self.name} ({self.id})"


class EventDate(models.Model):
    """
    The connecting model for events and dates
    """
    id = models.UUIDField(
        _("Unique id for the event / date connection"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )

    date = models.DateField(
        _("Suitable date for the event"),
    )

    voters = models.ManyToManyField(
        EventDateVoter,
        blank=True
    )

    def __str__(self):
        return f"{self.event.name} - {self.date} ({self.id})"
