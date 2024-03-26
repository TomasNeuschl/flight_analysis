from django.db import models

from flight_analysis.settings import CHARFIELD_MAX_LENGTH, INFLUXDB_HOST, INFLUXDB_PORT, \
    INFLUXDB_DATABASE
from flight_data.models.base import BaseModel
from flight_data.services.Influx_service import InfluxService


class Status(BaseModel):
    csv_name = models.CharField(max_length=CHARFIELD_MAX_LENGTH,
                                verbose_name="File name",
                                null=True)
    flight = models.OneToOneField("Flight", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "status"
        verbose_name_plural = "status"

    def delete(self, *args, **kwargs):
        self.csv_name = None
        InfluxService(
            host=INFLUXDB_HOST,
            port=INFLUXDB_PORT,
            database=INFLUXDB_DATABASE,
        ).delete_data("status_id", self.id)
        self.save()
