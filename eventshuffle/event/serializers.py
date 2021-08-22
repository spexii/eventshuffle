# Third party imports
from rest_framework import serializers

# Local application imports
from .models import Event


class EventListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for list view showing only event id and name.
    """

    class Meta:
        model = Event
        fields = ["id", "name"]


class EventRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    """
    More detailed serializer for single event view.
    """
    dates = serializers.SerializerMethodField()
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ["id", "name", "dates", "votes"]

    def get_dates(self, obj):
        """
        Get the dates for the event.
        """
        return obj.get_dates()

    def get_votes(self, obj):
        """
        Get the votes for the event dates.
        """
        return obj.get_votes()
