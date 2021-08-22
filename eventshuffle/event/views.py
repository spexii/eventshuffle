# Third party imports
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Local application imports
from .models import Event
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
