from rest_framework import serializers

from flight_data.models.flight import Flight


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"
