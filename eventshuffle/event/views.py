# Third party imports
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Local application imports
from .functions import validate_dates
from .models import Event, EventDate, EventDateVoter
from .serializers import EventListSerializer, EventRetrieveSerializer, EventRetrieveResultSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for events
    """
    queryset = Event.objects.all().order_by('name')
    serializer_class = EventListSerializer

    def get_serializer_class(self):
        """Defines a different serializer for single event retrieve view.

        Returns:
            Serializer: The serializer to use
        """

        if self.action == "retrieve":
            return EventRetrieveSerializer

        return EventListSerializer

    @action(detail=True, methods=['get'])
    def results(self, request, pk):
        """A custom action view to display event voting results.

        Returns:
            Response: The serialized voting result view
        """
        event = self.get_object()

        serializer = EventRetrieveResultSerializer(event, context={'request': request})

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def vote(self, request, pk):
        """A custom action view for voting an event date.

        Returns:
            Response: The serialized event with all dates and votes.
        """
        event = self.get_object()

        # Mandatory values are voter's name and
        name = request.data.get("name", None)
        votes = request.data.get("votes", None)

        if not name:
            return Response({
                "error": "Voter's name missing!"
            }, status=status.HTTP_400_BAD_REQUEST)

        error = validate_dates(votes, event)

        # If date validation results to an error, abort adding votes for an event
        if error:
            return Response({
                "error": error
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get or create a voter depending on if voter is found by name or not
            voter, created = EventDateVoter.objects.get_or_create(name=name)
        except Exception as e:
            return Response({
                "error": f"Couldn't get or create voter: {e}"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Go through votes (dates) and add the voter to corresponding EventDate object
        for vote in votes:
            # Get the event date object by event and date string,
            # and add the voter to that
            ed = EventDate.objects.get(event=event, date=vote)
            ed.voters.add(voter)

        serializer = EventRetrieveSerializer(event, context={'request': request})

        return Response(serializer.data)
