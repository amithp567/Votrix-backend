from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistrationSerializer(serializers.ModelSerializer):
    role=serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    class Meta:
        model=User
        fields=['username','password','role']
        extra_kwargs={
            'password':{'write_only':True,
                        'required':True
                    }
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


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'role'
        ]

    
class UserLoginSerializer(serializers.Serializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = []

    def to_representation(self, instance):
        data = super().to_representation(instance)
        refresh = RefreshToken.for_user(instance)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data

    