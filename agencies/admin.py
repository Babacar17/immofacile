from django.contrib import admin
from .models import AgencyReview

@admin.register(AgencyReview)
class AgencyReviewAdmin(admin.ModelAdmin):
    list_display  = ('agency','reviewer','rating','created_at')
    list_filter   = ('rating',)
    search_fields = ('agency__agency_name','reviewer__username')
