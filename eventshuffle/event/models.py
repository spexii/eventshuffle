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
