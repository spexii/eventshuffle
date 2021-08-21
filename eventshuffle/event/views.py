# Third party imports
from rest_framework import viewsets

# Local application imports
from .models import Event
from .serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for events
    """
    queryset = Event.objects.all().order_by('name')
    serializer_class = EventSerializer
