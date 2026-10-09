from django.db import models
from elections.models import Election, Candidate


class Vote(models.Model):
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name="votes"
    )

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="votes"   # 🔥 REQUIRED for results
    )

    nullifier = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote for {self.candidate.name} in Election {self.election.id}"
