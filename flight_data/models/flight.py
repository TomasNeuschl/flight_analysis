from django.db import models

from flight_analysis.settings import CHARFIELD_MAX_LENGTH
from flight_data.models.base import BaseModel


class Flight(BaseModel):
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)