# Third party imports
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Local application imports
from .models import Event
from .serializers import EventListSerializer, EventRetrieveSerializer

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
