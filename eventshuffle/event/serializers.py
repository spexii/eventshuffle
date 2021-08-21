# Third party imports
from rest_framework import serializers

# Local application imports
from .models import Event


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "url", "name"]
