from django.db import models
from django.utils import timezone
from locations.models import Panchayat

class Election(models.Model):
    name = models.CharField(max_length=100)
    panchayat = models.ForeignKey("locations.Panchayat", on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def refresh_status(self):
        now = timezone.now()

        if self.start_time <= now <= self.end_time:
            if not self.is_active:
                self.is_active = True
                self.save(update_fields=["is_active"])
        else:
            if self.is_active:
                self.is_active = False
                self.save(update_fields=["is_active"])


class Candidate(models.Model):
    election = models.ForeignKey(
        "Election",   # 🔥 STRING reference (important)
        related_name="candidates",
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100, blank=True, null=True)
    symbol = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.name} - {self.election.name}"
