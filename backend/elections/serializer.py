from rest_framework import serializers
from .models import Election, Candidate
from common.exceptions import ValidationException

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            "id", 
            "name", 
            "party", 
            "symbol"
        ]  

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

    def validate(self, attrs):
        start = attrs.get('start_time')
        end = attrs.get('end_time')

        if start > end:
            raise ValidationException(
                "End date must be greater that start date."
            )

        overlapping = Election.objects.filter(
            start_time__lt=end,
            end_time__gt=start
        )

        if overlapping.exists():
            raise ValidationException(
                "A election already during exist in this time period"
            )

        return attrs

    def create(self, validated_data):
        return Election.objects.create(
            **validated_data,
            is_active=False
        )


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
