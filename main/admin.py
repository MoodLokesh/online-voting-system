from django.contrib import admin
from .models import Candidate

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("name", "total_votes")

    def total_votes(self, obj):
        return obj.votes.count()   # ✅ CORRECT (related_name)

    total_votes.short_description = "Total Votes"
