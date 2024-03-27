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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = None

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
    def data(self):
        if not self._data:
            self._data = self.retrieve_data()
        return self._data

    @property
    def path_data(self):
        data = self.data
        return [[entry[data['columns'].index('longitude')],
                 entry[data['columns'].index('latitude')]] for entry in data['values']]

    @staticmethod
    def _calculate_speed(velocity_x, velocity_y, velocity_z):
        return ((float(velocity_x) ** 2 + float(velocity_y) ** 2 + float(
            velocity_z) ** 2) ** 0.5) * 18 / 5

    @property
    def speed_data(self):
        data = self.data
        velocities = [[entry[data['columns'].index('velocity_x')],
                       entry[data['columns'].index('velocity_y')],
                       entry[data['columns'].index('velocity_z')],
                       entry[data['columns'].index('time')]] for entry in
                      data['values']]

        return [{'speed': self._calculate_speed(entry[0], entry[1], entry[2]),
                 'time': entry[3]} for entry
                in velocities]

    @property
    def altitude_data(self):
        data = self.data
        return [{'altitude': entry[data['columns'].index('altitude')],
                 'time': entry[data['columns'].index('time')]} for entry in
                data['values']]
