from django.contrib import admin
from .models import Panchayat
# Register your models here.
@admin.register(Panchayat)
class PanchayatAdmin(admin.ModelAdmin):
    list_display = ("name", "district", "state")
    search_fields = ("name", "district", "state")
