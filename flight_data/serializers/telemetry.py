from rest_framework import serializers


class TelemetrySerializer(serializers.Serializer):
    path = serializers.ListField(
        child=serializers.ListField(child=serializers.FloatField()))
