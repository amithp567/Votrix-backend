from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    role=serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    class Meta:
        model=User
        fields=['username','password','role']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def create(self, validated_data):
        role=validated_data.pop('role')
        user=User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        UserProfile.objects.create(
            user=user,role=role,approved=False
        )
        return user