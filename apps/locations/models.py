
from django.db import models

class Panchayat(models.Model):
    name = models.CharField(max_length=100, unique=True)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.district})"
