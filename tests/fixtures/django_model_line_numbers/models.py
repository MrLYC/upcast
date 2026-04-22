from django.db import models


class TimestampedRecord(models.Model):
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
