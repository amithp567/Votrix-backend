from .constants import AGENT, COMMISSIONER
from rest_framework.permissions import BasePermission

class IsCommissioner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and hasattr(user, 'profile')
            and user.profile.role == COMMISSIONER
            and user.profile.approved
        )

class IsAgent(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and hasattr(user, 'profile')
            and user.profile.role == AGENT
            and user.profile.approved
        )