from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import (
    UserRegistrationSerializer,
    UserLoginSerializer
)
from .models import UserProfile
from django.contrib.auth import authenticate
from common.permissions import IsCommissioner

class RegisterUserView(APIView):
    def post(self,request):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message":"User registered, approvel pending"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    
class LoginUserView(APIView):
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')

        user=authenticate(username=username,password=password)

        if not user:
            return Response(
                {"message":"Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        profile=UserProfile.objects.filter(user=user).first()

        if (not profile) or (not profile.approved):
            return Response(
                {"message":"User not approved"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(
                UserLoginSerializer(user).data,
                status=status.HTTP_200_OK
        )


class PendingAgentsView(APIView):
    permission_classes = [IsCommissioner]

    def get(self, request):
        agents = UserProfile.objects.filter(
            role="Agent",
            approved=False
        )

        data = [
            {
                "id": agent.id,
                "username": agent.user.username,
                "role" : agent.role
            }
            for agent in agents
        ]

        return Response(data, status=status.HTTP_200_OK)

    
class ApproveAgentView(APIView):
    permission_classes = [IsCommissioner]
    def post(self, request, agent_id):
        try:
            profile = UserProfile.objects.get(
                id=agent_id,
                role="Agent"
            )
            profile.approved = True
            profile.save()

            return Response(
                {"message": "Agent approved"},
                status=status.HTTP_200_OK
            )

        except UserProfile.DoesNotExist:
            return Response(
                {"message": "Agent not found"},
                status=status.HTTP_404_NOT_FOUND
            )
