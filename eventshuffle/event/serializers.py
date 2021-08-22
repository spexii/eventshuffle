# Third party imports
from rest_framework import serializers

# Local application imports
from .models import Event


class EventSerializer(serializers.HyperlinkedModelSerializer):
    dates = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ["id", "url", "name", "dates"]

    def get_dates(self, obj):
        """
        Get the dates for the event.
        """
        return obj.get_dates()
