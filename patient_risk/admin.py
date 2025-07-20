from django.contrib import admin

from .models import PatientRiskAssessment


@admin.register(PatientRiskAssessment)
class PatientRiskAssessmentAdmin(admin.ModelAdmin):
    list_display = ("person", "chads_score")
    search_fields = ("person__name",)
    list_filter = ("chads_score",)
    ordering = ("-chads_score",)
