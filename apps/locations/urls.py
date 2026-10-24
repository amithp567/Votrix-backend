from django.urls import path
from .views import PanchayatListView

urlpatterns = [
    path("", PanchayatListView.as_view()),
]
