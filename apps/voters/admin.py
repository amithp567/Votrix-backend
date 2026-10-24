from django.contrib import admin
from .models import Voter

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('name', 'panchayat', 'district', 'state', 'created_at')
    search_fields = ('name', 'panchayat', 'district')
