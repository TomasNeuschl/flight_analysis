from rest_framework import serializers


class SpeedSerializer(serializers.Serializer):
    speed = serializers.FloatField()
    time = serializers.CharField()


class AltitudeSerializer(serializers.Serializer):
    altitude = serializers.FloatField()
    time = serializers.CharField()


class TelemetrySerializer(serializers.Serializer):
    path = serializers.ListField(
        child=serializers.ListField(child=serializers.FloatField()))
    speed = SpeedSerializer(many=True)
    altitude = AltitudeSerializer(many=True)
