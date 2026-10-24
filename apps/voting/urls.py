from django.urls import path
from .views import CastVoteView,ElectionResultView

urlpatterns = [
    path('cast/', CastVoteView.as_view(), name='cast-vote'),
    path("results/<str:panchayat>/", ElectionResultView.as_view())
,
]
