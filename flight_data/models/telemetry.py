from django.db import models

from flight_analysis.settings import CHARFIELD_MAX_LENGTH, INFLUXDB_HOST, INFLUXDB_PORT, \
    INFLUXDB_DATABASE
from flight_data.models.base import BaseModel
from flight_data.services.Influx_service import InfluxService


class Telemetry(BaseModel):
    csv_name = models.CharField(max_length=CHARFIELD_MAX_LENGTH,
                                verbose_name="File name",
                                null=True)
    flight = models.OneToOneField("Flight", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "telemetry"
        verbose_name_plural = "telemetry"

    def delete(self, *args, **kwargs):
        self.csv_name = None
        InfluxService(
            host=INFLUXDB_HOST,
            port=INFLUXDB_PORT,
            database=INFLUXDB_DATABASE,
        ).delete_data("telemetry_data", "telemetry_id", self.id)
        self.save()

    def retrieve_data(self):
        return InfluxService(
            host=INFLUXDB_HOST,
            port=INFLUXDB_PORT,
            database=INFLUXDB_DATABASE,
        ).retrieve_data("telemetry_data", "telemetry_id", self.id)

    @property
    def path_data(self):
        data = self.retrieve_data()
        path = [[entry[data['columns'].index('longitude')],
                 entry[data['columns'].index('latitude')]] for entry in data['values']]
        return path
