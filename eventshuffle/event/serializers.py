# Third party imports
from rest_framework import serializers

# Local application imports
from .functions import validate_dates
from .models import Event, EventDate


class EventListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for list view showing only event id and name.
    """

    class Meta:
        model = Event
        fields = ["id", "name"]

    def create(self, validated_data):
        # Access the dates in post data with the initial data. The
        # validated data doesn't have those, since dates is not a
        # field of Event model.
        dates = self.initial_data.pop("dates", None)

        error = validate_dates(dates)

        # If date validation results to an error, abort event creation
        if error:
            raise serializers.ValidationError(error)

        # Create the event
        event = Event.objects.create(**validated_data)

        # Add the date(s) for the event
        try:
            for date_str in dates:
                event_date = EventDate.objects.create(event=event, date=date_str)
        except Exception as e:
            # In case of error the event creation is rolled back
            event.delete()
            raise serializers.ValidationError(f"Event creating failed! Error: {e}")

        return event


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

class EventRetrieveResultSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for single event containing the results of voting.
    """
    suitable_dates = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ["id", "name", "suitable_dates"]

    def get_suitable_dates(self, obj):
        """
        Get the votes for the event dates.
        """
        return obj.get_votes(suitable_for_all=True)
