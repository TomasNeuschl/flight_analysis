from django.db import models

from flight_analysis.settings import CHARFIELD_MAX_LENGTH
from flight_data.models.base import BaseModel


class Status(BaseModel):
    csv_name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    flight = models.ForeignKey("Flight", on_delete=models.CASCADE)
