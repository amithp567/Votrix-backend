from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Count


from .models import Election, Candidate
from .serializer import (
    ElectionCreateSerializer,
    ElectionReadSerializer,
    CandidateSerializer
)

class CreateElectionView(APIView):
    def post(self, request):
        serializer = ElectionCreateSerializer(data=request.data)
        if serializer.is_valid():
            election = serializer.save() 
            return Response({"id": election.id}, status=201)
        return Response(serializer.errors, status=400)


class AddCandidateView(APIView):
    def post(self, request, election_id):
        try:
            election = Election.objects.get(id=election_id)
        except Election.DoesNotExist:
            return Response({"error": "Election not found"}, status=404)

        if election.is_active:
            return Response(
                {"error": "Cannot add candidates after voting starts"},
                status=403
            )

        serializer = CandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(election=election)
            return Response({"message": "Candidate added"}, status=201)

        return Response(serializer.errors, status=400)


class StartVotingView(APIView):
    def post(self, request, election_id):
        try:
            election = Election.objects.get(id=election_id)
        except Election.DoesNotExist:
            return Response({"error": "Election not found"}, status=404)

        if election.is_active:
            return Response({"error": "Voting already started"}, status=400)

        election.is_active = True
        election.save(update_fields=["is_active"])

        return Response({"message": "Voting started"}, status=200)


class EndElectionView(APIView):
    def post(self, request, election_id):
        try:
            election = Election.objects.get(id=election_id)
        except Election.DoesNotExist:
            return Response({"error": "Election not found"}, status=404)

        if not election.is_active:
            return Response({"error": "Election already ended"}, status=400)

        election.is_active = False
        election.end_time = timezone.now()
        election.save(update_fields=["is_active", "end_time"])

        return Response({"message": "Election ended"}, status=200)


class ActiveElectionView(APIView):
    def get(self, request):
        election = Election.objects.filter(is_active=True).first()

        if not election:
            return Response({"error": "No active election"}, status=404)

        return Response(ElectionReadSerializer(election).data, status=200)


class GetCandidatesByPanchayatView(APIView):
    def get(self, request, panchayat_id):
        election = Election.objects.filter(
            panchayat_id=panchayat_id,
            is_active=True
        ).first()

        if not election:
            return Response(
                {"error": "No active election for this panchayat"},
                status=404
            )

        return Response(ElectionReadSerializer(election).data, status=200)


class ElectionCandidatesView(APIView):
    def get(self, request, election_id):
        try:
            election = Election.objects.get(id=election_id)
        except Election.DoesNotExist:
            return Response({"error": "Election not found"}, status=404)

        if not election.is_active:
            return Response({"error": "Election not active"}, status=400)

        candidates = Candidate.objects.filter(election=election).values(
            "id", "name", "party"
        )

        return Response({"candidates": list(candidates)}, status=200)
    
class ElectionResultView(APIView):
    def get(self, request, election_id):
        try:
            election = Election.objects.get(id=election_id)
        except Election.DoesNotExist:
            return Response(
                {"error": "Election not found"},
                status=404
            )

        if timezone.now() < election.end_time:
            return Response(
                {"error": "Results available only after election ends"},
                status=403
            )

        results = (
            Candidate.objects
            .filter(election=election)
            .annotate(vote_count=Count("votes")) 
            .values("id", "name", "party", "vote_count")
            .order_by("-vote_count")
        )

        return Response({
            "election_id": election.id,
            "election_name": election.name,
            "status": "ENDED",
            "results": list(results),
        })
class LatestElectionResultView(APIView):
    def get(self, request):
        election = (
            Election.objects
            .filter(end_time__lt=timezone.now())
            .order_by("-end_time")
            .first()
        )

        if not election:
            return Response(
                {"error": "No completed election yet"},
                status=404
            )

        results = (
            Candidate.objects
            .filter(election=election)
            .annotate(vote_count=Count("votes"))
            .values("id", "name", "party", "vote_count")
            .order_by("-vote_count")
        )

        return Response({
            "election_id": election.id,
            "election_name": election.name,
            "status": "ENDED",
            "results": list(results),
        })
