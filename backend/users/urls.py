from django.urls import path
from .views import (
    RegisterUserView,
    LoginUserView,
    PendingAgentsView,
    ApproveAgentView
)

urlpatterns = [
    path("register/", RegisterUserView.as_view()),
    path("login/", LoginUserView.as_view()),
    # new changes
    path("agents/pending/", PendingAgentsView.as_view()),
    path("agents/approve/<int:agent_id>/", ApproveAgentView.as_view()),
]
