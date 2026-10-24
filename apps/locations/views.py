from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Panchayat

class PanchayatListView(APIView):
    def get(self, request):
        data = Panchayat.objects.values("id", "name")
        return Response(data)
