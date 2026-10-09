from django.urls import path
from .views import (
    CreateElectionView,
    AddCandidateView,
    StartVotingView,
    EndElectionView,
    ActiveElectionView,
    GetCandidatesByPanchayatView,
    ElectionCandidatesView,
    ElectionResultView,
    LatestElectionResultView,
)

urlpatterns = [
    path("create/", CreateElectionView.as_view()),
    path("<int:election_id>/add-candidate/", AddCandidateView.as_view()),
    path("<int:election_id>/start/", StartVotingView.as_view()),
    path("<int:election_id>/end/", EndElectionView.as_view()),
    path("active/", ActiveElectionView.as_view()),
    path("candidates/<int:panchayat_id>/", GetCandidatesByPanchayatView.as_view()),
    path("candidates/by-election/<int:election_id>/", ElectionCandidatesView.as_view()),
    path("<int:election_id>/results/", ElectionResultView.as_view()),
    path("results/latest/", LatestElectionResultView.as_view()),


]
