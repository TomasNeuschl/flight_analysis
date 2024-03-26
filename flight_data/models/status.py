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
        ).delete_data("status_data", "status_id", self.id)
        self.save()

    def retrieve_data(self):
        return InfluxService(
            host=INFLUXDB_HOST,
            port=INFLUXDB_PORT,
            database=INFLUXDB_DATABASE,
        ).retrieve_data("status_data", "status_id", self.id)

    @property
    def signal_quality_data(self):
        data = self.retrieve_data()
        result = []
        columns = data['columns']
        values = data['values']

        time_index = columns.index('time')
        rsrq_index = columns.index('rsrq')
        snr_index = columns.index('snr')

        for entry in values:
            entry_dict = {'time': entry[time_index], 'rsrq': entry[rsrq_index],
                          'snr': entry[snr_index]}
            result.append(entry_dict)
        return result
