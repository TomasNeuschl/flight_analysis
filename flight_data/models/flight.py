from django.db import models

from flight_analysis.settings import CHARFIELD_MAX_LENGTH
from flight_data.models.base import BaseModel
from flight_data.models.status import Status
from flight_data.models.telemetry import Telemetry


class Flight(BaseModel):
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
            Telemetry.objects.create(flight=self)
            Status.objects.create(flight=self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "flight"
        verbose_name_plural = "flights"
