from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from flight_data.models.flight import Flight
from flight_data.serializers.flight import FlightSerializer
from flight_data.serializers.status import StatusSerializer
from flight_data.serializers.telemetry import TelemetrySerializer


class FlightView(viewsets.GenericViewSet):
    serializer = FlightSerializer
    queryset = Flight.objects
    serializer_classes = {
        "flight_telemetry": TelemetrySerializer,
        "flight_status": StatusSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer)

    @extend_schema(operation_id="flight_telemetry")
    @action(detail=True, methods=["get"], url_path="telemetry")
    def telemetry(self, request, *args, **kwargs):
        flight = self.get_object()
        telemetry = flight.telemetry
        serializer = TelemetrySerializer(data={
            'path': telemetry.path_data,
            'speed': telemetry.speed_data,
            'altitude': telemetry.altitude_data,
        })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

    @extend_schema(operation_id="flight_status")
    @action(detail=True, methods=["get"], url_path="status")
    def status(self, request, *args, **kwargs):
        flight = self.get_object()
        status = flight.status
        serializer = StatusSerializer(data={'signal_quality': status.signal_quality_data})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
