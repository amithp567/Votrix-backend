from rest_framework import serializers
from .models import Voter


class VoterRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Voter
        fields = [
            "name",
            "house_no",
            "panchayat",
            "district",
            "state",
        ]

    def create(self, validated_data):
        """
        Just create the voter with raw fingerprint.
        Poseidon hash + merkle_leaf will be added in the view.
        """
        return Voter.objects.create(**validated_data)
