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

    def get_votes(self, suitable_for_all=False):
        """Gets by default all the event dates with corresponding votes.
        If suitable for all is True, this returns only the event dates
        that are suitable for all voters of this event.

        Args:
            suitable_for_all (bool, optional): Are only dates suitable for all returned. Defaults to False.

        Returns:
            list: List of objects containing dates and votes for them.
        """
        votes = []

        # The default queryset is to get all dates for the event
        queryset = EventDate.objects.filter(event=self).order_by("date")

        # If only dates suitable for all voters of the event are wanted,
        # the queryset must be modified
        if suitable_for_all:
            # Get all distinct voters of this event
            all_voters = EventDate.get_all_voters(self)

            # The following queryset gets all event date objects, that voted
            # exactly by all voters of this event
            queryset = EventDate.objects.filter(
                event=self,
                voters__in=all_voters
            ).annotate(
                count=models.Count('voters')
            ).filter(
                count=len(all_voters)
            )

        # Build the vote object for the serializer
        for ed in queryset:
            vote = {
                "date": ed.date,
                "people": []
            }

            for voter in ed.voters.all():
                vote["people"].append(voter.name)

            votes.append(vote)

        return votes


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

    @staticmethod
    def get_all_voters(event):
        """Gets a distinct list of voters from all dates of the event.

        Args:
            event (Event): The related event

        Returns:
            set: All the voters
        """
        # Voters are added to set to exclude duplicates
        voters = set()

        # Go through event dates of the event and build the list of distinct voters 
        for ed in EventDate.objects.filter(event=event).order_by("date"):
            voters = voters.union(ed.voters.all())

        return voters