from rest_framework import serializers


class SignalSerializer(serializers.Serializer):
    rsrq = serializers.IntegerField()
    snr = serializers.IntegerField()
    time = serializers.DateTimeField()


class StatusSerializer(serializers.Serializer):
    signal_quality = SignalSerializer(many=True)
