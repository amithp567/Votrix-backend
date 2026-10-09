from django.urls import path
from .views import RegisterVoterView,MerkleRootView,MerkleProofView,VerifyVoterView

urlpatterns = [
    path("register/", RegisterVoterView.as_view()),
    path("merkle-proof/", MerkleProofView.as_view()),
    path("merkle-root/", MerkleRootView.as_view()),
    path("verify/", VerifyVoterView.as_view()),
]
