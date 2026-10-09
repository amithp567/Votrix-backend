from django.db import models
from locations.models import Panchayat


class Voter(models.Model):
    name = models.CharField(max_length=100)
    house_no = models.IntegerField()
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    panchayat = models.ForeignKey(Panchayat, on_delete=models.CASCADE)
    fingerprint_id = models.IntegerField(unique=True)
    merkle_leaf = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.panchayat}"