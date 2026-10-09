from django.contrib import admin
from django.utils import timezone
from .models import Election, Candidate


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "panchayat",
        "start_time",
        "end_time",
        "status",
        "is_active",
    )

    list_filter = (
        "panchayat",
        "is_active",
        "start_time",
        "end_time",
    )

    search_fields = ("name", "panchayat__name")
    ordering = ("-start_time",)

    def status(self, obj):
        now = timezone.now()
        if obj.start_time > now:
            return "UPCOMING"
        elif obj.end_time < now:
            return "ENDED"
        return "ACTIVE"

    status.short_description = "Election Status"


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "party",
        "symbol",
        "election",
    )

    list_filter = (
        "party",
        "election",
    )

    search_fields = (
        "name",
        "party",
    )
