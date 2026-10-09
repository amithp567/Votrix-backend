from rest_framework import serializers
from .models import Election, Candidate


# ----------------------------
# Candidate Serializer
# ----------------------------
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ["id", "name", "party", "symbol"]


# ----------------------------
# Election CREATE Serializer
# ----------------------------
class ElectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = [
            "id",
            "name",
            "panchayat",
            "start_time",
            "end_time",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        # force default inactive
        return Election.objects.create(
            **validated_data,
            is_active=False
        )


# ----------------------------
# Election READ Serializer
# ----------------------------
class ElectionReadSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)

    class Meta:
        model = Election
        fields = [
            "id",
            "name",
            "panchayat",
            "start_time",
            "end_time",
            "is_active",
            "candidates",
        ]
