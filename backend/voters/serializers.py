from rest_framework import serializers
from .models import Voter


class VoterRegistrationSerializer(serializers.ModelSerializer):
    """
    IMPORTANT DESIGN RULE:
    - Serializer only validates & saves raw data
    - NO hashing here (SHA256 or Poseidon)
    - NO uniqueness checks here
    - Poseidon + uniqueness is handled in the VIEW
    """

    

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
